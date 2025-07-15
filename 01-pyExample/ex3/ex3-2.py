#반복문 loop statement(repetitive) str 반복적으로 코드를 수행하는 문장
# for문 # while문

#for variable in sequence(range, list, tuple, string) : 
# code that is repetitively executed ( indentation is required)

# loop variable (from 0 to 4) for 5 times

for i in range(5) :
    print(f'loop count: {i}') 

#from 1 to 20
for i in range (1,21):       # for starting from 1 you can designate starting point
    print(f'loop count(index):{i}')
    

#from 1 to 20 while doubling each time
for i in range(1,101,2):
    print(f'loop count(index){i}')

#1
for i in range (1,101):
    if i%2 == 0 :
        print({i})
#2
for i in range (1,101):
    if i%2 == 0 and   i%3 == 0 : #if 안넣어도 됨
            print({i})
   
#3
sum = 0
for i in range (1,101):
    sum= sum + i
    print((sum))

max({sum:sum+ i})
#4

for i in range (1,101):
    myi = str(i)
    if myi.find('3') !=-1 :
        print({i})