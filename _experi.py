# 들여쓰기 오류와 논리 오류가 있습니다. 아래와 같이 수정하면 정상 작동합니다.
num = int(input("put your num : "))
count = 0
while True:
    num = int(input("put your num : "))
    if num % 7 == 0 and num != 0:
        print("7의 배수입니다")
        count += 1
        num = num // 7
    else:
        continue