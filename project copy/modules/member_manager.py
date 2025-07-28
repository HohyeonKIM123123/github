# Member management system
from typing import List, Dict, Optional
from datetime import datetime
from .db_utils import DatabaseManager

class MemberManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_member(self, name: str, email: str, phone: str, address: str = "") -> bool:
        """새 회원 추가"""
        try:
            query = """
            INSERT INTO members (name, email, phone, address, status)
            VALUES (?, ?, ?, ?, 'active')
            """
            return self.db.execute_update(query, (name, email, phone, address)) > 0
        except Exception as e:
            print(f"회원 추가 실패: {e}")
            return False
    
    def get_member_by_id(self, member_id: int) -> Optional[Dict]:
        """ID로 회원 정보 조회"""
        query = "SELECT * FROM members WHERE id = ?"
        result = self.db.execute_query(query, (member_id,))
        return result[0] if result else None
    
    def get_member_by_email(self, email: str) -> Optional[Dict]:
        """이메일로 회원 정보 조회"""
        query = "SELECT * FROM members WHERE email = ?"
        result = self.db.execute_query(query, (email,))
        return result[0] if result else None
    
    def search_members(self, keyword: str) -> List[Dict]:
        """회원 검색 (이름, 이메일, 전화번호)"""
        query = """
        SELECT * FROM members 
        WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
        ORDER BY name
        """
        search_term = f"%{keyword}%"
        return self.db.execute_query(query, (search_term, search_term, search_term))
    
    def get_all_members(self, status: str = None) -> List[Dict]:
        """모든 회원 조회"""
        if status:
            query = "SELECT * FROM members WHERE status = ? ORDER BY name"
            return self.db.execute_query(query, (status,))
        else:
            query = "SELECT * FROM members ORDER BY name"
            return self.db.execute_query(query)
    
    def update_member(self, member_id: int, **kwargs) -> bool:
        """회원 정보 수정"""
        try:
            allowed_fields = ['name', 'email', 'phone', 'address']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(member_id)
            query = f"UPDATE members SET {', '.join(updates)} WHERE id = ?"
            
            return self.db.execute_update(query, tuple(values)) > 0
        except Exception as e:
            print(f"회원 정보 수정 실패: {e}")
            return False
    
    def deactivate_member(self, member_id: int) -> bool:
        """회원 비활성화"""
        query = "UPDATE members SET status = 'inactive' WHERE id = ?"
        return self.db.execute_update(query, (member_id,)) > 0
    
    def activate_member(self, member_id: int) -> bool:
        """회원 활성화"""
        query = "UPDATE members SET status = 'active' WHERE id = ?"
        return self.db.execute_update(query, (member_id,)) > 0
    
    def get_member_loan_history(self, member_id: int) -> List[Dict]:
        """회원의 대출 이력 조회"""
        query = """
        SELECT l.*, b.title, b.author
        FROM loans l
        JOIN books b ON l.book_id = b.id
        WHERE l.member_id = ?
        ORDER BY l.loan_date DESC
        """
        return self.db.execute_query(query, (member_id,))
    
    def get_member_current_loans(self, member_id: int) -> List[Dict]:
        """회원의 현재 대출 중인 도서"""
        query = """
        SELECT l.*, b.title, b.author
        FROM loans l
        JOIN books b ON l.book_id = b.id
        WHERE l.member_id = ? AND l.status = 'active'
        ORDER BY l.due_date
        """
        return self.db.execute_query(query, (member_id,))
    
    def get_member_statistics(self, member_id: int) -> Dict:
        """회원 통계 정보"""
        stats_query = """
        SELECT 
            COUNT(*) as total_loans,
            COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned_books,
            COUNT(CASE WHEN status = 'active' THEN 1 END) as current_loans,
            COUNT(CASE WHEN status = 'active' AND due_date < date('now') THEN 1 END) as overdue_books
        FROM loans 
        WHERE member_id = ?
        """
        result = self.db.execute_query(stats_query, (member_id,))
        return result[0] if result else {
            'total_loans': 0,
            'returned_books': 0, 
            'current_loans': 0,
            'overdue_books': 0
        }
    
    def delete_member(self, member_id: int) -> bool:
        """회원 삭제 (대출 이력이 없는 경우만)"""
        try:
            # 대출 이력 확인
            loan_check = self.db.execute_query(
                "SELECT COUNT(*) as count FROM loans WHERE member_id = ?", 
                (member_id,)
            )[0]
            
            if loan_check['count'] > 0:
                print("대출 이력이 있는 회원은 삭제할 수 없습니다.")
                return False
            
            query = "DELETE FROM members WHERE id = ?"
            return self.db.execute_update(query, (member_id,)) > 0
            
        except Exception as e:
            print(f"회원 삭제 실패: {e}")
            return False