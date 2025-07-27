import React, { useState, useEffect } from "react";

const SearchResult: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [articles, setArticles] = useState<any[]>([]);
  
  const handleSearch = () => {
    fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => setArticles(data.articles))
      .catch((err) => console.error("검색 실패:", err));
  };

  return (
    <div>
      <h1>당신의 지식이 진실인지 확인해보세요</h1>
      <input 
        type="text" 
        placeholder="검색어를 입력하세요" 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <button onClick={handleSearch}>검색</button>
      <div>
        {articles.length > 0 ? (
          <ul>
            {articles.map((article, index) => (
              <li key={index}>
                <h3>{article.title}</h3>
                <p>{article.summary}</p>
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                  원본 기사 읽기
                </a>
              </li>
            ))}
          </ul>
        ) : (
          <p>검색된 기사가 없습니다.</p>
        )}
      </div>
    </div>
  );
};

export default SearchResult;