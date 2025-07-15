

#pandas reading and writing CSV by library
#pandas : library which is specialized for analazing data 
#       : it is so useful to handle second dimetion data
#  pip install pandas


import pandas as pd

data = {
    "이름":["홍길동", "김철수", "이영희"],
    "나이":[30,25,35],
    "도시":["서울","부산","수원"]
}
#데이터 프레임 객체 생성
df= pd.DataFrame( data )
print(df)
# SAVE it as a CSV
df.to_csv("people_pandas.csv",index=False, encoding = 'utf-8')
print(" saving complete")

#pandas로 csv파일 읽어 들이기
df = pd.read_csv("people_pandas.csv",encoding = "utf-8-sig")
print(df)