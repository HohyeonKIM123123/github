import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime
import numpy as np

st.set_page_config(page_title="한달살러 프로그램 탐색기", layout="wide", page_icon="🌟")

# ✅ 데이터 로드
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "monthler_simple.csv")
    try:
        df = pd.read_csv(csv_path)
        return df.fillna('')
    except Exception as e:
        st.error(f"❌ 데이터 로드 실패: {e}")
        return pd.DataFrame()

# ✅ 지원금 숫자 추출
def extract_support_amount(support_text):
    if not support_text or pd.isna(support_text):
        return 0
    numbers = re.findall(r'[\d,]+', str(support_text))
    if numbers:
        try:
            amount = int(numbers[0].replace(',', ''))
            if '만원' in support_text:
                amount *= 10000
            return amount
        except:
            return 0
    return 0

# ✅ 지역 정리
def clean_region(region_text):
    if not region_text:
        return '전국'
    major = ['서울','부산','대구','인천','광주','대전','울산','경기','강원','충북','충남','전북','전남','경북','경남','제주']
    for r in major:
        if r in region_text:
            return r
    return region_text

# ✅ 데이터 전처리
df = load_data()
if df.empty:
    st.stop()

df['support_amount'] = df['지원금'].apply(extract_support_amount)
df['region_clean'] = df['region'].apply(clean_region)

# ✅ 사이드바 필터
with st.sidebar:
    st.header("📍 필터")
    regions = ['전체'] + sorted(df['region_clean'].unique())
    selected_region = st.selectbox("지역", regions)

    # 지원금 슬라이더 추가
    min_support = int(df['support_amount'].min())
    max_support = int(df['support_amount'].max())
    support_range = st.slider("지원금 범위(원)", min_value=min_support, max_value=max_support, value=(min_support, max_support), step=10000, format="%d")

    keyword = st.text_input("키워드 검색", placeholder="숙소 이름 또는 지역")

    sort_option = st.selectbox("정렬 기준", ["최신순", "지원금 높은순", "지원금 낮은순", "이름순"])

# ✅ 필터 적용
filtered_df = df.copy()

if selected_region != '전체':
    filtered_df = filtered_df[filtered_df['region_clean'] == selected_region]

# 지원금 슬라이더 범위 필터 적용
filtered_df = filtered_df[(filtered_df['support_amount'] >= support_range[0]) & (filtered_df['support_amount'] <= support_range[1])]

if keyword:
    filtered_df = filtered_df[
        filtered_df['name'].str.contains(keyword, case=False, na=False) |
        filtered_df['region'].str.contains(keyword, case=False, na=False)
    ]

if sort_option == '최신순':
    filtered_df = filtered_df.sort_values('collected_at', ascending=False)
elif sort_option == '지원금 높은순':
    filtered_df = filtered_df.sort_values('support_amount', ascending=False)
elif sort_option == '지원금 낮은순':
    filtered_df = filtered_df.sort_values('support_amount', ascending=True)
elif sort_option == '이름순':
    filtered_df = filtered_df.sort_values('name')

# ✅ 헤더
st.markdown("<h1 style='text-align: center;'>🌟 한달살러 프로그램 탐색기</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>전국 체험형 숙소 프로그램을 쉽게 찾아보세요</p>", unsafe_allow_html=True)

# ✅ 통계
st.info(f"🔍 총 {len(filtered_df)}개 프로그램")

# ✅ 카드 리스트 렌더링
if len(filtered_df) == 0:
    st.warning("조건에 맞는 프로그램이 없습니다. 필터를 조정해보세요.")
else:
    for idx, row in filtered_df.iterrows():
        img_url = row['img_url'] if pd.notna(row['img_url']) and row['img_url'] else "https://via.placeholder.com/120x80?text=No+Image"
        support = "무료" if row['support_amount'] == 0 else f"{row['support_amount'] // 10000:,}만원"
        dday = row['dday']
        # dday가 배열/리스트/numpy.ndarray면 첫 번째 값만 사용
        if isinstance(dday, (list, tuple, np.ndarray)) and len(dday) > 0:
            dday = dday[0]
        # dday가 None, 빈 문자열, 혹은 숫자가 아니면 문자열 그대로 출력
        if pd.isna(dday) or dday == '':
            deadline = ""
        elif str(dday).strip().lstrip('-').isdigit():
            if int(dday) == 0:
                deadline = "마감"
            else:
                deadline = f"D-{int(dday)}"
        else:
            deadline = str(dday)
        applicants = f"{int(row['applicants'])}명 지원" if pd.notna(row['applicants']) else "지원자 모집중"

        st.markdown(f"""
        <div style="border:1px solid #ddd; border-radius:15px; padding:1rem; margin-bottom:1rem; display:flex; gap:1rem;">
            <img src="{img_url}" width="120" height="80" style="border-radius:12px; object-fit:cover;">
            <div style="flex:1;">
                <h4>{row['name']}</h4>
                <p>📍 {row['region_clean']} &nbsp; | &nbsp; 💰 {support} &nbsp; | &nbsp; 🗓 {deadline} &nbsp; | &nbsp; 👥 {applicants}</p>
            </div>
            <div style="display:flex; align-items:center;">
                <a href="https://www.monthler.kr/" target="_blank">
                    <button style="padding:0.5rem 1rem; border:none; background:#667eea; color:white; border-radius:10px;">자세히 보기</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ✅ 다운로드 버튼
with st.sidebar:
    st.markdown("---")
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 CSV 다운로드", data=csv, file_name="monthler_filtered.csv", mime="text/csv")

# ✅ 푸터
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:gray;'>최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)
