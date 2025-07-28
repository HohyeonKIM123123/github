# Book management system with search and registration
from typing import List, Dict, Optional
from .db_utils import DatabaseManager
import re

class BookManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_book(self, title: str, author: str, isbn: str, category: str, 
                 publisher: str = None, publication_date: str = None, 
                 total_copies: int = 1, location: str = None) -> bool:
        """새 도서 등록"""
        try:
            # ISBN 중복 체크
            if self.get_book_by_isbn(isbn):
                return False, "이미 등록된 ISBN입니다."
            
            query = """
            INSERT INTO books (title, author, isbn, category, publisher, 
                             publication_date, total_copies, available_copies, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            result = self.db.execute_update(query, (
                title, author, isbn, category, publisher, 
                publication_date, total_copies, total_copies, location
            ))
            
            if result > 0:
                # 추천 시스템에 새 도서 추가
                book_id = self.get_book_by_isbn(isbn)['id']
                self._add_to_recommendations(book_id)
                return True, "도서가 성공적으로 등록되었습니다."
            
            return False, "도서 등록에 실패했습니다."
            
        except Exception as e:
            return False, f"오류 발생: {str(e)}"
    
    def search_books(self, query: str, search_type: str = "all") -> List[Dict]:
        """도서 검색 (제목, 저자, ISBN, 카테고리별)"""
        if not query.strip():
            return self.get_all_books()
        
        search_query = f"%{query}%"
        
        if search_type == "title":
            sql = "SELECT * FROM books WHERE title LIKE ? ORDER BY title"
            params = (search_query,)
        elif search_type == "author":
            sql = "SELECT * FROM books WHERE author LIKE ? ORDER BY author"
            params = (search_query,)
        elif search_type == "isbn":
            sql = "SELECT * FROM books WHERE isbn LIKE ? ORDER BY isbn"
            params = (search_query,)
        elif search_type == "category":
            sql = "SELECT * FROM books WHERE category LIKE ? ORDER BY category"
            params = (search_query,)
        else:  # all
            sql = """
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?
            ORDER BY title
            """
            params = (search_query, search_query, search_query, search_query)
        
        return self.db.execute_query(sql, params)
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """ID로 도서 조회"""
        query = "SELECT * FROM books WHERE id = ?"
        result = self.db.execute_query(query, (book_id,))
        return result[0] if result else None
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Dict]:
        """ISBN으로 도서 조회"""
        query = "SELECT * FROM books WHERE isbn = ?"
        result = self.db.execute_query(query, (isbn,))
        return result[0] if result else None
    
    def get_all_books(self, limit: int = 100) -> List[Dict]:
        """모든 도서 조회 (페이징)"""
        query = "SELECT * FROM books ORDER BY title LIMIT ?"
        return self.db.execute_query(query, (limit,))
    
    def update_book(self, book_id: int, **kwargs) -> bool:
        """도서 정보 수정"""
        if not kwargs:
            return False
        
        # 수정 가능한 필드들
        allowed_fields = ['title', 'author', 'category', 'publisher', 
                         'publication_date', 'total_copies', 'location']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        # available_copies 업데이트 (total_copies 변경 시)
        if 'total_copies' in kwargs:
            current_book = self.get_book_by_id(book_id)
            if current_book:
                loaned_copies = current_book['total_copies'] - current_book['available_copies']
                new_available = max(0, kwargs['total_copies'] - loaned_copies)
                updates.append("available_copies = ?")
                values.append(new_available)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(book_id)
        
        query = f"UPDATE books SET {', '.join(updates)} WHERE id = ?"
        return self.db.execute_update(query, tuple(values)) > 0
    
    def delete_book(self, book_id: int) -> bool:
        """도서 삭제 (대출 중이 아닌 경우만)"""
        # 대출 중인지 확인
        loan_check = """
        SELECT COUNT(*) as active_loans 
        FROM loans 
        WHERE book_id = ? AND status = 'active'
        """
        result = self.db.execute_query(loan_check, (book_id,))
        
        if result[0]['active_loans'] > 0:
            return False, "대출 중인 도서는 삭제할 수 없습니다."
        
        # 도서 삭제
        query = "DELETE FROM books WHERE id = ?"
        if self.db.execute_update(query, (book_id,)) > 0:
            # 추천 테이블에서도 제거
            self.db.execute_update("DELETE FROM book_recommendations WHERE book_id = ?", (book_id,))
            return True, "도서가 삭제되었습니다."
        
        return False, "도서 삭제에 실패했습니다."
    
    def get_available_books(self) -> List[Dict]:
        """대출 가능한 도서 목록"""
        query = "SELECT * FROM books WHERE available_copies > 0 ORDER BY title"
        return self.db.execute_query(query)
    
    def update_book_availability(self, book_id: int, change: int) -> bool:
        """도서 재고 수량 변경 (대출/반납 시 호출)"""
        query = """
        UPDATE books 
        SET available_copies = available_copies + ?
        WHERE id = ? AND available_copies + ? >= 0
        """
        return self.db.execute_update(query, (change, book_id, change)) > 0
    
    def get_low_stock_books(self, threshold: int = None) -> List[Dict]:
        """재고 부족 도서 목록 (자동 발주용)"""
        if threshold is None:
            # 시스템 설정에서 임계값 가져오기
            setting_query = "SELECT setting_value FROM system_settings WHERE setting_key = 'stock_threshold'"
            result = self.db.execute_query(setting_query)
            threshold = int(result[0]['setting_value']) if result else 2
        
        query = "SELECT * FROM books WHERE available_copies <= ? ORDER BY available_copies"
        return self.db.execute_query(query, (threshold,))
    
    def get_categories(self) -> List[str]:
        """모든 카테고리 목록"""
        query = "SELECT DISTINCT category FROM books ORDER BY category"
        result = self.db.execute_query(query)
        return [row['category'] for row in result]
    
    def _add_to_recommendations(self, book_id: int):
        """새 도서를 추천 시스템에 추가"""
        query = """
        INSERT OR IGNORE INTO book_recommendations (book_id, recommendation_score, loan_frequency)
        VALUES (?, 0.0, 0)
        """
        self.db.execute_update(query, (book_id,))
    
    def validate_isbn(self, isbn: str) -> bool:
        """ISBN 형식 검증"""
        # ISBN-10 또는 ISBN-13 형식 검증
        isbn = re.sub(r'[^0-9X]', '', isbn.upper())
        
        if len(isbn) == 10:
            # ISBN-10 검증
            return self._validate_isbn10(isbn)
        elif len(isbn) == 13:
            # ISBN-13 검증
            return self._validate_isbn13(isbn)
        
        return False
    
    def _validate_isbn10(self, isbn: str) -> bool:
        """ISBN-10 체크섬 검증"""
        if len(isbn) != 10:
            return False
        
        total = 0
        for i, char in enumerate(isbn[:-1]):
            if not char.isdigit():
                return False
            total += int(char) * (10 - i)
        
        check_digit = isbn[-1]
        if check_digit == 'X':
            total += 10
        elif check_digit.isdigit():
            total += int(check_digit)
        else:
            return False
        
        return total % 11 == 0
    
    def _validate_isbn13(self, isbn: str) -> bool:
        """ISBN-13 체크섬 검증"""
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        
        total = 0
        for i, char in enumerate(isbn[:-1]):
            weight = 1 if i % 2 == 0 else 3
            total += int(char) * weight
        
        check_digit = (10 - (total % 10)) % 10
        return check_digit == int(isbn[-1])