import sqlite3

db_path = r'D:\Windows_user\Documents\GitHub\github\13-dbms\students.db'

#전체학생 조회
conn = sqlite3.connect (db_path)

print(conn) 


cursor = conn.cursor()

#학생정보 수정 
query = """
update student
SET name = ? , age = ?, grade = ?
where name = ? 
"""
cursor.execute(query, ('홍길동2', 456 , 'C0', '홍길동'))
conn.commit() #수정사항을 실제 db파일에 적용한다.
conn.close ()

print("학생정보 수정 완료 ")



# conn.close()

# print("\n=== 검색 학생 목록 ===")
# if student_list :
#     for student in student_list :
#         print (student)
#         print (f"id :{student[0]}, name : {student[1]}, grade : {student[3]}")
# else:
#     print("검색된 학생이 없습니다.")