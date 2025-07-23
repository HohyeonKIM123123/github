# Streamlit 기반 전세 시세 위험도 분석기 (시각화 강화 + 컬럼 필터링)
import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import datetime
import numpy as np
import plotly.graph_objects as go

@st.cache_data
def load_legal_codes(filepath='법정동코드.txt'):
    df = pd.read_csv(filepath, sep='\t', dtype=str, encoding='cp949')
    df = df[df['폐지여부'] == '존재']
    df['법정동명'] = df['법정동명'].str.strip()
    return df

def get_legal_code(addr, legal_df):
    addr = addr.replace('  ', ' ').strip()
    parts = addr.split()
    if len(parts) < 2:
        st.error("❌ 주소가 너무 짧습니다.")
        return None

    exact_match = legal_df[legal_df['법정동명'] == addr]
    if not exact_match.empty:
        return exact_match.iloc[0]['법정동코드'][:5]

    for i in range(len(parts), 0, -1):
        for j in range(len(parts) - i + 1):
            combo = ' '.join(parts[j:j+i])
            match = legal_df[legal_df['법정동명'].str.endswith(combo)]
            if not match.empty:
                return match.iloc[0]['법정동코드'][:5]

    last_part = parts[-1]
    match = legal_df[legal_df['법정동명'].str.endswith(last_part)]
    if not match.empty:
        return match.iloc[0]['법정동코드'][:5]

    return None

@st.cache_data(show_spinner=False)
def fetch_rent_data(code, ym, property_type="아파트"):
    key = "Pc%2FJQOiyQ467BxatmVf2UbZKY9eyzrJuSHu383ozvdaXp0GVEgRInW1EbE2AO6JGmjp8ghHpq90Y4m0G6FV7nQ%3D%3D"
    base = "http://apis.data.go.kr/1613000/RTMSDataSvc"
    endpoint = f"{base}AptRent/getRTMSDataSvcAptRent" if property_type == "아파트" else f"{base}RHRent/getRTMSDataSvcRHRent"
    url = f"{endpoint}?serviceKey={key}&LAWD_CD={code}&DEAL_YMD={ym}&numOfRows=100&pageNo=1"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        root = ET.fromstring(res.content)
        items = root.findall(".//item")
        if not items:
            return pd.DataFrame()

        data = []
        for item in items:
            try:
                deposit = int(item.findtext("deposit", "0").replace(",", "").strip())
                area = float(item.findtext("excluUseAr", "0").strip())
                apt = item.findtext("aptNm") or item.findtext("mhouseNm") or "정보없음"
                deal_date = f"{item.findtext('dealYear')}-{item.findtext('dealMonth').zfill(2)}-{item.findtext('dealDay').zfill(2)}"
                monthly_rent = item.findtext("monthlyRent")
                row = {
                    "단지": apt.strip(),
                    "보증금": deposit,
                    "면적": area,
                    "층": item.findtext("floor"),
                    "건축년도": item.findtext("buildYear"),
                    "거래일": deal_date,
                    "월세": monthly_rent,
                }
                data.append(row)
            except:
                continue
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def filter_by_area(df, area, tol=3):
    return df[(df['면적'] >= area - tol) & (df['면적'] <= area + tol)]

st.set_page_config(page_title="전세 위험도 분석", layout="wide")
st.title("🏠 전세 시세 위험도 분석기")

legal_df = load_legal_codes()
tab1, tab2 = st.tabs(["📝 입력", "📊 분석 결과"])

with tab1:
    address = st.text_input("📍 주소", "서울특별시 강남구 역삼동")
    area = st.number_input("📐 전용면적(㎡)", 0.0)
    deposit = st.number_input("💰 보증금(만원)", 0)
    property_type = st.radio("🏢 주택 유형", ["아파트", "연립다세대"], horizontal=True)
    today = datetime.datetime.now()
    month_options = [(today - datetime.timedelta(days=30*i)).strftime("%Y%m") for i in range(12)]
    selected_month = st.selectbox("📅 기준 월", options=month_options)
    search_all = st.checkbox("📆 최근 1년치 데이터로 분석", False)

    if st.button("🔍 분석하기"):
        code = get_legal_code(address, legal_df)
        if not code:
            st.error("❌ 주소를 다시 입력해주세요.")
        else:
            dfs = []
            months = month_options if search_all else [selected_month]
            with st.spinner(f"데이터 수집 중 ({'전체기간' if search_all else selected_month})..."):
                for ym in months:
                    df = fetch_rent_data(code, ym, property_type)
                    if not df.empty:
                        dfs.append(df)
            if not dfs:
                st.warning("❗ 데이터가 없습니다.")
            else:
                all_df = pd.concat(dfs)
                filtered = filter_by_area(all_df, area)
                if filtered.empty:
                    st.warning("⚠️ 유사 면적의 데이터가 없습니다.")
                else:
                    avg = filtered['보증금'].mean()
                    risk = "적정"
                    if deposit > avg * 1.2:
                        risk = "높음"
                    elif deposit < avg * 0.8:
                        risk = "낮음"
                    # 입력 보증금과 평균 보증금 비율 계산
                    deposit_percentage = ((deposit - avg) / avg) * 100
                    st.session_state['result'] = {
                        "df": filtered,
                        "area": area,
                        "deposit": deposit,
                        "avg": avg,
                        "risk": risk,
                        "deposit_percentage": deposit_percentage,
                        "address": address,
                        "property_type": property_type
                    }
                    st.success("✅ 분석이 완료되었습니다. 결과 탭을 확인하세요.")

with tab2:
    if 'result' not in st.session_state:
        st.info("👈 먼저 왼쪽에서 분석을 진행해주세요.")
    else:
        r = st.session_state['result']
        df = r['df']
        st.subheader(f"{r['address']} {r['property_type']} 전세 분석 결과")
        st.write(f"📐 면적: {r['area']}㎡ ±3㎡ | 💰 보증금: {r['deposit']:,}만원 | 평균: {int(r['avg']):,}만원")

        # 🔥 위험도 강조 박스
        color = {'높음': 'red', '낮음': 'green', '적정': 'blue'}[r['risk']]
        st.markdown(f"""
            <div style='padding: 15px; background-color: #f9f9f9; border-left: 10px solid {color}; border-radius: 5px;'>
            <h3 style='color: {color}; margin: 0;'>위험도: {r['risk']}</h3>
            <p style='margin: 0;'>입력한 보증금은 평균 대비 {r['deposit_percentage']:.2f}% {'높습니다' if r['deposit_percentage'] > 0 else '낮습니다'}.</p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 🔍 컬럼별 필터링
        with st.expander("🔎 상세 필터링 옵션"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                floor_filter = st.multiselect("층수", sorted(df['층'].dropna().unique().tolist()))
            with col2:
                year_filter = st.multiselect("건축년도", sorted(df['건축년도'].dropna().unique().tolist()))
            with col3:
                apt_filter = st.multiselect("단지명", sorted(df['단지'].dropna().unique().tolist()))
            with col4:
                rent_type_filter = st.multiselect("거래 유형", ['월세', '전세'], default=['월세', '전세'])

        df_show = df.copy()
        if floor_filter:
            df_show = df_show[df_show['층'].isin(floor_filter)]
        if year_filter:
            df_show = df_show[df_show['건축년도'].isin(year_filter)]
        if apt_filter:
            df_show = df_show[df_show['단지'].isin(apt_filter)]
        if rent_type_filter:
            if '월세' in rent_type_filter:
                df_show = df_show[df_show['월세'].notna()]
            if '전세' in rent_type_filter:
                df_show = df_show[df_show['월세'].isna()]

        # 📈 보증금과 면적 산점도
        st.markdown("### 📊 보증금 vs 면적 산점도")
        fig = go.Figure(go.Scatter(x=df_show['면적'], y=df_show['보증금'], mode='markers', marker=dict(color='skyblue', size=8)))
        fig.update_layout(title="보증금 vs 면적", xaxis_title="면적 (㎡)", yaxis_title="보증금 (만원)")
        st.plotly_chart(fig)