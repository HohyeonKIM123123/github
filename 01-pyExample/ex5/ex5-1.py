#its hard for me to articulate what i've been going trough, but i can't say i dont love you
# cus i love you i try to find a way to comunicate the thoughts that i hold 

# purpose
# 1. removing duplicates from a code
# 2. recycling code
# 3. simplifying and modularizing code

# declaration statement of function
# calling statement of function
# 4 patterns of funcution

# 1. mediator x return value x
def my_func():
    print("my_func() called")  #declaration statement

my_func()  #calling statement

# 2. mediator o return value x
def my_func2(name):
    print(f"{name}님 환영합니다")

my_func2('tom')

# 3. mediator x return value o
def my_func3():
    print('my_func3 called!')
    return 'yeahahahah'

name2 = my_func3()
print(name2)



# 4. mediator o return value o

def my_func4(x,y):
    print('my_func4 called!')
    return x + y
sum = my_func4(10, 20)
print(sum)


# the basic answer of mediator variable
def show_message(message, sender= "unknowm"):
      print(f"Message: {sender}")
show_message("Hello, World!", "representor")
show_message("Hello, World!") 

# changable ingreadient list : there are mediators 
# the input of calling statement : ingredient
# the input of declaration statement : mediator    
def func_sum( *nums) :
    sum = 0
    for num in nums :
        sum
    return sum

print(func_sum(1, 2, 3, 4, 5))  # calling statement with mediator

                 