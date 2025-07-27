import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [articles, setArticles] = useState([]);

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearch = async () => {
    if (query) {
      const response = await fetch(`http://localhost:5000/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setArticles(data);
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', textAlign: 'center', flexDirection: 'column' }}>
      <div style={{ padding: '2rem' }}>
        <h1>당신의 지식이 진실인지 확인해보세요</h1>
        <h3>과학 기반 기사 검색과 AI 요약 기능을 제공하는 플랫폼입니다.</h3>

        <input
          type="text"
          placeholder="검증하고 싶은 정보를 입력하세요."
          value={query}
          onChange={handleInputChange}
          style={{
            padding: '0.5rem',
            fontSize: '1rem',
            marginTop: '1rem',
            width: '60%',
            borderRadius: '5px',
            border: '1px solid #ccc',
            textAlign: 'center'
          }}
        />

        <button
          onClick={handleSearch}
          style={{
            padding: '0.5rem',
            fontSize: '1rem',
            marginTop: '1rem',
            borderRadius: '5px',
            border: '1px solid #ccc',
            backgroundColor: '#4CAF50',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          검색
        </button>

        {articles.length > 0 && (
          <ul>
            {articles.map((article, index) => (
              <li key={index}>
                <a href={article.link} target="_blank" rel="noopener noreferrer">{article.title}</a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
