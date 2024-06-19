import hou
from PySide2.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QHBoxLayout

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
        self.setWindowTitle("Geometries") # set window title

        # Create a central widget and set a layout
        central_widget = QWidget() # create a base class for all UI Objects
        main_layout = QVBoxLayout() # layout child widgets vertically
        h_layout = QHBoxLayout() # layout child widgets horizontally
        v_layout = QVBoxLayout() #vertical layout for second column
        h_layout2 = QHBoxLayout() #horizontal layout for labels on top

        # Create some widgets
        self.label = QLabel("The List of Geometries and selected Node's children are: \n")
        self.button = QPushButton("Okay") 
        self.list_widget1 = QListWidget()
        self.list_widget2 = QListWidget()
        self.label2 = QLabel("Selected Node:")
        self.label3 = QLabel("None")

        # Add items to the list widgets
        items1 = self.listOfGeos()
        self.list_widget1.addItems(items1)

        #default item for list2
        self.list_widget2.addItems(["Nothing is selected"])
        
        #connect item selection of list1 with function 
        self.list_widget1.itemClicked.connect(self.listOfSelect) #mouseclick
        self.list_widget1.itemActivated.connect(self.listOfSelect) #keyboard enter
        
        #Connect the button's click signal to a method
        self.button.clicked.connect(self.close_window)

        # Add widgets to the main horizontal layout
        h_layout.addWidget(self.list_widget1)
        #add layout to second colum
        h_layout.addLayout(v_layout)
        
        #add layout for top labels
        v_layout.addLayout(h_layout2)
        
        #add widgets to inner label layout
        h_layout2.addWidget(self.label2)
        h_layout2.addWidget(self.label3)
        
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
        self.context = hou.node("/obj")
        allNodes = self.context.children() # store the child nodes
        geos = [] # empty list for storing geometry
        for node in allNodes:
            type = node.type().description() # check the type
            if type == "Geometry": # condition for geo
                geos.append(node) # add the node in list
        geoNames = []
        for geo in geos:
            geoNames.append(geo.name())
        return geoNames
    
    def listOfSelect(self,item):
        """
        This function returns a list of all the nodes inside the selected nodes.
        """
        sel =self.context.node(item.text()) #get the text from item and store the respective node
        childNodes = sel.children() #store child nodes
        self.label3.setText(item.text())#change the label
        if not childNodes:
                self.list_widget2.clear() 
                self.list_widget2.addItems(["Node is Empty"])
        else:        
            nodeNames = []
            for node in childNodes:
                nodeNames.append(node.name())
            self.list_widget2.clear() 
            self.list_widget2.addItems(nodeNames)

window = GeoNames() # object creation
window.show() # show the window
