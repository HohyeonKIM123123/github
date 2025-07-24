import sqlite3

db_path = r'D:\Windows_user\Documents\GitHub\github\13-dbms\students.db'

#전체학생 조회
conn = sqlite3.connect (db_path)

print(conn) 


cursor = conn.cursor()

#학생정보 삭제
query = """
delete from student
where name = ? 
"""
cursor.execute(query, ('홍길동2',))
conn.commit() #수정사항을 실제 db파일에 적용한다.
conn.close ()

print("학생정보 삭제 완료 ")

who knows how long i loved you. you know i loved you steal.
will i wait a lonly lifetime
if you want me to i will



