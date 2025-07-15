#list

# empty list
empty_list = []
print (empty_list)

numbers = [1, 2, 3, 4, 5]
mixed_list = ["apple", 123, 3.14, True]
nested_list = [[1,2],["a", "b"], [True, False]]

print(numbers[0]) # print index0 in the list
print(numbers [:3]) # from zero to 2 ingredients
print(numbers [1:]) # from 1 to last ingredients
print(numbers [::]) # every ingredients
print(numbers [::2]) # every second ingredients
print(numbers [::-1]) # every ingredients in reverse direction

# replace ingredient
my_list =  ["a", "b", "c"]
my_list[1] = "hello" #replace
print(my_list)
# my_list[3] = "d" }}}} isn't working

my_list.append("d") # "append" is always add it at the last place
print(my_list)

my_list.insert(0,"z") # now you can put it in the first place as well
print(my_list)

my_list.extend(mixed_list) #you can merge/combine your list with another list
print(my_list)


# delete ingredients
del my_list[2]
print(my_list)

#remove 
my_list.remove("z")
print(my_list)

popped_item = my_list.pop(0) # they reture the 0 ing after removing it 
print(popped_item)
print(my_list)
# then they show the "a" after deleting it.

my_list.clear()
print(my_list)

#the length of list
print(len(mixed_list))



#how to sort it in ascending order (descending order)

scores = [85, 97, 78, 92, 65]

scores.sort()
print(scores)

scores.reverse()
print(scores)

print(scores.count(92))
print(scores.index(92))

