import hou
import sys
import os

from PySide2 import QtCore,QtUiTools, QtWidgets


class testApp(QtWidgets.QWidget):
    def __init__(self):
        super(testApp,self).__init__()
        uiPath = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/QtUI/polyOperate.ui"
        self.ui = QtUiTools.QUiLoader().load(uiPath,parentWidget = self)
        self.setParent(hou.ui.mainQtWindow(),QtCore.Qt.Window)
        self.setWindowTitle("Test App")

win = testApp()
win.show()