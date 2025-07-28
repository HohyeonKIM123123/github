# Streamlit web application - Main entry point for deployment
import streamlit as st
import sys
import os
from dotenv import load_dotenv

# 프로젝트 경로 추가
project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'project')
sys.path.append(project_path)

# 환경변수 로드 (.env 파일 직접 읽기)
env_path = os.path.join(project_path, '.env')

# 환경변수 로드 (로컬 개발용)
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# Streamlit Cloud용 secrets 처리
try:
    if hasattr(st, 'secrets'):
        for key, value in st.secrets.items():
            os.environ[key] = str(value)
except:
    pass

# 백업으로 dotenv도 시도
load_dotenv(env_path)

from modules.db_utils import DatabaseManager
from modules.loan_logic import LoanManager
from modules.email_notifier import EmailNotifier
from modules.report_generator import ReportGenerator

# 페이지 설정
st.set_page_config(
    page_title="도서관 관리 시스템",
    page_icon="📚",
    layout="wide"
)

# 기본 스타일 설정
def set_basic_styles():
    """기본 스타일을 설정하는 함수"""
    st.markdown(
        """
        <style>
        /* 사이드바 버튼 스타일 */
        .stSidebar .stButton > button {
            width: 100%;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin: 0.2rem 0;
            transition: all 0.3s ease;
            font-weight: 500;
            color: #495057;
        }
        
        .stSidebar .stButton > button:hover {
            background-color: #3498db;
            color: white;
            border-color: #3498db;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* 사이드바 메트릭 스타일 */
        .stSidebar div[data-testid="metric-container"] {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 0.5rem;
            border-radius: 6px;
            margin: 0.2rem 0;
        }
        
        /* 메트릭 카드 스타일 */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* 탭 스타일 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f8f9fa;
            border-radius: 8px;
        }
        
        /* 폼 스타일 */
        .stForm {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        
        /* 제목 스타일 */
        h1, h2, h3 {
            color: #2c3e50;
        }
        
        /* 사이드바 제목 스타일 */
        .stSidebar h1, .stSidebar h2, .stSidebar h3 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 데이터베이스 연결
@st.cache_resource
def init_database():
    db_path = os.path.join(project_path, 'db', 'library.db')
    
    # 데이터베이스가 없으면 초기화
    if not os.path.exists(db_path):
        from modules.database_init import DatabaseInitializer
        initializer = DatabaseInitializer(db_path)
        initializer.initialize_database()
        
        # 샘플 데이터 추가
        try:
            from modules.guardian_1000_full import insert_guardian_1000_novels
            insert_guardian_1000_novels()
        except Exception as e:
            st.warning(f"샘플 데이터 추가 실패: {e}")
    
    return DatabaseManager(db_path)

def main():
    # 기본 스타일 적용
    set_basic_styles()
    
    st.title("📚 도서관 관리 시스템")
    
    db_manager = init_database()
    loan_manager = LoanManager(db_manager)
    email_notifier = EmailNotifier()
    report_generator = ReportGenerator(db_manager)
    
    # 추가 매니저들
    from modules.member_manager import MemberManager
    from modules.book_manager import BookManager
    member_manager = MemberManager(db_manager)
    book_manager = BookManager(db_manager)
    
    # 사이드바 메뉴
    st.sidebar.title("📚 도서관 관리")
    st.sidebar.markdown("---")
    
    # 메뉴 버튼들
    if st.sidebar.button("📊 대시보드", use_container_width=True):
        st.session_state.current_menu = "대시보드"
    
    if st.sidebar.button("📖 도서 관리", use_container_width=True):
        st.session_state.current_menu = "도서 관리"
    
    if st.sidebar.button("👥 회원 관리", use_container_width=True):
        st.session_state.current_menu = "회원 관리"
    
    if st.sidebar.button("📋 대출 관리", use_container_width=True):
        st.session_state.current_menu = "대출 관리"
    
    if st.sidebar.button("⚠️ 연체 관리", use_container_width=True):
        st.session_state.current_menu = "연체 관리"
    
    if st.sidebar.button("📈 보고서", use_container_width=True):
        st.session_state.current_menu = "보고서"
    
    # 현재 메뉴 상태 관리
    if 'current_menu' not in st.session_state:
        st.session_state.current_menu = "대시보드"
    
    menu = st.session_state.current_menu
    
    # 현재 선택된 메뉴 표시
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**현재 페이지:** {menu}")
    
    # 시스템 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 시스템 정보")
    
    # 실시간 통계
    total_books = db_manager.execute_query("SELECT COUNT(*) as count FROM books")[0]['count']
    active_loans = db_manager.execute_query("SELECT COUNT(*) as count FROM loans WHERE status = 'active'")[0]['count']
    total_members = db_manager.execute_query("SELECT COUNT(*) as count FROM members WHERE status = 'active'")[0]['count']
    
    st.sidebar.metric("총 도서", f"{total_books:,}권")
    st.sidebar.metric("대출 중", f"{active_loans}건")
    st.sidebar.metric("활성 회원", f"{total_members}명")

    # 메뉴별 페이지 처리 (기존 로직 그대로 사용)
    if menu == "대시보드":
        st.header("📊 대시보드")
        
        # 실제 데이터베이스에서 통계 조회
        total_books_query = "SELECT COUNT(*) as count FROM books"
        total_books = db_manager.execute_query(total_books_query)[0]['count']
        
        active_loans_query = "SELECT COUNT(*) as count FROM loans WHERE status = 'active'"
        active_loans = db_manager.execute_query(active_loans_query)[0]['count']
        
        total_members_query = "SELECT COUNT(*) as count FROM members WHERE status = 'active'"
        total_members = db_manager.execute_query(total_members_query)[0]['count']
        
        overdue_summary = report_generator.get_overdue_summary()
        overdue_count = overdue_summary.get('total_overdue', 0)
        
        # 메트릭 표시
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 도서 수", f"{total_books:,}")
        
        with col2:
            st.metric("활성 대출", f"{active_loans}")
        
        with col3:
            st.metric("총 회원 수", f"{total_members}")
        
        with col4:
            st.metric("연체 도서", f"{overdue_count}")
        
        # 추가 통계 정보
        st.subheader("📈 상세 통계")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("카테고리별 도서 현황")
            category_query = """
            SELECT category, COUNT(*) as count 
            FROM books 
            GROUP BY category 
            ORDER BY count DESC
            """
            categories = db_manager.execute_query(category_query)
            
            if categories:
                import pandas as pd
                df_categories = pd.DataFrame(categories)
                df_categories.columns = ['카테고리', '도서 수']
                st.dataframe(df_categories, use_container_width=True)
        
        with col2:
            st.subheader("최근 대출 현황")
            recent_loans_query = """
            SELECT l.loan_date, b.title, m.name
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN members m ON l.member_id = m.id
            WHERE l.status = 'active'
            ORDER BY l.loan_date DESC
            LIMIT 10
            """
            recent_loans = db_manager.execute_query(recent_loans_query)
            
            if recent_loans:
                for loan in recent_loans:
                    st.write(f"• {loan['loan_date']} - {loan['title']} ({loan['name']})")
            else:
                st.info("최근 대출 기록이 없습니다.")
    
    elif menu == "도서 관리":
        st.header("📖 도서 관리")
        
        tab1, tab2, tab3 = st.tabs(["도서 목록", "도서 검색", "도서 추가"])
        
        with tab1:
            st.subheader("도서 목록")
            
            # 페이징을 위한 설정
            page_size = 20
            page = st.number_input("페이지", min_value=1, value=1) - 1
            offset = page * page_size
            
            # 전체 도서 수 조회
            total_books_query = "SELECT COUNT(*) as count FROM books"
            total_books = db_manager.execute_query(total_books_query)[0]['count']
            
            # 도서 목록 조회
            books_query = f"""
            SELECT id, title, author, category, publisher, total_copies, available_copies
            FROM books 
            ORDER BY title 
            LIMIT {page_size} OFFSET {offset}
            """
            books = db_manager.execute_query(books_query)
            
            st.write(f"총 {total_books}권의 도서가 있습니다. (페이지 {page + 1})")
            
            if books:
                # 도서 목록을 테이블로 표시
                import pandas as pd
                df = pd.DataFrame(books)
                df.columns = ['ID', '제목', '저자', '카테고리', '출판사', '총 권수', '대출 가능']
                st.dataframe(df, use_container_width=True)
            else:
                st.info("이 페이지에는 도서가 없습니다.")
        
        with tab2:
            st.subheader("도서 검색")
            
            search_type = st.selectbox(
                "검색 유형", 
                ["all", "title", "author", "category"],
                format_func=lambda x: {"all": "전체", "title": "제목", "author": "저자", "category": "카테고리"}[x]
            )
            
            search_query = st.text_input("검색어를 입력하세요")
            
            if search_query:
                search_results = book_manager.search_books(search_query, search_type)
                
                if search_results:
                    st.write(f"검색 결과: {len(search_results)}권")
                    
                    for book in search_results:
                        with st.expander(f"{book['title']} - {book['author']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**ISBN:** {book['isbn']}")
                                st.write(f"**카테고리:** {book['category']}")
                            with col2:
                                st.write(f"**출판사:** {book['publisher']}")
                                st.write(f"**대출 가능:** {book['available_copies']}권")
                else:
                    st.info("검색 결과가 없습니다.")
        
        with tab3:
            st.subheader("새 도서 추가")
            
            with st.form("add_book"):
                title = st.text_input("도서명*", placeholder="도서 제목을 입력하세요")
                author = st.text_input("저자*", placeholder="저자명을 입력하세요")
                isbn = st.text_input("ISBN*", placeholder="ISBN을 입력하세요")
                
                # 기존 카테고리 목록 가져오기
                categories_query = "SELECT DISTINCT category FROM books ORDER BY category"
                existing_categories = [row['category'] for row in db_manager.execute_query(categories_query)]
                
                category_options = existing_categories + ["새 카테고리 추가"]
                selected_category = st.selectbox("카테고리*", category_options)
                
                if selected_category == "새 카테고리 추가":
                    category = st.text_input("새 카테고리명", placeholder="새 카테고리를 입력하세요")
                else:
                    category = selected_category
                
                publisher = st.text_input("출판사", placeholder="출판사명을 입력하세요")
                publication_date = st.text_input("출간일", placeholder="YYYY-MM-DD 형식")
                total_copies = st.number_input("총 권수", min_value=1, value=1)
                location = st.text_input("위치", placeholder="도서 위치 (예: A구역-1층)")
                
                if st.form_submit_button("도서 추가"):
                    if title and author and isbn and category:
                        success, message = book_manager.add_book(
                            title=title,
                            author=author,
                            isbn=isbn,
                            category=category,
                            publisher=publisher,
                            publication_date=publication_date,
                            total_copies=total_copies,
                            location=location
                        )
                        
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error("필수 항목(*)을 모두 입력해주세요.")
    
    else:
        st.info(f"{menu} 페이지는 준비 중입니다.")

if __name__ == "__main__":
    main()