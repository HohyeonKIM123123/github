#set (bunch)
# its not overlapped, nonsequential set 
# Intersection  // # union // # difference

set_0 = set ([1,2,3])
set_1 = set ([1, 2, 3])
set_2 = set ("hello")
set_3 = set ()

print(set_0) # what do you expect to see from it
print(set_1)
print(set_2)
print(set_3)

#if you wanna use "Index", you get to change the set to list
list_0 = list(set_0)
print (list_0)
print(list_0[0])
# change list to set
list_10 = [10,20,30]
set_10 = set(list_10)
print(set_10)

#calculating the "Set"
s1= set ([1,2,3,4,5,6])
s2= set ([4,5,6,7,8,9])
#intersection (find the common things)
print(s1&s2)
print( s1.intersection(s2))
#union (merge the sets)
print( s1 | s2)
print(s1.union (s2))
#difference
print(s1 - s2)
print(s2 - s1)
print(s1.difference(s2))

#adding ingredient
s3= set ([1,2])
s3.add (3)    #we use "append" when we edit the list
print(s3)

s3.update([4, 5, 6])
print(s3)

#deleting ingredient
s3.remove(3)
print(s3)
print(s3.clear())