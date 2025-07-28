import sys, os
sys.path.append('project')
from modules.db_utils import DatabaseManager

db = DatabaseManager('project/db/library.db')

print("=== 재고 수정 시작 ===")

# 각 도서별로 실제 대출 중인 수량 계산
books = db.execute_query("SELECT id, title, total_copies FROM books")

for book in books:
    book_id = book['id']
    total_copies = book['total_copies']
    
    # 실제 대출 중인 수량 계산
    active_loans = db.execute_query(
        "SELECT COUNT(*) as count FROM loans WHERE book_id = ? AND status = 'active'",
        (book_id,)
    )[0]['count']
    
    # 올바른 available_copies 계산
    correct_available = total_copies - active_loans
    
    # 업데이트
    db.execute_update(
        "UPDATE books SET available_copies = ? WHERE id = ?",
        (correct_available, book_id)
    )
    
    if active_loans > 0:
        print(f"{book['title']}: 총 {total_copies}권, 대출 중 {active_loans}권, 가용 {correct_available}권")

print("\n=== 수정 완료 ===")

# 최종 결과 확인
result = db.execute_query('''
SELECT 
    SUM(total_copies) as total_copies,
    SUM(available_copies) as available_copies,
    SUM(total_copies - available_copies) as loaned_copies
FROM books
''')

active_loans_total = db.execute_query("SELECT COUNT(*) as count FROM loans WHERE status = 'active'")[0]['count']

print(f"총 보유: {result[0]['total_copies']}권")
print(f"대출 가능: {result[0]['available_copies']}권") 
print(f"대출 중 (계산): {result[0]['loaned_copies']}권")
print(f"대출 중 (실제): {active_loans_total}건")

if result[0]['loaned_copies'] == active_loans_total:
    print("✅ 재고 계산이 정확합니다!")
else:
    print("❌ 재고 계산에 오류가 있습니다.")