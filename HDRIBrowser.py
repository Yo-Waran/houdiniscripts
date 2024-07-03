
import hou
import sys
import os
from PySide2 import QtCore,QtUiTools, QtWidgets , QtGui

from PIL import Image

def onCreateInterface():

    global widget
    global Qtable #table for items

    #new elements
    global slider
    global percent
    global sbox

    ui_file_path = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/QtUI/HDRIBrowser.ui"
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    widget = loader.load(ui_file)

    #initialize 
    Qtable = widget.table_hdri 
    slider = widget.sld_zoom #save the slider
    percent = widget.percent #save the percent
    percent.setText(str(slider.value())+ "%")
    sbox = widget.sbox_columns #save the spinbox

    #connecting widgets
    widget.btn_browse.clicked.connect(explore)
    widget.btn_thumbnail.clicked.connect(generate)
    widget.btn_import.clicked.connect(importHDRI)
    widget.input_path.textChanged.connect(update_UI)

    #new elements
    sbox.valueChanged.connect(update_UI)
    slider.valueChanged.connect(update_UI)
    
    #more tweaks
    Qtable.setShowGrid(0) #disable grid
    Qtable.setCornerButtonEnabled(0) #disable corner


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
    slidVal = slider.value() * 0.01 #store the value of slider
    maxColumn = sbox.value() #store the value of maximum columns
    percent.setText(str(slider.value())+ "%")

    #extract hdr images from dir
    hdrList = [] #list for HDRIs
    jpgList = [] #list of Jpeg thumbnails
    for f in data:
        if f.endswith(".exr"):
            hdrList.append(f)
        if f.endswith("jpeg"):
            jpgList.append(f)
    
    amount = len(hdrList) 
    column = maxColumn
    row = (amount+column-1)//column  #logic that rounds UP the division to an integer 
    Qtable.setRowCount(row) #set row
    Qtable.setColumnCount(column) #set column
    
    count = 0
    for x in hdrList:#iterate through the list of hdrs
        file_path = path + "/" + x #store the file path

        #logic for determing columns and rows
        xrow= int(count/column) #divide and round for rows
        xcol = count % column  #remaining of division for columns

        item = QtWidgets.QTableWidgetItem() #empty item node
        item.setData(QtCore.Qt.UserRole, file_path) #set some data to the node
        Qtable.setItem(xrow,xcol,item) #setting the item to our table

        count+=1 #increment

        jpgname = x.split(".")[0]+"_thumb.jpeg"
        if jpgname in jpgList:
            jpgpath = path +"/"+jpgname #full path of jpeg file
            icon = QtGui.QIcon(jpgpath) #make a new icon with the jpeh
            item.setIcon(icon) #set the icon to them

            #set icon resolution
            img  = Image.open(jpgpath)

            sizex , sizey = img.size[0]*slidVal,img.size[1]*slidVal
            size = QtCore.QSize(sizex,sizey)
            Qtable.setIconSize(size)
        else:
            item.setText(x)

        #header attributes    
        header = Qtable.horizontalHeader() #store the header
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  #stretch it full
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents) #stretch the header based on contents 
        vheader = Qtable.verticalHeader() #store the header
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  #stretch it full
        vheader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        

def generate():
    path = widget.input_path.text() #path from the field
    data = os.listdir(path)  #list the items
    hdrList = [] #list for HDRIs
    for f in data:
        if f.endswith(".exr"):
            jpg = f.split(".")[0]+"_thumb.jpeg"
            if jpg in data:
                print("skipping thumbnail Generation")
                continue #skips if jpeg exists already
            else: #else stores the hdr path
                file_path = path + "/" + f #store the file path
                hdrList.append(file_path)
    for h in hdrList: #iterate hdr list
        converter(h)
    update_UI()

def converter(hdrpath):

    try:
        #create nodes for conversions
        context = hou.node("/img") 
        img = context.createNode("img")
        file = img.createNode("file")
        rop = img.createNode("rop_comp")
        rop.setInput(0,file)
        img.layoutChildren() #layout

        #set image parameters
        file.parm("filename1").set(hdrpath) #set file name
        file.parm("overridesize").set("quarter") #set size of image to 1/8th

        #set rop parameters
        path = widget.input_path.text() #path from the field
        newname,ext = os.path.splitext(hdrpath) #spli extension
        new_path = newname+"_thumb.jpeg" #add new extension and suffix
        rop.parm("copoutput").set(new_path) #set parameter
        rop.parm("trange").set("off") #set range for render
        rop.parm("execute").pressButton()  #press the button


        #delete node
        img.destroy()
    except:
        pass

def importHDRI():
    context = hou.node("/obj") #store the context
    sel = Qtable.selectedItems() #store the selected item from QTable
            
    for item in sel:
        fullpath = item.data(QtCore.Qt.UserRole)

        splitname = fullpath.split("/")[-1].split(".")[0]

        nodename = "".join(c for c in splitname if c.isalnum()) #replace special characters with '_'

        envlight = context.createNode("envlight","lgt_"+nodename) #create the light
        envlight.parm("env_map").set(fullpath) #set the file name 
    context.layoutChildren() #layout