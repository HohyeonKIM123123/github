#project 2


class Calc:
    def __init__(self):
        self.result = 0

    def add(self, n):
        self.result += n

    def sub(self, n):
        self.result -= n


calc = Calc()

cola = 10
cider = 8
coffee = 5

while True: 
    print(f"""
=== 간단한 자판기 ===
     1. 콜라 - 1500원 ({cola}개)
     2. 사이다 - 1300원 ({cider}개) 
     3. 커피 - 2000원 ({coffee}개)
     4. 돈 넣기
     5. 거스름돈 반환
     6. 종료
    현재 투입된 금액 : "{calc.result}"
===================
""")    
    a = int(input("번호를 눌러주세요 : "))
    if a ==4 :
        n = int(input("투입할 금액을 눌러주세요 : "))
        calc.add(n)
        print(f"""{n}원이 투입되었습니다. 
                   총 금액 : {calc.result}원   """)
        
    elif a == 5 :
        print(f""" 거스름돈 {calc.result}원이 반환됩니다.\n이용해주셔서 감사합니다.   """)
        calc.sub(calc.result)
        
    elif a == 6 :
        print(" 이용해주셔서 감사합니다. ")

    elif a == 1 :
        if calc.result > 1500 and cola > 0 :
            cola -= 1
            calc.sub(1500)     
            print(f"콜라를 구매했습니다!\n 잔액은 {calc.result}입니다.")
        else :
            print("잔액또는 해당 상품의 잔고가 부족합니다.")    
    elif a == 2 :
        if calc.result > 1300 and cider > 0 :
            cider -= 1
            calc.sub(1300)     
            print(f"사이다를 구매했습니다!\n 잔액은 {calc.result}입니다.")
        else :
            print("잔액 또는 해당 상품의 잔고가 부족합니다.")    
    elif a == 3 :
        if calc.result > 2000 and coffee > 0 :
            coffee -= 1
            calc.sub(2000)     
            print(f"커피를 구매했습니다!\n 잔액은 {calc.result}입니다.")
        else :
            print("잔액 또는 해당 상품의 잔고가 부족합니다.")    
    else:
        print("유효한 숫자를 눌러주세요.")