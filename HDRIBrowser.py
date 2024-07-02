import contextlib
import hou
import sys
import os
from PySide2 import QtCore,QtUiTools, QtWidgets

def onCreateInterface():

    global widget
    global Qtable #table for items

    ui_file_path = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/QtUI/HDRIBrowser.ui"
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    widget = loader.load(ui_file)

    #initialize 
    Qtable = widget.table_hdri 

    #connecting Buttons
    widget.btn_browse.clicked.connect(explore)
    widget.btn_thumbnail.clicked.connect(generate)
    widget.btn_import.clicked.connect(importHDRI)
    widget.input_path.textChanged.connect(update_UI)
    
    return widget


def explore():

    inp_path = widget.input_path.text() #get the text from input
    if not inp_path:
        inp_path = "/jobs/tvcResources/bangComms/waranr/Downloads_Server/HDRI" #default directory
    browse_path = hou.ui._selectFile(start_directory = inp_path ,title = "Choose a folder containing the HDRIs", file_type = hou.fileType.Directory) #save the directory

    widget.input_path.setText(browse_path) #update the lineedit Text

def update_UI():

    path = widget.input_path.text() #path from the field
    data = os.listdir(path)  #list the items
    hdrList = [] #list for HDRIs
    for f in data:
        if f.endswith(".exr"):
            hdrList.append(f)
    
    amount = len(hdrList) 
    column = 3
    row = (amount+column-1)//column  #logic that rounds UP the division to an integer 
    Qtable.setRowCount(row) #set row
    Qtable.setColumnCount(column) #set column
    
    count = 0
    for x in hdrList:#iterate through the list of hdrs

        #logic for determing columns and rows
        xrow= int(count/column) #divide and round for rows
        xcol = count % column  #remaining of division for columns

        item = QtWidgets.QTableWidgetItem(x) #empty item node

        Qtable.setItem(xrow,xcol,item) #setting the item to our table

        count+=1 #increment

        header = Qtable.horizontalHeader() #store the header
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #stretch the header based on contents

def generate():

    print("generating Thumbnails")

def importHDRI():
    context = hou.node("/obj") #store the context
    sel = Qtable.selectedItems() #store the selected item from QTable
            
    for item in sel:
        envlight = context.createNode("envlight",item.text())
        envlight.parm("env_map").set(item.text())