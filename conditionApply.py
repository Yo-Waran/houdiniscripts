import hou
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

        #empty node
        self.falseNodes = None
        #CONNECT UI
        self.ui.cobx_operation.currentTextChanged.connect(self.updateUI) #when option changed
        self.ui.btn_execute.clicked.connect(self.execute) # when button pressed
        self.ui.btn_undo.clicked.connect(self.undo)

    def execute(self):

        sel = hou.selectedNodes() #store selected

        if not sel:
            hou.ui.displayMessage("Select something!")
            raise ValueError("Nothing selected")
        
        input = self.ui.input_expr.text() #store the given expression
        if len(input.split(" ")) !=3: #check for the length of expression
            hou.ui.displayMessage("Expecting a space between parameters, operator and Value (Ex: tx < 0)")

        else:
            givenParm, givenOp, givenValue = input.split(" ") #split and store them
            #convert givenValue to float
            givenValue = float(givenValue)

            self.falseNodes = [] #for collecting unmatching nodes

            for node in sel: #iterate through selection
                val = node.parm(givenParm).eval() #store the value of the node
                compResult = self.compare(val,givenOp,givenValue) #run the compare function and store the result
                if not compResult: #if result is false
                    self.falseNodes.append(node) #append it
            
            operation = self.ui.cobx_operation.currentText() #store the operation in comboBox


            falseNodeNames = [node.name() for node in self.falseNodes] #store the names only
            falseNodeNames = "\n".join(falseNodeNames) #convert to string

            if operation == "Hide":
                for node in self.falseNodes:#iterate falseNodes
                    node.setGenericFlag(hou.nodeFlag.Display,0)

            if operation == "Delete" :
                ask = self.ui.cbx_confirm.isChecked() #store the checkbox check
                if ask: #if checked
                    confirmation = hou.ui.displayMessage("You're about to delete the following nodes! \n"+ falseNodeNames,buttons = ["Okay","Cancel"]) #display the warning
                    if confirmation == 0: #first button clicked
                        delete = 1 #store the boolean
                    else:
                        delete = 0
                if ask == 0: #no checked
                    delete = 1 
                
                if delete:
                    for node in self.falseNodes:
                        node.destroy()


                

    def compare(self, val, givenOp, givenValue):

        if givenOp in OPERATIONS:
            result = OPERATIONS[givenOp](val, givenValue)
        else:
            hou.ui.displayMessage("Unsupported operator!")
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
    
    def undo(self):
        if not self.falseNodes:
            hou.ui.displayMessage("Nothing to Undo")
            raise ValueError("Perform some operation to Undo")
        for node in self.falseNodes: #iterate through all false nodes
            hou.undos.performUndo() #undo

        for node in self.falseNodes: #iterate again
            node.setSelected(1,0)#set selection


win = testApp()
win.show()
