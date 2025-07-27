from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')  # React 앱에서 입력받은 검색어
    print(f"Search query received: {query}")  # 입력받은 검색어 로그

    # 크롬 드라이버 로드
    driver = webdriver.Chrome(executable_path="path/to/chromedriver")

    try:
        print("Navigating to the website...")
        driver.get("https://www.sciencetimes.co.kr/main")
        time.sleep(2)

        # 팝업 닫기 (이미지 클릭)
        try:
            print("Trying to close popup...")
            close_popup_button = driver.find_element(By.CSS_SELECTOR, "#popup_30 .close")
            close_popup_button.click()
            print("Popup closed.")
        except Exception:
            print("No popup found, continuing...")  # 팝업이 없다면 그냥 넘어감

        # 검색창에 입력하기
        print("Entering search term in search box...")
        search_input = driver.find_element(By.CSS_SELECTOR, "input[name='search']")
        search_input.send_keys(query)

        # 검색 버튼 클릭
        print("Clicking search button...")
        search_button = driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > div.headerWrap > div.gnbWrap > div > div.header_search > a > img')
        search_button.click()
        time.sleep(2)

        # 첫 번째 결과 URL 가져오기
        print("Extracting first search result...")
        first_result = driver.find_element(By.CSS_SELECTOR, "div.search-result-item a")
        result_url = first_result.get_attribute('href')
        print(f"First result URL: {result_url}")

        return jsonify({'result': result_url})  # 결과 URL 반환
    except Exception as e:
        print(f"Error during crawling: {e}")
        return jsonify({'error': str(e)})

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
