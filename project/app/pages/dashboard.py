# Dashboard page
import streamlit as st

def show(db_manager, report_generator):
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