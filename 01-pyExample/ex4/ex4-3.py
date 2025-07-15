#he is so passionate that make me nut

#Dictionary 집 (key) -> House(Value)
#save the data which is paired as " Key":"value"

#empty dictionary
empty_dict = {}
print(empty_dict)

person = {
    "name":"홍길동" , 
    "age":30,
    "city":"seoul"
}
print(person)

print(person["name"])
print(person['age'])
print(person['city'])

print( person.get('name')) # using get f
print( person.get('address')) # None
print( person.get('address',"주소값 없음")) # setting it as a settled answer


#adding ingredient
dict_a = {}
dict_a['name '] = "홍길동"
dict_a['age'] = 30
print(dict_a) 

#deleting ingredient
del dict_a["age"]
print(dict_a)

#bringing "Key List"        It is the matter
personperson = {
    "name":"홍길동" , 
    "age":30,
    "city":"seoul"
}
print( person.keys())         # this object can not be used as in index or loop
print(list(person.keys())) # it change the form as a list

# "In" caculator - checking if a Key exist in a dict
print ("name" in person)   #gonna be true

person.clear() # delete all