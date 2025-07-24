import sqlite3

db_path = r'D:\Windows_user\Documents\GitHub\github\13-dbms\students.db'

#전체학생 조회
conn = sqlite3.connect (db_path)

print(conn) 


cursor = conn.cursor()

#조건적인  검색 (where절)
# query = 'SELECT * FROM student WHERE name ="홍길동"'
# cursor.execute(query)

#대체
query = 'SELECT * FROM student WHERE name = ? or name = ? '
cursor.execute(query, ('홍길동','아순신') ) # 튜플타입으로 매개변수를 넣는다. 
student_list = cursor.fetchall ()

conn.close()

print("\n=== 검색 학생 목록 ===")
if student_list :
    for student in student_list :
        print (student)
        print (f"id :{student[0]}, name : {student[1]}, grade : {student[3]}")
else:
    print("검색된 학생이 없습니다.")