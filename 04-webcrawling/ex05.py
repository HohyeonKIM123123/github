import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# select : css 선택자를 사용함 
# #titleline > a: 클래스 이름 titleline의 바로 밑의 a태그를 선택하라  
titles = soup.select('.titleline > a')
