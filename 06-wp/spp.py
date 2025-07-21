import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="한달살러 숙소 탐색기", layout="wide")
st.title("🏡 한달살러 숙소 탐색기")

@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "monthler_processed.csv")
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 먼저 크롤러를 실행해주세요.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

st.sidebar.header("🔎 숙소 필터")

# 지역
region_col = 'region' if 'region' in df.columns else None
if region_col:
    region_values = df[region_col].dropna()
    if not region_values.empty:
        regions = sorted(region_values.unique())
        selected_region = st.sidebar.multiselect("지역", regions, default=regions)
    else:
        selected_region = []
else:
    selected_region = []

# D-day
dday_col = 'dday' if 'dday' in df.columns else None
if dday_col and df[dday_col].notna().any():
    dday_values = df[dday_col].dropna()
    if not dday_values.empty:
        min_dday, max_dday = int(dday_values.min()), int(dday_values.max())
        dday_range = st.sidebar.slider("D-day", min_dday, max_dday, (min_dday, max_dday))
    else:
        dday_range = None
else:
    dday_range = None

# 지원자수
applicants_col = 'applicants' if 'applicants' in df.columns else None
if applicants_col and df[applicants_col].notna().any():
    applicants_values = df[applicants_col].dropna()
    if not applicants_values.empty:
        min_app, max_app = int(applicants_values.min()), int(applicants_values.max())
        applicants_range = st.sidebar.slider("지원자 수", min_app, max_app, (min_app, max_app))
    else:
        applicants_range = None
else:
    applicants_range = None

# 지원금 필터
support_col = '지원금' if '지원금' in df.columns else None
if support_col:
    support_values = df[support_col].dropna()
    if not support_values.empty:
        support_types = sorted(support_values.unique())
        selected_support = st.sidebar.multiselect("지원금 유형", support_types, default=support_types)
    else:
        selected_support = []
else:
    selected_support = []

# 모집기간 필터
period_col = '모집기간' if '모집기간' in df.columns else None
if period_col:
    period_values = df[period_col].dropna()
    if not period_values.empty:
        period_types = sorted(period_values.unique())
        selected_period = st.sidebar.multiselect("모집기간", period_types, default=period_types)
    else:
        selected_period = []
else:
    selected_period = []

# 키워드 검색
keyword = st.sidebar.text_input("🔍 키워드 검색 (숙소명, 상세설명 등)")

# 정렬
sort_options = ["최신 등록순"]
if dday_col:
    sort_options += ["D-day 빠른순", "D-day 느린순"]
if applicants_col:
    sort_options += ["지원자 많은순", "지원자 적은순"]
sort_by = st.sidebar.selectbox("정렬 기준", sort_options)

# 필터링
filtered_df = df.copy()

if region_col and selected_region:
    filtered_df = filtered_df[filtered_df[region_col].isin(selected_region)]

if dday_col and dday_range:
    filtered_df = filtered_df[
        (pd.to_numeric(filtered_df[dday_col], errors='coerce') >= dday_range[0]) &
        (pd.to_numeric(filtered_df[dday_col], errors='coerce') <= dday_range[1])
    ]

if applicants_col and applicants_range:
    filtered_df = filtered_df[
        (pd.to_numeric(filtered_df[applicants_col], errors='coerce') >= applicants_range[0]) &
        (pd.to_numeric(filtered_df[applicants_col], errors='coerce') <= applicants_range[1])
    ]

if support_col and selected_support:
    filtered_df = filtered_df[filtered_df[support_col].isin(selected_support)]

if period_col and selected_period:
    filtered_df = filtered_df[filtered_df[period_col].isin(selected_period)]

if keyword:
    keyword_cols = ['name', '상세설명', '지원금', '모집기간', 'region']
    cond = False
    for col in keyword_cols:
        if col in filtered_df.columns:
            cond = cond | filtered_df[col].astype(str).str.contains(keyword, case=False, na=False)
    filtered_df = filtered_df[cond]

# 정렬
if sort_by == "D-day 빠른순" and dday_col:
    filtered_df = filtered_df.sort_values(by=dday_col, ascending=True, na_position='last')
elif sort_by == "D-day 느린순" and dday_col:
    filtered_df = filtered_df.sort_values(by=dday_col, ascending=False, na_position='last')
elif sort_by == "지원자 많은순" and applicants_col:
    filtered_df = filtered_df.sort_values(by=applicants_col, ascending=False, na_position='last')
elif sort_by == "지원자 적은순" and applicants_col:
    filtered_df = filtered_df.sort_values(by=applicants_col, ascending=True, na_position='last')
else:
    filtered_df = filtered_df.sort_values(by="collected_at", ascending=False)

# 카드형 UI
st.write(f"🔎 총 {len(filtered_df)}개 숙소 검색됨")
if len(filtered_df) == 0:
    st.info('조건에 맞는 숙소가 없습니다.')
else:
    # 카드 outline 강조, 여백 최소화
    st.markdown("""
    <style>
    .card {
        border: 2.5px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin: 2px 0 2px 0;
        background-color: #f9f9f9;
        box-shadow: none;
        min-height: 400px;
        height: 400px;
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }
    .card-img-container {
        display: flex;
        align-items: stretch;
        justify-content: center;
        height: 400px;
        min-width: 0;
        max-width: 100%;
        width: 100%;
    }
    .card-img-container img {
        object-fit: cover;
        width: 100%;
        height: 400px;
        min-height: 400px;
        max-height: 400px;
        border-radius: 8px;
        background: #eee;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

    # 지원금액 숫자 필터 (만원, 원 등 한글/기호 제거 후 숫자만 추출)
    import re
    def extract_amount(val):
        if pd.isna(val):
            return None
        nums = re.findall(r'[\d,]+', str(val))
        if nums:
            try:
                return int(nums[0].replace(',', ''))
            except:
                return None
        return None
    if '지원금' in filtered_df.columns:
        filtered_df['지원금액'] = filtered_df['지원금'].apply(extract_amount)
        amt_series = filtered_df['지원금액'].dropna()
        if not amt_series.empty:
            min_amt, max_amt = int(amt_series.min()), int(amt_series.max())
            amt_range = st.sidebar.slider("지원금(원)", min_amt, max_amt, (min_amt, max_amt), step=10000)
            filtered_df = filtered_df[(filtered_df['지원금액'] >= amt_range[0]) & (filtered_df['지원금액'] <= amt_range[1])]

    # D-day 슬라이더 필터 (모집기간 필터 완전 제거)
    if 'dday' in filtered_df.columns and filtered_df['dday'].notna().any():
        dday_series = filtered_df['dday'].dropna()
        if not dday_series.empty:
            min_dday, max_dday = int(dday_series.min()), int(dday_series.max())
            dday_range = st.sidebar.slider("D-day", min_dday, max_dday, (min_dday, max_dday))
            filtered_df = filtered_df[(filtered_df['dday'] >= dday_range[0]) & (filtered_df['dday'] <= dday_range[1])]

    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                img_url = row['img_url'] if 'img_url' in row.index else None
                if isinstance(img_url, str) and img_url and img_url.startswith('/'):
                    img_url = 'https://www.monthler.kr' + img_url
                if isinstance(img_url, str) and img_url.startswith('http'):
                    st.markdown(f'<div class="card-img-container"><img src="{img_url}" alt="숙소 이미지" /></div>', unsafe_allow_html=True)
                else:
                    st.markdown("**이미지 없음**")
            with col2:
                st.markdown(f"## {row['name'] if 'name' in row.index else ''}")
                if dday_col is not None and dday_col in row.index and pd.notna(row[dday_col]):
                    dday_value = row[dday_col]
                    if dday_value == 0:
                        st.markdown("### ⏰ **마감**")
                    else:
                        st.markdown(f"### ⏰ **D-{dday_value}**")
                info_cols = st.columns(2)
                with info_cols[0]:
                    if 'region' in row.index and pd.notna(row['region']):
                        st.markdown(f"**📍 지역:** {row['region']}")
                    if '지원금' in row.index and pd.notna(row['지원금']):
                        st.markdown(f"**💰 지원금:** {row['지원금']}")
                    if '모집기간' in row.index and pd.notna(row['모집기간']):
                        st.markdown(f"**📋 모집기간:** {row['모집기간']}")
                with info_cols[1]:
                    if applicants_col is not None and applicants_col in row.index and pd.notna(row[applicants_col]):
                        st.markdown(f"**📊 지원자:** {row[applicants_col]}명")
                    if '모집상태' in row.index and pd.notna(row['모집상태']):
                        st.markdown(f"**📋 상태:** {row['모집상태']}")
                if '상세설명' in row.index and pd.notna(row['상세설명']):
                    desc = str(row['상세설명'])
                    if len(desc) > 200:
                        desc = desc[:200] + "..."
                    st.markdown(f"**📝 설명:** {desc}")
                if '연락처' in row.index and pd.notna(row['연락처']) and str(row['연락처']).strip():
                    st.markdown(f"**📞 연락처:** {row['연락처']}")
            st.markdown('</div>', unsafe_allow_html=True)

# 다운로드 버튼
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 CSV 다운로드",
    data=filtered_df.to_csv(index=False, encoding='utf-8-sig'),
    file_name="monthler_filtered.csv",
    mime="text/csv"
)