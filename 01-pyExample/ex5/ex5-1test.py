# 1 
x = int(input("X를 입력하십시오 : "))
y = int(input("Y를 입력하십시오 : "))
def func_multi(x,y) :
    print('func_multi is called!')
    return x*y
print(func_multi(x,y))


# 2
def func_hello(name):
    print(f"hello {name}!")
func_hello("bam")


# 3
def func_list(items):
    for item in items:
        print(item)
    return (items) 
combined_list = func_list("apple") + func_list("peach") + func_list("banana")
print("combined_list : ", combined_list)

#3 better answer 
# def func_list(fruit) :
#     fruitName = "".join(fruit)
#     return fruitName

# print(func_list(["사과","바나나","복숭아"]))

# 4 
def func_dist(x):
    if x % 2 == 0 :
        return " even "
    elif x % 2 == 1:
        return " odd " 
x = int(input("Enter a number: "))
print(func_dist(x))

#better answer you can check it from slack
def Is_even( n ) :
    return "even" if n % ==0 else " "


# 5
def func_rev(string):
    return string[::-1]
string= input( "Enter a string: ")
print(func_rev(string))