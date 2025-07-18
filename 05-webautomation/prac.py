# ex01.py

# 1. 멜론에 접속, 
# 2. 가수 이름 타이핑.
# 3. 곡 목록 10개를 각 SongNames songname으로 저장장 
# 4. 유튜브에 접속, 각 songname에 대해 첫번째 영상 링크를 땀.
# 5. 영상 링크를 mp3전환 사이트에 붙여넣고 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


singer_name = input("가수 이름을 입력하세요 : ")
# 크롬 드라이버 멜론으로 경로 지정
driver = webdriver.Chrome()
driver.get("https://www.melon.com/")
print("브라우저가 열렸습니다.")

search_box = driver.find_element(By.ID, "top_search")  #serching for name="q"  cus that is the search tab
search_box.send_keys(singer_name)  #google detect and think it as a computer cus it's sooo fast 
search_box.send_keys(Keys.RETURN)

time.sleep(10000)

# 4. 곡 제목 10개 수집
song_elements = driver.find_elements(By.CSS_SELECTOR, "a.fc_gray")
song_names = [elem.text for elem in song_elements[:10]]

# 5. 반복문으로 song_name 하나씩 처리
for i, song_name in enumerate(song_names, 1):
    print(f"{i}. {song_name}")

print(f"{i}. {song_name}")
time.sleep(10000)
# driver.quit()
# print("브라우저가 닫혔습니다")