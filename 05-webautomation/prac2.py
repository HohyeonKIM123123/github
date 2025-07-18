from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.melon.com/")
driver.implicitly_wait(5)

# 1) 검색
singer_name = input("가수 이름을 입력하세요 : ")
search_box = driver.find_element(By.ID, "top_search")
search_box.send_keys(singer_name, Keys.ENTER)

# 2) 검색 결과 로딩 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR, "table.service_list_song tbody tr"
)))

# 3) 곡이 들어 있는 <tr> 요소들 모두 가져오기
rows = driver.find_elements(By.CSS_SELECTOR, "table.service_list_song tbody tr")

# 4) 앞 10개 행에서 제목만 뽑아서 리스트에 저장
song_names = []
for row in rows[:10]:
    title_elem = row.find_element(By.CSS_SELECTOR, "td.ellipsis.rank01 a")
    song_names.append(title_elem.text)

# 5) 잘 담겼는지 출력
for idx, name in enumerate(song_names, 1):
    print(f"{idx}. {name}")