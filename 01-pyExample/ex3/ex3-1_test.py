# 연습문제
# 마이클의 영어 점수를 입력받고,
# 영어 점수가 90점 이상이면, 'A학점'
# 영어 점수가 80점 이상이면, 'B학점'
# 영어 점수가 70점 이상이면, 'C학점'
# 영어 점수가 60점 미만이면, 'D학점' 으로 출력하시오.

score = int(input("마이클씨 영어 점수를 입력하십시오 : "))
if score>=90:
    print("A학점")
elif score>=80:
    print("B학점")
elif score>=70:
    print('C학점')
elif score<70:
    print('D학점')

# else는 조건을 쓰지 않는다 말그대로 "아니면" 이기 때문
# “else never applies a condition explicitly, 
# because it already implies the condition:
#  ‘if none of the above are true.’”



#파이썬에서 랜덤수 발생
import random

random_int = random.randint(0,2)
#print(random_int)

if random_int==0:
    print("오늘의 날시는 비입니다. 우산을 챙기세요!")
elif random_int==1 :
    print("오늘의 날시는 흐림입니다. 나들이 가기 좋을 수도 있어요!")
else  :
    print("오늘의 날시는 맑음입니다. 화창한 하루 되세요~!")

