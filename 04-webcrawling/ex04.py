import requests
from bs4 import BeautifulSoup

url = "http://127.0.0.1:5500/test2.html"

html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

# thw way of approaching the Tag
print(soup.title)
print(soup.title.text)
print(soup.h1['id'])
print(soup.h1.text)
print(soup.p)
print(soup.p['class'])
print(soup.p['class'][0]) #you can extract exactly
print(soup.p.text)

print(soup.find_all ('p')[0])
print(soup.find_all ('p')[1])
print(soup.find_all ('a')[0]['href'])
print(soup.find_all ('a')[1]['href'])

print(soup.find('p'))  # 첫번째 피만
print(soup.find_all('p'))  #리스트 p
print(soup.find('p',class_='content'))
print(soup.find('h1', id='title'))





