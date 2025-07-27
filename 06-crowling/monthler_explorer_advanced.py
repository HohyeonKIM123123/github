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

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0')
    return webdriver.Chrome(options=chrome_options)

def extract_int(text):
    if not text:
        return None
    nums = re.findall(r'\d+', text.replace(',', ''))
    return int(nums[0]) if nums else None

def crawl_monthler_simple(max_count=100):
    driver = setup_driver()
    data = []
    try:
        driver.get("https://www.monthler.kr/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        time.sleep(2)

        # "더 보기" 버튼 반복 클릭
        while True:
            try:
                more_btn = driver.find_element(By.XPATH, "//button[contains(text(), '더 보기')]")
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(1)
                if len(driver.find_elements(By.CSS_SELECTOR, "article")) >= max_count:
                    break
            except:
                break

        cards = driver.find_elements(By.CSS_SELECTOR, "article")
        for i, card in enumerate(cards[:max_count]):
            soup = BeautifulSoup(card.get_attribute('outerHTML'), 'html.parser')
            
            name_tag = soup.find(['h3', 'h4', 'h5', 'strong'])
            name = name_tag.get_text(strip=True) if name_tag else f"숙소 {i+1}"
            
            img_tag = soup.find('img')
            img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''
            if img_url.startswith('/'):
                img_url = f"https://www.monthler.kr{img_url}"
            
            region = ""
            region_tag = soup.find('p', class_=re.compile('ProgramCard_txt_detail'))
            if region_tag:
                region = region_tag.get_text(strip=True)
            
            dday = None
            dday_tag = soup.find('span', class_=re.compile('ProgramCard_dday'))
            if dday_tag:
                dday_text = dday_tag.get_text(strip=True)
                dday = 0 if '마감' in dday_text else extract_int(dday_text)
            
            applicants = None
            applicants_tag = soup.find('div', class_=re.compile('ProgramCard_applicantsNumber'))
            if applicants_tag:
                applicants = extract_int(applicants_tag.get_text(strip=True))
            
            지원금 = ""
            subsidy_tag = soup.find('div', class_=re.compile('ProgramCard_txt_subsidy'))
            if subsidy_tag:
                지원금 = subsidy_tag.get_text(strip=True)
            
            모집상태 = dday_tag.get_text(strip=True) if dday_tag else ""

            data.append({
                "name": name,
                "img_url": img_url,
                "region": region,
                "dday": dday,
                "applicants": applicants,
                "지원금": 지원금,
                "모집상태": 모집상태,
                "collected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print(f"[{i+1}] {name} 수집 완료")

    finally:
        driver.quit()
    return data

def main():
    print("📦 한달살러 카드 정보 수집 시작")
    data = crawl_monthler_simple(max_count=100)
    df = pd.DataFrame(data)
    df.to_csv("monthler_simple.csv", index=False, encoding='utf-8-sig')
    print("✅ 저장 완료: monthler_simple.csv")
    print(df.head())

if __name__ == "__main__":
    main()