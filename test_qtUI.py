import hou
import sys
import os

from PySide2 import QtCore,QtUiTools, QtWidgets


class testApp(QtWidgets.QWidget):
    def __init__(self):
        super(testApp,self).__init__()
        uiPath = "/Users/ramyogeshwaran/Documents/Yogi/GitHub Repo/QtUi/test.ui"
        self.ui = QtUiTools.QUiLoader().load(uiPath,parentWidget = self)
        self.setParent(hou.ui.mainQtWindow(),QtCore.Qt.Window)
        self.setWindowTitle("Test App")

         #externally set a layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        #initialize
        self.percent = self.ui.lb_percent
        value = str(self.ui.sld_slider.value()) + " %"
        self.percent.setText(value)

        self.ui.button.setText("Click Me!")
        
        #connections
        self.ui.sld_slider.valueChanged.connect(self.updateUI)

    def updateUI(self):
        value = str(self.ui.sld_slider.value()) + " %"
        self.percent.setText(value)

win = testApp()
win.show()

