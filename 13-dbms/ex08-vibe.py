import sqlite3
import os

class MemberDB:
    def __init__(self):
        self.db_name = "member.db"
        self.create_database()
    
    def create_database(self):
        """데이터베이스 파일 생성 및 테이블 생성"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # member 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS member (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                joindate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"데이터베이스 '{self.db_name}' 생성 완료")
    
    def create_member(self, name, phone, address):
        """회원 생성 (Create)"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO member (name, phone, address)
                VALUES (?, ?, ?)
            ''', (name, phone, address))
            
            conn.commit()
            member_id = cursor.lastrowid
            conn.close()
            print(f"회원 등록 완료 (ID: {member_id})")
            return member_id
        except Exception as e:
            print(f"회원 등록 실패: {e}")
            return None
    
    def read_all_members(self):
        """전체 회원 조회 (Read)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM member')
        members = cursor.fetchall()
        conn.close()
        
        if members:
            print("\n=== 전체 회원 목록 ===")
            print("ID | 이름 | 핸드폰 | 주소 | 가입일시")
            print("-" * 70)
            for member in members:
                print(f"{member[0]} | {member[1]} | {member[2]} | {member[3]} | {member[4]}")
        else:
            print("등록된 회원이 없습니다.")
        
        return members
    
    def read_member_by_id(self, member_id):
        """특정 회원 조회"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM member WHERE id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        
        if member:
            print(f"\n=== 회원 정보 (ID: {member_id}) ===")
            print(f"이름: {member[1]}")
            print(f"핸드폰: {member[2]}")
            print(f"주소: {member[3]}")
            print(f"가입일시: {member[4]}")
        else:
            print(f"ID {member_id}인 회원을 찾을 수 없습니다.")
        
        return member
    
    def update_member(self, member_id, name=None, phone=None, address=None):
        """회원 정보 수정 (Update)"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # 기존 회원 정보 확인
            cursor.execute('SELECT * FROM member WHERE id = ?', (member_id,))
            existing_member = cursor.fetchone()
            
            if not existing_member:
                print(f"ID {member_id}인 회원을 찾을 수 없습니다.")
                conn.close()
                return False
            
            # 수정할 필드만 업데이트
            update_fields = []
            update_values = []
            
            if name is not None:
                update_fields.append("name = ?")
                update_values.append(name)
            if phone is not None:
                update_fields.append("phone = ?")
                update_values.append(phone)
            if address is not None:
                update_fields.append("address = ?")
                update_values.append(address)
            
            if not update_fields:
                print("수정할 내용이 없습니다.")
                conn.close()
                return False
            
            update_values.append(member_id)
            query = f"UPDATE member SET {', '.join(update_fields)} WHERE id = ?"
            
            cursor.execute(query, update_values)
            conn.commit()
            conn.close()
            
            print(f"회원 정보 수정 완료 (ID: {member_id})")
            return True
            
        except Exception as e:
            print(f"회원 정보 수정 실패: {e}")
            return False
    
    def delete_member(self, member_id):
        """회원 삭제 (Delete)"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # 회원 존재 확인
            cursor.execute('SELECT * FROM member WHERE id = ?', (member_id,))
            member = cursor.fetchone()
            
            if not member:
                print(f"ID {member_id}인 회원을 찾을 수 없습니다.")
                conn.close()
                return False
            
            cursor.execute('DELETE FROM member WHERE id = ?', (member_id,))
            conn.commit()
            conn.close()
            
            print(f"회원 삭제 완료 (ID: {member_id})")
            return True
            
        except Exception as e:
            print(f"회원 삭제 실패: {e}")
            return False

def main():
    """메인 실행 함수"""
    db = MemberDB()
    
    while True:
        print("\n=== 회원관리 시스템 ===")
        print("1. 회원 등록")
        print("2. 전체 회원 조회")
        print("3. 특정 회원 조회")
        print("4. 회원 정보 수정")
        print("5. 회원 삭제")
        print("6. 종료")
        
        choice = input("선택하세요 (1-6): ").strip()
        
        if choice == '1':
            print("\n=== 회원 등록 ===")
            name = input("이름: ").strip()
            phone = input("핸드폰 번호: ").strip()
            address = input("주소: ").strip()
            
            if name and phone and address:
                db.create_member(name, phone, address)
            else:
                print("이름, 핸드폰 번호, 주소는 필수입니다.")
        
        elif choice == '2':
            db.read_all_members()
        
        elif choice == '3':
            try:
                member_id = int(input("조회할 회원 ID: "))
                db.read_member_by_id(member_id)
            except ValueError:
                print("올바른 ID를 입력하세요.")
        
        elif choice == '4':
            try:
                member_id = int(input("수정할 회원 ID: "))
                
                print("수정할 정보를 입력하세요 (변경하지 않을 항목은 엔터):")
                name = input("새 이름: ").strip() or None
                email = input("새 이메일: ").strip() or None
                password = input("새 비밀번호: ").strip() or None
                phone = input("새 전화번호: ").strip() or None
                
                db.update_member(member_id, name, email, password, phone)
            except ValueError:
                print("올바른 ID를 입력하세요.")
        
        elif choice == '5':
            try:
                member_id = int(input("삭제할 회원 ID: "))
                confirm = input(f"정말로 ID {member_id} 회원을 삭제하시겠습니까? (y/N): ")
                if confirm.lower() == 'y':
                    db.delete_member(member_id)
                else:
                    print("삭제가 취소되었습니다.")
            except ValueError:
                print("올바른 ID를 입력하세요.")
        
        elif choice == '6':
            print("프로그램을 종료합니다.")
            break
        
        else:
            print("올바른 번호를 선택하세요.")

if __name__ == "__main__":
    main()