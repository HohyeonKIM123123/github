"""
SQLite 기초 CRUD 예제
- Create: 데이터 생성(추가)
- Read: 데이터 조회
- Update: 데이터 수정
- Delete: 데이터 삭제
"""

import sqlite3
import csv
from datetime import datetime
import os

db_path = r'C:\Users\ghgh2\OneDrive\바탕 화면\github\13-dbms\students.db'

def clear_all_students():
    """모든 학생 정보 삭제 (주의: 실제 데이터가 모두 삭제됩니다)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM students')
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"모든 학생 정보 삭제 완료: {deleted_count}명의 데이터가 삭제되었습니다.")
    return True

clear_all_students()

def create_database():
    """데이터베이스 연결 및 테이블 생성"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 학생 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
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

def read_csv_file(file_path):
    """CSV 파일 읽기"""
    students = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                students.append({
                    'name': row['name'],
                    'age': int(row['age']),
                    'grade': row['grade']
                })
        print(f"CSV 파일 읽기 완료: {len(students)}명의 학생 정보")
        return students
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return []
    except Exception as e:
        print(f"CSV 파일 읽기 중 오류 발생: {e}")
        return []

def insert_students_from_csv(students):
    """CSV 데이터를 SQLite 테이블에 삽입"""
    if not students:
        print("삽입할 데이터가 없습니다.")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    success_count = 0
    failed_count = 0
    
    for student in students:
        try:
            cursor.execute('''
                INSERT INTO students (name, age, grade) 
                VALUES (?, ?, ?)
            ''', (student['name'], student['age'], student['grade']))
            
            student_id = cursor.lastrowid
            print(f"학생 추가 완료 - ID: {student_id}, 이름: {student['name']}")
            success_count += 1
            
        except Exception as e:
            print(f"학생 추가 중 오류 발생 - 이름: {student['name']}, 오류: {e}")
            failed_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n=== 삽입 결과 ===")
    print(f"성공: {success_count}명")
    print(f"실패: {failed_count}명")
    
    return success_count > 0

def clear_all_students():
    """모든 학생 정보 삭제 (주의: 실제 데이터가 모두 삭제됩니다)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM students')
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"모든 학생 정보 삭제 완료: {deleted_count}명의 데이터가 삭제되었습니다.")
    return True

def main():
    """메인 함수 - CSV 데이터 삽입 예제 실행"""
    print("SQLite CSV 데이터 삽입 예제 시작")
    
    # 1. 데이터베이스 및 테이블 생성
    create_database()
    
    csv_file_path = r'C:\Users\ghgh2\OneDrive\바탕 화면\github\13-dbms\students_sample.csv'
    
    # 2. CSV 파일 읽기
    print(f"\n1. CSV 파일 읽기: {csv_file_path}")
    students = read_csv_file(csv_file_path)
    
    if not students:
        print("CSV 파일을 읽을 수 없습니다. 프로그램을 종료합니다.")
        return
    
    # 3. CSV 데이터 출력
    print("\n2. CSV 데이터 미리보기")
    for i, student in enumerate(students[:5], 1):  # 처음 5명만 출력
        print(f"{i}. 이름: {student['name']}, 나이: {student['age']}, 학년: {student['grade']}")
    if len(students) > 5:
        print(f"... 외 {len(students) - 5}명")
    
    clear_all_students ()

    # 4. 기존 데이터 확인
    print("\n3. 기존 데이터 확인")
    existing_students = read_all_students()
    
    # 5. CSV 데이터 삽입
    print("\n4. CSV 데이터 삽입")
    insert_success = insert_students_from_csv(students)
    
    if insert_success:
        print("CSV 데이터 삽입이 완료되었습니다.")
    else:
        print("CSV 데이터 삽입이 실패했습니다.")
    
    # 6. 삽입 후 전체 데이터 확인
    print("\n5. 삽입 후 전체 데이터 확인")
    read_all_students()
    
    # 7. 이름으로 학생 검색 테스트
    print("\n6. 이름으로 학생 검색 테스트")
    search_students_by_name("김")
    
    print("\nSQLite CSV 데이터 삽입 예제 완료")

if __name__ == "__main__":
    main()