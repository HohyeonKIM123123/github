# 3
def func_list(items):
    for item in items:
        print(item)
    return (items) 
combined_list = func_list("apple") + func_list("peach") + func_list("banana")
print("combined_list : ", combined_list)


def func_list(fruit) :
    fruitName = "".join(fruit)
    return fruitName

print(func_list(["사과","바나나","복숭아"]))

list



print(["사","사","람","바"])
print("".join(["사","사","람","바"]))
print(", \n".join(["사","사","람","바"]))