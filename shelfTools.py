"""Store .py file to Run"""
#SET SHORTCUT TO Alt+Ctrl+N

import hou

scriptPath = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/houdiniscripts"
# Store the file path using hou.ui.selectFile() and save it in Houdini's session


# Prompt user to select the file
selected_file = hou.ui.selectFile(start_directory=scriptPath,title="Select a Python Script")

# Check if a file was selected
if selected_file:
    # Store the selected file path in Houdini's session variable
    hou.session.external_script_path = selected_file
else:
    hou.ui.displayMessage("No file selected.")



"""Run the Code"""
#SET SHORTCUT TO Alt+Ctrl+M

# Retrieve the stored file path and execute the script

try:
    # Retrieve the stored file path from Houdini's session variable
    external_script_path = hou.session.external_script_path
    
    # Check if the path is not empty
    if external_script_path:
        # Open and execute the script
        with open(external_script_path, "r") as file:
            exec(file.read())
    else:
        hou.ui.displayMessage("No file path stored.")
except AttributeError:
    hou.ui.displayMessage("No file path stored. Please use the 'Store File Path' tool first.")



"""Export Node as Python Code"""

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




"""Load Node from Python Code"""
import os
import hou
current_path = "/usr/people/waranr/Desktop/test"

#user picks the file
file = hou.ui.selectFile(start_directory= current_path ,  title = "Load your file") #save the file path
openfile = hou.readFile(file) #opens the file 

#run the file
exec(openfile)
