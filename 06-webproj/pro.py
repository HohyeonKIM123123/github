from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# WebDriver 설정
driver = webdriver.Chrome()

# 사이언스타임즈 메인 페이지로 이동
driver.get("https://www.sciencetimes.co.kr/main")

# 카테고리 클릭
category = driver.find_element(By.CSS_SELECTOR, "body > div.wrapper > div.headerWrap > div.gnbWrap > div > nav > ul > li:nth-child(1) > a")
category.click()

# 페이지가 로드될 때까지 기다리기
sleep(3)

# 크롤링할 페이지 내용 추출 (예시)
page_content = driver.page_source
print(page_content)

# 브라우저 종료
driver.quit()