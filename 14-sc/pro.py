import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import datetime
import numpy as np
import plotly.graph_objects as go

# 🚩 1. 법정동 코드 불러오기
@st.cache_data
def load_legal_codes(filepath='법정동코드.txt'):
    # EUC-KR 또는 CP949 인코딩으로 파일 읽기
    df = pd.read_csv(filepath, sep='\t', dtype=str, encoding='cp949')
    df = df[df['폐지여부'] == '존재']  # 폐지된 동 제외
    df['법정동명'] = df['법정동명'].str.strip()
    return df

# 🚩 2. 법정동 이름 → 코드 변환 (최적화 버전)
def get_legal_code(addr, legal_df):
    addr = addr.replace('  ', ' ').strip()
    parts = addr.split()
    
    if len(parts) < 2:
        st.error("❌ 주소가 너무 짧습니다. 시/도, 시/군/구, 동/읍/면을 포함해주세요.")
        return None
    
    # 전체 주소 매칭
    exact_match = legal_df[legal_df['법정동명'] == addr]
    if not exact_match.empty:
        code = exact_match.iloc[0]['법정동코드'][:5]
        st.success(f"✅ 정확한 매칭 성공! '{addr}' (코드: {code})")
        return code
    
    # 조합 검색
    combinations = []
    for i in range(1, min(4, len(parts) + 1)):
        for j in range(len(parts) - i + 1):
            combo = ' '.join(parts[j:j+i])
            combinations.append(combo)
    
    # 가장 구체적인(긴) 조합부터 검색
    combinations.sort(key=len, reverse=True)
    
    for combo in combinations:
        # 정확한 매칭 시도
        exact_matches = legal_df[legal_df['법정동명'] == combo]
        if not exact_matches.empty:
            code = exact_matches.iloc[0]['법정동코드'][:5]
            st.success(f"✅ 찾았습니다! '{combo}' (코드: {code})")
            return code
        
        # 부분 매칭 시도
        partial_matches = legal_df[legal_df['법정동명'].str.endswith(combo)]
        if not partial_matches.empty:
            code = partial_matches.iloc[0]['법정동코드'][:5]
            full_name = partial_matches.iloc[0]['법정동명']
            st.success(f"✅ 부분 매칭 성공! '{combo}' → '{full_name}' (코드: {code})")
            return code
    
    # 마지막 단어만 검색
    if len(parts) >= 1:
        last_part = parts[-1]
        match = legal_df[legal_df['법정동명'].str.endswith(last_part)]
        if not match.empty:
            code = match.iloc[0]['법정동코드'][:5]
            full_name = match.iloc[0]['법정동명']
            st.success(f"✅ 동/읍/면 매칭 성공! '{last_part}' → '{full_name}' (코드: {code})")
            return code
    
    st.error("❌ 주소에서 법정동 코드를 찾을 수 없습니다.")
    st.warning("💡 팁: '서울특별시 강남구 역삼동'과 같이 시/도, 시/군/구, 동/읍/면을 모두 포함하여 입력해보세요.")
    return None

# 🚩 3. 국토부 실거래가 API 요청 (최적화 버전)
@st.cache_data(show_spinner=False)
def fetch_rent_data(code, ym, property_type="아파트"):
    # 디코딩된 서비스 키
    decoded_key = "Pc/JQOiyQ467BxatmVf2UbZKY9eyzrJuSHu383ozvdaXp0GVEgRInW1EbE2AO6JGmjp8ghHpq90Y4m0G6FV7nQ=="
    
    # 주택 유형에 따라 URL 선택
    base = "http://apis.data.go.kr/1613000"
    if property_type == "아파트":
        # 아파트 전세 API
        url = f"{base}/RTMSDataSvcAptRent/getRTMSDataSvcAptRent?serviceKey={decoded_key}&LAWD_CD={code}&DEAL_YMD={ym}&numOfRows=500&pageNo=1"
    else:
        # 연립다세대 전세 API
        url = f"{base}/RTMSDataSvcRHRent/getRTMSDataSvcRHRent?serviceKey={decoded_key}&LAWD_CD={code}&DEAL_YMD={ym}&numOfRows=500&pageNo=1"
    
    # 요청 헤더 추가
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*"
    }
    
    try:
        # 세션 생성 및 타임아웃 설정
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        
        # 직접 URL로 요청
        res = session.get(url, headers=headers, verify=False, timeout=30)
        
        if res.status_code != 200:
            return pd.DataFrame()
        
        # XML 파싱
        root = ET.fromstring(res.content)
        items = root.findall(".//item") or root.findall(".//items/item") or root.findall("*//item")
        
        if not items:
            return pd.DataFrame()
        
        # 데이터 처리
        results = []
        for item in items:
            try:
                # 필수 정보 확인
                deposit_elem = item.find("deposit")
                area_elem = item.find("excluUseAr")
                
                if deposit_elem is None or area_elem is None:
                    continue
                
                # 데이터 추출 및 변환
                deposit_text = deposit_elem.text.replace(",", "").replace(" ", "")
                deposit = int(deposit_text) if deposit_text else 0
                
                area_text = area_elem.text
                area = float(area_text) if area_text else 0
                
                # 주택 이름 찾기
                apt_elem = None
                for tag_name in ["mhouseNm", "aptNm", "아파트"]:
                    apt_elem = item.find(tag_name)
                    if apt_elem is not None and apt_elem.text and apt_elem.text.strip():
                        break
                
                apt = apt_elem.text.strip() if apt_elem is not None and apt_elem.text else "정보없음"
                
                # 추가 정보
                floor = item.findtext("floor")
                build_year = item.findtext("buildYear")
                
                # 계약일 정보
                deal_year = item.findtext("dealYear")
                deal_month = item.findtext("dealMonth", "").zfill(2)
                deal_day = item.findtext("dealDay", "").zfill(2)
                deal_date = f"{deal_year}-{deal_month}-{deal_day}" if deal_year else None
                
                # 월세 정보
                monthly_rent_text = item.findtext("monthlyRent", "0")
                monthly_rent = int(monthly_rent_text.replace(",", "")) if monthly_rent_text.strip() != "0" else None
                
                # 데이터 추가
                data = {
                    "단지": apt,
                    "보증금": deposit,
                    "면적": area
                }
                
                if floor:
                    data["층"] = floor
                
                if build_year:
                    data["건축년도"] = build_year
                
                if deal_date:
                    data["거래일"] = deal_date
                
                if monthly_rent:
                    data["월세"] = monthly_rent
                
                results.append(data)
            except Exception:
                continue
        
        return pd.DataFrame(results)
            
    except Exception:
        return pd.DataFrame()

# 🚩 4. 유사 면적 필터링
def filter_by_area(df, area, tol=3):
    return df[(df['면적'] >= area - tol) & (df['면적'] <= area + tol)]

# 🚩 Streamlit UI - 탭 기반 인터페이스
st.set_page_config(page_title="전세 시세 위험도 분석기", layout="wide")
st.title("🏠 전세 시세 위험도 분석기")

# 법정동 코드 로드
legal_df = load_legal_codes()

# 탭 생성
tab1, tab2 = st.tabs(["📝 입력", "📊 분석 결과"])

# 탭 1: 입력 폼
with tab1:
    st.markdown("전용면적 기준 실거래가와 입력 보증금을 비교합니다.")
    
    address = st.text_input("📍 주소 (예: 서울특별시 강남구 역삼동)")
    area = st.number_input("📐 전용면적 (㎡)", min_value=0.0, step=0.1)
    deposit = st.number_input("💰 보증금 (만원)", min_value=0)
    
    # 주택 유형 선택
    property_type = st.radio("🏢 주택 유형", ["아파트", "연립다세대"], horizontal=True)
    
    # 최근 12개월 옵션 생성
    current_date = datetime.datetime.now()
    month_options = []
    for i in range(12):
        date = current_date - datetime.timedelta(days=30*i)
        month_options.append(date.strftime("%Y%m"))
    
    month = st.selectbox("📅 기준 월", options=month_options)
    search_period = st.radio("🔍 검색 기간", ["선택한 월만", "1년치 데이터"], index=0)
    
    # 세션 상태 초기화
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
        st.session_state.analysis_data = None
    
    # 분석 버튼
    if st.button("🔍 분석하기"):
        with st.spinner("법정동 코드 검색 중..."):
            code = get_legal_code(address, legal_df)
            
        if not code:
            st.error("주소에서 법정동 코드를 찾을 수 없습니다.")
        else:
            st.write(f"▶ 법정동 코드: `{code}`")
            
            # 검색 기간에 따라 처리
            if search_period == "선택한 월만":
                # 선택한 월만 검색
                with st.spinner(f"📅 {month} 기준 데이터를 검색 중..."):
                    df = fetch_rent_data(code, month, property_type)
            else:
                # 1년치 데이터 검색
                with st.spinner("📅 최근 1년치 데이터를 검색 중..."):
                    # 진행 상황 표시
                    progress_bar = st.progress(0)
                    
                    # 최근 12개월 데이터 수집
                    all_data = []
                    for i, m in enumerate(month_options[:12]):
                        progress_bar.progress((i+1)/12)
                        month_df = fetch_rent_data(code, m, property_type)
                        if not month_df.empty:
                            # 월 정보 추가
                            month_df['거래월'] = m
                            all_data.append(month_df)
                    
                    # 모든 데이터 합치기
                    df = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
            
            if df.empty:
                st.warning("해당 조건의 실거래 데이터를 찾을 수 없습니다.")
                st.session_state.analysis_done = False
            else:
                st.success(f"✅ 총 {len(df)}개의 데이터를 수집했습니다.")
                
                # 면적 필터링
                df_filtered = filter_by_area(df, area)
                
                if df_filtered.empty:
                    st.warning(f"⚠️ 전용면적 {area}㎡ 근처(±3㎡)의 데이터가 없습니다.")
                    st.session_state.analysis_done = False
                else:
                    st.success(f"✅ 전용면적 {area}㎡ 근처(±3㎡)의 데이터: {len(df_filtered)}건")
                    
                    # 월세가 있는 매물 제외 (전세만 계산)
                    # 원본 데이터 백업
                    original_df_filtered = df_filtered.copy()
                    
                    # 순수 전세만 필터링 (월세 칼럼이 없거나 월세 값이 None인 경우만 포함)
                    if '월세' in df_filtered.columns:
                        df_filtered = df_filtered[df_filtered['월세'].isna()]
                        st.info(f"ℹ️ 월세 매물을 제외한 순수 전세 데이터: {len(df_filtered)}건")
                    
                    # 필터링 후 데이터가 없는 경우 처리
                    if df_filtered.empty:
                        st.warning("⚠️ 순수 전세 데이터가 없습니다. 월세 매물만 존재합니다.")
                        st.session_state.analysis_done = False
                    else:
                        # 통계 계산 (순수 전세만)
                        avg = df_filtered['보증금'].mean()
                        max_d = df_filtered['보증금'].max()
                        min_d = df_filtered['보증금'].min()
                        median = df_filtered['보증금'].median()
                        
                        # 위험도 평가
                        if deposit > avg * 1.2:
                            risk_level = "높음"
                            risk_color = "red"
                            risk_message = f"입력 보증금이 평균보다 {int((deposit/avg-1)*100)}% 높습니다."
                        elif deposit < avg * 0.8:
                            risk_level = "낮음"
                            risk_color = "green"
                            risk_message = f"입력 보증금이 평균보다 {int((1-deposit/avg)*100)}% 낮습니다."
                        else:
                            risk_level = "적정"
                            risk_color = "blue"
                            risk_message = "입력 보증금이 평균과 유사한 수준입니다."
                        
                        # 세션 상태에 분석 결과 저장
                        st.session_state.analysis_done = True
                        st.session_state.analysis_data = {
                            'address': address,
                            'area': area,
                            'deposit': deposit,
                            'search_period': search_period,
                            'month': month,
                            'df_filtered': df_filtered,
                            'avg': avg,
                            'max_d': max_d,
                            'min_d': min_d,
                            'median': median,
                            'risk_level': risk_level,
                            'risk_color': risk_color,
                            'risk_message': risk_message,
                            'property_type': property_type
                        }
                        
                        # 분석 완료 메시지 및 탭 전환 안내
                        st.success("✅ 분석이 완료되었습니다! '📊 분석 결과' 탭을 클릭하여 결과를 확인하세요.")

# 탭 2: 분석 결과
with tab2:
    if not st.session_state.get('analysis_done', False):
        st.info("👈 먼저 왼쪽 탭에서 주소와 면적을 입력하고 분석을 실행해주세요.")
    else:
        # 세션 상태에서 분석 결과 가져오기
        data = st.session_state.analysis_data
        address = data['address']
        area = data['area']
        deposit = data['deposit']
        search_period = data['search_period']
        df_filtered = data['df_filtered']
        avg = data['avg']
        max_d = data['max_d']
        min_d = data['min_d']
        median = data['median']
        risk_level = data['risk_level']
        risk_color = data['risk_color']
        risk_message = data['risk_message']
        property_type = data['property_type']
        
        # 결과 표시
        st.markdown(f"## 🏠 {address} {property_type} 전세 시세 분석 결과")
            
        st.markdown(f"**📐 전용면적:** {area}㎡ (±3㎡)")
        st.markdown(f"**💰 입력 보증금:** {deposit:,}만원")
        st.markdown(f"**📅 기준 기간:** {'선택한 월만' if search_period == '선택한 월만' else '최근 1년'}")
        st.markdown(f"**🔍 분석 데이터:** {len(df_filtered)}건")
        
        # 결과 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 평균 보증금", f"{int(avg):,}만원")
            st.metric("📈 최고 보증금", f"{max_d:,}만원")
        with col2:
            st.metric("📉 최저 보증금", f"{min_d:,}만원")
            st.metric("📊 중간값", f"{int(median):,}만원")
        
        # 위험도 분석
        st.markdown("## 💰 보증금 위험도 분석")
        st.markdown(f"<div style='padding: 10px; background-color: {'#ffcccc' if risk_level == '높음' else '#ccffcc' if risk_level == '낮음' else '#cce5ff'}; border-radius: 5px;'><h4 style='color: {risk_color}; margin: 0;'>위험도: {risk_level}</h4><p>{risk_message}</p></div>", unsafe_allow_html=True)
        
        if risk_level == "높음":
            st.warning("⚠️ 입력 보증금이 평균보다 **20% 이상 높습니다**. 주의하세요!")
        
        # 차트 표시
        st.markdown("## 📈 면적 대비 보증금 분포")
        
        # 면적 대비 보증금 산점도
        fig = go.Figure()
        
        # 데이터 포인트
        fig.add_trace(go.Scatter(
            x=df_filtered['면적'],
            y=df_filtered['보증금'],
            mode='markers',
            text=df_filtered['단지'],
            marker=dict(
                size=10,
                color='royalblue',
                opacity=0.7
            ),
            name='매물'
        ))
        
        # 입력 값
        fig.add_trace(go.Scatter(
            x=[area],
            y=[deposit],
            mode='markers',
            name='입력값',
            marker=dict(
                size=15,
                color='red',
                symbol='star'
            )
        ))
        
        fig.update_layout(
            title="면적 대비 보증금 분포",
            xaxis_title="전용면적 (㎡)",
            yaxis_title="보증금 (만원)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 입력 보증금 위치 표시
        percentile = sum(df_filtered['보증금'] < deposit) / len(df_filtered) * 100
        st.write(f"💡 입력하신 보증금 {deposit:,}만원은 상위 {100-percentile:.1f}% 수준입니다.")
        
        # 단지 검색 기능
        st.markdown("## 📋 단지 검색 및 상세 데이터")
        
        # 단지명 목록 추출 (중복 제거)
        complex_names = sorted(df_filtered['단지'].unique())
        
        # 검색창 추가
        search_query = st.text_input("🔍 단지명 검색", placeholder="검색할 단지명을 입력하세요...")
        
        if search_query:
            # 검색어를 포함하는 단지 필터링
            filtered_complexes = [name for name in complex_names if search_query.lower() in name.lower()]
            
            if filtered_complexes:
                # 검색 결과가 있는 경우
                st.success(f"✅ '{search_query}'(으)로 검색된 단지: {len(filtered_complexes)}개")
                
                # 검색된 단지 선택 옵션
                selected_complex = st.selectbox("단지 선택", filtered_complexes)
                
                # 선택된 단지의 데이터만 표시
                selected_data = df_filtered[df_filtered['단지'] == selected_complex]
                
                # 선택된 단지 정보 표시
                st.subheader(f"📌 {selected_complex} 정보")
                
                # 통계 계산
                complex_avg = selected_data['보증금'].mean()
                complex_max = selected_data['보증금'].max()
                complex_min = selected_data['보증금'].min()
                
                # 결과 표시
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("평균 보증금", f"{int(complex_avg):,}만원")
                with col2:
                    st.metric("최고 보증금", f"{complex_max:,}만원")
                with col3:
                    st.metric("최저 보증금", f"{complex_min:,}만원")
                
                # 선택된 단지 데이터 표시
                st.dataframe(selected_data.sort_values(by='보증금', ascending=False))
                
                # 전체 데이터와 비교
                st.subheader("📊 전체 평균과 비교")
                comparison = int((complex_avg / avg - 1) * 100)
                if comparison > 0:
                    st.info(f"이 단지의 평균 보증금은 전체 평균보다 {comparison}% 높습니다.")
                elif comparison < 0:
                    st.info(f"이 단지의 평균 보증금은 전체 평균보다 {abs(comparison)}% 낮습니다.")
                else:
                    st.info("이 단지의 평균 보증금은 전체 평균과 동일합니다.")
            else:
                # 검색 결과가 없는 경우
                st.warning(f"❌ '{search_query}'에 해당하는 단지가 없습니다.")
                
                # 전체 데이터 표시
                st.subheader("전체 데이터")
                st.dataframe(df_filtered.sort_values(by='보증금', ascending=False))
        else:
            # 검색어가 없는 경우 전체 데이터 표시
            st.dataframe(df_filtered.sort_values(by='보증금', ascending=False))