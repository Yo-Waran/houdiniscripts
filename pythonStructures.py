"""FUNCTIONS"""

def hi(name): #function defintion
    print("Hello! "+name) #output function
    
hi("Ram") #calling the function
#or we could do a list as well

names = ["John","Doe","Carl"] 

for x in names:
    hi(x) #callng the function on each item of the list


"""CLASSES"""
class greetings(): #class defintion
    def __init__(self): #initializing variables
        pass
    def hello(self,person): #method defintion
        print("Hola "+person)
    def bye(self,person):
        print("bye "+person)

#greetings().hello() #access hello method inside greetings class

obj1 = greetings() #creating an instance of the class

#or we we could iterate as well
for x in names:
    obj1.hello(x)

"""MODULES"""
import random
test = random.uniform(1,10) #random has a uniform function, which picks any number within the specified range
print(test) #return a random float everytime we print

testList= ["a","b","c","d"]
print(random.choice(testList)) #similarly choices will pick a random item from the list

import random as rd #making an alias

"""OS MODULE"""
import os #import the module
import hou

def dispWindow(listofItems): #func to create a displayWindow
    hou.ui.displayMessage("Your List of it items are : \n" + listofItems)

dir = os.environ#returns all the dictionaries that houdini uses


hdaList= [] #empty list to store the HDAs


for x,y in dir.items():#iterates through the directory
    #print(x) #x stores the keys
    #print(y) #y has the values

    #now to get only the pref folder , we use the HOUDINI_USER_PREF_DIR key

    if x == "HOUDINI_USER_PREF_DIR":
        pref = os.walk(y) #os.walk goes into the directory and returns the current paths, directories and files 
        for currentpath,directories,files in pref:
            if "otls" in currentpath:
                hdaList.extend(files)


listofhdas= "\n".join(hdaList) #making the list into string with each item on a new line
dispWindow(listofhdas) #call the window with the list of strings

"""Handling Text Files"""

#READING FILES 

filepath = "/usr/people/waranr/Desktop/readme.txt" #store the path of the file

file = open(filepath, "r") #read the contents of the file and store them as well

for characters in file:
    print(characters)

#WRITING FILES

newfilepath =  "/usr/people/waranr/Desktop/newdoc.txt" 
try:
    newfile = open(newfilepath, "x") #X flag is used to create a file
except:
    newfile = open(newfilepath,"w") #w flag is for writing something inside a document

newfile.write("THIS IS AN EXAMPLE of Adding  using Python")

newfile.close()

print("Override is done")

#Writing the OS.environ dictionary
import os

mynewcontent= os.environ #store the dictionary 

newfilepath =  "/usr/people/waranr/Desktop/newdoc.txt"  
try:
    newfile = open(newfilepath, "x") #X flag is used to create a file
except:
    newfile = open(newfilepath,"w") #w flag is for writing something inside a document

for keys,path in mynewcontent.items(): #iterate through the dict
    lines = keys + " : "+ path #save the keys and values in a string format
    newfile.write(lines+"\n") #write all of them on new lines

newfile.close() #close the document


#deleting a file
import os

checkfilepath =  "/usr/people/waranr/Desktop/readme.txt"  

span = os.path.exists(checkfilepath) #returns a boolean if the file exists

if span :
    os.remove(checkfilepath)
    print("removed the file")
else:
    print('nothing is removed')