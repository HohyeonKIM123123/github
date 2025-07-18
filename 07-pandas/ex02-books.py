import pandas as pd

df = pd.read_csv("./07-pandas/books.csv") 
print(df.head()) #첫 5줄
print()
print(df.info())

# 결측치 확인 및 제거
print(df.isnull().sum())
df = df.dropna()
print(df)

#중복 데이터 제거거
df = df.drop_duplicates()
print(df)

# 컬럼 타입 변환
print(df.info())
df['가격'] = df['가격'].astype(int)
print(df.info())