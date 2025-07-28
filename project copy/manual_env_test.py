import os

# .env 파일 직접 읽기
env_path = os.path.join(os.path.dirname(__file__), '.env')

print("=== .env 파일 직접 읽기 ===")
with open(env_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value
            print(f"설정: {key} = {value}")

print("\n=== 환경변수 확인 ===")
print(f"EMAIL_ADDRESS: {os.getenv('EMAIL_ADDRESS')}")
print(f"EMAIL_PASSWORD: {os.getenv('EMAIL_PASSWORD')}")
print(f"SMTP_SERVER: {os.getenv('SMTP_SERVER')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")

# 이메일 테스트
if os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'):
    print("\n=== 이메일 발송 테스트 ===")
    
    import sys
    sys.path.append(os.path.dirname(__file__))
    
    from modules.email_notifier import EmailNotifier
    
    test_books = [{
        'title': '해리 포터와 마법사의 돌',
        'loan_date': '2024-01-15',
        'due_date': '2024-01-29'
    }]
    
    notifier = EmailNotifier()
    
    try:
        result = notifier.send_overdue_notification(
            member_email=os.getenv('EMAIL_ADDRESS'),
            member_name="테스트 사용자",
            overdue_books=test_books
        )
        
        if result:
            print("✅ 이메일 발송 성공!")
        else:
            print("❌ 이메일 발송 실패!")
            
    except Exception as e:
        print(f"❌ 이메일 발송 중 오류: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ 이메일 설정이 완료되지 않았습니다.")