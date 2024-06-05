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




