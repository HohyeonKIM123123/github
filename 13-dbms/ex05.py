"""
SQLite 기초 CRUD 예제
- Create: 데이터 생성(추가)
- Read: 데이터 조회
- Update: 데이터 수정
- Delete: 데이터 삭제
"""

import sqlite3
from datetime import datetime

db_path = r'D:\Windows_user\Documents\GitHub\github\13-dbms\students.db'
def create_database():
    """데이터베이스 연결 및 테이블 생성"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 학생 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("데이터베이스 및 테이블 생성 완료")

def create_student(name, age, grade):
    """학생 정보 추가 (CREATE)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO students (name, age, grade) 
        VALUES (?, ?, ?)
    ''', (name, age, grade))
    
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    
    print(f"학생 정보 추가 완료 - ID: {student_id}, 이름: {name}")
    return student_id

def read_all_students():
    """모든 학생 정보 조회 (READ)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students ORDER BY id')
    students = cursor.fetchall()
    
    conn.close()
    
    print("\n=== 전체 학생 목록 ===")
    if students:
        for student in students:
            print(f"ID: {student[0]}, 이름: {student[1]}, 나이: {student[2]}, 학년: {student[3]}, 등록일: {student[4]}")
    else:
        print("등록된 학생이 없습니다.")
    
    return students

def read_student_by_id(student_id):
    """특정 학생 정보 조회 (READ)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    conn.close()
    
    if student:
        print(f"\n=== 학생 정보 (ID: {student_id}) ===")
        print(f"이름: {student[1]}, 나이: {student[2]}, 학년: {student[3]}, 등록일: {student[4]}")
    else:
        print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
    
    return student

def update_student(student_id, name=None, age=None, grade=None):
    """학생 정보 수정 (UPDATE)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 기존 데이터 조회
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
        conn.close()
        return False
    
    # 수정할 값들 설정 (None이 아닌 값만 수정)
    new_name = name if name else student[1]
    new_age = age if age else student[2]
    new_grade = grade if grade else student[3]
    
    cursor.execute('''
        UPDATE students 
        SET name = ?, age = ?, grade = ? 
        WHERE id = ?
    ''', (new_name, new_age, new_grade, student_id))
    
    conn.commit()
    conn.close()
    
    print(f"학생 정보 수정 완료 - ID: {student_id}")
    return True

def delete_student(student_id):
    """학생 정보 삭제 (DELETE)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 삭제 전 학생 정보 확인
    cursor.execute('SELECT name FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
        conn.close()
        return False
    
    # 학생 정보 삭제
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    
    conn.commit()
    conn.close()
    
    print(f"학생 정보 삭제 완료 - ID: {student_id}, 이름: {student[0]}")
    return True

def search_students_by_name(name):
    """이름으로 학생 검색 (READ - 조건부 조회)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE name LIKE ?', (f'%{name}%',))
    students = cursor.fetchall()
    
    conn.close()
    
    print(f"\n=== '{name}' 검색 결과 ===")
    if students:
        for student in students:
            print(f"ID: {student[0]}, 이름: {student[1]}, 나이: {student[2]}, 학년: {student[3]}")
    else:
        print(f"'{name}'을 포함한 학생을 찾을 수 없습니다.")
    
    return students

def main():
    """메인 함수 - CRUD 예제 실행"""
    print("SQLite CRUD 예제 시작")
    
    # 1. 데이터베이스 및 테이블 생성
    create_database()
    
    # 2. 학생 정보 추가 (CREATE)
    print("\n1. 학생 정보 추가 (CREATE)")
    id1 = create_student("김철수", 20, "2학년")
    id2 = create_student("이영희", 19, "1학년")
    id3 = create_student("박민수", 21, "3학년")
    id4 = create_student("최수진", 20, "2학년")
    
    # 3. 모든 학생 조회 (READ)
    print("\n2. 모든 학생 조회 (READ)")
    read_all_students()
    
    # 4. 특정 학생 조회 (READ)
    print("\n3. 특정 학생 조회 (READ)")
    read_student_by_id(id1)
    
    # 5. 학생 정보 수정 (UPDATE)
    print("\n4. 학생 정보 수정 (UPDATE)")
    update_student(id2, age=20, grade="2학년")
    read_student_by_id(id2)
    
    # 6. 이름으로 학생 검색 (READ - 조건부)
    print("\n5. 이름으로 학생 검색")
    search_students_by_name("김")
    
    # 7. 학생 정보 삭제 (DELETE)
    print("\n6. 학생 정보 삭제 (DELETE)")
    delete_student(id3)
    
    # 8. 삭제 후 전체 목록 확인
    print("\n7. 삭제 후 전체 목록 확인")
    read_all_students()
    
    print("\nSQLite CRUD 예제 완료")

if __name__ == "__main__":
    main()