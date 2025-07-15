#조건문
#특정 조건이 참일 때만, 코드를 실행하게 한다. 선택적 실행

#if 조건 (절, true 또는 false)
#   조건이 true일 때 실행될 코드 (들여쓰기 필수)


score = 85
if score >= 60:
    print("합격입니다!")


age = 15
if age >=18:
    print("성인입니다")
else:
    print("미성년자입니다.")

score1 = int(input("1의 score를 입력하세요 : "))

if score1 > 70 :
    print("합격입니다.")
else:
    print("불합격입니다.")

#if elif문
cost = int(input("예산을 입력하세요 : "))
if cost >=80 :
    print("80유로를 초과하셨습니다")
elif cost < 40 :
    print("40유로를 초과하셔야합니다.")

#if elif else문
month = 6
if month <= 3:
    print("1,2,3월")
elif month <= 6:
    print("4,5,6월")
else:
    print("그 외의 월")