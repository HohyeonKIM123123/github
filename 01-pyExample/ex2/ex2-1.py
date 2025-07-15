# 코멘트(주석)
print("hello python")
# : ctrl + /   넘모 넘모 재밌다
# 이렇게 주석을 달면, 실행이 안됨. 
print('hello python')
# 파이썬에서는 쌍따옴표 단따옴표 기능 구별 x 따옴표로 묶은 것은 문자열 데이터이다. 

#정수형
a = 123  #대입연산자 =는 오른쪽의 값을 왼쪽에 덮어쓰기한다 
#실수형
b = 3.14
#음수형
c = -123

print(a)
print(b)
print(a+b+c)

d = 4.24E10 #10의 10승 
print(d)

#10진수 0~9 그래서 10은 10으로 표시된다

#8진수 0~7 그래서 8은 10으로 표시된다
e=0o10
print(e)

#16진수0~9 a b c d e f 10 그래서 30은 1e이다.
f=0x10
print(f)


a = 3 #a값 덮어씌어짐
b = 7 #b값 덮어쓰기 *[변수의 재사용]

print( a + b )
print( a - b )
print( a / b ) 
print( a + b ) 

#✅ // 는 몫 연산자 (floor division) 입니다. 즉 소수점을 버리고 몫만 계산합니다.
print( a // b )
#✅  % 는 나머지 연산자 (modulo) 입니다. 몫을 버리고, 나머지만 출력합니다.
print( a % b )

# round는 소수점자리 표시 연산자입니다.
print(round(a/b,5))

print(round(a/b,5))