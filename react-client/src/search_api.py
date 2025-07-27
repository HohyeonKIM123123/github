import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/search", methods=["GET"])
def search_articles():
    query = request.args.get("q")
    if not query:
        return jsonify({"articles": []}), 400
    
    base_url = "https://www.sciencetimes.co.kr/?s="
    search_url = base_url + requests.utils.quote(query)
    
    # 페이지 요청 및 HTML 파싱
    res = requests.get(search_url)
    if res.status_code != 200:
        return jsonify({"articles": []}), 500
    
    soup = BeautifulSoup(res.text, "html.parser")
    
    # 기사 리스트를 찾아 파싱
    article_cards = soup.select("div.list-content > ul > li")
    articles = []
    
    for card in article_cards:
        title_elem = card.select_one("h4 > a")
        if title_elem:
            title = title_elem.text.strip()
            url = title_elem["href"]
            
            # 개별 기사 페이지에서 본문 가져오기
            article_res = requests.get(url)
            article_soup = BeautifulSoup(article_res.text, "html.parser")
            content_elem = article_soup.select_one("div.view-content")
            summary = content_elem.text.strip().split("\n")[0] if content_elem else "No summary available"
            
            articles.append({"title": title, "url": url, "summary": summary})
    
    return jsonify({"articles": articles})

if __name__ == "__main__":
    app.run(debug=False)