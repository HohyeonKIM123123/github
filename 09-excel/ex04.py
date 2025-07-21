"""
구글 시트 읽기 - 가장 심플한 버전
"""

import gspread
from google.oauth2.service_account import Credentials

# 구글 시트 API 스코프 설정
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 구글 시트 API 인증
creds = Credentials.from_service_account_file("./09-excel/credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# 구글 시트 열기
sheet = client.open("성적표").sheet1

print("📊 구글 시트 내용:")
print("-" * 30)

# 모든 값 읽어서 출력
for row in sheet.get_all_values():
    # 빈 셀 제거
    filtered_row = []
    for cell in row:
        if cell.strip():  # 빈 문자열이 아니면
            filtered_row.append(cell)
    
    if filtered_row:  # 빈 행이 아니면 출력
        print(filtered_row) 