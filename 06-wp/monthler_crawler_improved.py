import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, Tag
from datetime import datetime
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def extract_int(text):
    if not text:
        return None
    nums = re.findall(r'\d+', text.replace(',', ''))
    return int(nums[0]) if nums else None

def crawl_monthler_real(max_count=100):
    driver = setup_driver()
    data = []
    try:
        driver.get("https://www.monthler.kr/")
        time.sleep(3)
        # 카드가 뜰 때까지 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        # 더보기 반복
        while True:
            try:
                more_btn = driver.find_element(By.XPATH, "//button[contains(text(), '더 보기') or contains(text(), '더보기')]")
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(1.5)
                if len(driver.find_elements(By.CSS_SELECTOR, "article")) >= max_count:
                    break
            except Exception:
                break

        cards = driver.find_elements(By.CSS_SELECTOR, "article")
        for i, card in enumerate(cards[:max_count]):
            try:
                html = card.get_attribute('outerHTML') or ""
                soup = BeautifulSoup(html, 'html.parser')
                # 숙소명
                name = soup.find('h4') or soup.find('h3') or soup.find('h5') or soup.find('strong')
                name = name.get_text(strip=True) if name else f"숙소 {i+1}"
                # 이미지
                img = soup.find('img')
                img_url = img['src'] if img and isinstance(img, Tag) and img.has_attr('src') else ""
                if str(img_url).startswith('/'):
                    img_url = f"https://www.monthler.kr{img_url}"
                # D-day, 지원자수, 지역(카드에서)
                dday = None
                applicants = None
                region = ""
                dday_elem = soup.find('span', class_=re.compile('ProgramCard_dday'))
                if dday_elem:
                    dday_text = dday_elem.get_text(strip=True)
                    if 'D-' in dday_text:
                        dday = extract_int(dday_text)
                    elif '마감' in dday_text:
                        dday = 0
                applicants_elem = soup.find('div', class_=re.compile('ProgramCard_applicantsNumber'))
                if applicants_elem:
                    applicants = extract_int(applicants_elem.get_text())
                region_elem = soup.find('p', class_=re.compile('ProgramCard_txt_detail'))
                if region_elem:
                    region = region_elem.get_text(strip=True)
                # robust 팝업 닫기
                for _ in range(5):
                    try:
                        close_btns = driver.find_elements(By.CSS_SELECTOR, ".fixed.z-50 [class*=close], .fixed.z-50 button, .fixed.z-50 [role=button], .fixed.z-50, .fixed.z-50 [class*=Close], .fixed.z-50 [class*=닫기]")
                        for btn in close_btns:
                            if btn.is_displayed():
                                try:
                                    btn.click()
                                    time.sleep(0.3)
                                except Exception:
                                    pass
                        if not driver.find_elements(By.CSS_SELECTOR, ".fixed.z-50"):
                            break
                    except Exception:
                        break
                    time.sleep(0.2)
                # robust 카드 클릭 (여러 번 재시도)
                click_success = False
                for _ in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                        time.sleep(0.2)
                        card.click()
                        click_success = True
                        break
                    except Exception as e:
                        time.sleep(0.5)
                if not click_success:
                    print(f"카드 {i+1} 클릭 실패: {name}")
                    continue
                # 상세페이지 주요 요소가 뜰 때까지 명확히 대기
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#Detail_program_detail__SPpKX"))
                    )
                except Exception as e:
                    print(f"카드 {i+1} 상세페이지 로딩 실패: {name}, 에러: {e}")
                    driver.back()
                    time.sleep(1.5)
                    continue
                time.sleep(1.0)
                # 상세페이지 정보 robust하게 추출
                detail_html = driver.page_source
                detail_soup = BeautifulSoup(detail_html, 'html.parser')
                # 카테고리
                cat_div = detail_soup.find('div', class_='text-sm pt-0 leading-3')
                카테고리 = ""
                if cat_div and isinstance(cat_div, Tag) and '카테고리' in cat_div.get_text():
                    span = cat_div.find('span')
                    카테고리 = span.get_text(strip=True) if span else ""
                # 상세설명
                desc_elem = detail_soup.find('h3')
                상세설명 = desc_elem.get_text(strip=True) if desc_elem else ""
                # 활동기간, 모집인원, 모집기간, 지원금 등
                모집기간, 모집인원, 활동기간, 지원금 = "", "", "", ""
                for div in detail_soup.find_all('div', class_=re.compile('Detail_info_container')):
                    txt = div.get_text(" ", strip=True)
                    if '활동기간' in txt:
                        활동기간 = txt.split('활동기간 :')[-1].strip()
                    elif '모집인원' in txt:
                        모집인원 = txt.split('모집인원 :')[-1].strip()
                    elif '모집기간' in txt:
                        모집기간 = txt.split('모집기간 :')[-1].strip()
                    elif '지원금' in txt or '최대지원금' in txt:
                        지원금 = txt.split(':')[-1].strip()
                for strong in detail_soup.find_all('strong'):
                    if '지원' in strong.get_text():
                        지원금 += " / " + strong.get_text(strip=True)
                연락처 = ""
                for div in detail_soup.find_all('div', class_=re.compile('text-sm')):
                    if '이메일' in div.get_text() or '전화' in div.get_text():
                        연락처 += div.get_text(" ", strip=True) + " "
                모집상태 = ""
                dday_elem2 = detail_soup.find('span', string=re.compile(r'D-\d+|마감'))
                if dday_elem2:
                    모집상태 = dday_elem2.get_text(strip=True)
                detail_url = driver.current_url
                driver.back()
                time.sleep(1.5)
                card_data = {
                    'name': name,
                    'img_url': img_url,
                    'detail_url': detail_url,
                    'region': region,
                    'dday': dday,
                    'applicants': applicants,
                    '모집기간': 모집기간,
                    '모집인원': 모집인원,
                    '활동기간': 활동기간,
                    '지원금': 지원금,
                    '카테고리': 카테고리,
                    '상세설명': 상세설명,
                    '연락처': 연락처,
                    '모집상태': 모집상태,
                    'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                data.append(card_data)
            except Exception as e:
                print(f"카드 {i+1} 처리 오류: {name if 'name' in locals() else ''}, 에러: {e}")
                continue
        print(f"총 {len(data)}개 프로그램 데이터 수집 완료")
    finally:
        driver.quit()
    return data

def main():
    print("=== 한달살러 프로그램 데이터 크롤링 시작 ===")
    data = crawl_monthler_real(max_count=10)
    df = pd.DataFrame(data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "monthler_processed.csv")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"파일 저장: {output_file}")
    print(df.head())

if __name__ == "__main__":
    main()
