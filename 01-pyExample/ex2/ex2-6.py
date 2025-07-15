#형변환 type casting -데이터형이 변경되는 것
#암시적 형변환 #직접적인 형변환 x
x=3
y=4.12
z=x+y #다른 두개의 타입이 연산되면, 더 큰 타입으로 변경된다.
print(type(x)) #int
print(type(y)) #float
print(type(z)) #float

#명시적 형변환 #directed change by using function
myint=int("123")
myfloat = float( 123 )
mybool = bool(0) # 1은 트루
print(myint)
print(myfloat)
print(mybool)

try:
    myInt2 = int("123abc한글") #odd type
except:
    print("invalid syntax")

print(str(123))
print(str(3.14))
print(str([1,2,3]))


#파이썬에서 false로 간주하는 값
#숫자 0(정수, 실수)
#빈 문자열 ""
#빈 리스트 []
#빈 튜플 ()
#빈 딕셔너리 {}
#빈 세트 set()
#None

# except for above things, everything will be regarded as a "True"
print(bool(0))
print(bool(1))
print(bool(0.0))
print(bool("hello"))
print(bool(""))
print(bool([]))
print(bool([1,2]))
print(bool(()))
print(bool(None))

print(list("python"))
print(list((1,2,3)))
print(list(({1,2,3})))

print(tuple("python"))
print(tuple([1, 2, 3]))

print(set("python"))
print(set([1, 2, 3]))



# 변수와 상수
#변수 이름 정하는 법
# 1. 숫자로 시작하면 안됨.
myVar = 10
#1myvar2 =20 #이렇게 오류가 나벌임.
# 2. 특수문자(!@#)을 사용할 수 없음. (_언더바 예외)
_myvar = 11
#myvar$$$ = 12 #error appears like this

# 영소문자로 시작하고, 단어와 단어 사이에는 대문자 (camel case)를 사용함
myVarLikeThisSoYouCanRecognizeItSoEasily = "Camel Case"

myVar = 10
PI = 3.14
MY_CONST_VAR = 2000











