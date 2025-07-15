

#class 종합실습 


class Animal :
    def __init__(self,name):
        self.name = name
    def speak (self) :
        print(f"{self.name}이 소리를 냅니다.")
    def move (self) :
        print(f"{self.name}이 움직입니다.")
    pass

class Flyable:
    def fly (self) :
        print(f"{self.name}이 납니다.")
    pass

class Swimmable:
    def swim (self) :
         print(f"{self.name}이 헤엄칩니다.")
    pass

class Dog(Animal):
    def speak (self) : #오바라이팅 덮어쓰기?
        print(f"{self.name}이 멍멍 짖는다.")
    pass

class Duck(Animal,Flyable,Swimmable):
    def speak (self) :
        print(f"{self.name}이 꽥꽥 소리칩니다.")
    def move (self) :
        print(f"{self.name}이 움직입니다.")
    pass


# 현재 이 파일이 직접 실행되었는가 아니면 간접적으로 실행했는가. 메인일때만 실행되도록,. 
if __name__ == "__main__" :
    dog = Dog("바둑이")
    dog.speak()
    dog.move()
    duck=Duck("오리")
    duck.speak()
    duck.move()