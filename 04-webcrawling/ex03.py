import requests
from bs4 import BeautifulSoup

url ="http://127.0.0.1:5500/test2.html"

html = requests.get(url).text

#HTML 파싱(분석, Extraction)
soup = BeautifulSoup(html, 'html.parser') # i am gonna use parser

#H1 extraction
print( soup.find('h1').text)




