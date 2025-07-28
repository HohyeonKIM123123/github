# Loan management logic
from datetime import datetime, timedelta
from typing import List, Dict
from .db_utils import DatabaseManager

class LoanManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_loan(self, book_id: int, member_id: int, loan_date: str = None) -> bool:
        if not loan_date:
            loan_date = datetime.now().strftime('%Y-%m-%d')
        
        due_date = (datetime.strptime(loan_date, '%Y-%m-%d') + timedelta(days=14)).strftime('%Y-%m-%d')
        
        query = """
        INSERT INTO loans (book_id, member_id, loan_date, due_date, status)
        VALUES (?, ?, ?, ?, 'active')
        """
        return self.db.execute_update(query, (book_id, member_id, loan_date, due_date)) > 0
    
    def return_book(self, loan_id: int) -> bool:
        return_date = datetime.now().strftime('%Y-%m-%d')
        query = "UPDATE loans SET status = 'returned', return_date = ? WHERE id = ?"
        return self.db.execute_update(query, (return_date, loan_id)) > 0
    
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