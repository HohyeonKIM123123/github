from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from datetime import datetime
import urllib.parse

def crawl_han():
    """한경글로벌 마켓 크롤링"""
    
    # Chrome 설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("🚀 한경글로벌마켓 크롤링 시작...")
        
        # 1. 한경 메인 페이지 접속
        print("📰 한경 메인 페이지 접속 중...")
        driver.get("https://www.hankyung.com/globalmarket/news-globalmarket")
        time.sleep(3)
        
        # 뉴스 링크 수집
        news_list = []                           
        
        # HTML 문서에서 모든 <a> 태그를 선택함
        links = driver.find_elements(By.XPATH, "//ul[@class='news-list']/li//h2[@class='news-tit']/a")
        
        for i, link in enumerate(links[:10]):  # 상위 10개만
            try:
                title = link.text.strip()
                url = link.get_attribute('href')
                
                # 이미지 URL 추출 (photo 태그 우선)
                img_url = "이미지 없음"  # 기본 값 설정
                try:
                    # 1. 사진 (photo) 관련 이미지 추출
                    img_el = link.find_element(By.XPATH, ".//ancestor::li//img[contains(@src, 'photo')]")
                    img_url = img_el.get_attribute("src")
                    
                    # 이미지 URL을 디코딩하여 추출된 링크를 실제 이미지 링크로
                    img_url = urllib.parse.unquote(img_url)  # 디코딩 처리
                    
                    # 불필요한 아이콘 이미지 (예: 회원 전용 이미지) 제외
                    if 'icon' in img_url or 'svg' in img_url:
                        img_url = "이미지 없음"
                    print(f"🖼️ 추출된 이미지 URL: {img_url}")
                except Exception as e:
                    print(f"⚠️ 이미지 URL 추출 실패: {e}")
                
                if title and url and len(title) > 10:  # 유효한 제목만
                    news_list.append({
                        'index': len(news_list) + 1,
                        'title': title,
                        'link': url,
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'image': img_url
                    })
                    print(f"📰 [{len(news_list)}] {title[:50]}... (이미지: {img_url})")
            except Exception as e:
                print(f"⚠️ 뉴스 항목 처리 실패: {e}")
                continue
        
        return news_list
        
    except Exception as e:
        print(f"❌ 에러: {e}")
        return []
    finally:
        driver.quit()

def save_csv(news_list):
    """CSV 파일 저장"""
    if not news_list:
        print("❌ 저장할 데이터가 없습니다.")
        return
    
    filename = f"it_news_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # CSV 파일 헤더
        writer.writerow(['index', 'title', 'link', 'time'])  # 첫 번째 줄: 제목 정보
        
        # 뉴스 데이터
        for item in news_list:
            writer.writerow([item['index'], item['title'], item['link'], item['time']])  # 첫 번째 줄 (제목)
            writer.writerow([item['image']])  # 두 번째 줄 (이미지 URL)
    
    print(f"✅ 저장완료: {filename} ({len(news_list)}개)")

def main():
    # 크롤링 실행
    news = crawl_han()
    
    # 결과 출력
    if news:
        print(f"\n📊 총 {len(news)}개 뉴스 수집완료!")
        save_csv(news)
    else:
        print("❌ 뉴스를 가져올 수 없습니다.")

if __name__ == "__main__":
    main()