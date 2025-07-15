#class inherit    부모 클래스의 자산을 자식에게 넘겨주는 것
# 
# 부모 클래스
class Animal:
    age = 0
    def sleep(self) :
        print("잔다")

    pass

class Dog(Animal):  #Dog =caracter of  animal + caracter of  dog강아지 고유의 특성
    pass

class Cat(Animal):   #cat = caracter of animal + caracter of cat
    pass

dog1= Dog()
print( dog1.age)
cat1 = Cat()
print( cat1.age)


#class 다중상속
class Flyable:
    def fly(self) :
        print("날 수 있다")


class Bird(Animal,Flyable):
    pass

bird1=Bird()
bird1.fly()
bird1.sleep()