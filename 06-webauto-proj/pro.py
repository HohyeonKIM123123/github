# streamlit_app.py
# 전체 통합 버전

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# ============ 설정 ============
DATA_PATH = 'naver_blog_processed.json'  # 전처리된 데이터 경로
ALADIN_API_KEY = 'YOUR_ALADIN_API_KEY'  # 본인 API 키 입력

# ============ 데이터 로드 ============
@st.cache_data
def load_data():
    df = pd.read_json(DATA_PATH)
    df = df.dropna(subset=['book'])
    return df

df = load_data()

# ============ 필터 설정 ============
st.sidebar.title("🔍 필터")

age_options = sorted(df['age_group'].dropna().unique())
job_options = sorted(df['job'].dropna().unique())
genre_options = sorted(df['genre'].dropna().unique()) if 'genre' in df.columns else []
sentiment_options = ['positive', 'neutral', 'negative']
gender_options = ['남', '여'] if 'gender' in df.columns else []
region_options = sorted(df['region'].dropna().unique()) if 'region' in df.columns else []

age_selected = st.sidebar.multiselect("연령대", age_options, default=age_options)
job_selected = st.sidebar.multiselect("직업", job_options, default=job_options)
genre_selected = st.sidebar.multiselect("장르", genre_options, default=genre_options) if genre_options else []
sentiment_selected = st.sidebar.multiselect("감성", sentiment_options, default=sentiment_options)
gender_selected = st.sidebar.multiselect("성별", gender_options, default=gender_options) if gender_options else []
region_selected = st.sidebar.multiselect("지역", region_options, default=region_options) if region_options else []

# 필터 적용
filtered = df[
    df['age_group'].isin(age_selected) &
    df['job'].isin(job_selected) &
    df['sentiment'].isin(sentiment_selected)
]
if genre_options:
    filtered = filtered[filtered['genre'].isin(genre_selected)]
if gender_options:
    filtered = filtered[filtered['gender'].isin(gender_selected)]
if region_options:
    filtered = filtered[filtered['region'].isin(region_selected)]

# ============ 추천 알고리즘 ============
def recommend_books(df, age=None, job=None, genre=None, vibe=None):
    data = df.copy()
    if age:
        data = data[data['age_group'] == age]
    if job:
        data = data[data['job'] == job]
    if genre:
        data = data[data['genre'] == genre]
    if vibe:
        data = data[data['sentiment'] == vibe]
    top_books = data['book'].value_counts().head(5)
    return top_books.index.tolist()

# ============ 알라딘 API 연동 ============
def get_book_info_from_aladin(title):
    url = f"http://www.aladin.co.kr/ttb/api/ItemSearch.aspx?ttbkey={ALADIN_API_KEY}&Query={title}&QueryType=Title&MaxResults=1&SearchTarget=Book&output=JS&Version=20131101"
    try:
        res = requests.get(url)
        data = res.json()
        if data['item']:
            book = data['item'][0]
            return {
                'title': book.get('title'),
                'author': book.get('author'),
                'publisher': book.get('publisher'),
                'price': book.get('priceSales'),
                'image': book.get('cover'),
                'link': book.get('link')
            }
    except:
        pass
    return {}

# ============ 본문 ============
st.title("📚 연령·직업·장르별 책 트렌드 분석 및 추천")

# 추천 섹션
st.header("🎯 맞춤형 도서 추천")
with st.form("recommend_form"):
    c1, c2 = st.columns(2)
    age_input = c1.selectbox("연령대 선택", age_options)
    job_input = c2.selectbox("직업 선택", job_options)
    genre_input = st.selectbox("장르 선택", genre_options) if genre_options else None
    vibe_input = st.radio("감성 톤", sentiment_options)
    submitted = st.form_submit_button("추천 받기")

    if submitted:
        results = recommend_books(df, age_input, job_input, genre_input, vibe_input)
        for book in results:
            meta = get_book_info_from_aladin(book)
            st.markdown(f"### {meta.get('title', book)}")
            col1, col2 = st.columns([1, 3])
            with col1:
                if meta.get('image'):
                    st.image(meta['image'], use_column_width=True)
            with col2:
                st.markdown(f"**저자**: {meta.get('author', '-')}")
                st.markdown(f"**출판사**: {meta.get('publisher', '-')}")
                st.markdown(f"**가격**: {meta.get('price', '-')}원")
                if meta.get('link'):
                    st.markdown(f"[알라딘에서 보기]({meta['link']})")

# 트렌드 분석
st.header("📊 전체 트렌드 분석")
if not filtered.empty:
    st.subheader("TOP 10 언급 도서")
    top_books = filtered['book'].value_counts().head(10)
    st.bar_chart(top_books)

    st.subheader("감성 비율")
    sent_ratio = filtered['sentiment'].value_counts(normalize=True) * 100
    fig = px.pie(names=sent_ratio.index, values=sent_ratio.values, title="감성 분석")
    st.plotly_chart(fig)

    st.subheader("연령–직업별 도서 언급")
    pivot = pd.pivot_table(filtered, index='age_group', columns='job', values='book', aggfunc='count', fill_value=0)
    fig2, ax2 = plt.subplots()
    sns.heatmap(pivot, annot=True, fmt='d', cmap='Blues', ax=ax2)
    st.pyplot(fig2)
else:
    st.warning("조건에 맞는 데이터가 없습니다.")

st.markdown("""
---
✅ 기능 요약:
- 세부 필터: 연령대, 직업, 감성, 성별, 지역, 장르
- 실시간 추천: 유저 맞춤 도서 추천
- 알라딘 API 연동: 이미지, 저자, 링크 제공
- 트렌드 시각화: 바차트, 파이차트, 히트맵
""")
