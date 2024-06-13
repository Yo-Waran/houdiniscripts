"""HDA Button"""

def button():
    print("My Button is clicked")
#use hou.phm().button() as a callback script in a button    


"""Event Handlers"""
import hou
#on Created
current_node = hou.pwd() #store current node
print(current_node)

#On Created
current_node = kwargs["node"]  #stores the correct value for current node's name
print(current_node)

#change color on Creation
current_node = kwargs["node"]
current_node.setColor(hou.Color(1,0,0)) #set the current color

#ON NAME CHANGE
current_node = kwargs["node"]
current_node.setColor(hou.Color(0,0,1)) #set the current color


#ON INPUT CHANGES

current_node = kwargs["node"] #store the node key
index = kwargs["input_index"] #store the number of the input
my_input = current_node.inputs()[index] #store the input node 
new_name = current_node.name() + "_input_" + str(index) + "_" + my_input.name() #store a new name
my_input.setName(new_name) #rename the node


"""Modules Practice"""
def ratio():
    node = hou.pwd() #store current node
    scale = node.parm("sphere1_scale").eval() #store the scale value
    node.parm("sphere1_rows").set(int(scale)*10) #set the rows according to scale
    node.parm("polyextrude1_dist").set(int(scale)*0.2) #set the distance according to scale as well


"""SuperObjectMerger"""
#Python Module for Import Button in a HDA
def importObj():
    node = hou.pwd() #store current node
    multiparm = node.parm("numObj")
    selectedObj=hou.ui.selectNode(title = "Add Objects", multiple_select = 1,node_type_filter = hou.nodeTypeFilter.Obj)#select the nodes
    if selectedObj == None:
        pass
    else:    
        for obj in selectedObj:
            num = multiparm.evalAsInt() #store the value in the multiparm as Int
            multiparm.insertMultiParmInstance(num) #add objects in multiparm
            node.parm("objpath"+str(num+1)).set(obj) #set the parameter value of each object with their respective object path
            