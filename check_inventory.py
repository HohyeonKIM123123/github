import sys, os
sys.path.append('project')
from modules.db_utils import DatabaseManager

db = DatabaseManager('project/db/library.db')

# 현재 재고 상태 확인
result = db.execute_query('''
SELECT 
    SUM(total_copies) as total_copies,
    SUM(available_copies) as available_copies,
    SUM(total_copies - available_copies) as loaned_copies
FROM books
''')

print('=== 현재 재고 상태 ===')
print(f"총 보유: {result[0]['total_copies']}권")
print(f"대출 가능: {result[0]['available_copies']}권") 
print(f"대출 중: {result[0]['loaned_copies']}권")

# 음수 재고 도서 확인
negative = db.execute_query('''
SELECT id, title, total_copies, available_copies 
FROM books 
WHERE available_copies < 0
LIMIT 10
''')

print(f'\n=== 음수 재고 도서: {len(negative)}권 ===')
for book in negative:
    print(f"ID {book['id']}: {book['title']}")
    print(f"  총 {book['total_copies']}권, 가용 {book['available_copies']}권")

# 실제 대출 현황 확인
active_loans = db.execute_query('''
SELECT COUNT(*) as count FROM loans WHERE status = 'active'
''')

print(f'\n=== 실제 대출 현황 ===')
print(f"활성 대출: {active_loans[0]['count']}건")

# 재고 수정
print('\n=== 재고 수정 중 ===')
db.execute_update('''
UPDATE books 
SET available_copies = CASE 
    WHEN available_copies < 0 THEN 0
    ELSE available_copies 
END
''')

print("음수 재고를 0으로 수정했습니다.")

# 수정 후 상태 확인
result_after = db.execute_query('''
SELECT 
    SUM(total_copies) as total_copies,
    SUM(available_copies) as available_copies,
    SUM(total_copies - available_copies) as loaned_copies
FROM books
''')

print('\n=== 수정 후 재고 상태 ===')
print(f"총 보유: {result_after[0]['total_copies']}권")
print(f"대출 가능: {result_after[0]['available_copies']}권") 
print(f"대출 중: {result_after[0]['loaned_copies']}권")