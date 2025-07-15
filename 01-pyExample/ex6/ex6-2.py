# Reading and writing CSV
# CSV (Comma seperated Value): 엑셀 DB와 호환됨 
# ex)
# 번호  이름    학번 
# 1    hong   0001


import csv #using :csv: module (standard library) , pip install csv


data = [
    ["이름","나이","도시"],
    ['홍길동', 30, '서울'],
    ['김철수', 32, '부산'],
    ['수철김', 23, '부천'],
    ['철김수', 15, '남산'],
    ['김철기', 2, '무주공산']


]

# saving as a "csv"
with open ("people.csv", "w", newline = "", encoding = 'utf-8') as f:
#newline = removing empthy space
    writer = csv.writer(f)
    writer.writerows(data)
#writerrows() : saving all of the 2 dimetion list

print( "complete saving csv file ")

# reading csv file
with open ("people.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
            print(row)