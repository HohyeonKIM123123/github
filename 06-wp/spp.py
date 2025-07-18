import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="한달살러 숙소 탐색기", layout="wide")
st.title("🏡 한달살러 숙소 탐색기")

@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "monthler_processed.csv")
    df = pd.read_csv(csv_path)
    return df

df = load_data()

st.sidebar.header("🔎 숙소 필터")

# 지역
region_col = 'region' if 'region' in df.columns else None
if region_col:
    region_values = df[region_col]
    if isinstance(region_values, pd.Series):
        regions = sorted(region_values.dropna().unique())
    else:
        try:
            regions = sorted(list(set([v for v in list(region_values) if pd.notna(v)])))
        except Exception:
            regions = []
    selected_region = st.sidebar.multiselect("지역", regions, default=regions)
else:
    selected_region = []

# 가격
price_col = None
for col in ['지원금', 'price', '참가비', '비용']:
    if col in df.columns:
        price_col = col
        break
if price_col:
    price_series = pd.to_numeric(df[price_col], errors='coerce').dropna()
    if not price_series.empty:
        min_price, max_price = int(price_series.min()), int(price_series.max())
        price_range = st.sidebar.slider("지원금(가격)", min_price, max_price, (min_price, max_price))
    else:
        price_range = None
        st.sidebar.info("가격 데이터가 없습니다.")
else:
    price_range = None
    st.sidebar.info("가격 정보가 없습니다.")

# 숙소 유형
room_type_col = None
for col in ['카테고리', 'room_type', '프로그램유형', '모집분야']:
    if col in df.columns:
        room_type_col = col
        break
if room_type_col:
    room_types = sorted(df[room_type_col].dropna().unique())
    selected_types = st.sidebar.multiselect("카테고리(유형)", room_types, default=room_types)
else:
    selected_types = []

# D-day
dday_col = 'dday' if 'dday' in df.columns else None
if dday_col and df[dday_col].notna().any():
    min_dday, max_dday = int(df[dday_col].min()), int(df[dday_col].max())
    dday_range = st.sidebar.slider("D-day", min_dday, max_dday, (min_dday, max_dday))
else:
    dday_range = None

# 지원자수
applicants_col = 'applicants' if 'applicants' in df.columns else None
if applicants_col and df[applicants_col].notna().any():
    min_app, max_app = int(df[applicants_col].min()), int(df[applicants_col].max())
    applicants_range = st.sidebar.slider("지원자 수", min_app, max_app, (min_app, max_app))
else:
    applicants_range = None

# 키워드 검색
keyword = st.sidebar.text_input("🔍 키워드 검색 (숙소명, 상세설명 등)")

# 정렬
sort_options = ["최신 등록순"]
if price_col:
    sort_options += ["가격 낮은순", "가격 높은순"]
if dday_col:
    sort_options += ["D-day 빠른순"]
if applicants_col:
    sort_options += ["지원자 많은순"]
sort_by = st.sidebar.selectbox("정렬 기준", sort_options)

# 필터링
filtered_df = df.copy()
if region_col and selected_region:
    filtered_df = filtered_df[filtered_df[region_col].isin(selected_region)]
if price_col and price_range:
    filtered_df = filtered_df[(pd.to_numeric(filtered_df[price_col], errors='coerce').between(*price_range))]
if room_type_col and selected_types:
    filtered_df = filtered_df[filtered_df[room_type_col].isin(selected_types)]
if dday_col and dday_range:
    filtered_df = filtered_df[(pd.to_numeric(filtered_df[dday_col], errors='coerce').between(*dday_range))]
if applicants_col and applicants_range:
    filtered_df = filtered_df[(pd.to_numeric(filtered_df[applicants_col], errors='coerce').between(*applicants_range))]
if keyword:
    keyword_cols = ['name', '상세설명', '모집기간', '모집인원', '활동기간', '연락처']
    cond = False
    for col in keyword_cols:
        if col in filtered_df.columns:
            cond = cond | filtered_df[col].astype(str).str.contains(keyword, case=False, na=False)
    filtered_df = filtered_df[cond]

# 정렬
if sort_by == "가격 낮은순" and price_col:
    filtered_df = filtered_df.sort_values(by=price_col, ascending=True)
elif sort_by == "가격 높은순" and price_col:
    filtered_df = filtered_df.sort_values(by=price_col, ascending=False)
elif sort_by == "D-day 빠른순" and dday_col:
    filtered_df = filtered_df.sort_values(by=dday_col, ascending=True)
elif sort_by == "지원자 많은순" and applicants_col:
    filtered_df = filtered_df.sort_values(by=applicants_col, ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="collected_at", ascending=False)

# 카드형 UI
st.write(f"🔎 총 {len(filtered_df)}개 숙소 검색됨")
if len(filtered_df) == 0:
    st.info('조건에 맞는 숙소가 없습니다.')
else:
    rows = [filtered_df.iloc[i:i+2] for i in range(0, len(filtered_df), 2)]
    for row_df in rows:
        cols = st.columns(2)
        for idx, (_, row) in enumerate(row_df.iterrows()):
            with cols[idx]:
                st.markdown('---')
                if 'img_url' in row and isinstance(row['img_url'], str) and row['img_url']:
                    st.image(row['img_url'], use_column_width=True)
                st.markdown(f"### {row['name']}")
                if 'region' in row:
                    st.markdown(f"**지역:** {row['region']}")
                if price_col and price_col in row:
                    st.markdown(f"**지원금:** {row[price_col]}")
                if room_type_col and room_type_col in row:
                    st.markdown(f"**카테고리:** {row[room_type_col]}")
                if dday_col and dday_col in row:
                    st.markdown(f"**D-day:** {row[dday_col]}")
                if applicants_col and applicants_col in row:
                    st.markdown(f"**지원자수:** {row[applicants_col]}")
                for col in ['모집기간', '모집인원', '활동기간', '상세설명', '연락처', '모집상태']:
                    if col in row and row[col]:
                        st.markdown(f"**{col}:** {row[col]}")
                if 'detail_url' in row and row['detail_url']:
                    st.markdown(f"[상세페이지 이동하기]({row['detail_url']})", unsafe_allow_html=True)
                st.markdown('---')

# 다운로드 버튼
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 CSV 다운로드",
    data=filtered_df.to_csv(index=False, encoding='utf-8-sig'),
    file_name="monthler_filtered.csv",
    mime="text/csv"
)