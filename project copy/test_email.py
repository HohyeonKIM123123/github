import os
import sys
from dotenv import load_dotenv

# 환경변수 로드 (여러 방법 시도)
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"환경변수 파일 경로: {env_path}")
print(f"파일 존재 여부: {os.path.exists(env_path)}")

# 방법 1: 경로 지정
load_dotenv(env_path)

# 방법 2: 기본 로드
load_dotenv()

# 방법 3: 강제 오버라이드
load_dotenv(env_path, override=True)

sys.path.append(os.path.dirname(__file__))

from modules.email_notifier import EmailNotifier

def test_email():
    print("=== 이메일 설정 확인 ===")
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    
    print(f"EMAIL_ADDRESS: {email_address}")
    print(f"EMAIL_PASSWORD: {'설정됨' if email_password else '설정 안됨'}")
    print(f"SMTP_SERVER: {smtp_server}")
    print(f"SMTP_PORT: {smtp_port}")
    
    if not email_address or not email_password:
        print("❌ 이메일 설정이 완료되지 않았습니다.")
        return
    
    print("\n=== 이메일 발송 테스트 ===")
    
    # 테스트용 연체 도서 데이터
    test_books = [{
        'title': '해리 포터와 마법사의 돌',
        'loan_date': '2024-01-15',
        'due_date': '2024-01-29'
    }]
    
    # EmailNotifier 인스턴스 생성
    notifier = EmailNotifier()
    
    # 테스트 이메일 발송
    try:
        result = notifier.send_overdue_notification(
            member_email=email_address,  # 본인에게 테스트 발송
            member_name="테스트 사용자",
            overdue_books=test_books
        )
        
        if result:
            print("✅ 이메일 발송 성공!")
        else:
            print("❌ 이메일 발송 실패!")
            
    except Exception as e:
        print(f"❌ 이메일 발송 중 오류: {e}")

if __name__ == "__main__":
    test_email()