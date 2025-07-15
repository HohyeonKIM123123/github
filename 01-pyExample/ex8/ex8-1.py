#예외처리

#존재하지 않는 파일 열기
# f = open ("없는파일", "r")

# 0 으로 나누기
# num = 0 
# print (5 / num )

#리스트인덱스 오류 
# a= [1,2,3]
# print(a[3])


try :
    5/0
except ZeroDivisionError as e :
    print (e)


    
try:
    age = int(input("나이를 입력하세요 : "))
except:
    print("아라비아 숫자로 입력하세요.")
else: #오류가 없을때
    if age <= 18:
        print ("미성년자입니다")

    else:
        print("성인입니다.")

try :
    f = open ("없는", "R")
except:
    print("없는 파일 오류.")
    f = None
finally :
    if f : #만약 f가 생성되어 있다면 
        f.close()