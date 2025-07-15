math = set({"철수", "영희", "민수"})
science = set({"지민", "영희", "민수"})

#liking both of them
print(math.intersection(science))

#liking at least one of them
print(math.union(science))

#Those who like only math
print(math.difference(science))
    