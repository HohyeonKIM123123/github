# proj01.py

# 1인 개인 미니 프로젝트

# 간단한 계산기
# 콘솔 기반의 간단한 사칙연산이 가능한 계산기를 만들어 봅니다.
# 클래스로 설계하면 더 좋습니다.

# 입력/출력 예시

class Calc:
    def add(self, n, n2):
        return n + n2

    def sub(self, n, n2):
        return n - n2

    def mul(self, n, n2):
        return n * n2

    def di(self, n, n2):
        if n2 != 0:
            return n / n2
        else:
            return "0으로 나눌 수 없습니다."


calc = Calc()

while True: 
    print("""
=== 간단한 계산기 ===
     1. 덧셈
     2. 뺄셈
     3. 곱셈
     4. 나눗셈
     5. 종료
===================
""")    
    f = int(input("기능을 선택하세요: "))
    n = int(input("첫번째 수를 입력하세요."))
    n2 = int(input("두번째 수를 입력하세요."))      

    if f == 1 :
        calc.add(n, n2)  # n을 더함
        print(f"결과는 '{n}' + '{n2}' = '{calc.add(n, n2)}'입니다.")  # 결과 출력
        continue
    elif f == 2 :
        calc.sub(n, n2)  
        print(f"결과는 '{n}' - '{n2}' = '{calc.sub(n, n2)}'입니다.")  # 결과 출력
        continue   
    elif f == 3 :
        calc.mul(n, n2)  
        print(f"결과는 '{n}' X '{n2}' = '{calc.mul(n, n2)}'입니다.")  # 결과 출력
        continue
    elif f == 4 :
        calc.di(n, n2)  
        print(f"결과는 '{n}' / '{n2}' = '{calc.di(n, n2)}'입니다.")  # 결과 출력
        continue
    elif f == 5 :  
        print("계산기를 종료합니다.")
        continue
  












