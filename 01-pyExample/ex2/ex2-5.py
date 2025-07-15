#파이썬의 주요 데이터 타입

#숫자 : number
  #정수형 : int
age=30
year=2025  
print(age)
print(year)
print(type(age))
  #실수형 : float
pi=3.141592
print(pi)
print(type(pi))
  #복소수형 : complex
c1= 3+4j
print(type(c1))
print(c1.real) #실수부
print(c1.imag) #허수부

#문자열 : string
string1 = 'hello'
string2 = 'hi'
print(type(string1))
print(len(string1))


#리스트 : List
mylist = [1, 2, 'hello', 3.14, True]
print(type(mylist))
print(mylist[0])
print(mylist[2])
mylist.append('new')
print(mylist)



#튜플 : tuple
tuple= (10, 20, 'APPLE', False)
print(type(tuple))
print(tuple[2])
#tuple.append('new') 작동불가
print(tuple)


#딕셔너리 : dictionary key와 value의 쌍으로 이루어진 비순차형 자료
person = { 'name' : 'alice', 'age':30, 'city':'seoul' }
print(type(person))
print(person['name'])          
print(person['age'])        
print(person['city'])        
print(person)       
print(person.keys())       
print(person.values())


#세트 : Set -중복되지 않는 요소들로 이루어진 비순차형 자료
myset = {1, 2, 3, 2, 1} #2와 1이 중복되더라도, 출력되지 않음.
print(myset)
#값은 {1, 2, 3}이 나옴. 

#불리언 Boolean
is_true = True
print(type(is_true))

#값없음 NoneType - none 이라는 단일 값을 가짐. its used a lot when you change the value of the variable value
result = None
if result == None:
    print('there is no result')

print(type(result))