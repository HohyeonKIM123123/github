import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import datetime

# 🚩 1. 법정동 코드 불러오기
@st.cache_data
def load_legal_codes(filepath='법정동코드.txt'):
    # EUC-KR 또는 CP949 인코딩으로 파일 읽기
    df = pd.read_csv(filepath, sep='\t', dtype=str, encoding='cp949')
    df = df[df['폐지여부'] == '존재']  # 폐지된 동 제외
    df['법정동명'] = df['법정동명'].str.strip()
    return df

legal_df = load_legal_codes()

# 🚩 2. 법정동 이름 → 코드 변환
def get_legal_code(addr):
    st.info(f"🔍 주소 '{addr}'에서 법정동 코드 검색 중...")
    
    # 주소 분석을 위한 전처리
    addr = addr.replace('  ', ' ').strip()  # 중복 공백 제거
    
    # 주소를 공백으로 분리하여 각 부분 추출
    parts = addr.split()
    
    if len(parts) < 2:
        st.error("❌ 주소가 너무 짧습니다. 시/도, 시/군/구, 동/읍/면을 포함해주세요.")
        return None
    
    # 검색 방법 1: 전체 주소로 정확히 매칭
    st.write("🔍 방법 1: 전체 주소로 정확히 매칭 시도")
    exact_match = legal_df[legal_df['법정동명'] == addr]
    if not exact_match.empty:
        code = exact_match.iloc[0]['법정동코드'][:5]
        st.success(f"✅ 정확한 매칭 성공! '{addr}' (코드: {code})")
        return code
    
    # 검색 방법 2: 시/도 + 시/군/구 + 동/읍/면 조합으로 검색
    st.write("🔍 방법 2: 시/도 + 시/군/구 + 동/읍/면 조합으로 검색")
    
    # 주소 조합 생성 (뒤에서부터 조합)
    combinations = []
    for i in range(1, min(4, len(parts) + 1)):
        for j in range(len(parts) - i + 1):
            combo = ' '.join(parts[j:j+i])
            combinations.append(combo)
    
    # 가장 구체적인(긴) 조합부터 검색
    combinations.sort(key=len, reverse=True)
    
    for combo in combinations:
        st.write(f"- 검색 중: '{combo}'")
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
    
    # 검색 방법 3: 동/읍/면 이름만으로 검색 (마지막 부분)
    if len(parts) >= 1:
        last_part = parts[-1]
        st.write(f"🔍 방법 3: 동/읍/면 이름만으로 검색 - '{last_part}'")
        
        # 동/읍/면 이름으로 끝나는 법정동 검색
        dong_matches = legal_df[legal_df['법정동명'].str.endswith(last_part)]
        
        if not dong_matches.empty:
            # 시/도 또는 시/군/구가 주소에 포함된 결과 우선
            for i in range(len(parts) - 1):
                filtered = dong_matches[dong_matches['법정동명'].str.contains(parts[i])]
                if not filtered.empty:
                    dong_matches = filtered
                    break
            
            code = dong_matches.iloc[0]['법정동코드'][:5]
            full_name = dong_matches.iloc[0]['법정동명']
            st.success(f"✅ 동/읍/면 매칭 성공! '{last_part}' → '{full_name}' (코드: {code})")
            return code
    
    st.error("❌ 주소에서 법정동 코드를 찾을 수 없습니다.")
    st.warning("💡 팁: '서울특별시 강남구 역삼동'과 같이 시/도, 시/군/구, 동/읍/면을 모두 포함하여 입력해보세요.")
    return None

# 🚩 3. 국토부 실거래가 API 요청
def fetch_rent_data(code, ym, service_key):
    # 직접 작동하는 URL 사용
    # 디코딩된 서비스 키
    decoded_key = "Pc/JQOiyQ467BxatmVf2UbZKY9eyzrJuSHu383ozvdaXp0GVEgRInW1EbE2AO6JGmjp8ghHpq90Y4m0G6FV7nQ=="
    
    # 요청 헤더 추가
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    
    # HTTP URL 사용 (SSL 오류 방지)
    url = f"http://apis.data.go.kr/1613000/RTMSDataSvcRHRent/getRTMSDataSvcRHRent?serviceKey={decoded_key}&LAWD_CD={code}&DEAL_YMD={ym}&numOfRows=100&pageNo=1"
    
    try:
        st.info(f"🔄 API 요청 중: {url}")
        st.write(f"법정동 코드: {code}, 계약년월: {ym}")
        
        # 세션 생성 및 타임아웃 설정
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
        
        # 직접 URL로 요청
        st.write("API 요청 시작... (최대 10분 소요)")
        res = session.get(url, headers=headers, verify=False, timeout=600)  # 타임아웃 10분으로 증가
        
        if res.status_code != 200:
            st.warning(f"⚠️ API 요청 실패: 상태 코드 {res.status_code}")
            return None
        
        # 응답에 오류 메시지가 포함되어 있는지 확인
        if "SERVICE_KEY_IS_NOT_REGISTERED_ERROR" in res.text:
            st.warning("⚠️ API 키 오류: 등록되지 않은 API 키입니다.")
            return None
        
        if "OpenAPI_ServiceResponse" in res.text and "errMsg" in res.text:
            st.warning("⚠️ API 응답에 오류 메시지가 포함되어 있습니다.")
            return None
        
        # XML 파싱
        try:
            root = ET.fromstring(res.content)
        except ET.ParseError as e:
            st.error(f"❌ XML 파싱 오류: {str(e)}")
            return None
        
        # 항목 찾기
        items = root.findall(".//item")
        
        # 항목이 없으면 다른 경로 시도
        if not items:
            items = root.findall(".//items/item")
        
        # 그래도 없으면 다른 경로 시도
        if not items:
            items = root.findall("*//item")
        
        if len(items) == 0:
            st.warning("⚠️ 검색된 데이터가 없습니다.")
            return None
        
        # 데이터 처리
        results = []
        for item in items:
            try:
                # 필수 정보 확인
                deposit_elem = item.find("deposit") or item.find("보증금액")
                area_elem = item.find("excluUseAr") or item.find("전용면적")
                apt_elem = item.find("aptNm") or item.find("아파트")
                
                if deposit_elem is None or area_elem is None:
                    continue
                
                # 데이터 추출 및 변환
                deposit_text = deposit_elem.text.replace(",", "").replace(" ", "")
                deposit = int(deposit_text) if deposit_text else 0
                
                area_text = area_elem.text
                area = float(area_text) if area_text else 0
                
                apt = apt_elem.text if apt_elem is not None and apt_elem.text else "정보없음"
                
                # 추가 정보 (있는 경우만)
                floor_elem = item.find("floor") or item.find("층")
                floor = floor_elem.text if floor_elem is not None else None
                
                build_year_elem = item.find("buildYear") or item.find("건축년도")
                build_year = build_year_elem.text if build_year_elem is not None else None
                
                # 계약일 정보
                deal_year_elem = item.find("dealYear") or item.find("년")
                deal_month_elem = item.find("dealMonth") or item.find("월")
                deal_day_elem = item.find("dealDay") or item.find("일")
                
                deal_date = None
                if deal_year_elem is not None and deal_month_elem is not None and deal_day_elem is not None:
                    deal_year = deal_year_elem.text
                    deal_month = deal_month_elem.text.zfill(2)
                    deal_day = deal_day_elem.text.zfill(2)
                    deal_date = f"{deal_year}-{deal_month}-{deal_day}"
                
                # 월세 정보
                monthly_rent_elem = item.find("monthlyRent") or item.find("월세")
                monthly_rent = None
                if monthly_rent_elem is not None and monthly_rent_elem.text.strip() != "0":
                    monthly_rent = int(monthly_rent_elem.text.replace(",", "").replace(" ", ""))
                
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
            except Exception as e:
                continue
        
        df = pd.DataFrame(results)
        if not df.empty:
            st.success(f"📋 처리된 데이터 건수: {len(df)}개")
            return df
        else:
            st.warning("⚠️ 데이터 처리 후 결과가 없습니다.")
            return None
            
    except Exception as e:
        st.error(f"❌ API 요청 중 오류 발생: {str(e)}")
        
    # API 요청 실패 시 샘플 데이터 제공
    st.info("📊 API 서버에 연결할 수 없어 참고용 샘플 데이터를 제공합니다.")
    
    import numpy as np
    
    # 지역 코드에 따라 다른 평균 보증금 설정
    region_code = int(code[:2])
    if region_code == 11:  # 서울
        area_ranges = [(20, 40, 25000), (40, 60, 35000), (60, 85, 45000), (85, 120, 60000)]
        apt_names = ["래미안", "자이", "힐스테이트", "푸르지오", "롯데캐슬", "e편한세상", "더샵", "아이파크"]
    elif region_code in [28, 41]:  # 인천, 경기
        area_ranges = [(20, 40, 15000), (40, 60, 22000), (60, 85, 30000), (85, 120, 40000)]
        apt_names = ["래미안", "자이", "힐스테이트", "푸르지오", "동양", "신성", "우방", "두산"]
    else:  # 기타 지역
        area_ranges = [(20, 40, 8000), (40, 60, 12000), (60, 85, 18000), (85, 120, 25000)]
        apt_names = ["푸르지오", "동양", "신성", "우방", "두산", "대우", "현대", "삼성"]
    
    # 샘플 데이터 생성
    sample_size = 20
    sample_data = []
    
    # 현재 날짜 기준으로 최근 3개월 내 날짜 생성
    today = datetime.datetime.now()
    
    for i in range(sample_size):
        # 면적 범위 랜덤 선택
        area_min, area_max, avg_deposit = area_ranges[np.random.randint(0, len(area_ranges))]
        
        # 면적은 선택된 범위 내에서 랜덤 생성
        sample_area = round(np.random.uniform(area_min, area_max), 2)
        
        # 보증금은 평균의 80%~120% 사이에서 랜덤 생성 (100만원 단위로 반올림)
        variation = np.random.uniform(0.8, 1.2)
        sample_deposit = int(round(avg_deposit * variation / 100) * 100)
        
        # 아파트 이름 랜덤 선택
        apt_name = np.random.choice(apt_names)
        apt_number = np.random.randint(1, 5)
        
        # 거래 날짜 생성 (최근 3개월 내)
        days_ago = np.random.randint(1, 90)
        deal_date = today - datetime.timedelta(days=days_ago)
        
        sample_data.append({
            "단지": f"{apt_name} {apt_number}차",
            "보증금": sample_deposit,
            "면적": sample_area,
            "층": np.random.randint(1, 20),
            "거래일": deal_date.strftime("%Y-%m-%d"),
            "건축년도": str(np.random.randint(1990, 2020))
        })
    
    df = pd.DataFrame(sample_data)
    
    # 면적 기준으로 정렬
    df = df.sort_values(by='면적')
    
    return df

# 🚩 4. 유사 면적 필터링
def filter_by_area(df, area, tol=3):
    return df[(df['면적'] >= area - tol) & (df['면적'] <= area + tol)]

# 🚩 Streamlit UI
st.title("🏠 전세 시세 위험도 분석기")
st.markdown("전용면적 기준 실거래가와 입력 보증금을 비교합니다.")

address = st.text_input("📍 주소 (예: 서울특별시 강남구 역삼동)")
area = st.number_input("� 전주용면적 (㎡)", min_value=0.0, step=0.1)
deposit = st.number_input("💰 보증금 (만원)", min_value=0)

# 최근 12개월 옵션 생성
import datetime
current_date = datetime.datetime.now()
month_options = []
for i in range(12):
    date = current_date - datetime.timedelta(days=30*i)
    month_options.append(date.strftime("%Y%m"))

month = st.selectbox("📅 기준 월", options=month_options)
search_period = st.radio("� 검,색 기간", ["선택한 월만", "1년치 데이터"], index=0)

if st.button("🔍 분석하기"):
    code = get_legal_code(address)
    if not code:
        st.error("주소에서 법정동 코드를 찾을 수 없습니다.")
    else:
        st.write(f"▶ 법정동 코드: `{code}`")
        # 인코딩된 키 사용
        key = "Pc%2FJQOiyQ467BxatmVf2UbZKY9eyzrJuSHu383ozvdaXp0GVEgRInW1EbE2AO6JGmjp8ghHpq90Y4m0G6FV7nQ%3D%3D"
        
        # 검색 기간에 따라 처리
        if search_period == "선택한 월만":
            # 선택한 월만 검색
            st.info(f"📅 {month} 기준 데이터를 검색합니다.")
            df = fetch_rent_data(code, month, key)
        else:
            # 1년치 데이터 검색
            st.info("📅 최근 1년치 데이터를 검색합니다.")
            
            # 진행 상황 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 최근 12개월 데이터 수집
            all_data = []
            for i, m in enumerate(month_options[:12]):
                status_text.text(f"🔍 {m} 데이터 검색 중... ({i+1}/12)")
                progress_bar.progress((i+1)/12)
                
                month_df = fetch_rent_data(code, m, key)
                if month_df is not None and not month_df.empty:
                    # 월 정보 추가
                    month_df['거래월'] = m
                    all_data.append(month_df)
            
            # 모든 데이터 합치기
            if all_data:
                df = pd.concat(all_data, ignore_index=True)
                st.success(f"✅ 총 {len(df)}개의 데이터를 수집했습니다.")
            else:
                df = None
                st.warning("❌ 1년치 데이터를 찾을 수 없습니다.")
            
            # 진행 상황 표시 제거
            status_text.empty()
        
        if df is None or df.empty:
            st.warning("해당 조건의 실거래 데이터를 찾을 수 없습니다.")
        else:
            # 데이터 요약 정보 표시
            st.info(f"📊 수집된 전체 데이터: {len(df)}건")
            
            # 면적 필터링
            df_filtered = filter_by_area(df, area)
            
            if df_filtered.empty:
                st.warning(f"⚠️ 전용면적 {area}㎡ 근처(±3㎡)의 데이터가 없습니다.")
            else:
                st.success(f"✅ 전용면적 {area}㎡ 근처(±3㎡)의 데이터: {len(df_filtered)}건")
                
                # 통계 계산
                avg = df_filtered['보증금'].mean()
                max_d = df_filtered['보증금'].max()
                min_d = df_filtered['보증금'].min()
                median = df_filtered['보증금'].median()

                # 결과 표시
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 평균 보증금", f"{int(avg):,}만원")
                    st.metric("� 최고 보보증금", f"{max_d:,}만원")
                with col2:
                    st.metric("📉 최저 보증금", f"{min_d:,}만원")
                    st.metric("� 최중간값", f"{int(median):,}만원")

                # 위험도 분석
                st.subheader("💰 보증금 위험도 분석")
                if deposit > avg * 1.2:
                    st.error("⚠️ 입력 보증금이 평균보다 **20% 이상 높습니다**. 주의하세요!")
                    st.write(f"- 입력 보증금 {deposit:,}만원은 평균 {int(avg):,}만원보다 {int((deposit/avg-1)*100)}% 높습니다.")
                elif deposit < avg * 0.8:
                    st.success("✅ 입력 보증금이 평균보다 낮습니다.")
                    st.write(f"- 입력 보증금 {deposit:,}만원은 평균 {int(avg):,}만원보다 {int((1-deposit/avg)*100)}% 낮습니다.")
                else:
                    st.info("ℹ️ 입력 보증금이 평균과 유사한 수준입니다.")
                    st.write(f"- 입력 보증금 {deposit:,}만원은 평균 {int(avg):,}만원과 비슷한 수준입니다.")

                # 데이터 테이블 표시
                st.subheader("📋 상세 데이터")
                st.dataframe(df_filtered.sort_values(by='보증금', ascending=False))