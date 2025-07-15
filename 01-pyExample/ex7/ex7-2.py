#계산기 기능 구현 - 함수
#계산기 기능 구현 - 클래스

result1 = 0
result2 = 0

def add(num):    #함수 안에서 선언 (생성)된 변수는 바깥쪽에서 볼 수 없음
    global result1  #글로벌이란 키워드 안쓰면 함수 밖의 변수 인식 안함
    result1 +=num
    return result1

print(add(10))
print(add(20))


def sum(num) :
    global result1
    result1 -= num 
    return result1

print(sum(10))

class Calc:
    result = 0
    def add (self,num):
        self.result +=num
    def sub(self, num):
        self.result -= num

calc=Calc()
calc.add(10)
print(calc.result)
calc.add(10)

print(calc.result)
calc.sub(10)
print(calc.result)
calc.sub(10)
print(calc.result)

class Farm :
    carret_number = 0 
    def plant(self, num) :
        self.carret_number += num

farming = Farm()
farming.plant(10)
print(farming.carret_number)


