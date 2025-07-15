# # comprehensive practice

# import random
# count = 0
# x = random.randint(1,20)

# while True :
#     y = int(input("'Put the num between 1~20 : '"))
#     if y>21 or y<0 :
#         print("'better to put the num between 1~20'")
#         continue
#     elif x < y :
#         print("'Too big'")
#         count += 1
#         continue
#     elif x == y :
#         print(f"'correct! you got it at the {count}time'"+"" )
#         break
#     elif x > y :
#         print("'Too small'")
#         count += 1
#         continue




# pratice 2
while True:
    def book_list(name) :
        return print(f""" == Book manage system ==
         ----Book's name : '{name}'"----
        1. Rent 2.Return 3. Search 4. End
        """)
    print("번호를 입력해주세요")
    name = str(input("책 제목을 입력해주세요 : "))
    book_list(name)
