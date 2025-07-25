"""
Supabase 기초 CRUD 예제
- Create: 데이터 생성(추가)
- Read: 데이터 조회
- Update: 데이터 수정
- Delete: 데이터 삭제
"""

import os
from supabase import create_client, Client
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()


# Supabase 설정
# 환경변수에서 설정을 가져오거나 직접 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY)
# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_database():
    """데이터베이스 테이블 생성 (Supabase에서는 SQL 에디터에서 실행)"""
    # Supabase에서는 테이블을 SQL 에디터에서 생성해야 합니다
    # 아래는 참고용 SQL 스크립트입니다
    sql_script = '''
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Seoul')
    );
    '''
    print("Supabase SQL 에디터에서 다음 스크립트를 실행하세요:")
    print(sql_script)
    print("데이터베이스 테이블 생성 완료")

def create_student(name, age, grade):
    """학생 정보 추가 (CREATE)"""
    try:
        data = {
            'name': name,
            'age': age,
            'grade': grade
        }
        
        result = supabase.table('students').insert(data).execute()
        
        if result.data:
            student_id = result.data[0]['id']
            print(f"학생 정보 추가 완료 - ID: {student_id}, 이름: {name}")
            return student_id
        else:
            print("학생 정보 추가 실패")
            return None
            
    except Exception as e:
        print(f"학생 정보 추가 중 오류 발생: {e}")
        return None

def read_all_students():
    """모든 학생 정보 조회 (READ)"""
    try:
        result = supabase.table('students').select('*').order('id').execute()
        students = result.data
        
        print("\n=== 전체 학생 목록 ===")
        if students:
            for student in students:
                print(f"ID: {student['id']}, 이름: {student['name']}, 나이: {student['age']}, 학년: {student['grade']}, 등록일: {student['created_at']}")
        else:
            print("등록된 학생이 없습니다.")
        
        return students
        
    except Exception as e:
        print(f"학생 정보 조회 중 오류 발생: {e}")
        return []

def read_student_by_id(student_id):
    """특정 학생 정보 조회 (READ)"""
    try:
        result = supabase.table('students').select('*').eq('id', student_id).execute()
        students = result.data
        
        if students:
            student = students[0]
            print(f"\n=== 학생 정보 (ID: {student_id}) ===")
            print(f"이름: {student['name']}, 나이: {student['age']}, 학년: {student['grade']}, 등록일: {student['created_at']}")
            return student
        else:
            print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
            return None
            
    except Exception as e:
        print(f"학생 정보 조회 중 오류 발생: {e}")
        return None

def update_student(student_id, name=None, age=None, grade=None):
    """학생 정보 수정 (UPDATE)"""
    try:
        # 기존 데이터 조회
        result = supabase.table('students').select('*').eq('id', student_id).execute()
        #연쇄문, 결과 나오면 셀렉트하고 조건걸고 (eq) 실행하고, 간결해짐.
        students = result.data
        
        if not students:
            print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
            return False
        
        student = students[0]
        
        # 수정할 값들 설정 (None이 아닌 값만 수정)
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if age is not None:
            update_data['age'] = age
        if grade is not None:
            update_data['grade'] = grade
        
        if update_data:
            result = supabase.table('students').update(update_data).eq('id', student_id).execute()
            
            if result.data:
                print(f"학생 정보 수정 완료 - ID: {student_id}")
                return True
            else:
                print("학생 정보 수정 실패")
                return False
        else:
            print("수정할 데이터가 없습니다.")
            return False
            
    except Exception as e:
        print(f"학생 정보 수정 중 오류 발생: {e}")
        return False

def delete_student(student_id):
    """학생 정보 삭제 (DELETE)"""
    try:
        # 삭제 전 학생 정보 확인
        result = supabase.table('students').select('name').eq('id', student_id).execute()
        students = result.data
        
        if not students:
            print(f"ID {student_id}인 학생을 찾을 수 없습니다.")
            return False
        
        student_name = students[0]['name']
        
        # 학생 정보 삭제
        result = supabase.table('students').delete().eq('id', student_id).execute()
        
        if result.data:
            print(f"학생 정보 삭제 완료 - ID: {student_id}, 이름: {student_name}")
            return True
        else:
            print("학생 정보 삭제 실패")
            return False
            
    except Exception as e:
        print(f"학생 정보 삭제 중 오류 발생: {e}")
        return False

def search_students_by_name(name):
    """이름으로 학생 검색 (READ - 조건부 조회)"""
    try:
        # PostgreSQL의 ILIKE를 사용하여 대소문자 구분 없이 검색
        result = supabase.table('students').select('*').ilike('name', f'%{name}%').execute()
        students = result.data
        
        print(f"\n=== '{name}' 검색 결과 ===")
        if students:
            for student in students:
                print(f"ID: {student['id']}, 이름: {student['name']}, 나이: {student['age']}, 학년: {student['grade']}")
        else:
            print(f"'{name}'을 포함한 학생을 찾을 수 없습니다.")
        
        return students
        
    except Exception as e:
        print(f"학생 검색 중 오류 발생: {e}")
        return []

def setup_environment():
    """환경 설정 확인"""
    print("=== Supabase 환경 설정 확인 ===")
    print(f"SUPABASE_URL: {SUPABASE_URL}")
    print(f"SUPABASE_KEY: {SUPABASE_KEY[:10]}..." if SUPABASE_KEY != 'your-supabase-anon-key' else "SUPABASE_KEY: 설정되지 않음")
    
    if SUPABASE_URL == 'your-supabase-url' or SUPABASE_KEY == 'your-supabase-anon-key':
        print("\n⚠️  경고: Supabase 설정이 필요합니다!")
        print("1. .env 파일을 생성하고 다음을 추가하세요:")
        print("   SUPABASE_URL=your-actual-supabase-url")
        print("   SUPABASE_KEY=your-actual-supabase-anon-key")
        print("2. 또는 코드에서 직접 설정하세요.")
        return False
    return True

def main():
    """메인 함수 - CRUD 예제 실행"""
    print("Supabase CRUD 예제 시작")
    
    # 환경 설정 확인
    if not setup_environment():
        print("환경 설정을 완료한 후 다시 실행하세요.")
        return
    
    # 1. 데이터베이스 테이블 생성 안내
    print("\n1. 데이터베이스 테이블 생성")
    create_database()
    
    # 2. 학생 정보 추가 (CREATE)
    print("\n2. 학생 정보 추가 (CREATE)")
    id1 = create_student("김철수", 20, "2학년")
    id2 = create_student("이영희", 19, "1학년")
    id3 = create_student("박민수", 21, "3학년")
    id4 = create_student("최수진", 20, "2학년")
    
    # 3. 모든 학생 조회 (READ)
    print("\n3. 모든 학생 조회 (READ)")
    read_all_students()
    
    # 4. 특정 학생 조회 (READ)
    if id1:
        print("\n4. 특정 학생 조회 (READ)")
        read_student_by_id(id1)
    
    # 5. 학생 정보 수정 (UPDATE)
    if id2:
        print("\n5. 학생 정보 수정 (UPDATE)")
        update_student(id2, age=20, grade="2학년")
        read_student_by_id(id2)
    
    # 6. 이름으로 학생 검색 (READ - 조건부)
    print("\n6. 이름으로 학생 검색")
    search_students_by_name("김")
    
    # 7. 학생 정보 삭제 (DELETE)
    if id3:
        print("\n7. 학생 정보 삭제 (DELETE)")
        delete_student(id3)
    
    # 8. 삭제 후 전체 목록 확인
    print("\n8. 삭제 후 전체 목록 확인")
    read_all_students()
    
    print("\nSupabase CRUD 예제 완료")

if __name__ == "__main__":
    main()