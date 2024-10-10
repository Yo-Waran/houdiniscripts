import hou

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


##########################################################################

#To load UI in a python pane tab you use the following code

########################################################################
# Replace the sample code below with your own to create a
# PyQt5 or PySide2 interface.  Your code must define an
# onCreateInterface() function that returns the root widget of
# your interface.
########################################################################

import hou

from PySide2 import QtCore,QtUiTools, QtWidgets

def onCreateInterface():
    global widget
    ui_file_path = "<pathOfUI>"
    loader = QtUiTools.QUiLoader()
    ui_file = QtCore.QFile(ui_file_path)
    ui_file.open(QtCore.QFile.ReadOnly)
    widget = loader.load(ui_file)
    return widget
