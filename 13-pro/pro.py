import streamlit as st
import subprocess
import sys
import os

# 필요한 라이브러리 설치 (Streamlit Cloud에서 실행 시 필요)
def install_packages():
    try:
        import selenium
        import webdriver_manager
    except ImportError:
        st.info("필요한 라이브러리를 설치하는 중입니다. 잠시만 기다려주세요...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager", "pandas"])
        st.success("라이브러리 설치가 완료되었습니다. 앱을 다시 시작합니다.")
        st.rerun()
        
# 환경 확인 함수
def is_streamlit_cloud():
    """Streamlit Cloud 환경인지 확인"""
    return os.environ.get('STREAMLIT_SHARING') == 'true' or os.environ.get('IS_STREAMLIT_CLOUD') == 'true'

# 라이브러리 설치 함수 호출
install_packages()

# 필요한 라이브러리 임포트
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# 슬라이더 관련 함수 제거 - 이제 크롤링 후 스트림릿에서 직접 필터링

def fetch_dabang_rooms(region, room_type, deal_types, monthly_range, deposit_range, approval_date="전체", floor_options=[]):
    st.write("[1/9] 크롬 드라이버 실행 중...")
    options = webdriver.ChromeOptions()
    
    # Streamlit Cloud 환경에서는 headless 모드 사용
    if is_streamlit_cloud():
        st.info("Streamlit Cloud 환경에서 실행 중입니다. Headless 모드로 실행합니다.")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
    
    options.add_argument("--start-maximized")
    # 클릭 문제 해결을 위한 옵션 추가
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        st.error(f"크롬 드라이버 실행 실패: {e}")
        st.error("이 앱은 로컬 환경에서만 실행 가능합니다. Streamlit Cloud에서는 웹 브라우저 접근이 제한됩니다.")
        st.info("로컬에서 실행하려면 다음 명령어를 사용하세요: streamlit run pro.py")
        return pd.DataFrame()
    wait = WebDriverWait(driver, 20)

    st.write("[2/9] 다방 접속 중...")
    driver.get("https://www.dabangapp.com/")
    time.sleep(3)  # 로딩 시간 증가

    st.write("[3/9] 지역 검색 중...")
    try:
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search-input")))
        search_input.clear()
        search_input.send_keys(region)
        time.sleep(2)  # 검색 결과가 나타날 때까지 대기
        
        # 검색 결과 목록에서 첫 번째 항목 클릭
        try:
            # 첫 번째 검색 결과 항목 클릭 (JavaScript 사용)
            driver.execute_script("""
                var firstResult = document.querySelector("#search-region-subway-univ-list > div > div > div:nth-child(1) > button:nth-child(1)");
                if (firstResult) {
                    firstResult.click();
                }
            """)
            st.write("✅ 검색 결과에서 첫 번째 항목 선택됨")
        except Exception as e:
            st.warning(f"검색 결과 선택 실패, 엔터키로 대체: {e}")
            search_input.send_keys(Keys.ENTER)
            
        time.sleep(3)  # 로딩 시간 증가
    except Exception as e:
        st.error(f"검색 입력 실패: {e}")
        driver.quit()
        return pd.DataFrame()

    st.write("[4/9] 매물 유형 클릭 중...")
    try:
        # JavaScript로 직접 클릭 (클릭 인터셉트 문제 해결)
        if room_type == "원/투룸":
            driver.execute_script("document.querySelector(\"a[href='/map/onetwo']\").click();")
        elif room_type == "아파트":
            driver.execute_script("document.querySelector(\"a[href='/map/apt']\").click();")
        elif room_type == "주택/빌라":
            driver.execute_script("document.querySelector(\"a[href='/map/house']\").click();")
        elif room_type == "오피스텔":
            driver.execute_script("document.querySelector(\"a[href='/map/officetel']\").click();")
        
        time.sleep(3)  # 로딩 시간 증가
    except Exception as e:
        st.error(f"매물 유형 클릭 실패 (JavaScript): {e}")
        # 대체 방법 시도
        try:
            st.write("대체 방법으로 매물 유형 클릭 시도...")
            map_type = ""
            if room_type == "원/투룸":
                map_type = "onetwo"
            elif room_type == "아파트":
                map_type = "apt"
            elif room_type == "주택/빌라":
                map_type = "house"
            elif room_type == "오피스텔":
                map_type = "officetel"
            
            # URL로 직접 이동
            driver.get(f"https://www.dabangapp.com/map/{map_type}")
            time.sleep(3)
        except Exception as e2:
            st.error(f"대체 방법 매물 유형 접근 실패: {e2}")
            driver.quit()
            return pd.DataFrame()

    st.write("[5/9] 거래유형 버튼 클릭 중...")
    try:
        # JavaScript로 직접 클릭
        driver.execute_script("document.querySelector('button.dock-btn').click();")
        time.sleep(2)
        
        # 거래 유형 설정 (매매 포함)
        deal_dict = {"월세": "월세", "전세": "전세", "매매": "매매"}
        for label, text in deal_dict.items():
            if label in deal_types:
                try:
                    # JavaScript로 체크박스 상태 확인 및 변경
                    is_checked = driver.execute_script(f"""
                        var checkbox = document.evaluate("//p[text()='{text}']/preceding-sibling::input", 
                                                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return checkbox.checked;
                    """)
                    
                    if not is_checked:
                        driver.execute_script(f"""
                            var checkbox = document.evaluate("//p[text()='{text}']/preceding-sibling::input", 
                                                            document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            checkbox.click();
                        """)
                        st.write(f"✅ {label} 체크됨")
                except Exception as e:
                    st.warning(f"{label} 체크박스 처리 중 오류: {e}")
            else:
                try:
                    # JavaScript로 체크박스 상태 확인 및 변경
                    is_checked = driver.execute_script(f"""
                        var checkbox = document.evaluate("//p[text()='{text}']/preceding-sibling::input", 
                                                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (checkbox) return checkbox.checked;
                        return false;
                    """)
                    
                    if is_checked:
                        driver.execute_script(f"""
                            var checkbox = document.evaluate("//p[text()='{text}']/preceding-sibling::input", 
                                                            document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (checkbox) checkbox.click();
                        """)
                        st.write(f"❌ {label} 체크 해제됨")
                except Exception as e:
                    st.warning(f"{label} 체크박스 처리 중 오류: {e}")
        
        # 확인 버튼 클릭
        time.sleep(1)
        try:
            driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.includes('확인')) {
                        buttons[i].click();
                        break;
                    }
                }
            """)
            time.sleep(1)
        except:
            pass
    except Exception as e:
        st.error(f"거래유형 열기 실패: {e}")
        driver.quit()
        return pd.DataFrame()
        
    # 사용승인일 필터 적용
    if approval_date != "전체":
        st.write("[5-1/9] 사용승인일 필터 적용 중...")
        try:
            # 사용승인일 버튼 클릭
            driver.execute_script("""
                var buttons = document.querySelectorAll('button.dock-btn');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.includes('사용승인일')) {
                        buttons[i].click();
                        break;
                    }
                }
            """)
            time.sleep(1)
            
            # 선택한 사용승인일 옵션 클릭
            option_text = approval_date
            driver.execute_script(f"""
                var labels = document.querySelectorAll('label');
                for (var i = 0; i < labels.length; i++) {{
                    if (labels[i].textContent.includes('{option_text}')) {{
                        labels[i].click();
                        break;
                    }}
                }}
            """)
            time.sleep(1)
            
            # 확인 버튼 클릭
            driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.includes('확인')) {
                        buttons[i].click();
                        break;
                    }
                }
            """)
            time.sleep(1)
            st.write(f"✅ 사용승인일 '{approval_date}' 필터 적용됨")
        except Exception as e:
            st.warning(f"사용승인일 필터 적용 중 오류: {e}")
            # 계속 진행
            
    # 층수 필터 적용
    if floor_options:
        st.write("[5-2/9] 층수 필터 적용 중...")
        try:
            # 층수 버튼 클릭 - 정확한 선택자 사용
            driver.execute_script("""
                // 1. 정확한 선택자로 층수 버튼 찾기 (제공된 선택자 사용)
                var floorButtons = document.querySelectorAll('.sc-esMOmu.cMGjks > div > button');
                
                // 모든 버튼 확인
                for (var i = 0; i < floorButtons.length; i++) {
                    var buttonText = floorButtons[i].textContent || '';
                    if (buttonText.includes('층수')) {
                        floorButtons[i].click();
                        console.log('층수 버튼 클릭 성공');
                        return true;
                    }
                }
                
                // 2. 다른 방법으로 시도
                var dockButtons = document.querySelectorAll('.dock-btn');
                for (var i = 0; i < dockButtons.length; i++) {
                    var buttonText = dockButtons[i].textContent || '';
                    if (buttonText.includes('층수')) {
                        dockButtons[i].click();
                        console.log('dock-btn 클래스로 층수 버튼 클릭 성공');
                        return true;
                    }
                }
                
                // 3. 모든 버튼 시도
                var allButtons = document.querySelectorAll('button');
                for (var i = 0; i < allButtons.length; i++) {
                    var buttonText = allButtons[i].textContent || '';
                    if (buttonText.includes('층수')) {
                        allButtons[i].click();
                        console.log('일반 버튼으로 층수 버튼 클릭 성공');
                        return true;
                    }
                }
                
                console.log('층수 버튼을 찾을 수 없음');
                return false;
            """)
            
            # 충분한 대기 시간 추가
            time.sleep(3)
            
            time.sleep(2)  # 층수 옵션이 나타날 때까지 충분히 대기
            
            # 기본적으로 모든 층수 옵션이 선택되어 있으므로, 
            # 사용자가 선택한 옵션만 남기고 나머지는 해제
            
            # 모든 층수 옵션
            all_floor_options = ["1층", "2층이상", "반지하", "옥탑"]
            
            # 사용자가 선택하지 않은 옵션 해제
            for option in all_floor_options:
                if option not in floor_options:
                    driver.execute_script(f"""
                        var labels = document.querySelectorAll('label');
                        for (var i = 0; i < labels.length; i++) {{
                            if (labels[i].textContent.includes('{option}')) {{
                                // 이미 선택되어 있다면 클릭하여 해제
                                var input = labels[i].querySelector('input');
                                if (input && input.checked) {{
                                    labels[i].click();
                                }}
                                break;
                            }}
                        }}
                    """)
                    time.sleep(0.5)
                    st.write(f"❌ '{option}' 층수 필터 해제됨")
            
            # 사용자가 선택한 옵션이 해제되어 있다면 다시 선택
            for option in floor_options:
                driver.execute_script(f"""
                    var labels = document.querySelectorAll('label');
                    for (var i = 0; i < labels.length; i++) {{
                        if (labels[i].textContent.includes('{option}')) {{
                            // 선택되어 있지 않다면 클릭하여 선택
                            var input = labels[i].querySelector('input');
                            if (input && !input.checked) {{
                                labels[i].click();
                            }}
                            break;
                        }}
                    }}
                """)
                time.sleep(0.5)
                st.write(f"✅ '{option}' 층수 필터 적용됨")
            
            # 확인 버튼 클릭
            driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {
                    if (buttons[i].textContent.includes('확인')) {
                        buttons[i].click();
                        break;
                    }
                }
            """)
            time.sleep(1)
        except Exception as e:
            st.warning(f"층수 필터 적용 중 오류: {e}")
            # 계속 진행

    # 슬라이더 조정 단계 생략 - 크롤링 후 스트림릿에서 직접 필터링
    st.write("[6/9] 매물 데이터 수집 준비 중...")

    st.write("[7/9] 매물 정보 로딩 중...")
    try:
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)
        
        # 매물 유형에 따라 다른 선택자 사용
        selector = "#onetwo-list > div > ul > li"
        if room_type == "아파트":
            selector = "#apt-list > div > ul > li"
        elif room_type == "주택/빌라":
            selector = "#house-list > div > ul > li"
        elif room_type == "오피스텔":
            selector = "#officetel-list > div > ul > li"
            
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

        items = driver.find_elements(By.CSS_SELECTOR, selector)
        st.write(f"총 매물: {len(items)}개")
    except Exception as e:
        st.error(f"매물 목록 로딩 실패: {e}")
        driver.quit()
        return pd.DataFrame()

    st.write("[8/9] 매물 파싱 중...")
    data = []
    for idx, item in enumerate(items[:100]):
        try:
            img = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            # 가격/타입
            try:
                price_title = item.find_element(By.CSS_SELECTOR, "h1").text
            except:
                price_title = ""
            # 방옵션
            try:
                room_info = item.find_element(By.CSS_SELECTOR, "p").text
            except:
                room_info = ""
            # 면적/층/관리비
            try:
                area_floor_fee = item.find_elements(By.CSS_SELECTOR, "p")[1].text
            except:
                area_floor_fee = ""
            # 설명
            try:
                desc = item.find_elements(By.CSS_SELECTOR, "p")[2].text
            except:
                desc = ""
            data.append({
                "썸네일": img,
                "가격/타입": price_title,
                "방옵션": room_info,
                "면적/층/관리비": area_floor_fee,
                "설명": desc
            })
            st.write(f"{idx+1}번째 매물 파싱 완료: {price_title}")
        except Exception as e:
            st.warning(f"{idx+1}번 매물 오류: {e}")
            continue

    driver.quit()
    st.write("[9/9] 크롤링 완료 ✅")
    return pd.DataFrame(data)

# 가격 정보 추출 함수
def extract_price_info(price_text):
    """가격/타입 텍스트에서 보증금과 월세 추출"""
    deposit = 0
    monthly = 0
    deal_type = "월세"  # 기본값
    
    try:
        # 디버깅용 출력
        # st.write(f"가격 정보 파싱: {price_text}")
        
        if '/' in price_text:  # 월세 형식 (보증금/월세)
            deal_type = "월세"
            parts = price_text.split('/')
            
            # 첫 번째 부분은 보증금
            deposit_part = parts[0].strip()
            deposit = parse_korean_amount(deposit_part)
            
            # 두 번째 부분은 월세
            monthly_part = parts[1].strip()
            monthly = parse_korean_amount(monthly_part)
        
        elif '전세' in price_text:  # 전세 형식
            deal_type = "전세"
            # 전세는 보증금만 있고 월세는 0
            deposit_part = price_text.replace('전세', '').strip()
            deposit = parse_korean_amount(deposit_part)
            monthly = 0
            
        elif '매매' in price_text:  # 매매 형식
            deal_type = "매매"
            # 매매는 매매가만 있고 월세는 0
            price_part = price_text.replace('매매', '').strip()
            deposit = parse_korean_amount(price_part)
            monthly = 0
            
        else:  # 숫자만 있는 경우 (전세로 간주)
            deal_type = "전세"
            deposit = parse_korean_amount(price_text)
            monthly = 0
            
    except Exception as e:
        st.warning(f"가격 정보 추출 중 오류: {e} - {price_text}")
        
    return deposit, monthly, deal_type

def parse_korean_amount(amount_text):
    """한국식 금액 표기(억, 만)를 숫자로 변환"""
    try:
        import re
        
        # 숫자만 추출
        amount = 0
        
        # "억" 처리
        if '억' in amount_text:
            billion_parts = amount_text.split('억')
            
            # 억 단위 추출
            billion_value = re.findall(r'\d+', billion_parts[0])
            if billion_value:
                amount += int(billion_value[0]) * 10000  # 1억 = 10000만원
            
            # 억 이하 단위 추출
            if len(billion_parts) > 1 and billion_parts[1].strip():
                million_value = re.findall(r'\d+', billion_parts[1])
                if million_value:
                    amount += int(million_value[0])
        else:
            # 억 단위가 없는 경우
            numbers = re.findall(r'\d+', amount_text)
            if numbers:
                amount = int(numbers[0])
        
        return amount
    except Exception as e:
        st.warning(f"금액 파싱 오류: {e} - {amount_text}")
        return 0

# 나무 원목 스타일 CSS
def load_wood_style():
    return """
    <style>
    .wood-container {
        background-color: #f5f1e8;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(139, 69, 19, 0.2);
        border: 1px solid #d9b38c;
    }
    
    .wood-header {
        background: linear-gradient(to right, #8B4513, #A0522D);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-weight: bold;
        text-align: center;
    }
    
    .wood-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 0;
        border-left: 5px solid #8B4513;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    
    .uniform-card {
        min-height: 180px;
        display: flex;
        flex-direction: column;
    }
    
    .price-tag {
        background-color: #8B4513;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .room-info {
        color: #5D4037;
        font-size: 14px;
        margin-bottom: 5px;
    }
    
    .room-desc {
        color: #795548;
        font-style: italic;
        margin-top: auto;
    }
    
    .filter-section {
        background-color: #e8dcc9;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #d9b38c;
    }
    
    .filter-title {
        color: #5D4037;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .property-card-container {
        margin-bottom: 20px;
        border-bottom: 1px solid #d9b38c;
        padding-bottom: 20px;
    }
    
    .card-divider {
        border: 0;
        height: 1px;
        background-color: #d9b38c;
        margin: 10px 0;
    }
    
    .no-image {
        background-color: #e8dcc9;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #8B4513;
        font-style: italic;
        border-radius: 8px;
    }
    
    /* 이미지 크기 통일 */
    .stImage img {
        object-fit: cover;
        height: 200px;
        width: 100%;
        border-radius: 8px;
    }
    </style>
    """

# ================================
# Streamlit UI - 메인 페이지와 결과 페이지 분리
# ================================
st.set_page_config(page_title="다방 매물 크롤러", layout="wide")
st.markdown(load_wood_style(), unsafe_allow_html=True)

# 페이지 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'search'

# 검색 페이지
if st.session_state.page == 'search':
    st.markdown('<h1 style="color:#8B4513; text-align:center;">🏠 다방 매물 실시간 크롤링</h1>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="wood-container">', unsafe_allow_html=True)
        
        region = st.text_input("📍 지역 입력 (예: 서울시 마포구 합정동)")
        
        col1, col2 = st.columns(2)
        with col1:
            room_type = st.radio("🏠 매물 유형 선택", ["원/투룸", "아파트", "주택/빌라", "오피스텔"], horizontal=True)
        with col2:
            # 매물 유형에 따라 거래 유형 옵션 변경
            if room_type == "원/투룸":
                deal_type_options = ["월세", "전세"]
            else:
                deal_type_options = ["월세", "전세", "매매"]
            
            deal_types = st.multiselect("💰 거래 유형 선택", deal_type_options, default=deal_type_options[:2])
        
        # 사용승인일 선택 추가
        approval_date = st.selectbox("🗓️ 사용승인일", ["전체", "5년 이내", "10년 이내", "15년 이내", "15년 이상"], index=0)
        
        # 층수 필터 추가 - 기본값으로 모든 옵션 선택
        floor_options = st.multiselect("🏢 층수", ["1층", "2층이상", "반지하", "옥탑"], 
                                     default=["1층", "2층이상", "반지하", "옥탑"],
                                     help="선택하지 않으면 모든 층수가 포함됩니다")
        
        if st.button("🔍 검색 시작", key="search_btn"):
            # 지역 입력 유효성 검사
            if not region.strip():
                st.error("지역을 입력해주세요!")
            else:
                with st.spinner("크롤링 중..."):
                    # 슬라이더 값은 크롤링에 사용하지 않고 나중에 필터링에만 사용
                    df = fetch_dabang_rooms(region, room_type, deal_types, (0, 500), (0, 20000), approval_date, floor_options)
            
            if not df.empty:
                # 데이터프레임에 보증금, 월세, 거래유형 컬럼 추가
                df['보증금'] = 0
                df['월세'] = 0
                df['거래유형'] = ""
                
                # 가격 정보 추출
                for idx, row in df.iterrows():
                    deposit, monthly, deal_type = extract_price_info(row['가격/타입'])
                    df.at[idx, '보증금'] = deposit
                    df.at[idx, '월세'] = monthly
                    df.at[idx, '거래유형'] = deal_type
                
                # 세션 상태에 데이터 저장
                st.session_state.crawled_data = df
                st.session_state.room_type = room_type
                st.session_state.region = region
                st.session_state.approval_date = approval_date
                
                # 결과 페이지로 이동
                st.session_state.page = 'results'
                st.rerun()
            else:
                st.warning("매물을 찾을 수 없습니다.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 결과 페이지
elif st.session_state.page == 'results':
    df = st.session_state.crawled_data
    room_type = st.session_state.room_type
    region = st.session_state.region
    approval_date = st.session_state.approval_date if 'approval_date' in st.session_state else "전체"
    
    # 헤더 및 검색 정보
    st.markdown(f'<h1 style="color:#8B4513; text-align:center;">🏠 {region} {room_type} 매물 검색 결과</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:#5D4037;">사용승인일: {approval_date}</p>', unsafe_allow_html=True)
    
    # 뒤로가기 버튼
    if st.button("← 새 검색하기"):
        st.session_state.page = 'search'
        st.rerun()
    
    # 필터링 섹션
    st.markdown('<div class="wood-container">', unsafe_allow_html=True)
    st.markdown('<div class="wood-header">매물 필터링</div>', unsafe_allow_html=True)
    
    # 거래 유형 필터
    deal_types = df['거래유형'].unique().tolist()
    selected_deal_types = st.multiselect("거래 유형", deal_types, default=deal_types)
    
    col1, col2 = st.columns(2)
    with col1:
        # 보증금 최대값 계산 (데이터 기반)
        max_deposit = max(df['보증금'].max(), 20000)
        deposit_range = st.slider("보증금/매매가 범위 (만 원)", 
                                 0, int(max_deposit), 
                                 (0, int(max_deposit)), 
                                 step=100)
    
    with col2:
        # 월세 최대값 계산 (데이터 기반)
        max_monthly = max(df['월세'].max(), 500)
        monthly_range = st.slider("월세 범위 (만 원)", 
                                 0, int(max_monthly), 
                                 (0, int(max_monthly)), 
                                 step=5)
    
    # 필터링 적용
    filtered_df = df[
        (df['보증금'] >= deposit_range[0]) & 
        (df['보증금'] <= deposit_range[1]) & 
        (df['월세'] >= monthly_range[0]) & 
        (df['월세'] <= monthly_range[1]) &
        (df['거래유형'].isin(selected_deal_types))
    ]
    
    st.markdown(f'<div class="filter-title">검색 결과: {len(filtered_df)}건</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 표시
    if not filtered_df.empty:
        st.markdown('<div class="wood-container">', unsafe_allow_html=True)
        st.markdown('<div class="wood-header">매물 목록</div>', unsafe_allow_html=True)
        
        # 매물 카드 표시 (1xn 형식으로 표시)
        for idx, row in filtered_df.iterrows():
            # 각 카드를 감싸는 컨테이너
            st.markdown('<div class="property-card-container">', unsafe_allow_html=True)
            
            # 이미지와 정보를 가로로 배치
            col1, col2 = st.columns([1, 2])
            
            # 왼쪽 열: 이미지
            with col1:
                if row['썸네일'] and row['썸네일'] != "":
                    st.image(row['썸네일'], use_container_width=True)
                else:
                    # 이미지가 없을 경우 대체 이미지나 메시지
                    st.markdown('<div class="no-image">이미지 없음</div>', unsafe_allow_html=True)
            
            # 오른쪽 열: 매물 정보
            with col2:
                st.markdown(f'''
                <div class="wood-card uniform-card">
                    <div class="price-tag">{row['가격/타입']}</div>
                    <div class="room-info"><strong>방 정보:</strong> {row['방옵션']}</div>
                    <div class="room-info"><strong>상세:</strong> {row['면적/층/관리비']}</div>
                    <div class="room-desc">{row['설명']}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # 구분선 추가
            st.markdown('<hr class="card-divider">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 원본 데이터 표시 옵션
        with st.expander("원본 데이터 보기"):
            st.dataframe(filtered_df)
    else:
        st.warning("선택한 조건에 맞는 매물이 없습니다. 필터 조건을 변경해보세요.")

    