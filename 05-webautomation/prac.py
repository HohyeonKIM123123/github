from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse
import re
import random

# 가수 이름 입력
singer_name = input("가수 이름을 입력하세요: ")

# 크롬 옵션 설정 (User-Agent, Accept-Language 등 추가)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
chrome_options.add_argument("accept-language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7")

# 크롬 드라이버 열기
driver = webdriver.Chrome(options=chrome_options)

# navigator.webdriver, languages, platform, plugins 속성 완전 제거
stealth_script = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
Object.defineProperty(navigator, 'languages', {get: () => ['ko-KR', 'ko', 'en-US', 'en']});
Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
"""
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": stealth_script}
)

# 멜론 통합검색 페이지로 이동
encoded_name = urllib.parse.quote(singer_name)
search_url = f"https://www.melon.com/search/total/index.htm?q={encoded_name}&section=&mwkLogType=T"
driver.get(search_url)
driver.implicitly_wait(10)
print("브라우저가 열렸습니다.")

# 페이지 로딩 대기
time.sleep(3)

def clean_song_name(song_name):
    """곡명에서 불필요한 텍스트를 제거하는 함수"""
    # 상세정보 페이지 이동, 재생, 담기 등의 텍스트 제거
    unwanted_texts = [
        "상세정보 페이지 이동",
        "재생",
        "담기",
        "HOT",
        "곡정보 보기",
        "페이지 이동"
    ]
    
    cleaned_name = song_name
    for unwanted in unwanted_texts:
        cleaned_name = cleaned_name.replace(unwanted, "")
    
    # 연속된 공백 제거
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    
    return cleaned_name

try:
    # 곡 섹션이 나타날 때까지 대기
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3:contains('곡'), .section_song")))
    
    # 곡 섹션 찾기
    song_section = driver.find_element(By.XPATH, "//h3[contains(text(), '곡')]/following-sibling::*[1]")
    
    # 곡 목록에서 곡명 추출
    song_elements = song_section.find_elements(By.CSS_SELECTOR, "a[href*='goSongDetail'], .ellipsis.rank01 a")
    
    song_names = []
    for i, elem in enumerate(song_elements[:10]):  # 10곡만 추출
        try:
            song_name = elem.text.strip()
            if song_name and len(song_name) > 1:  # 의미있는 텍스트만 추가
                cleaned_name = clean_song_name(song_name)
                if cleaned_name:  # 정리 후에도 텍스트가 남아있으면 추가
                    song_names.append(cleaned_name)
        except:
            continue
    
    # 결과 출력
    if song_names:
        print(f"\n🎵 '{singer_name}'의 곡 제목 리스트:")
        for i, song in enumerate(song_names, 1):
            print(f"{i}. {song}")
    else:
        print(f"\n❌ '{singer_name}'의 곡을 찾을 수 없습니다.")
        
except Exception as e:
    print(f"❌ 곡 목록을 가져오는 중 오류가 발생했습니다: {e}")
    
    # 대안 방법: 다른 선택자 시도
    try:
        print("대안 방법을 시도합니다...")
        
        # 곡 섹션을 다른 방법으로 찾기
        song_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='goSongDetail']")
        
        song_names = []
        for i, elem in enumerate(song_elements[:10]):
            try:
                song_name = elem.text.strip()
                if song_name and len(song_name) > 1:  # 의미있는 텍스트만 추가
                    cleaned_name = clean_song_name(song_name)
                    if cleaned_name:  # 정리 후에도 텍스트가 남아있으면 추가
                        song_names.append(cleaned_name)
            except:
                continue
        
        if song_names:
            print(f"\n🎵 '{singer_name}'의 곡 제목 리스트:")
            for i, song in enumerate(song_names, 1):
                print(f"{i}. {song}")
        else:
            print(f"\n❌ '{singer_name}'의 곡을 찾을 수 없습니다.")
            
    except Exception as e2:
        print(f"❌ 대안 방법도 실패했습니다: {e2}")
        
        # 마지막 대안: 페이지 소스에서 직접 추출
        try:
            print("마지막 대안 방법을 시도합니다...")
            page_source = driver.page_source
            
            # 곡명이 포함된 링크들을 찾기
            song_pattern = r'goSongDetail[^"]*"[^>]*>([^<]+)</a>'
            matches = re.findall(song_pattern, page_source)
            
            song_names = []
            for match in matches[:10]:
                song_name = match.strip()
                if song_name and len(song_name) > 1:
                    cleaned_name = clean_song_name(song_name)
                    if cleaned_name:  # 정리 후에도 텍스트가 남아있으면 추가
                        song_names.append(cleaned_name)
            
            if song_names:
                print(f"\n🎵 '{singer_name}'의 곡 제목 리스트:")
                for i, song in enumerate(song_names, 1):
                    print(f"{i}. {song}")
            else:
                print(f"\n❌ '{singer_name}'의 곡을 찾을 수 없습니다.")
                
        except Exception as e3:
            print(f"❌ 모든 방법이 실패했습니다: {e3}")

# 곡명 추출이 성공한 경우에만 유튜브 자동화 진행
if song_names:
    print("\n[유튜브에서 곡명 검색 및 MP3 변환/다운로드 자동화 시작]")
    for idx, song in enumerate(song_names, 1):
        try:
            # 1. 유튜브에서 곡 검색 및 링크 추출 (오류 방지 강화)
            driver.get("https://www.youtube.com/")
            wait = WebDriverWait(driver, 10)
            try:
                search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#search")))
            except:
                search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.yt-searchbox-input")))
            search_box.clear()
            search_query = f"{singer_name}-{song}"
            search_box.send_keys(search_query)
            search_box.send_keys(Keys.RETURN)

            # 여러 개의 영상 결과 중 실제 영상만 추출
            video_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ytd-video-renderer a#video-title"))
            )
            video_url = None
            for link in video_links:
                href = link.get_attribute("href")
                if href and "watch?v=" in href:
                    video_url = href
                    break

            if not video_url:
                print(f"{idx}. '{search_query}'의 유튜브 영상 링크를 찾을 수 없습니다.")
                continue
            else:
                print(f"{idx}. '{search_query}' → {video_url}")
            # 유튜브 구간에서는 딜레이 없음

            # video_url이 None이 아닐 때만 변환/다운로드 진행
            driver.get("https://ko.onlymp3.io/1/")
            driver.delete_all_cookies()  # 쿠키 초기화(로봇 인증 회피에 도움)
            # 랜덤 딜레이(1~3초)
            time.sleep(random.uniform(1, 3))
            # 사람 행동 시뮬레이션: 스크롤 및 마우스 이동
            driver.execute_script("window.scrollTo(0, 200);")
            time.sleep(random.uniform(0.5, 1.5))
            # 마우스 이동(가상)
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                input_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
                ActionChains(driver).move_to_element(input_box).perform()
            except:
                pass
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            input_box.clear()
            input_box.send_keys(video_url)
            print(f"{idx}. 링크 입력 완료: {video_url}")
            # 랜덤 딜레이(1~3초)
            time.sleep(random.uniform(1, 3))
            convert_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], button.convert"))
            )
            convert_btn.click()
            print(f"{idx}. 변환 버튼 클릭!")
            # 랜덤 딜레이(1~3초)
            time.sleep(random.uniform(1, 3))
            download_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.download-button, a[href*='mp3'], a.btn-download"))
            )
            download_btn.click()
            print(f"{idx}. 다운로드 버튼 클릭!")
            # 다운로드 대기 최소화
            time.sleep(random.uniform(1, 2))
            # 다운로드 후 팝업/경고창 처리
            try:
                alert = driver.switch_to.alert
                alert.accept()
                print(f"{idx}. 경고창 닫음")
            except:
                pass
            # 새 창이 뜨면 닫기
            if len(driver.window_handles) > 1:
                main_window = driver.current_window_handle
                for handle in driver.window_handles:
                    if handle != main_window:
                        driver.switch_to.window(handle)
                        driver.close()
                driver.switch_to.window(main_window)
        except Exception as e:
            print(f"{idx}. '{song}'의 자동화 중 오류: {e}")
            driver.save_screenshot(f'error_{idx}.png')
        # 유튜브 구간에서는 딜레이 없음
else:
    print("\n유튜브/OnlyMP3 자동화는 곡명이 추출된 경우에만 진행됩니다.")

print("\n1초 후 브라우저가 종료됩니다...")
time.sleep(1)
driver.quit()
