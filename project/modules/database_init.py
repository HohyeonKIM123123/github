# Database initialization and schema setup
import sqlite3
import os
from datetime import datetime

class DatabaseInitializer:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.ensure_db_directory()
    
    def ensure_db_directory(self):
        """데이터베이스 디렉토리가 없으면 생성"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def create_tables(self):
        """모든 테이블 생성"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 도서 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE,
                    category TEXT NOT NULL,
                    publisher TEXT,
                    publication_date TEXT,
                    total_copies INTEGER DEFAULT 1,
                    available_copies INTEGER DEFAULT 1,
                    location TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 회원 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    address TEXT,
                    membership_type TEXT DEFAULT 'regular',
                    registration_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # 대출 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    loan_date TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    return_date TEXT,
                    status TEXT DEFAULT 'active',
                    renewal_count INTEGER DEFAULT 0,
                    fine_amount REAL DEFAULT 0.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (member_id) REFERENCES members (id)
                )
            ''')
            
            # 예약 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    reservation_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    priority INTEGER DEFAULT 1,
                    FOREIGN KEY (book_id) REFERENCES books (id),
                    FOREIGN KEY (member_id) REFERENCES members (id)
                )
            ''')
            
            # 대출 통계 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loan_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    total_loans INTEGER DEFAULT 0,
                    total_returns INTEGER DEFAULT 0,
                    new_members INTEGER DEFAULT 0,
                    overdue_count INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 인기 도서 추천 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS book_recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    recommendation_score REAL DEFAULT 0.0,
                    loan_frequency INTEGER DEFAULT 0,
                    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            
            # 자동 발주 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auto_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    requested_quantity INTEGER NOT NULL,
                    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    supplier TEXT,
                    estimated_cost REAL,
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
            
            # 시스템 설정 테이블
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE NOT NULL,
                    setting_value TEXT NOT NULL,
                    description TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print("데이터베이스 테이블이 성공적으로 생성되었습니다.")
    
    def insert_default_settings(self):
        """기본 시스템 설정 삽입"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            default_settings = [
                ('loan_period_days', '14', '기본 대출 기간 (일)'),
                ('max_renewals', '2', '최대 연장 횟수'),
                ('overdue_fine_per_day', '100', '일일 연체료 (원)'),
                ('max_loans_per_member', '5', '회원당 최대 대출 권수'),
                ('stock_threshold', '2', '자동 발주 임계값'),
                ('email_notifications', 'true', '이메일 알림 활성화'),
                ('auto_order_enabled', 'true', '자동 발주 활성화')
            ]
            
            for key, value, desc in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description)
                    VALUES (?, ?, ?)
                ''', (key, value, desc))
            
            conn.commit()
            print("기본 시스템 설정이 삽입되었습니다.")
    
    def create_indexes(self):
        """성능 향상을 위한 인덱스 생성"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 자주 검색되는 컬럼들에 인덱스 생성
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)',
                'CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)',
                'CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn)',
                'CREATE INDEX IF NOT EXISTS idx_books_category ON books(category)',
                'CREATE INDEX IF NOT EXISTS idx_members_email ON members(email)',
                'CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status)',
                'CREATE INDEX IF NOT EXISTS idx_loans_due_date ON loans(due_date)',
                'CREATE INDEX IF NOT EXISTS idx_loans_book_id ON loans(book_id)',
                'CREATE INDEX IF NOT EXISTS idx_loans_member_id ON loans(member_id)'
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            print("데이터베이스 인덱스가 생성되었습니다.")
    
    def initialize_database(self):
        """전체 데이터베이스 초기화"""
        print("데이터베이스 초기화를 시작합니다...")
        self.create_tables()
        self.insert_default_settings()
        self.create_indexes()
        print("데이터베이스 초기화가 완료되었습니다.")

def main():
    """데이터베이스 초기화 실행"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
    initializer = DatabaseInitializer(db_path)
    initializer.initialize_database()

if __name__ == "__main__":
    main()