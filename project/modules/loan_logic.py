# Loan management logic
from datetime import datetime, timedelta
from typing import List, Dict
from .db_utils import DatabaseManager

class LoanManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_loan(self, book_id: int, member_id: int, loan_date: str = None) -> bool:
        try:
            if not loan_date:
                loan_date = datetime.now().strftime('%Y-%m-%d')
            
            # 대출 가능한지 확인
            book_query = "SELECT available_copies FROM books WHERE id = ?"
            book_result = self.db.execute_query(book_query, (book_id,))
            
            if not book_result or book_result[0]['available_copies'] <= 0:
                return False
            
            due_date = (datetime.strptime(loan_date, '%Y-%m-%d') + timedelta(days=14)).strftime('%Y-%m-%d')
            
            # 대출 기록 생성
            loan_query = """
            INSERT INTO loans (book_id, member_id, loan_date, due_date, status)
            VALUES (?, ?, ?, ?, 'active')
            """
            loan_created = self.db.execute_update(loan_query, (book_id, member_id, loan_date, due_date)) > 0
            
            if loan_created:
                # 도서 재고 감소
                update_book_query = "UPDATE books SET available_copies = available_copies - 1 WHERE id = ?"
                self.db.execute_update(update_book_query, (book_id,))
                return True
            
            return False
            
        except Exception as e:
            print(f"대출 처리 중 오류: {e}")
            return False
    
    def return_book(self, loan_id: int) -> bool:
        try:
            # 먼저 대출 정보 조회
            loan_query = "SELECT book_id FROM loans WHERE id = ? AND status = 'active'"
            loan_result = self.db.execute_query(loan_query, (loan_id,))
            
            if not loan_result:
                return False
            
            book_id = loan_result[0]['book_id']
            return_date = datetime.now().strftime('%Y-%m-%d')
            
            # 대출 상태 업데이트
            update_loan_query = "UPDATE loans SET status = 'returned', return_date = ? WHERE id = ?"
            loan_updated = self.db.execute_update(update_loan_query, (return_date, loan_id)) > 0
            
            if loan_updated:
                # 도서 재고 증가
                update_book_query = "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?"
                self.db.execute_update(update_book_query, (book_id,))
                return True
            
            return False
            
        except Exception as e:
            print(f"반납 처리 중 오류: {e}")
            return False
    
    def get_overdue_loans(self) -> List[Dict]:
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT l.*, b.title, m.name, m.email 
        FROM loans l
        JOIN books b ON l.book_id = b.id
        JOIN members m ON l.member_id = m.id
        WHERE l.due_date < ? AND l.status = 'active'
        """
        return self.db.execute_query(query, (today,))