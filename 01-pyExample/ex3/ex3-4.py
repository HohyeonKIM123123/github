
# cola = 3
# cider = 2
# orange = 4
# while True :
#     num = int(input("제품번호를 입력해주세요."))
#     if num == 1:
#         if cola <1 :
#             print("콜라 잔고가 떨어졌습니다.")
#             continue
#         else :
#             cola -= 1
#             print("콜라가 나옵니다")
#             continue
#     elif num == 2: 
#         if cider <1 :
#             print("사이다 잔고가 떨어졌습니다.")
#             continue
#         else :
#             cider -= 1
#             print("사이다가 나옵니다")
#             continue

#     elif num ==3 :
#         if orange <1 :
#             print("오렌지쥬스 잔고가 떨어졌습니다.")
#             continue
#         else :
#             orange -= 1
#             print("오렌지쥬스가 나옵니다")
#             continue
#     else :
#         print("제품번호를 확인해 주세요.")






import random

print(" 빠바바밤~")

count = 0
strike = 0
ball = 0

while True :
    count +=1
    print(f'"{count}번 송구!"')
   
    result = random.randint(1,10)
    if result <8 :
        strike += 1
    else :
        ball += 1

    print (f'"{strike}" 스트라이크 "{ball}" 볼!')

    if strike ==3 :
            print( "삼진아웃!")
            break

    elif ball ==4 :
            print( "볼넷!")
            break

            
    