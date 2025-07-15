# 문자열 다루기 
str = "Life is too short, you need python"
print( str )

#여러줄 문자열
multiline = """
Life is too short
you need python
is this sentences included?
"""
print(multiline)

# 문자열 중간에 단따옴표 넣기
print( "Python\'s favorite food is perl ")
# 문자열 중간에 쌍따옴표 넣기
print( 'Python\"s favorite food is perl' )

#문자열 합치기
print( "Python" + "is fun")
print( "Python" * 3 )
print( "=" * 50 )

#문자열 인덱싱
str = "Life is too short, you need Python"
print(str[0]) #첫번째 문자
print(str[1]) 
print(str[-1])
print(str[-2]) #마지막 문자
#문자열 슬라이싱
print( str[0:4]) # "Life" 시작인덱스:끝인덱스+1
print( str[0:5]) # "Life "
# " you need python 출력"
print( str[19:])
print( str[:17])
print( str[19:-7])

#문자열 포매팅(문자열에 변수값 넣기)
print( " I eat %d apple" % 3)
print( " I eat %d apples, I sell %d apples" % (3, 2))
print( "%0.4f" % 3.42134234) #소수점 4자리까지 출력
print( "%10.4f" % 3.42134234) # 전체 자릿수 10개 소수점 4자리까지 출력

# 문자열 개수 세기
a = "hobby" 
print( a.count("b"))

# 문자 위치 찾기 
a = "python is best choice"
print( a.find('b')) # 값이 10이라면 찾음
print( a.find('k')) # 값이 -1이라면 못찾음
print( a.index('n')) # 5번째 위치에 n이 있음.
# print( a.index('k')) # 못찾으면 value error 가뜸 그래서 확실할 때만 쓰고,
# print( a.index('c')) # 
try:
    print( a.index('k')) #못찾음 value error
except ValueError: #make it detour
    print("substring not found")


# 구분자 넣기
a= ","
print( a.join('abcd')) #a,b,c,d

# 양쪽 공백 지우기
a = " HI "
print( a.strip())

# 문자열 나누기
a= "life is too short"
print(a.split()) #result is shown as list 
a= "life:is:too:short"
print( a.split(':') ) # they specify the delimiter in detail. 구분자를 구체적으로 기술한다

# 문자열 바꾸기
a= "Life is too short"
print(a.replace('Life', "your leg"))