import os
from dotenv import load_dotenv

# .env 파일 내용 직접 읽기
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f".env 파일 경로: {env_path}")

with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print("=== .env 파일 내용 ===")
    print(repr(content))
    print("=== .env 파일 내용 (일반) ===")
    print(content)

# 환경변수 로드 전
print(f"\n로드 전 EMAIL_PASSWORD: {os.getenv('EMAIL_PASSWORD')}")

# 환경변수 로드
load_dotenv(env_path)

# 환경변수 로드 후
print(f"로드 후 EMAIL_PASSWORD: {os.getenv('EMAIL_PASSWORD')}")
print(f"로드 후 EMAIL_ADDRESS: {os.getenv('EMAIL_ADDRESS')}")

# 모든 환경변수 확인
print("\n=== 모든 환경변수 ===")
for key, value in os.environ.items():
    if 'EMAIL' in key:
        print(f"{key}: {value}")