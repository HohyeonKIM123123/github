# 한달살러 숙소 탐색기

한달살러(https://www.monthler.kr/) 사이트에서 숙소 데이터를 크롤링하고, Streamlit으로 상세 필터링과 정렬 기능을 갖춘 맞춤형 숙소 탐색 웹앱입니다.

## 🚀 주요 기능

### 크롤링 기능
- Selenium과 BeautifulSoup를 사용한 자동 데이터 수집
- 카드 리스트와 상세페이지 정보 수집
- 최대 500개까지 "더 보기" 버튼을 클릭해 데이터 확장
- D-day가 만료된 프로그램 자동 제외
- 다양한 방법으로 상세페이지 링크 추출

### 전처리 기능
- 가격, 지역, 기간, D-day, 지원자 수를 숫자형으로 변환
- 혜택/특징을 리스트화
- 프로그램명 기반 카테고리 자동 분류
- 지역 정보를 시/도, 시군구로 분리

### Streamlit 앱 기능
- **다양한 필터**: 지역, 가격, 카테고리, D-day, 혜택
- **정렬 기능**: 최신순, 가격순, D-day순, 지원자순
- **카드형 리스트**: 이미지와 상세 정보 표시
- **지도 뷰**: Folium을 사용한 인터랙티브 지도
- **통계 차트**: 카테고리별, 지역별 분포 차트
- **데이터 다운로드**: CSV, Excel 형식으로 다운로드

## 📦 설치 및 실행

### 1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Chrome WebDriver 설치
Chrome 브라우저가 설치되어 있어야 합니다. 최신 버전의 Chrome을 사용하세요.

### 3. 크롤링 실행
```bash
python monthler_crawler_fixed.py
```
- 한달살러 사이트에서 데이터를 수집합니다
- `monthler_processed.csv` 파일이 생성됩니다 (Streamlit 앱용)
- 백업용 타임스탬프 파일도 함께 생성됩니다

### 4. Streamlit 앱 실행
```bash
streamlit run streamlit_app_fixed.py
```
- 브라우저에서 `http://localhost:8501`로 접속
- 수집된 데이터를 탐색하고 필터링할 수 있습니다

## 📊 데이터 구조

수집되는 데이터 필드:
- `name`: 프로그램명
- `detail_url`: 상세페이지 링크
- `img_url`: 이미지 URL
- `region`: 지역 정보
- `fee`: 참가비
- `period`: 기간
- `d_day`: D-day
- `applicants`: 지원자 수
- `features`: 혜택/특징
- `category`: 카테고리 (자동 분류)
- `region_city`: 시/도
- `region_district`: 시군구
- `fee_num`: 참가비 (숫자)
- `d_day_num`: D-day (숫자)
- `applicants_num`: 지원자 수 (숫자)

## 📁 파일 구조

```
06-wp/
├── monthler_crawler_fixed.py    # 크롤링 + 전처리 스크립트 (수정됨)
├── streamlit_app_fixed.py       # Streamlit 웹앱 (수정됨)
├── requirements.txt             # 필요한 패키지 목록
├── README.md                   # 사용법 안내
├── monthler_processed.csv      # 전처리 완료 데이터 (Streamlit 앱용)
└── monthler_processed_YYYYMMDD_HHMMSS.csv  # 백업용 데이터
```

## 🎯 사용법

### 크롤링
1. `python monthler_crawler_fixed.py` 실행
2. 크롤링 진행 상황을 콘솔에서 확인
3. 완료 후 `monthler_processed.csv` 파일 생성

### Streamlit 앱
1. `streamlit run streamlit_app_fixed.py` 실행
2. 브라우저에서 웹앱 접속
3. 사이드바에서 원하는 필터 설정
4. 메인 화면에서 결과 확인
5. 지도 뷰, 통계 차트, 데이터 다운로드 활용

## 🔧 주요 기술

- **크롤링**: Selenium, BeautifulSoup
- **데이터 처리**: Pandas, NumPy
- **웹앱**: Streamlit
- **시각화**: Plotly, Folium
- **파일 처리**: CSV, Excel

## ⚠️ 주의사항

- 크롤링 시 웹사이트의 이용약관을 준수하세요
- 과도한 요청을 피하고 적절한 딜레이를 두세요
- 수집된 데이터는 개인적인 용도로만 사용하세요
- 웹사이트 구조 변경 시 크롤링 코드 수정이 필요할 수 있습니다

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다. 