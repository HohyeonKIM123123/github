

#practice
# 1. export only even, from 1 to 10 using "while statement" and "continue"
count = 0
while count <10 :    
    count += 1
    if count %2 == 1 :
        continue
    print(count)

#answer
num = 1
while num < 11 :
    num += 1
    if num % 2 ==1 :
        continue
    print(num)
    
# runtime debug tool
# 1. write the end point 
# 2. run and debug
# 3. step over by f10

#2. export all multiple of 2 and 3 within 100 using "while statement" 
count = 0
while count <100 :    
    count += 1
    if count %2 == 0 and count %5 ==0 :
        print(count)

#3. Get a number between 1 and 10 using an infinite loop.

while   True :
    name = int(input("1~10사이의 수를 입력하십시오 : "))
    if name== 10 :
        print("10을 입력하셨습니다.")
        break
    print(f'{name}')

#answer
while True :
    n= int(input("1~10사이의 정수 입력: "))
    if 0<= n <= 9 :
        print (n)
    elif n ==10 :
        print( "10 종료 ")
        break
    else:
        print("1~10 사이의 정수가 아닙니다.")

# 4 making 
for i in range(1, 10):
    print(f'3 X {i} = {3 * i}')


for i in range(1,100):
    print(f"7 x {i} = {7*i}")
#5

number = int(input('자릿수를 파악할 수를 넣어주세요'))
count=1
while True :
    number=number//10
    if number == 0 :
        break
    count += 1

print(f'자릿수는{count}입니다.')


