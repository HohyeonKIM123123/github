# Report generation utilities
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from .db_utils import DatabaseManager

class ReportGenerator:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def generate_monthly_report(self, year: int, month: int) -> Dict:
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        # 월별 대출 통계
        loan_query = """
        SELECT COUNT(*) as total_loans,
               COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned_loans,
               COUNT(CASE WHEN status = 'active' THEN 1 END) as active_loans
        FROM loans 
        WHERE loan_date >= ? AND loan_date < ?
        """
        loan_stats = self.db.execute_query(loan_query, (start_date, end_date))[0]
        
        # 인기 도서 TOP 10
        popular_books_query = """
        SELECT b.title, COUNT(*) as loan_count
        FROM loans l
        JOIN books b ON l.book_id = b.id
        WHERE l.loan_date >= ? AND l.loan_date < ?
        GROUP BY b.id, b.title
        ORDER BY loan_count DESC
        LIMIT 10
        """
        popular_books = self.db.execute_query(popular_books_query, (start_date, end_date))
        
        return {
            'period': f"{year}년 {month}월",
            'loan_statistics': loan_stats,
            'popular_books': popular_books,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def export_to_excel(self, report_data: Dict, filename: str) -> bool:
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 통계 시트
                stats_df = pd.DataFrame([report_data['loan_statistics']])
                stats_df.to_excel(writer, sheet_name='대출통계', index=False)
                
                # 인기 도서 시트
                popular_df = pd.DataFrame(report_data['popular_books'])
                popular_df.to_excel(writer, sheet_name='인기도서', index=False)
            
            return True
        except Exception as e:
            print(f"Excel 파일 생성 실패: {e}")
            return False
    
    def get_overdue_summary(self) -> Dict:
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
        SELECT COUNT(*) as total_overdue,
               COUNT(DISTINCT member_id) as affected_members,
               AVG(julianday(?) - julianday(due_date)) as avg_overdue_days
        FROM loans 
        WHERE due_date < ? AND status = 'active'
        """
        return self.db.execute_query(query, (today, today))[0]