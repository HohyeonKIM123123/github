import pandas as pd

df = pd.read_csv("./07-pandas/books.csv")

# 평균, 최대값 등 통계
print(df.describe())

# 그룹별 통계
grouped = df.groupby("카테고리")["가격"].mean()
print(grouped)

# 정렬
df = df.sort_values(by="가격", ascending=False) #내림차순순
print(df)