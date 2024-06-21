import hou
from PySide2.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QHBoxLayout,QLineEdit

#declare global dict for suffixes
SUFFIXES = {
    "Sphere" : "SPR",
    "Transform" : "TRM",
    "Null" : "NL",
    "Box" : "BX",
    "Scatter" : "SCT",
    "Grid" : "GRD"
}

#class definition
class GeoNames(QMainWindow):
    """
    This is a Geo Names class that prints only the Geometry nodes in our Houdini Scene

    Methods:
        __init__: Initializes GeoNames class and creates the QTWindow
        close_window : function to close the Main window
        listOfGeos: function that returns only the list of geometries
        listOfSelect: function that returns the child nodes present in the selected item
    """

    def __init__(self):
        super(GeoNames, self).__init__() # retain parent class parameters
        self.setWindowTitle("Geometries Renamer") # set window title
        self.childNodes = None #default child
        self.present_path = ""
        self.setStyleSheet("background-color: rgba(50,50,50,100)") #add color to it

        # Create a central widget and set a layout
        central_widget = QWidget() # create a base class for all UI Objects
        main_layout = QVBoxLayout() # layout child widgets vertically
        h_layout = QHBoxLayout() # layout child widgets horizontally
        v_layout = QVBoxLayout() #vertical layout for second column
        h_layout2 = QHBoxLayout() #horizontal layout for labels on top
        h_layout3 = QHBoxLayout()#horizontal layout for text field and button

        # Create some widgets
        self.label = QLabel("Current Context: " + self.present_path)
        self.button = QPushButton("Save Changes and Exit") 
        self.list_widget1 = QListWidget()
        self.list_widget2 = QListWidget()
        self.label2 = QLabel("Selected Node:")
        self.selectedNode = QLabel("None")
        self.textField = QLineEdit()
        self.renameButton = QPushButton()

        #WIDGET FUNCTIONS
        
        #Syle the label
        self.label.setStyleSheet("""
            color: Black;
            font-size: 15px;
            background-color: darkgrey;
            border: 10px solid grey;
            padding: 10px;
        """)


        #textfield
        self.textField.setPlaceholderText("Rename Child Nodes (Suffix added Automatically)")

        #renamebutton
        self.renametext1 = "Set All" #rename variable
        self. renametext2 = "Set Selected" #rename variable 2
        self.renameButton.clicked.connect(self.renamer)

        # Add items to the list widgets
        items1 = self.listOfGeos()
        #self.list_widget1.addItem("Present Directory:" + self.present_path)
        self.list_widget1.addItems(items1)

        #default item for list2
        self.list_widget2.addItems(["Nothing is selected"])
        self.list_widget2.setSelectionMode(QListWidget.MultiSelection) #enable Multi selection
        self.on_selection() #run it on start
        self.list_widget2.itemSelectionChanged.connect(self.on_selection) #change button name based on selection

        
        
        #connect item selection of list1 with function 
        self.list_widget1.itemClicked.connect(self.listOfSelect) #mouseclick
        self.list_widget1.itemActivated.connect(self.listOfSelect) #keyboard enter
        
        #Connect the button's click signal to a method
        self.button.clicked.connect(self.close_window)

        #LAYOUTS

        #Add text field and rename button to layout
        h_layout3.addWidget(self.textField)
        h_layout3.addWidget(self.renameButton)

        # Add widgets to the main horizontal layout
        h_layout.addWidget(self.list_widget1)
        #add layout to second colum
        h_layout.addLayout(v_layout)
        
        #add layout for top labels
        v_layout.addLayout(h_layout2)
        
        #add widgets to inner label layout
        h_layout2.addWidget(self.label2)
        h_layout2.addWidget(self.selectedNode)

        #add one more layout to top
        v_layout.addLayout(h_layout3)
        
        #add widget to second column
        v_layout.addWidget(self.list_widget2)

        # Add widgets to the main vertical layout
        main_layout.addWidget(self.label)
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.button)

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)

        # Set the central widget to the main window
        self.setCentralWidget(central_widget)

    def close_window(self):
        self.close() # function that closes the Main Window
        
    def listOfGeos(self):
        """
        This function returns a list of all the Geometries in the /obj context in the Houdini Scene.
        """
        editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor) #store the Network editor
        self.present_path = editor.pwd().path() #store the path of the current directory open in the Editor
        self.context = hou.node(self.present_path) # get the node of that path
        self.label.setText("Current Context: " + self.present_path)

        allNodes = self.context.children() # store the child nodes
        geos = [] # empty list for storing geometry
        for node in allNodes:
            type = node.type().description() # check the type
            if type == "Geometry": # condition for geo
                geos.append(node) # add the node in list
        geoNames = []
        for geo in geos:
            geoNames.append(geo.name())
        if not geoNames:
            geoNames.append("No Geo Nodes in the current Context ")            
        return geoNames
    
    def listOfSelect(self,item):
        """
        This function returns a list of all the nodes inside the selected nodes.
        """
        sel =self.context.node(item.text()) #get the text from item and store the respective node
        try:
            self.childNodes = sel.children() #store child nodes
            self.selectedNode.setText(item.text())#change the label
            if not self.childNodes:
                    self.list_widget2.clear() 
                    self.list_widget2.addItems(["Node is Empty"])
            else:        
                nodeNames = []
                for node in self.childNodes:
                    nodeNames.append(node.name())
                self.list_widget2.clear() 
                self.list_widget2.addItems(nodeNames)
        except AttributeError:
            self.list_widget2.clear()
            self.list_widget2.addItems(["Empty Context"])
    
    def renamer(self):
        """
        This function renames the child node's based on the 
        """
        name = self.textField.text() #set the string to text field's text
        if not name:
            name = self.selectedNode.text() #default string value is selected Node
        
        self.selectedItems = self.list_widget2.selectedItems() #store the selected Items
        self.selectedTexts = [item.text() for item in self.selectedItems] #store the text from items

        if self.childNodes: #error out early

            self.selectedChildNodes = [] #empty list
            for node in self.childNodes: #iterate through all children
                for item in self.selectedTexts: #iterate through each selection
                    if item == node.name(): #if matches
                        self.selectedChildNodes.append(node) #append it to the list

            if not self.selectedChildNodes:
                self.selectedChildNodes = self.childNodes #select all if nothing selected

            for node in self.selectedChildNodes: #iterate child nodes
                type = node.type().description() #store the type
                suffix  = SUFFIXES.get(type,"UNKNOWN") #match type with defintion
                newname = name+"_"+suffix #new name 
                node.setName(newname) #rename the nodes
            self.listOfSelect(self.selectedNode) #refresh the list again  
        else:
            print("Skipping renamer")
            return None           
    
    def on_selection(self):
        if len(self.list_widget2.selectedItems())<1:
            self.renameButton.setText(self.renametext1)
        else:
            self.renameButton.setText(self.renametext2)            
            
window = GeoNames() # object creation
window.show() # show the window


