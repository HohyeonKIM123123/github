#while statement(40%) -for statement (60%)

#form
# make loop variable clear 
#while 
    #if conditional clause is true it is executed repetitively
    #increase and decrease in conditional clause 

#countdown 5sec
count = 5
import time
while count > 0:   
    print (f'{count}')
    #time.sleep(1)
    count -= 1 #Putting comprehensive calculator A-=B -> A= A - B        
    # at this point, it compare to while condition, so if it is still true then it's executed again
print ('Blast off!')



#if you get stuck in an infinite loop,
    #1. after opening the console, press CTRL+C simultaneously
    #2. press the delete button in the consol 
    #3. simply restart the "VScode"
    #3. Terminate the python process in the Task manager

# making the infinite loop - vending machine, lift program

count = 0
import time
while True :
    print(f'infinite loop-{count}')
    if count > 9:
        break #terminate the infinite loop
    count += 1
    #time.sleep(1)
print('terminate infinite loop!')


# continue statement : terminate the loop right away, return to the first place of loop
# export from 1 to 10
for i in range(1,11) :
    if i % 2 ==0:  #if it is even (odd)
        continue       #terminate it , pass the underneath print statement
    print( i )


# practice
# 1. export only even, from 1 to 10 using "while statement" and "continue"
count = 0
while count <10 :    
    count += 1
    if count %2 == 1 :
        continue
    print(count)
