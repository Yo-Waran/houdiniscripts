"""CREATING NODES"""
import hou

newobject = hou.node("/obj") #select the network and store it in a variable

newmesh = newobject.createNode("geo","container") #using the createNode() passing node type and name

file = newmesh.createNode("file","newFile") #creates another node inside the mesh node. 

"""MODIFYING NODES"""
objects = hou.node("/obj") #define the context to search in 
donObj = objects.node("donut") #pass the exact name of the node

print(donObj) #prints the name of the node that has been created already

print(donObj.path()) #prints the full path of the node 
print(donObj.position())#prints 2D position in network veiwer
print(donObj.type().description()) #prints the description

"""NODE MANIPULATION"""

#Creating a bunch of spheres

import hou

objects = hou.node("/obj") #context to be created in

for x in range(6): 
    container = objects.createNode("geo","geo_sphere_"+str(x)) #creates a container node with varying Names
    geometry = container.createNode("sphere") #inside which we create a sphere
    mypos = (x*2,0) #make a tuple for the 2D coordinates which increases horizontally
    container.setPosition(mypos) #set the positions of the container
    container.parm("tx").set(x*5) #set the tx parameter of the container.
    mycoord = (x*2,x*3,x*5) # a 3 axes coordinate as a tuple
    container.parmTuple("t").set(mycoord) #passing all the three parameters using a tuple


"""Coloring Nodes"""


objects = hou.node("/obj") #context to be created in

usrcolor = hou.ui.selectColor()#used for picking a color manually
for x in range(12): 
    container = objects.createNode("geo","geo_sphere_"+str(x)) #creates a container node with varying Names
    mypos = (x*2,0) #make a tuple for the 2D coordinates which increases horizontally
    container.setPosition(mypos) #set the positions of the container
    print(container.color()) #returns the color of the node  
    rgb= (0.5,0.2,x*0.1) #rgb tuple used for setting colors
    container.setColor(hou.Color(rgb)) #set the color of the node

"""Shape of Nodes"""
import hou

editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
shapes = editor.nodeShapes() #returns a tuple of shapes of Nodes that are available
print(shapes)

objects = hou.node("/obj") #context to be created in

for x in range(12): 
    container = objects.createNode("geo","geo_sphere_"+str(x)) #creates a container node with varying Names
    mypos = (x*2,0) #make a tuple for the 2D coordinates which increases horizontally
    container.setPosition(mypos) #set the positions of the container
    print(container.color()) #returns the color of the node  
    rgb= (0.5,0.2,x*0.1) #rgb tuple used for setting colors
    container.setColor(hou.Color(rgb)) #set the color of the node
    container.setUserData("nodeshape","wave")

"""SELECTED NODES"""

import hou

context = hou.node("/obj") #define context

sel = hou.selectedNodes() #STORING THE SELECTED NODES

print(sel)


# SETTING COLOR TO EVEN/ODD numbers in the node names
import hou

context = hou.node("/obj") #define context

sel = hou.selectedNodes() #STORING THE SELECTED NODES
 
rgb1 = (0.5,0.2,0.6)
rgb2 = (0.8,0.9,0.1)

#iterating through selection
for i in sel:
    name = str(i)
    splitName=name.split("_") #splits the string
    suffix = splitName[-1] #store only the suffix
    if int(suffix)%2==0:
        i.setColor(hou.Color(rgb1)) #sets a color for even numbers in the node name
    else:
        i.setColor(hou.Color(rgb2)) #sets another color for odd numbers in the node name


"""DISPLAY FLAG"""

import hou

context = hou.node("/obj")

sel = hou.selectedNodes()

for i in sel:
    if i.isDisplayFlagSet()==1:
        print(i.name()+" is visible")
    else:
        print(i.name()+ " is not visible")
        i.destroy() #used to delete a node

"""LOD Mapping"""    
import hou
context = hou.node("/obj") #define the context

ex1 = context.node("subnet1") 

childNodes = ex1.allSubChildren() #returns a list of direct children in the context

for i in childNodes:
    nodeType = i.type().description()
    if nodeType == "Geometry": #check if node is Geo
        try:
            midfile = i.node("file1") #stores the file1
            midfilepath = midfile.parm("file").eval() #query the parameter
            midfilepath = midfilepath.split("/") #split the path
            index  = midfilepath.index("midpoly") #find the index
            midfilepath[index] = "highpoly" #replace the item
            highfilepath = ("/").join(midfilepath) #join it and store it again 
            highfile = i.createNode("file","file2") #create a new node called file2
            highfile.parm("file").set(highfilepath) #set the filepath
            highfile.moveToGoodPosition()#translare 2D position of node
            
            #Setting Flags
            midfile.setDisplayFlag(1)
            highfile.setRenderFlag(1)

            
        except AttributeError: #excepting an error if no File node in geo
            print("no file1")
            pass



"""NODE CONNECTIONS"""

import hou

class ASSETIMPORT():
    def __init__(self):
        pass


    def importFiles(self):

        context = hou.node("/obj") #define context

        geometry = context.createNode("geo","MYASSETS") #declare a geo
 
        mydir = hou.ui.selectFile(title = "Select your file", multiple_select = 1 ) #let user pick the files

        mydir = mydir.split(" ; ") #splitting the long string

        merge = geometry.createNode("merge","MERGE_ALL") #creating a mergeNode

        count = 0
        for assetpath in mydir: #iterating through each assets

            #Extracting the name
            fileName = assetpath.split("/") #splitting the path
            fileName = fileName[-1].split(".")[0] # eg : we split box.obj into box and obj 
        
            #CREATING
            fileNode = geometry.createNode("file",fileName) #create file node
            mat = geometry.createNode("material","mat_"+fileName) #create material
            pack = geometry.createNode("pack","pack_"+fileName) #create pack node

            #SETTING INPUTS
            mat.setInput(0,fileNode) 
            pack.setInput(0,mat)
            merge.setInput(count,pack)  #adding each pack node to the merge Input
            
            #SETTING PARAMETERS
            fileNode.parm("file").set(assetpath)
            pack.parm("pivot").set("origin") #setting pack node parameter
            
            count+=1

        #Layingout
        geometry.layoutChildren()

obj1 = ASSETIMPORT()
obj1.importFiles()


