import hou
import sys
import os
import operator

from PySide2 import QtCore,QtUiTools, QtWidgets

OPERATIONS = {
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt

}

class testApp(QtWidgets.QWidget):
    def __init__(self):
        super(testApp,self).__init__() #inherit construction from QWidgets
        uiPath = "/jobs/tvcResources/bangComms/waranr/Scripts/Git_Repository/QtUI/conditionApply.ui" #path of UI
        self.ui = QtUiTools.QUiLoader().load(uiPath,parentWidget = self) #store our UI

         # Set layout for the parent widget again!
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)

        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)
        self.setWindowTitle("Conditions Apply")

        #CONNECT UI
        self.ui.cobx_operation.currentTextChanged.connect(self.updateUI) #when option changed
        self.ui.btn_execute.clicked.connect(self.execute) # when button pressed

    def execute(self):
        sel = hou.selectedNodes() #store selected

        if not sel:
            hou.ui.displayMessage("Select something!")
        
        input = self.ui.input_expr.text() #store the given expression
        if len(input.split(" ")) !=3: #check for the length of expression
            hou.ui.displayMessage("Expecting a space between parameters, operator and Value (Ex: tx < 0)")
        else:
            givenParm, givenOp, givenValue = input.split(" ") #split and store them
            #convert givenValue to float
            givenValue = float(givenValue)

            for node in sel: #iterate through selection
                val = node.parm(givenParm).eval() #store the value of the node
                compResult = self.compare(val,givenOp,givenValue) #run the compare function and store the result
                print(compResult)

    def compare(self, val, givenOp, givenValue):
        if givenOp in OPERATIONS:
            result = OPERATIONS[givenOp](val, givenValue)
        else:
            raise ValueError("Unsupported operator!")
        return result


    def updateUI(self):
        btn = self.ui.btn_execute #store execute button
        text = self.ui.cobx_operation.currentText() #store the text
        ask = self.ui.cbx_confirm #store the checkbox
        if text == "Hide":
            btn.setText("EXECUTE HIDE") #change text in button
            ask.hide() #hide the confirm check box
        if text == "Delete" :
            btn.setText("EXECUTE DELETE") #similar
            ask.show()  #show the confirm check box



win = testApp()
win.show()
