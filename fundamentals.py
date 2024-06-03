"""PYTHON FUNDAMENTALS"""
#print() is used to Display output on the screen
print("*"*55)
print("START OF THE PROGRAM")

"""DATA TYPES"""

print(1) #integer
print(1.0) #float
print("Hello") #string

"""VARIABLES"""
test = 2.0 + 4
print(test) #results a float of 6.0

"""LIST AND TUPLES"""

mylist = ["a","b","c"] #creating basic list
print(mylist)
print(mylist[-1]) #indexing a list
print(mylist[:-2]) #slicing a list

mylist.remove("b") #removing an item
mylist.append("d") #adding an item

mytuple = ("a1","b1","c1") #creating a tuple
print(mytuple) 

"""Join/Split Lists"""

mystring = ("/".join(mylist)) #joining lists
print(mystring.split("/")) #spliting strings into lists 

node = "asset_flower"
print(node.split("_")[-1]) #spliting and indexing a string

"""LIST METHODS"""

exList1 = ["item1","item2","item3","item4"]
position = exList1.index("item3") #storing an index 
print(position)
print(exList1[:position])
print(len(exList1)) #length of the list
print(exList1.pop(1)) #remove a specific element in a list
print(exList1.count("item4")) #number of repetitions of an element

"""For LOOPS"""

count = 1
for x in exList1:
    print(str(count)+" item is:"+x)
    count += 1
    
"""CONDITIONS"""

count = 1
for x in exList1:
    if count<3:
        print(str(count)+" item is:"+x)
    count += 1
#similarly we have elif, else, ==,!= , or , and to match conditions with.

"""EXTRACTING LISTS"""
exList2 = []
count = 1
for x in exList1:
    if count<3:
        exList2.append(x) #appedning the conditioned items
    count += 1
print(exList2)

"""NESTED LOOPS"""
for i in range(5):
    print(i)
    for x in exList1:
        if count<3:
            exList2.append(x) #appedning the conditioned items
            count += 1
print(exList2)

"""IF SHORT"""

test = "item3"

if test in exList1:
    print(test + " in LIST")
else :
    print(test+" NOT IN LIST")
    
#these two statements can comprehended with

#print(test+" in LIST") if test in exList1 else print(test + " NOT in LIST") #comprehended if condition

newList = [node for node in exList1 if "item" in node]
print(newList)

"""While Loops"""

x = 1
while x <= 10:
    print(x)
    x+=1

"""DICTIONARIES"""

myasset = {
    "name":"pinetree",
    "variant":"a1",
    "hgt":6.35,
    "lgt":2.2
}

print(myasset) #print whole dict
print(myasset.keys()) #prints only the keys
print(myasset.items())#prints all the items

myasset["color"]="red" #modifying the dict
 
print(myasset)

for x,y in myasset.items(): #iterating through the dict
    print("My asset's "+ x + " is " + str(y))

"""TRY/EXCEPT"""

list01= [1,2,3,4,"test","apples"]

for x in list01: 
    try: #if integer it will try this
        print(x+10)
    except: #else we print it as it is.
        print(x)


