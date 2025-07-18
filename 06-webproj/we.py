import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=chrome_options)

def crawl_monthler():
    url = "https://www.monthler.kr/"
    driver = setup_driver()
    driver.get(url)
    time.sleep(3)

    data = []

    # '더 보기' 버튼 최대 4번 클릭
    for click_count in range(4):
        try:
            more_button = driver.find_element(By.XPATH, "//button[contains(text(), '더 보기')]")
            driver.execute_script("arguments[0].click();", more_button)
            print(f"[+] '더 보기' 클릭 {click_count+1}회")
            time.sleep(2)
        except NoSuchElementException:
            print("[-] '더 보기' 버튼 없음, 클릭 종료")
            break

    # 카드 수집
    cards = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/program"]')
    print(f"[+] 총 {len(cards)}개 카드 발견")

    for idx, card in enumerate(cards):
        try:
            html = card.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            # 링크
            detail_url = card.get_attribute('href')
            if detail_url.startswith("/"):
                detail_url = "https://www.monthler.kr" + detail_url

            # 제목
            title_elem = soup.find(['h3', 'h4', 'strong'])
            title = title_elem.get_text(strip=True) if title_elem else f"제목 없음 {idx+1}"

            # 이미지
            img_elem = soup.find('img')
            img_url = img_elem['src'] if img_elem else ""
            if img_url.startswith('/'):
                img_url = "https://www.monthler.kr" + img_url

            # 텍스트
            text_snippets = soup.get_text(separator='|', strip=True)

            data.append({
                'name': title,
                'detail_url': detail_url,
                'img_url': img_url,
                'raw_text': text_snippets
            })

            print(f"  [{idx+1}] 수집 완료: {title}")

        except Exception as e:
            print(f"[!] 카드 수집 중 오류 ({idx+1}): {e}")
            continue

    driver.quit()
    print(f"[✅] 최종 수집 수: {len(data)}개")
    return data

def process_data(raw_data):
    df = pd.DataFrame(raw_data)

    def extract_city(text):
        cities = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', 
                  '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
        for city in cities:
            if city in text:
                return city
        return '기타'

    df['region_city'] = df['raw_text'].apply(extract_city)
    df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df

def main():
    print("====== 한달살러 숙소 크롤링 시작 ======")
    raw_data = crawl_monthler()

    if not raw_data:
        print("❌ 데이터 없음. 종료")
        return

    df = process_data(raw_data)
    df.to_csv("monthler_processed.csv", index=False, encoding='utf-8-sig')

    print("✅ 저장 완료: monthler_processed.csv")
    print("총 수집 항목 수:", len(df))
    print(df.head(3))

if __name__ == "__main__":
    main()