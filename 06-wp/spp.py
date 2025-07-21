import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
import numpy as np

st.set_page_config(page_title="한달살러 프로그램 탐색기", layout="wide", page_icon="🌟")

# 커스텀 CSS - 더욱 세련된 디자인
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    .main {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    .filter-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
    }
    
    .program-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .program-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .program-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
    }
    
    .card-grid {
        display: grid;
        grid-template-columns: auto 1fr auto;
        gap: 1.5rem;
        align-items: center;
    }
    
    .card-image {
        width: 120px;
        height: 80px;
        border-radius: 12px;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .card-content {
        flex: 1;
    }
    
    .program-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    
    .program-info {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin: 1rem 0;
    }
    
    .info-badge {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        white-space: nowrap;
    }
    
    .info-badge.location {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
    }
    
    .info-badge.support {
        background: linear-gradient(45deg, #00b894, #00a085);
    }
    
    .info-badge.deadline {
        background: linear-gradient(45deg, #e17055, #d63031);
    }
    
    .info-badge.applicants {
        background: linear-gradient(45deg, #a29bfe, #6c5ce7);
    }
    
    .link-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .link-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-decoration: none;
        color: white;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #6c757d;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: border-color 0.3s ease;
    }
    
    .sidebar .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .sidebar .stMultiSelect > div > div {
        background-color: white;
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# 메인 헤더
st.markdown("""
<div class="main-header">
    <h1>🌟 한달살러 프로그램 탐색기</h1>
    <p>전국의 다양한 체험 프로그램과 이벤트를 한눈에 찾아보세요</p>
</div>
""", unsafe_allow_html=True)

# 데이터 로드
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "monthler_processed.csv")
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다. monthler_crawler_improved.py를 실행해서 데이터를 수집해주세요.")
    st.stop()

# 데이터 전처리
def preprocess_data(df):
    """데이터 전처리"""
    # 결측값 처리
    df = df.fillna('')
    
    # 지원금 정보 추출
    df['support_amount'] = df['지원금'].apply(extract_support_amount)
    
    # 지역 정보 정리
    df['region_clean'] = df['region'].apply(clean_region)
    
    # 모집 상태 정리
    df['status_clean'] = df['모집상태'].apply(lambda x: '모집중' if pd.isna(x) or x == '' else x)
    
    return df

def extract_support_amount(support_text):
    """지원금 정보에서 금액 추출"""
    if pd.isna(support_text) or support_text == '':
        return 0
    
    # 숫자 추출
    numbers = re.findall(r'[\d,]+', str(support_text))
    if numbers:
        # 쉼표 제거하고 숫자로 변환
        amount = int(numbers[0].replace(',', ''))
        # 만원 단위 처리
        if '만원' in str(support_text):
            amount *= 10000
        return amount
    return 0

def clean_region(region_text):
    """지역 정보 정리"""
    if pd.isna(region_text) or region_text == '':
        return '전국'
    
    # 주요 지역 추출
    major_regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    
    for region in major_regions:
        if region in str(region_text):
            return region
    
    return str(region_text)

# 데이터 전처리 실행
df = preprocess_data(df)

# 사이드바 필터
with st.sidebar:
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.header("🔍 프로그램 필터")
    
    # 지역 필터
    regions = ['전체'] + sorted(df['region_clean'].unique().tolist())
    selected_region = st.selectbox("📍 지역", regions)
    
    # 지원금 필터
    support_options = ['전체', '무료', '100만원 이하', '500만원 이하', '1000만원 이하', '1000만원 이상']
    selected_support = st.selectbox("💰 지원금", support_options)
    
    # 키워드 검색
    keyword = st.text_input("🔍 키워드 검색", placeholder="프로그램명, 내용 등")
    
    # 정렬 옵션
    sort_option = st.selectbox("📊 정렬 기준", [
        "최신순", "지원금 높은순", "지원금 낮은순", "이름순"
    ])
    
    st.markdown('</div>', unsafe_allow_html=True)

# 필터링 로직
filtered_df = df.copy()

# 지역 필터
if selected_region != '전체':
    filtered_df = filtered_df[filtered_df['region_clean'] == selected_region]

# 지원금 필터
if selected_support != '전체':
    if selected_support == '무료':
        filtered_df = filtered_df[filtered_df['support_amount'] == 0]
    elif selected_support == '100만원 이하':
        filtered_df = filtered_df[filtered_df['support_amount'] <= 1000000]
    elif selected_support == '500만원 이하':
        filtered_df = filtered_df[filtered_df['support_amount'] <= 5000000]
    elif selected_support == '1000만원 이하':
        filtered_df = filtered_df[filtered_df['support_amount'] <= 10000000]
    elif selected_support == '1000만원 이상':
        filtered_df = filtered_df[filtered_df['support_amount'] > 10000000]

# 키워드 검색
if keyword:
    keyword_condition = (
        filtered_df['name'].str.contains(keyword, case=False, na=False) |
        filtered_df['상세설명'].str.contains(keyword, case=False, na=False) |
        filtered_df['region'].str.contains(keyword, case=False, na=False)
    )
    filtered_df = filtered_df[keyword_condition]

# 정렬
if sort_option == "최신순":
    filtered_df = filtered_df.sort_values('collected_at', ascending=False)
elif sort_option == "지원금 높은순":
    filtered_df = filtered_df.sort_values('support_amount', ascending=False)
elif sort_option == "지원금 낮은순":
    filtered_df = filtered_df.sort_values('support_amount', ascending=True)
elif sort_option == "이름순":
    filtered_df = filtered_df.sort_values('name')

# 통계 표시
st.markdown(f"""
<div class="stats-container">
    <div class="stats-number">{len(filtered_df)}</div>
    <div>개의 프로그램을 찾았습니다</div>
</div>
""", unsafe_allow_html=True)

# 프로그램 카드 표시
if len(filtered_df) == 0:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <h3>조건에 맞는 프로그램이 없습니다</h3>
        <p>필터 조건을 조정해보세요</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, (_, program) in enumerate(filtered_df.iterrows()):
        # 지원금 정보 포맷팅
        support_text = "무료"
        if program['support_amount'] > 0:
            if program['support_amount'] >= 10000:
                support_text = f"{program['support_amount']//10000:,}만원"
            else:
                support_text = f"{program['support_amount']:,}원"
        
        # 모집기간 정보
        deadline = program.get('모집기간', '')
        if deadline:
            deadline_text = f"📅 {deadline}"
        else:
            deadline_text = "📅 상시모집"
        
        # 지원자 수 정보
        applicants = program.get('applicants', '')
        applicants_text = f"👥 {applicants}명 지원" if applicants else "👥 지원자 모집중"
        
        # 이미지 URL 처리
        img_url = program.get('img_url', '')
        if not img_url or pd.isna(img_url):
            img_url = "https://via.placeholder.com/120x80?text=No+Image"
        
        st.markdown(f"""
        <div class="program-card">
            <div class="card-grid">
                <img src="{img_url}" class="card-image" alt="프로그램 이미지">
                <div class="card-content">
                    <div class="program-title">{program['name']}</div>
                    <div class="program-info">
                        <span class="info-badge location">📍 {program['region_clean']}</span>
                        <span class="info-badge support">💰 {support_text}</span>
                        <span class="info-badge deadline">{deadline_text}</span>
                        <span class="info-badge applicants">{applicants_text}</span>
                    </div>
                </div>
                <div>
                    <a href="https://www.monthler.kr/" class="link-button" target="_blank">
                        자세히 보기
                    </a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 사이드바 다운로드
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 필터 결과")
    st.write(f"총 {len(filtered_df)}개 프로그램")
    
    if len(filtered_df) > 0:
        csv_data = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 결과 다운로드 (CSV)",
            data=csv_data,
            file_name=f"monthler_programs_{len(filtered_df)}개.csv",
            mime="text/csv"
        )

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🌟 한달살러 프로그램 탐색기 | 전국의 다양한 프로그램을 한눈에</p>
    <p style="font-size: 0.9rem;">마지막 업데이트: {}</p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)