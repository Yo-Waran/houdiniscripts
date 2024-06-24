import hou
import toolutils

#Load the file
file_path = "/usr/people/waranr/Desktop/test/geo1.py" #file path
openfile = hou.readFile(file_path) #open file 
exec(openfile) #execute the file


#store the nodes
selected_node = hou.selectedNodes()[0] #save selected node
name_node = selected_node.name() #save the name of the node
tt_node = hou.node("/obj/geo1") #save the imported node
context = selected_node.parent() #save the context

#subnetize model and imported file
subnet = context.collapseIntoSubnet((selected_node,tt_node),"Turntable_"+ name_node) #store the subnet


tt_node = hou.node(subnet.path()+"/geo1") #store tt_node again
selected_node = hou.node(subnet.path()+"/"+name_node)  #store selected geo again
  
#set transform for the imported geo
myTTpos = (-0.045,0.035,-0.2)
myTTscale = 0.01
myTTrot = -90
tt_node.parmTuple("t").set(myTTpos)
tt_node.parm("scale").set(myTTscale)
tt_node.parm("ry").set(myTTrot)

#create cam

cam = subnet.createNode("cam","TT_cam_"+name_node)
tt_node.setInput(0,cam) #set inputs


#look through the camera
viewer = toolutils.sceneViewer().curViewport() #store viewport
viewer.lockCameraToView(True) #lock cam
selected_node.setSelected(1,clear_all_selected = True) #set selection
viewer.frameSelected() #frame


viewer.saveViewToCamera(cam) #save the cam pos
viewer.setCamera(cam) #change the current cam

cam.parm("focal").set(50)
cam.parm("aperture").set(41)
#zvalue = cam.parm("tz").eval()

tupleVal = cam.parmTuple("t").eval()
tx,ty,tz = tupleVal

#cam.parmTuple("t").set((tx,ty,tz))
 
subnet.layoutChildren() #clean node pos