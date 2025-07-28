import os
from dotenv import load_dotenv

# .env 파일 경로
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f".env 파일 경로: {env_path}")
print(f".env 파일 존재: {os.path.exists(env_path)}")

# 환경변수 로드
load_dotenv(env_path)

# 환경변수 확인
email_address = os.getenv('EMAIL_ADDRESS')
email_password = os.getenv('EMAIL_PASSWORD')

print(f"EMAIL_ADDRESS: {email_address}")
print(f"EMAIL_PASSWORD: {'설정됨' if email_password else '설정 안됨'}")
print(f"EMAIL_PASSWORD 길이: {len(email_password) if email_password else 0}")