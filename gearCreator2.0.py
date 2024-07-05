"""
Script Name: gearCreator2.0.py
Author: Ram Yogeshwaran
Company: The Mill
Contact: Ram.Yogeshwaran@themill.com
Description: This script generates a procedural Gear in Houdini.
"""

import hou

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow , QPushButton , QGridLayout, QWidget, QLabel,QSlider, QDoubleSpinBox , QSpinBox

class GearCreator(QMainWindow):
    """
    This is a Gear class that lets us create a gear and modify it , if required.
        
    Methods:
        __init__: Initializes the Gear class.
        buildUI: builds the widgets and layouts in the main window and displays it
        makeGear: creates a gear with the set values from the Widgets
        modifyGear: modifies the created gear's Height,length or teeths according to the values in the widgets
        teethsText : gets the value from the spinbox and assigns it to the teeths slider
    """

    def __init__(self):
        """Initializes the Gear class."""

        super(GearCreator,self).__init__() #initialize the parent class parameters
        self.setWindowTitle("Gear Creator")
        self.buildUI() #builds the UI

    def buildUI(self):
        """  This method builds the widgets and layouts in the main window and displays it"""

        #main widget
        central_widget = QWidget() #main widget
        self.setCentralWidget(central_widget) #set central widget

        #main layout
        central_layout = QGridLayout()
        central_widget.setLayout(central_layout)

        ###### MAKE GEAR ROW #######

        label1 = QLabel("Step 1: Make the Gear")
        makeBtn = QPushButton("Make Gear!")

        #add it to layout
        central_layout.addWidget(label1,0,0)
        central_layout.addWidget(makeBtn,0,1,1,3)

        #connections
        makeBtn.clicked.connect(self.makeGear)

        ###### TEETHS ROW #######
        label2 = QLabel("Step 2: Modify it to your liking")
        self.teethSlider = QSlider(QtCore.Qt.Horizontal) 
        self.teethSlider.setMinimum(5)
        self.teethSlider.setMaximum(100)

        self.teethInp = QSpinBox()
        self.teethInp.setMinimumWidth(100)

        teethsLabel = QLabel('Teeths')

        self.teethReset = QPushButton("Reset")

        #add it to layout
        central_layout.addWidget(label2,1,0)
        central_layout.addWidget(self.teethSlider,2,0)
        central_layout.addWidget(self.teethInp,2,1)
        central_layout.addWidget(teethsLabel,2,2)
        central_layout.addWidget(self.teethReset,2,3)

        #connections
        self.teethSlider.valueChanged.connect(self.modifyGear) #call the function
        self.teethSlider.valueChanged.connect(lambda val : self.teethInp.setValue(val)) #connect slider change and line edit

        self.teethInp.setValue(self.teethSlider.value())
        self.teethInp.editingFinished.connect(self.teethText)

        self.teethReset.clicked.connect(lambda :self.teethSlider.setValue(25))

        ###### LENGTH ROW #######
        
        self.lengthSBox = QDoubleSpinBox()
        self.lengthSBox.setMinimum(0.1)

        lengthLabel = QLabel('Length')

        self.lengthReset = QPushButton("Reset")

        #add it to layout
        central_layout.addWidget(self.lengthSBox,3,0,1,2)
        central_layout.addWidget(lengthLabel,3,2)
        central_layout.addWidget(self.lengthReset,3,3)

        #connections
        self.lengthSBox.valueChanged.connect(self.modifyGear) #call the function

        self.lengthReset.clicked.connect(lambda :self.lengthSBox.setValue(0.5))

        ###### HEIGHT ROW #######

        self.heightSBox = QDoubleSpinBox()

        self.heightSBox.setMinimum(0.1)

        heightLabel = QLabel('Height')

        self.heightReset = QPushButton("Reset")

        #add it to layout
        central_layout.addWidget(self.heightSBox,4,0,1,2)
        central_layout.addWidget(heightLabel,4,2)
        central_layout.addWidget(self.heightReset,4,3)

        #connections
        self.heightSBox.valueChanged.connect(self.modifyGear) #call the function

        self.heightReset.clicked.connect(lambda :self.heightSBox.setValue(1))

        ###### CLOSE ROW #######

        closeLabel = QLabel("Step 3: Disconnect and Save the Gear")
        closeBtn = QPushButton("Close!")

        #add it to layout
        central_layout.addWidget(closeLabel,5,0)
        central_layout.addWidget(closeBtn,5,1,1,3)

        #connections
        closeBtn.clicked.connect(self.close)

    def makeGear(self):

        """This method creates a gear with the set values from the Widgets"""
        
        try:
            #create nodes
            context = hou.node("/obj")
            gearContainer = context.createNode("geo","myGear")

            self.tube = gearContainer.createNode('tube')
            thickness = gearContainer.createNode('polyextrude::2.0')

            self.grpNode = gearContainer.createNode('groupcreate')
            self.extrude = gearContainer.createNode('polyextrude::2.0')


            #tube parameters
            self.tube.parm('type').set(1)
            self.tube.parm('radscale').set(0.5)

            self.height = self.tube.parm('height')
            self.height.set(self.heightSBox.value())
            
            self.columns = self.tube.parm('cols')
            self.columns.set(self.teethSlider.value()*2)


            #extrude parameters
            thickness.parm('dist').set(0.2)
            thickness.parm('outputback').set(1)

            #alternate faces parameters
            cols = self.columns.eval()
            facesString = "{0}-{1}:2".format(cols,cols*2-1)
            self.grpName = 'alternateFaces'
            self.grpNode.parm('groupname').set(self.grpName)
            self.grpNode.parm('basegroup').set(facesString)

            #extrude teeth parameters
            self.extrude.parm('group').set(self.grpName)
            self.extrude.parm('dist').set(self.lengthSBox.value())

            #connections
            thickness.setInput(0,self.tube)
            self.grpNode.setInput(0,thickness)
            self.extrude.setInput(0,self.grpNode)

            #set display flag
            self.extrude.setDisplayFlag(1)
            self.extrude.setRenderFlag(1)
            self.extrude.setTemplateFlag(1)


            #layout children
            gearContainer.layoutChildren()
        except :
            hou.ui.displayMessage("Unable to Make your Gear!")

    def modifyGear(self):

        """ This method modifies the created gear's Height,length or teeths according to the values in the widgets """

        teethVal = self.teethSlider.value() #store teeths from slider
        lengthVal = self.lengthSBox.value() #store length from sbox
        heightVal = self.heightSBox.value() #store height from sbox

        try:
            #modify teeths
            self.columns.set(teethVal*2) #update columns
            cols = self.columns.eval()
            facesString = "{0}-{1}:2".format(cols,cols*2-1)
            self.grpNode.parm('basegroup').set(facesString) #update alternatefaces

            #modify length
            self.extrude.parm('dist').set(lengthVal)

            #modify height
            self.height.set(heightVal)
        except AttributeError:
            pass
   
    def teethText(self):

        """This method gets the value from the spinbox and assigns it to the teeths slider"""

        # Check if the input is an integer
        text = self.teethInp.value()
        try:
            val = int(text)
            self.teethSlider.setValue(int(val))
        except ValueError:
            # If not an integer, reset
            self.teethReset.click()

obj = GearCreator()
obj.show()


"""
MIT License

Copyright (c) 2024 Ram Yogeshwaran

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
