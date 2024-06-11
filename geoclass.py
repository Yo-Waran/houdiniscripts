"""Reading a single point geometry"""

import hou

mysel = hou.selectedNodes()[0] #store the unpack node

geometry = mysel.geometry() #store the geometry 

mypoint = geometry.point(15) #store the point

print(str(mypoint.number()) + str(mypoint.position()))


"""Reading Multiple points"""

mysel = hou.selectedNodes()[0] #store the unpack node

geometry = mysel.geometry() #store the geometry 

mypoints = geometry.globPoints("15-20") #store the points

for point in mypoints:
    print(point.position())

"""Get attribute Values"""

import hou

mysel = hou.selectedNodes()[0] #store the unpack node

geometry = mysel.geometry() #store the geometry 


for point in geometry.points():
    attribute = point.globalAttribs()
    print(attribute)
  

"""Reference Current SOP Node"""

node = hou.pwd() #reference current node
geo = node.geometry() #store the geometry

myprim = geo.globPrims("20") #store the primitive

node.setName(myprim[0].attribValue("name")) #set the name with name attribute's value

"""Write Attribute value"""
node = hou.pwd()
geo = node.geometry()

for prim in geo.prims(): #iterating the primitives
    number = prim.number() #storing the primitive number
    prim.setAttribValue("name","test"+str(number))#  replace the name to something else
    


"""Adding an Attribute"""
node = hou.pwd()
geo = node.geometry()

geo.addAttrib(hou.attribType.Prim,"name","default") #adding an attribute with default values


for prim in geo.prims():
    number = prim.attribValue("name") 
    prim. ("name","test"+str(number))#populating the attribute with some value


"""Group Manipulation"""    
node = hou.pwd()
geo = node.geometry()

cd = (0,1,0) #create a colour 1 tuple
cd2 = (0,0,1) #create a colour 2 tuple
geo.addAttrib(hou.attribType.Point,"Cd",cd) #add colour attribute to the geo and set its colour to color 1
grp = geo.createPointGroup("mypointGroup") #create a point group


mypoints = geo.globPoints("0-1000") #add points 0-100 to a variable

for pt in mypoints:
    grp.add(pt) #appends the points to the group
    pt.setAttribValue("Cd",cd2) #changes the colour value of the point
    


"""Groups using Bounding Box"""

node = hou.pwd()
geo = node.geometry()

box = node.inputs()[1] #gets the second input of the sop node
bbox = box.geometry().boundingBox() #makes a bounding box of the box the geometry

cd = (0,1,0)
cd2 = (0,0,1)
geo.addAttrib(hou.attribType.Point,"Cd",cd)
grp = geo.createPointGroup("mypointGroup")



for pt in geo.points(): #iterates through all points
    pos = pt.position() #stores the position of the point
    included = bbox.contains(pos) #check if this point is inside the bouding box
    if included == 1: 
        grp.add(pt) #adds the point to the group if contained 
        pt.setAttribValue("Cd",cd2) #changes its colour as well
    
geo.deletePoints(grp.points()) #deletes the point inside the group that is contained inside the bounding box



