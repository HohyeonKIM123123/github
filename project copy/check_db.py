import sqlite3
import os

db_path = os.path.join('project', 'db', 'library.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 도서 수 확인
cursor.execute('SELECT COUNT(*) FROM books')
book_count = cursor.fetchone()[0]
print(f'총 도서 수: {book_count}')

# 샘플 도서 확인
cursor.execute('SELECT title, author FROM books LIMIT 10')
books = cursor.fetchall()
print('\n샘플 도서:')
for title, author in books:
    print(f'- {title} by {author}')

conn.close()