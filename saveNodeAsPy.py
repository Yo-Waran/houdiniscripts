"""Saving any node as a Python code"""
import os #operating system for environ
import hou

#store what to save
sel = hou.selectedNodes()[0] #store the selected node
code = sel.asCode(brief=0,recurse=1) #converts the node into a code

#set file name
UI = hou.ui.readInput(initial_contents = sel.name(),message = "Set the name of the file", buttons = ["save","cancel"],title = "Script Name")#name of the script
scriptname = UI[1]
if UI[0]==0: #if save button is clicked
    #set file path to houdini preferences
    path = os.environ #dictionary of all paths used by Houdini
    pref = path.get("HOUDINI_USER_PREF_DIR") #get the prefs path (use this for default directory if you want)
    
    custom_path = "/usr/people/waranr/Desktop/test/"
    file_path = custom_path + scriptname + ".py" #new full path

    #write the file
    file = open(file_path,"w")
    file.write(code)
    file.close()
else:
    pass

"""Loading files into the scene"""

import os
import hou
current_path = "/usr/people/waranr/Desktop/test"

#user picks the file
file = hou.ui.selectFile(start_directory= current_path ,  title = "Load your file") #save the file path
openfile = hou.readFile(file) #opens the file 

#run the file
exec(openfile) #executes the file



"""Camera and Scene Viewer"""

import toolutils

cam = hou.node("/obj/cam1") #cam path

frameBox = hou.selectedNodes()[0]#save the node to frame the camera on

#SAVE CAM Parameters
focal = cam.parm("focal").eval()
aperture = cam.parm("aperture").eval()

viewer = toolutils.sceneViewer().curViewport() #store current viewport
viewer.lockCameraToView(True)#lock camera

viewer.frameSelected() #frame viewport
viewer.saveViewToCamera(cam) #save translation to cam

#Reapply CAM Parameters
cam.parm("focal").set(focal)
cam.parm("aperture").set(aperture )

#set camera
viewer.setCamera(cam) #set current camera to the stored cam 