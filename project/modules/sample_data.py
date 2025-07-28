# Sample data insertion for testing
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.db_utils import DatabaseManager
from modules.book_manager import BookManager
from modules.member_manager import MemberManager
from modules.loan_logic import LoanManager
from datetime import datetime, timedelta

def insert_sample_data():
    """샘플 데이터 삽입"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
    db_manager = DatabaseManager(db_path)
    book_manager = BookManager(db_manager)
    member_manager = MemberManager(db_manager)
    loan_manager = LoanManager(db_manager)
    
    print("샘플 데이터 삽입을 시작합니다...")
    
    # 샘플 도서 데이터
    sample_books = [
        ("해리 포터와 마법사의 돌", "J.K. 롤링", "9788983920775", "소설", "문학수첩", "1999-12-01"),
        ("1984", "조지 오웰", "9788937460777", "소설", "민음사", "1984-01-01"),
        ("코스모스", "칼 세이건", "9788983711892", "과학", "사이언스북스", "1980-01-01"),
        ("사피엔스", "유발 하라리", "9788934972464", "역사", "김영사", "2011-01-01"),
        ("클린 코드", "로버트 C. 마틴", "9788966260959", "컴퓨터", "인사이트", "2008-01-01"),
        ("데미안", "헤르만 헤세", "9788937460893", "소설", "민음사", "1919-01-01"),
        ("총, 균, 쇠", "재레드 다이아몬드", "9788934942467", "역사", "김영사", "1997-01-01"),
        ("어린왕자", "생텍쥐페리", "9788932917245", "소설", "열린책들", "1943-01-01"),
        ("파이썬 완벽 가이드", "마크 루츠", "9788968482397", "컴퓨터", "한빛미디어", "2013-01-01"),
        ("미움받을 용기", "기시미 이치로", "9788996991304", "자기계발", "인플루엔셜", "2013-01-01")
    ]
    
    print("도서 데이터 삽입 중...")
    for title, author, isbn, category, publisher, pub_date in sample_books:
        book_manager.add_book(title, author, isbn, category, publisher, pub_date)
    
    # 샘플 회원 데이터
    sample_members = [
        ("김철수", "kim.cs@email.com", "010-1234-5678", "서울시 강남구"),
        ("이영희", "lee.yh@email.com", "010-2345-6789", "서울시 서초구"),
        ("박민수", "park.ms@email.com", "010-3456-7890", "경기도 성남시"),
        ("정수진", "jung.sj@email.com", "010-4567-8901", "인천시 남동구"),
        ("최동현", "choi.dh@email.com", "010-5678-9012", "부산시 해운대구"),
        ("한미영", "han.my@email.com", "010-6789-0123", "대구시 수성구"),
        ("윤재호", "yoon.jh@email.com", "010-7890-1234", "광주시 서구"),
        ("강소라", "kang.sr@email.com", "010-8901-2345", "대전시 유성구"),
        ("임태준", "lim.tj@email.com", "010-9012-3456", "울산시 남구"),
        ("송하늘", "song.hn@email.com", "010-0123-4567", "세종시")
    ]
    
    print("회원 데이터 삽입 중...")
    for name, email, phone, address in sample_members:
        member_manager.add_member(name, email, phone, address)
    
    # 샘플 대출 데이터 (일부는 연체되도록)
    print("대출 데이터 삽입 중...")
    
    # 현재 대출 중인 도서들
    current_loans = [
        (1, 1, "2024-01-15"),  # 연체
        (2, 2, "2024-01-20"),  # 연체
        (3, 3, "2024-02-01"),  # 정상
        (4, 4, "2024-02-05"),  # 정상
        (5, 5, "2024-02-10"),  # 정상
    ]
    
    for book_id, member_id, loan_date in current_loans:
        loan_manager.create_loan(book_id, member_id, loan_date)
    
    # 반납 완료된 대출들
    returned_loans = [
        (6, 1, "2024-01-01", "2024-01-10"),
        (7, 2, "2024-01-05", "2024-01-15"),
        (8, 3, "2024-01-10", "2024-01-20"),
        (9, 4, "2024-01-15", "2024-01-25"),
        (10, 5, "2024-01-20", "2024-01-30"),
    ]
    
    for book_id, member_id, loan_date, return_date in returned_loans:
        # 대출 생성
        loan_manager.create_loan(book_id, member_id, loan_date)
        
        # 가장 최근 대출 ID 찾기
        recent_loan = db_manager.execute_query(
            "SELECT id FROM loans WHERE book_id = ? AND member_id = ? ORDER BY id DESC LIMIT 1",
            (book_id, member_id)
        )
        
        if recent_loan:
            loan_id = recent_loan[0]['id']
            # 반납 처리
            db_manager.execute_update(
                "UPDATE loans SET status = 'returned', return_date = ? WHERE id = ?",
                (return_date, loan_id)
            )
    
    print("샘플 데이터 삽입이 완료되었습니다!")
    
    # 데이터 확인
    print("\n=== 데이터 확인 ===")
    books = db_manager.execute_query("SELECT COUNT(*) as count FROM books")
    members = db_manager.execute_query("SELECT COUNT(*) as count FROM members")
    loans = db_manager.execute_query("SELECT COUNT(*) as count FROM loans")
    
    print(f"도서: {books[0]['count']}권")
    print(f"회원: {members[0]['count']}명")
    print(f"대출 기록: {loans[0]['count']}건")
    
    # 연체 도서 확인
    overdue = db_manager.execute_query("""
        SELECT COUNT(*) as count FROM loans 
        WHERE status = 'active' AND due_date < date('now')
    """)
    print(f"연체 도서: {overdue[0]['count']}건")

if __name__ == "__main__":
    insert_sample_data()