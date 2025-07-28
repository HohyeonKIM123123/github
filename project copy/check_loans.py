import sqlite3
import os

db_path = os.path.join('project', 'db', 'library.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 활성 대출 확인
cursor.execute('''
SELECT l.id, l.book_id, l.member_id, l.status, l.due_date, b.title, m.name 
FROM loans l 
JOIN books b ON l.book_id = b.id 
JOIN members m ON l.member_id = m.id 
WHERE l.status = "active"
ORDER BY l.due_date
''')

loans = cursor.fetchall()
print('활성 대출:')
for loan in loans:
    print(f'대출ID: {loan[0]}, 도서ID: {loan[1]}, 회원ID: {loan[2]}, 상태: {loan[3]}, 반납예정: {loan[4]}, 도서: {loan[5]}, 회원: {loan[6]}')

conn.close()