import hou
import sys
import os

from PySide2 import QtCore,QtUiTools, QtWidgets


class testApp(QtWidgets.QWidget):
    def __init__(self):
        super(testApp,self).__init__() #inherit construction from QWidgets
        uiPath = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/QtUI/polyOperate.ui" #path of UI
        self.ui = QtUiTools.QUiLoader().load(uiPath,parentWidget = self) #store our UI
        self.setParent(hou.ui.mainQtWindow(),QtCore.Qt.Window) 
        self.setWindowTitle("Test App")
        
        #connect BUTTONS
        self.ui.btn_extrude.clicked.connect(lambda : self.createNode("polyextrude::2.0")) 
        self.ui.btn_bevel.clicked.connect(lambda : self.createNode("polybevel::3.0"))       
        self.ui.btn_cut.clicked.connect(lambda : self.createNode("polycut"))       
        self.ui.btn_fill.clicked.connect(lambda : self.createNode("polyfill")) 
        


    def createNode(self,nodeType):

        context = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd() #store the current working directory without any selection

        #finding the node with displayFlag
        for node in context.children(): #iterate through children
            if node.isDisplayFlagSet() == 1 : #check if display flag set
                myinput = node

        #create nodes and connect them
        mynode = context.createNode(nodeType) #create extrude
        mynode.setInput(0,myinput)#connect them

        #set flags
        mynode.setDisplayFlag(1) #set display flag
        mynode.setRenderFlag(1) #set render flag
        mynode.setGenericFlag(hou.nodeFlag.Current,1) #set selection
        mynode.setTemplateFlag(1) #set template flag

        #position the created node under our node
        nodePos = myinput.position() #save the position of the node
        newPos = (nodePos[0],nodePos[1]-1) #make a new (x,y) coordinate
        mynode.setPosition(newPos) #set the exture position under it



win = testApp()
win.show()
