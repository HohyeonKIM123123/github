import requests

url = "https://www.naver.com"

# http의 응답은 4가지 형태의 데이터가 옴 
# 1. html 파일   2. json   3. sml   4.file (bin) download

response = requests.get(url)

print(response.text)