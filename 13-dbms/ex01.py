"""
SQLite 기초 CRUD 예제 
create: data forming 
read : data query
update: data modify
Delete: removing data
"""


import sqlite3

db_path = r'D:\Windows_user\Documents\GitHub\github\13-dbms\students.db'

#전체학생 조회
conn = sqlite3.connect (db_path)

print(conn) 


cursor = conn.cursor()

cursor.execute('SELECT * FROM student ORDER BY id')
student_list = cursor.fetchall ()

conn.close()

print("\n=== 전체 학생 목록 ===")
if student_list :
    for student in student_list :
        print (student)
else:
    print("학생목록이 없습니다.")