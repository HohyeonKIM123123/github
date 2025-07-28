# Streamlit web application
import streamlit as st
import sys
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# 데이터베이스 연결
@st.cache_resource
def init_database():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'library.db')
    return DatabaseManager(db_path)

def main():
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
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        ["대시보드", "도서 관리", "회원 관리", "대출 관리", "연체 관리", "보고서"]
    )
    
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
            
            # 대출 가능한 도서 vs 대출 중인 도서
            availability_query = """
            SELECT 
                SUM(total_copies) as total_copies,
                SUM(available_copies) as available_copies,
                SUM(total_copies - available_copies) as loaned_copies
            FROM books
            """
            availability = db_manager.execute_query(availability_query)[0]
            
            st.subheader("도서 재고 현황")
            st.write(f"**총 보유 도서:** {availability['total_copies']}권")
            st.write(f"**대출 가능:** {availability['available_copies']}권")
            st.write(f"**대출 중:** {availability['loaned_copies']}권")
        
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
            
            # 인기 도서 TOP 5
            st.subheader("인기 도서 TOP 5")
            popular_books_query = """
            SELECT b.title, COUNT(*) as loan_count
            FROM loans l
            JOIN books b ON l.book_id = b.id
            GROUP BY b.id, b.title
            ORDER BY loan_count DESC
            LIMIT 5
            """
            popular_books = db_manager.execute_query(popular_books_query)
            
            if popular_books:
                for i, book in enumerate(popular_books, 1):
                    st.write(f"{i}. {book['title']} ({book['loan_count']}회)")
            else:
                st.info("대출 기록이 없습니다.")
        
        # 월별 대출 통계 (간단한 차트)
        st.subheader("📊 월별 대출 통계")
        monthly_stats_query = """
        SELECT 
            strftime('%Y-%m', loan_date) as month,
            COUNT(*) as loan_count
        FROM loans
        WHERE loan_date >= date('now', '-12 months')
        GROUP BY strftime('%Y-%m', loan_date)
        ORDER BY month
        """
        monthly_stats = db_manager.execute_query(monthly_stats_query)
        
        if monthly_stats:
            import pandas as pd
            df_monthly = pd.DataFrame(monthly_stats)
            df_monthly.columns = ['월', '대출 수']
            st.line_chart(df_monthly.set_index('월'))
        else:
            st.info("월별 통계 데이터가 없습니다.")
    
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
                
                # 도서 상세 정보 보기
                selected_book_id = st.selectbox(
                    "상세 정보를 볼 도서 선택", 
                    options=[0] + [book['id'] for book in books],
                    format_func=lambda x: "선택하세요" if x == 0 else next(book['title'] for book in books if book['id'] == x)
                )
                
                if selected_book_id != 0:
                    book_detail = db_manager.execute_query(
                        "SELECT * FROM books WHERE id = ?", 
                        (selected_book_id,)
                    )[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**제목:** {book_detail['title']}")
                        st.write(f"**저자:** {book_detail['author']}")
                        st.write(f"**ISBN:** {book_detail['isbn']}")
                        st.write(f"**카테고리:** {book_detail['category']}")
                    
                    with col2:
                        st.write(f"**출판사:** {book_detail['publisher']}")
                        st.write(f"**출간일:** {book_detail['publication_date']}")
                        st.write(f"**총 권수:** {book_detail['total_copies']}")
                        st.write(f"**대출 가능:** {book_detail['available_copies']}")
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
                            st.rerun()  # 페이지 새로고침
                        else:
                            st.error(message)
                    else:
                        st.error("필수 항목(*)을 모두 입력해주세요.")
    
    elif menu == "회원 관리":
        st.header("👥 회원 관리")
        
        tab1, tab2, tab3 = st.tabs(["회원 목록", "회원 검색", "회원 추가"])
        
        with tab1:
            st.subheader("회원 목록")
            
            # 회원 목록 조회
            members_query = """
            SELECT id, name, email, phone, status, registration_date
            FROM members 
            ORDER BY name
            """
            members = db_manager.execute_query(members_query)
            
            if members:
                st.write(f"총 {len(members)}명의 회원이 있습니다.")
                
                # 회원 목록을 테이블로 표시
                import pandas as pd
                df = pd.DataFrame(members)
                df.columns = ['ID', '이름', '이메일', '전화번호', '상태', '가입일']
                st.dataframe(df, use_container_width=True)
                
                # 회원 상세 정보 보기
                selected_member_id = st.selectbox(
                    "상세 정보를 볼 회원 선택", 
                    options=[0] + [member['id'] for member in members],
                    format_func=lambda x: "선택하세요" if x == 0 else next(member['name'] for member in members if member['id'] == x)
                )
                
                if selected_member_id != 0:
                    member_detail = db_manager.execute_query(
                        "SELECT * FROM members WHERE id = ?", 
                        (selected_member_id,)
                    )[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**이름:** {member_detail['name']}")
                        st.write(f"**이메일:** {member_detail['email']}")
                        st.write(f"**전화번호:** {member_detail['phone']}")
                    
                    with col2:
                        st.write(f"**주소:** {member_detail['address']}")
                        st.write(f"**상태:** {member_detail['status']}")
                        st.write(f"**가입일:** {member_detail['registration_date']}")
                    
                    # 회원의 대출 통계
                    member_stats = member_manager.get_member_statistics(selected_member_id)
                    
                    st.subheader("대출 통계")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("총 대출", member_stats['total_loans'])
                    with col2:
                        st.metric("반납 완료", member_stats['returned_books'])
                    with col3:
                        st.metric("대출 중", member_stats['current_loans'])
                    with col4:
                        st.metric("연체", member_stats['overdue_books'])
                    
                    # 현재 대출 중인 도서 (연체 우선 표시)
                    current_loans_query = """
                    SELECT l.*, b.title, b.author,
                           CASE WHEN l.due_date < date('now') THEN 1 ELSE 0 END as is_overdue,
                           julianday('now') - julianday(l.due_date) as days_overdue
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    WHERE l.member_id = ? AND l.status = 'active'
                    ORDER BY is_overdue DESC, l.due_date ASC
                    """
                    current_loans = db_manager.execute_query(current_loans_query, (selected_member_id,))
                    
                    if current_loans:
                        st.subheader("현재 대출 중인 도서")
                        for loan in current_loans:
                            is_overdue = loan['is_overdue']
                            days_overdue = int(loan['days_overdue']) if loan['days_overdue'] > 0 else 0
                            
                            if is_overdue:
                                st.error(f"🚨 **연체 {days_overdue}일** - {loan['title']} by {loan['author']}")
                                st.write(f"   대출일: {loan['loan_date']} | 반납예정일: {loan['due_date']}")
                            else:
                                st.success(f"📖 {loan['title']} by {loan['author']}")
                                st.write(f"   대출일: {loan['loan_date']} | 반납예정일: {loan['due_date']}")
                    else:
                        # 현재 대출이 없으면 최근 대출 이력 보여주기
                        recent_loans_query = """
                        SELECT l.*, b.title, b.author
                        FROM loans l
                        JOIN books b ON l.book_id = b.id
                        WHERE l.member_id = ? AND l.status = 'returned'
                        ORDER BY l.return_date DESC
                        LIMIT 5
                        """
                        recent_loans = db_manager.execute_query(recent_loans_query, (selected_member_id,))
                        
                        if recent_loans:
                            st.subheader("최근 대출 이력")
                            for loan in recent_loans:
                                st.info(f"📚 {loan['title']} by {loan['author']}")
                                st.write(f"   대출: {loan['loan_date']} ~ 반납: {loan['return_date']}")
                        else:
                            st.info("대출 이력이 없습니다.")
                    
                    # 대출 이력 전체 보기 (접을 수 있는 형태)
                    with st.expander("전체 대출 이력 보기"):
                        all_loans_query = """
                        SELECT l.*, b.title, b.author
                        FROM loans l
                        JOIN books b ON l.book_id = b.id
                        WHERE l.member_id = ?
                        ORDER BY l.loan_date DESC
                        """
                        all_loans = db_manager.execute_query(all_loans_query, (selected_member_id,))
                        
                        if all_loans:
                            for loan in all_loans:
                                status_icon = "📖" if loan['status'] == 'active' else "✅"
                                status_text = "대출 중" if loan['status'] == 'active' else "반납 완료"
                                
                                st.write(f"{status_icon} **{loan['title']}** by {loan['author']} ({status_text})")
                                if loan['status'] == 'active':
                                    st.write(f"   대출일: {loan['loan_date']} | 반납예정일: {loan['due_date']}")
                                else:
                                    st.write(f"   대출일: {loan['loan_date']} | 반납일: {loan['return_date']}")
                                st.write("---")
                        else:
                            st.info("대출 이력이 없습니다.")
            else:
                st.info("등록된 회원이 없습니다.")
        
        with tab2:
            st.subheader("회원 검색")
            
            search_query = st.text_input("이름, 이메일, 전화번호로 검색")
            
            if search_query:
                search_results = member_manager.search_members(search_query)
                
                if search_results:
                    st.write(f"검색 결과: {len(search_results)}명")
                    
                    for member in search_results:
                        with st.expander(f"{member['name']} ({member['email']})"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**전화번호:** {member['phone']}")
                                st.write(f"**상태:** {member['status']}")
                            with col2:
                                st.write(f"**주소:** {member['address']}")
                                st.write(f"**가입일:** {member['registration_date']}")
                else:
                    st.info("검색 결과가 없습니다.")
        
        with tab3:
            st.subheader("새 회원 등록")
            
            with st.form("add_member"):
                name = st.text_input("이름*", placeholder="회원 이름을 입력하세요")
                email = st.text_input("이메일*", placeholder="이메일 주소를 입력하세요")
                phone = st.text_input("전화번호", placeholder="전화번호를 입력하세요")
                address = st.text_area("주소", placeholder="주소를 입력하세요")
                
                if st.form_submit_button("회원 등록"):
                    if name and email:
                        if member_manager.add_member(name, email, phone, address):
                            st.success("회원이 성공적으로 등록되었습니다!")
                            st.rerun()  # 페이지 새로고침
                        else:
                            st.error("회원 등록에 실패했습니다. (이메일 중복 가능성)")
                    else:
                        st.error("필수 항목(*)을 모두 입력해주세요.")
    
    elif menu == "대출 관리":
        st.header("📋 대출 관리")
        
        tab1, tab2, tab3 = st.tabs(["대출 처리", "반납 처리", "대출 현황"])
        
        with tab1:
            st.subheader("도서 대출")
            
            # 회원 선택
            members = db_manager.execute_query("SELECT id, name, email FROM members WHERE status = 'active' ORDER BY name")
            if members:
                member_options = {f"{m['name']} ({m['email']})": m['id'] for m in members}
                selected_member = st.selectbox("회원 선택", options=list(member_options.keys()))
                member_id = member_options[selected_member] if selected_member else None
                
                # 대출 가능한 도서 선택
                available_books = db_manager.execute_query("""
                    SELECT id, title, author, available_copies 
                    FROM books 
                    WHERE available_copies > 0 
                    ORDER BY title
                """)
                
                if available_books:
                    book_options = {f"{b['title']} by {b['author']} (재고: {b['available_copies']}권)": b['id'] for b in available_books}
                    selected_book = st.selectbox("도서 선택", options=list(book_options.keys()))
                    book_id = book_options[selected_book] if selected_book else None
                    
                    if st.button("대출 처리", type="primary"):
                        if member_id and book_id:
                            # 회원의 현재 대출 수 확인
                            current_loans_count = db_manager.execute_query(
                                "SELECT COUNT(*) as count FROM loans WHERE member_id = ? AND status = 'active'",
                                (member_id,)
                            )[0]['count']
                            
                            if current_loans_count >= 5:  # 최대 5권 제한
                                st.error("회원당 최대 5권까지만 대출 가능합니다.")
                            else:
                                if loan_manager.create_loan(book_id, member_id):
                                    # 도서 재고 업데이트
                                    book_manager.update_book_availability(book_id, -1)
                                    st.success("대출이 처리되었습니다!")
                                    st.rerun()
                                else:
                                    st.error("대출 처리에 실패했습니다.")
                        else:
                            st.error("회원과 도서를 모두 선택해주세요.")
                else:
                    st.warning("현재 대출 가능한 도서가 없습니다.")
            else:
                st.warning("등록된 회원이 없습니다.")
        
        with tab2:
            st.subheader("도서 반납")
            
            # 현재 대출 중인 도서 목록 표시
            active_loans = db_manager.execute_query("""
                SELECT l.id, l.book_id, l.member_id, l.loan_date, l.due_date,
                       b.title, b.author, m.name, m.email,
                       CASE WHEN l.due_date < date('now') THEN 1 ELSE 0 END as is_overdue,
                       julianday('now') - julianday(l.due_date) as days_overdue
                FROM loans l
                JOIN books b ON l.book_id = b.id
                JOIN members m ON l.member_id = m.id
                WHERE l.status = 'active'
                ORDER BY is_overdue DESC, l.due_date ASC
            """)
            
            if active_loans:
                st.write(f"현재 {len(active_loans)}건의 대출이 있습니다.")
                
                # 반납할 대출 선택
                loan_options = {}
                for loan in active_loans:
                    is_overdue = loan['is_overdue']
                    days_overdue = int(loan['days_overdue']) if loan['days_overdue'] > 0 else 0
                    
                    if is_overdue:
                        status_text = f"🚨 연체 {days_overdue}일"
                    else:
                        status_text = "📖 정상"
                    
                    loan_text = f"{status_text} | {loan['title']} | {loan['name']} | 대출ID: {loan['id']}"
                    loan_options[loan_text] = loan['id']
                
                selected_loan = st.selectbox("반납할 대출 선택", options=list(loan_options.keys()))
                loan_id = loan_options[selected_loan] if selected_loan else None
                
                if loan_id:
                    # 선택된 대출의 상세 정보 표시
                    selected_loan_info = next(loan for loan in active_loans if loan['id'] == loan_id)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**도서:** {selected_loan_info['title']}")
                        st.write(f"**저자:** {selected_loan_info['author']}")
                        st.write(f"**회원:** {selected_loan_info['name']}")
                    
                    with col2:
                        st.write(f"**대출일:** {selected_loan_info['loan_date']}")
                        st.write(f"**반납예정일:** {selected_loan_info['due_date']}")
                        if selected_loan_info['is_overdue']:
                            st.error(f"**연체:** {int(selected_loan_info['days_overdue'])}일")
                    
                    if st.button("반납 처리", type="primary"):
                        if loan_manager.return_book(loan_id):
                            # 도서 재고 업데이트
                            book_manager.update_book_availability(selected_loan_info['book_id'], 1)
                            st.success("반납이 처리되었습니다!")
                            st.rerun()
                        else:
                            st.error("반납 처리에 실패했습니다.")
            else:
                st.info("현재 대출 중인 도서가 없습니다.")
        
        with tab3:
            st.subheader("대출 현황")
            
            # 전체 대출 통계
            loan_stats = db_manager.execute_query("""
                SELECT 
                    COUNT(*) as total_loans,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_loans,
                    COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned_loans,
                    COUNT(CASE WHEN status = 'active' AND due_date < date('now') THEN 1 END) as overdue_loans
                FROM loans
            """)[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("총 대출", loan_stats['total_loans'])
            with col2:
                st.metric("대출 중", loan_stats['active_loans'])
            with col3:
                st.metric("반납 완료", loan_stats['returned_loans'])
            with col4:
                st.metric("연체", loan_stats['overdue_loans'])
            
            # 현재 대출 중인 도서 목록
            if active_loans:
                st.subheader("현재 대출 중인 도서")
                
                import pandas as pd
                df_data = []
                for loan in active_loans:
                    is_overdue = loan['is_overdue']
                    days_overdue = int(loan['days_overdue']) if loan['days_overdue'] > 0 else 0
                    
                    status = f"연체 {days_overdue}일" if is_overdue else "정상"
                    
                    df_data.append({
                        '대출ID': loan['id'],
                        '도서명': loan['title'],
                        '회원명': loan['name'],
                        '대출일': loan['loan_date'],
                        '반납예정일': loan['due_date'],
                        '상태': status
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            
            # 연체 도서 알림 발송 섹션
            overdue_loans = [loan for loan in active_loans if loan['is_overdue']]
            
            if overdue_loans:
                st.subheader("🚨 연체 도서 알림 발송")
                
                # 회원별로 연체 도서 그룹화
                overdue_by_member = {}
                for loan in overdue_loans:
                    member_id = loan['member_id']
                    if member_id not in overdue_by_member:
                        overdue_by_member[member_id] = {
                            'name': loan['name'],
                            'email': loan['email'],
                            'books': []
                        }
                    overdue_by_member[member_id]['books'].append(loan)
                
                st.write(f"연체 회원 {len(overdue_by_member)}명에게 알림을 발송할 수 있습니다.")
                
                # 개별 알림 발송
                for member_id, member_data in overdue_by_member.items():
                    with st.expander(f"📧 {member_data['name']} ({member_data['email']}) - {len(member_data['books'])}권 연체"):
                        st.write("**연체 도서 목록:**")
                        for book in member_data['books']:
                            days_overdue = int(book['days_overdue'])
                            st.write(f"• {book['title']} (연체 {days_overdue}일)")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"개별 알림 발송", key=f"individual_{member_id}"):
                                if email_notifier.send_overdue_notification(
                                    member_data['email'],
                                    member_data['name'],
                                    member_data['books']
                                ):
                                    st.success("알림이 발송되었습니다!")
                                else:
                                    st.error("알림 발송에 실패했습니다.")
                        
                        with col2:
                            # 이메일 미리보기
                            if st.button(f"이메일 미리보기", key=f"preview_{member_id}"):
                                preview_content = f"""
**받는 사람:** {member_data['email']}
**제목:** 도서관 연체 도서 알림

안녕하세요 {member_data['name']}님,

다음 도서들이 연체되었습니다:

"""
                                for book in member_data['books']:
                                    days_overdue = int(book['days_overdue'])
                                    preview_content += f"- {book['title']} (대출일: {book['loan_date']}, 반납예정일: {book['due_date']}, 연체: {days_overdue}일)\n"
                                
                                preview_content += """
빠른 시일 내에 반납해 주시기 바랍니다.

감사합니다.
도서관 관리시스템
"""
                                st.text_area("이메일 내용", preview_content, height=200, key=f"preview_content_{member_id}")
                
                # 전체 알림 발송
                st.write("---")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📧 전체 연체 알림 발송", type="primary"):
                        success_count = 0
                        total_count = len(overdue_by_member)
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i, (member_id, member_data) in enumerate(overdue_by_member.items()):
                            status_text.text(f"발송 중... {member_data['name']} ({i+1}/{total_count})")
                            
                            if email_notifier.send_overdue_notification(
                                member_data['email'],
                                member_data['name'],
                                member_data['books']
                            ):
                                success_count += 1
                            
                            progress_bar.progress((i + 1) / total_count)
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        if success_count == total_count:
                            st.success(f"모든 연체 알림이 성공적으로 발송되었습니다! ({success_count}/{total_count})")
                        else:
                            st.warning(f"일부 알림 발송에 실패했습니다. 성공: {success_count}/{total_count}")
                
                with col2:
                    # 이메일 설정 상태 확인
                    st.write("**이메일 설정 상태:**")
                    import os
                    email_configured = bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))
                    
                    if email_configured:
                        st.success("✅ 이메일 설정 완료")
                    else:
                        st.error("❌ 이메일 설정 필요")
                        st.write("환경변수에 EMAIL_ADDRESS와 EMAIL_PASSWORD를 설정해주세요.")
            
            # 최근 반납된 도서
            recent_returns = db_manager.execute_query("""
                SELECT l.return_date, b.title, m.name
                FROM loans l
                JOIN books b ON l.book_id = b.id
                JOIN members m ON l.member_id = m.id
                WHERE l.status = 'returned' AND l.return_date IS NOT NULL
                ORDER BY l.return_date DESC
                LIMIT 10
            """)
            
            if recent_returns:
                st.subheader("최근 반납 도서")
                for ret in recent_returns:
                    st.write(f"• {ret['return_date']} - {ret['title']} ({ret['name']})")
            else:
                st.info("최근 반납 기록이 없습니다.")
    
    elif menu == "연체 관리":
        st.header("⚠️ 연체 관리")
        
        overdue_loans = loan_manager.get_overdue_loans()
        
        if overdue_loans:
            st.subheader(f"연체 도서 목록 ({len(overdue_loans)}건)")
            
            for loan in overdue_loans:
                with st.expander(f"{loan['title']} - {loan['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**대출일:** {loan['loan_date']}")
                        st.write(f"**반납예정일:** {loan['due_date']}")
                    with col2:
                        st.write(f"**회원:** {loan['name']}")
                        st.write(f"**이메일:** {loan['email']}")
                    
                    if st.button(f"알림 발송", key=f"notify_{loan['id']}"):
                        if email_notifier.send_overdue_notification(
                            loan['email'], loan['name'], [loan]
                        ):
                            st.success("알림이 발송되었습니다!")
                        else:
                            st.error("알림 발송에 실패했습니다.")
        else:
            st.info("연체된 도서가 없습니다.")
    
    elif menu == "보고서":
        st.header("📈 보고서")
        
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("연도", min_value=2020, max_value=2030, value=2024)
        with col2:
            month = st.number_input("월", min_value=1, max_value=12, value=1)
        
        if st.button("월간 보고서 생성"):
            report = report_generator.generate_monthly_report(year, month)
            
            st.subheader(f"{report['period']} 대출 통계")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 대출", report['loan_statistics']['total_loans'])
            with col2:
                st.metric("반납 완료", report['loan_statistics']['returned_loans'])
            with col3:
                st.metric("대출 중", report['loan_statistics']['active_loans'])
            
            if report['popular_books']:
                st.subheader("인기 도서 TOP 10")
                for i, book in enumerate(report['popular_books'], 1):
                    st.write(f"{i}. {book['title']} ({book['loan_count']}회)")

if __name__ == "__main__":
    main()