# 📚 도서관 관리 시스템

Guardian 스타일의 375권 명작 소설을 포함한 완전한 도서관 관리 시스템입니다.

## 🚀 기능

- **📊 대시보드**: 실시간 통계 및 현황
- **📖 도서 관리**: 도서 등록/검색/수정
- **👥 회원 관리**: 회원 등록/검색/수정
- **📋 대출 관리**: 대출/반납 처리
- **⚠️ 연체 관리**: 연체 도서 관리 및 이메일 알림
- **📈 보고서**: 월간 보고서 생성

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Database**: SQLite
- **Backend**: Python
- **Email**: SMTP (Gmail)

## 📦 설치 및 실행

### 로컬 실행
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Streamlit Cloud 배포
1. GitHub에 프로젝트 업로드
2. Streamlit Cloud에서 앱 생성
3. Secrets에 이메일 설정 추가:
   - `EMAIL_ADDRESS`: Gmail 주소
   - `EMAIL_PASSWORD`: Gmail 앱 비밀번호
   - `SMTP_SERVER`: smtp.gmail.com
   - `SMTP_PORT`: 587

## 📊 데이터

- **375권의 Guardian 스타일 명작 소설**
- **자동 데이터베이스 초기화**
- **샘플 회원 및 대출 데이터**

## 🔧 환경 설정

로컬 개발시 `project/.env` 파일에 다음 설정:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
LIBRARY_NAME=우리 도서관
ADMIN_EMAIL=admin@library.com
```

## 📝 라이선스

MIT License