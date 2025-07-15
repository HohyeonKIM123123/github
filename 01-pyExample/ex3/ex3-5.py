#double repeat statement. loop is in another loop

for i in range(0, 6) :
    print (f'i={i}')
    for j in range (0, 6) :
        print(f'j={j}', end=",") # no text change by using distinguished character
    print() # simple text change

# so you can make a time table by using that 
# 1x1 1x2 1x3 ~~~
# 2x1 2x2 2x3 ~~~
# 3x1 3x2 3x3 ~~~
# ~~~ ~~~ ~~~ ~~~
# bigger is faster

for dan in range (2,10):
    print(f"{dan}")
    for num in range(1,10):
        print(f"{dan} x {num}= {dan*num:}")
    print()


# spotting star
# making a star with 5x5
#range (stop) 5 => 0~4
#range (start, stop) 1,5 => 0~4
#range (start, stop, step ) 1,10,2 => 1 3 5 7 9

N=int(input("How many band do you want?"))
M=1
for i in range(N) :
    for j in range (M) :
        print('=', end = "")
    M +=2
    print()



    if M >15 :
        break