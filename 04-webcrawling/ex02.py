

import requests

url ="http://127.0.0.1:5500/gif-2025/04-webcrawling/ex01_test1.html"

html = requests.get(url).text

print(html)


# h1 태그 직접 내용 추출
start = html.find("<h1>")
end = html.find("</h1>")

h1_content = html[start+4:end]
print(h1_content)
