# Create File 

f= open("test1.txt", 'w', encoding = 'utf-8')   #second one is option  #한글을 위해 encoding~
# "w" stand for  "writing"   , "r" reading , "a" adding 
f.write('test file. \n this is test file')
f.close() # close file

#reading and fecthing file 

f= open("test1.txt", 'r', encoding = 'utf-8')
while True:
    line = f.readline()
    if not line : 
        break
    print (line)
f.close()

f= open("test1.txt", 'r', encoding = 'utf-8')
Lines = f.readlines()
for line in Lines: 
    print(  line.strip()  )
f.close()

# adding content in the file
f=open("test1.txt", "a")
f.write("\n this is added by bam \n")
f.close()


# using "with"
with open("test1.txt", "a" ) as f:
    f.write ("this is added 22. 2\n")