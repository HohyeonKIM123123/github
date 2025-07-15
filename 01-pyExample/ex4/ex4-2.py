#Tuple
#It's totally same with the List but it is the type which is not changeable.
# it is for deliver fixed value, and it's used return value as well.
#empty tuple 
e_t = ()
print(e_t)

#declaration of tuple
num = (1, 2, 3, 4, 5)
print(num)
num2= 10, 20, 30
print(num2)
#if there is a ingredient, you should use " , "
num3 = (5) # it is just 5
num4 = (5,) # there you go now you have a tuple

print(num3)
print(num4)

# use the "tuple" as a  return value of the function.
def get_user_data() :   # now we gonna define it
    return "김철수", 15, "서울"   # as a tuple 

name, age, city = get_user_data()
print( name, age, city)
print (type(get_user_data()))