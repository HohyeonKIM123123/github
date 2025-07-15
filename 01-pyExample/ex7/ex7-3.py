

#생성자 함수 클래스 객체가 생성될 떄 자동 호출되늖 함수

class Car:
    def __init__(self) :
        print("creator is called")
        pass #아무 수행도 안함


car = Car()

class Voltcar:
    brand = ""
    color = ""
    def __init__(self, brand , color) :
        self.brand = brand   
        self.color = color

    def info(self) :
        print (f"{self.brand},{self.color}")
        
vc = Voltcar ("tesla", "blue")
vc.info()