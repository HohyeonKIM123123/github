
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']

#개인에 따라 수정 필요 - 다운로드 받았던 키 값 경로 

json_key_path = r"C:\Users\ghgh2\OneDrive\바탕 화면\modular-rush-466605-m9-d44d490d0ba3.json"

credential = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
gc = gspread.authorize(credential)


#개인에 따라 수정 필요 - 스프레드시트 url 가져오기
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1eDV1eFwtmo2kKKrdistaWKpNr3ASVusNSQSEKSCZYd4/edit?gid=0#gid=0"

doc = gc.open_by_url(spreadsheet_url)

#개인에 따라 수정 필요 - 시트 선택하기 (시트명을 그대로 입력해주면 된다.)
sheet = doc.worksheet("시트1")

#데이터 프레임 생성하기
df = pd.DataFrame(sheet.get_all_values())

#불러온 데이터 프레임 정리
df.rename(columns=df.iloc[0], inplace = True)
df.drop(df.index[0], inplace=True)

print(df.head())