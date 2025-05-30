"""
Script Name: shaderCreatorHoudini.py
Author: Ram Yogeshwaran
Company: The Mill
Contact: Ram.Yogeshwaran@themill.com
Description: This script is used to create Arnold/MaterialX shaders in Houdini
"""

import os
import hou
from PySide2 import QtCore, QtUiTools, QtWidgets,QtGui

#Define Global Suffixes for various texture types

SUFFIXES = {
    '_DIF': 'base_color_path',
    '_RGH': 'roughness_path',
    '_NRM': 'normal_path',
    '_DSP': 'displacement_path',
    '_MTL': 'metalness_path'
}

VP2SUFFIX = {
    'VP2' : 'vp2_path'
}

def get_parent_window():
    parent = hou.qt.mainWindow()
    return parent

class ShaderCreatorHoudiniWindow(QtWidgets.QDialog):

    """
    This is a ShaderCreatorHoudiniWindow class that lets us create the UI for this tool 
    
    Methods:
        __init__: Initializes the ShaderCreatorHoudiniWindow class and connections to certain widget
        buildUI: builds additional UI for the Shader Creator Window
        materialXCreation: This function determines whether or not MaterialX nodes will be created during creation
        autoConvertTextures: This function creates an arnold rop and toggles the auto generate tx textures to be on
        useExistingTextures: This function creates an arnold rop and toggles the use existing tx textures to be on
        clickAllButtons: This function creates all the shader for the shader widgets
        browseFolder: This function creates a dialog for the user to choose their texture folder
        findPrefixes: This function finds the releavant prefixes and populates the shader widgets accordingly
        populate: This function populates the Arnold shaderWidget instances on the scroll area
        clearWidgets: This Function clears all the shader widgets in the scroll area

    """
    
    def __init__(self,parent=get_parent_window()):
        """
        This is the Constructor function to initialize all the necessary variables ,dict and also connections
        
        Args:
            None
        Returns:
            None
        """

        super(ShaderCreatorHoudiniWindow, self).__init__(parent)
        uiPath ="QtUi/masterUIShaderCreator.ui"
        self.mainWindow = QtUiTools.QUiLoader().load(uiPath,parentWidget = self)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.mainWindow)
        self.setWindowTitle("Houdini Shader Creator")
        self.setLayout(self.layout)

        #properties
        self.mainWindow.VP2Widget.setVisible(False)
        self.mainWindow.VP2Widget.destroy(True)
        self.mainWindow.standardSurfaceWidget.setVisible(False)
        self.mainWindow.standardSurfaceWidget.destroy(True)

        #connections
        self.mainWindow.btn_browse.clicked.connect(self.browseFolder)
        self.mainWindow.input_folderPath.textChanged.connect(self.findPrefixes)

        # Set size policies for main window
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.adjustSize()
        self.setMaximumWidth(695)

        #run initial functions
        self.buildUI()
        self.findPrefixes() #default run it
        
    def buildUI(self):
        """
        This function builds additional UI for the Shader Creator Window
        
        Args:
            None
        Returns:
            None
        """

        #scroll widget to scroll through lights created
        scrollWidget = QtWidgets.QWidget() #new empty widget
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum) #doesnt stretch the scroll area
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget) #add vertical layout to it
        self.scrollLayout.setStretch(0,1)

        self.scrollArea = QtWidgets.QScrollArea() #add a scroll area
        self.scrollArea.setWidgetResizable(True) #make it resizable
        self.scrollArea.setWidget(scrollWidget) #add the scrollwidget inside the scroll area
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # Set the width of the scroll area to match the content's width

        #buttons
        btn_createAllShaders = QtWidgets.QPushButton("Create  All Shaders")
        btn_createAllShaders.setToolTip("Create all the shaders listed above ") 
        btn_createAllShaders.setMinimumHeight(70)
        custom_font = QtGui.QFont()
        custom_font.setBold(True)
        custom_font.setPointSize(15)  # Set to your desired size
        btn_createAllShaders.setFont(custom_font)

        #bold font
        bold_font = QtGui.QFont()
        bold_font.setBold(True)

        #checkboxes
        cbox_layout = QtWidgets.QHBoxLayout()
        cbox_autoConvertTextures = QtWidgets.QCheckBox("Auto Convert Textures to TX")
        cbox_useExistingTextures = QtWidgets.QCheckBox("Use Existing TX Textures")
        cbox_generateMaterialX = QtWidgets.QCheckBox("Generate MaterialX Shaders")
        cbox_generateMaterialX.setFont(bold_font)

        #get the houdini version and disable for versions other than 20
        houdini_version = hou.applicationVersion() #returns a tuple of the version number ex:(20,0,0)
        if houdini_version[0] < 20:
            cbox_generateMaterialX.setEnabled(False)#disable the cbox
            cbox_generateMaterialX.setToolTip("(Requires Houdini version 20 or Higher)") #set tooltip

        #progress bar
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setFont(bold_font)
        self.progressBar.setStyleSheet("QProgressBar {border: 0px;} QProgressBar::chunk {background-color: rgb(0, 150, 200); color: rgb(0,0,0)};")

        #add to layouts
        cbox_layout.addWidget(cbox_autoConvertTextures)
        cbox_layout.addWidget(cbox_useExistingTextures)
        cbox_layout.addWidget(cbox_generateMaterialX)
        self.mainWindow.main_layout.addLayout(cbox_layout,1,0)
        self.mainWindow.main_layout.addWidget(self.scrollArea,2,0) #1 = second row, 0 = 1st column, 1=  size of row , 2 = size of columns
        self.layout.addWidget(btn_createAllShaders)
        self.layout.addWidget(self.progressBar)

        #connections
        btn_createAllShaders.clicked.connect(self.clickAllButtons)
        cbox_autoConvertTextures.toggled.connect(lambda val : self.autoConvertTextures(val))
        cbox_useExistingTextures.toggled.connect(lambda val: self.useExistingTextures(val))
        cbox_generateMaterialX.toggled.connect(lambda val: self.materialXCreation(val))

        #default materialXCreation
        self.isMtlx = False

        #progressbar value
        self.progressBar.setValue(0)

    def materialXCreation(self,val):
        """
        This function determines whether or not MaterialX nodes will be created during creation.

        Args:
            val: Boolean to determine checkbox state
        Returns:
            None
        """
        self.isMtlx = val
        if self.isMtlx :
            #clear and reset the UI
            self.clearWidgets()
            self.findPrefixes()

            print("MaterialX Shaders will be created")
        else:
            #clear and reset the UI
            self.clearWidgets()
            self.findPrefixes()
            print("Arnold Shaders will be created")
    
    def autoConvertTextures(self,val):
        """
        This function creates an arnold rop and toggles the auto generate tx textures to be on

        Args:
            val: Boolean to determine checkbox state
        Returns:
            None
        """
        context = hou.node("/out") #defin context

        noRop = True #boolean to check node existence
        for node in context.children(): #check the types
            if node.type().name() == "arnold": #if arnold exists
                noRop = False #set the boolean to False
                arnoldRop = node
        
        #if no rop node found
        if noRop:
            arnoldRop = context.createNode("arnold")

        #toggle the parameters
        arnoldRop.parm("ar_texture_auto_maketx").set(val) #toggle based on our toggle

    def useExistingTextures(self,val):
        """
        This function creates an arnold rop and toggles the use existing tx textures to be on

        Args:
            val: Boolean to determine checkbox state 
        Returns:
            None
        """
            
        context = hou.node("/out") #defin context

        noRop = True #boolean to check node existence
        for node in context.children(): #check the types
            if node.type().name() == "arnold": #if arnold exists
                noRop = False #set the boolean to False
                arnoldRop = node
        
        #if no rop node found
        if noRop:
            arnoldRop = context.createNode("arnold")

        #toggle the parameters
        arnoldRop.parm("ar_texture_use_existing_tx").set(val) #toggle based on our toggle
    
    def clickAllButtons(self):
        """
        This function creates all the shader for the shader widgets
        
        Args:
            None
        Returns:
            None
        """

        shaderWidgets = self.findChildren(ShaderCreator)

        total_steps = len(shaderWidgets) #total steps for calculating percentage
        if self.isMtlx:
            i = 0 #counter variable for keeping track of iterations
            for widget in shaderWidgets:
                widget.createMtlxShader()

                #update progress bar
                i=i+1 #add the step counter
                progress_value = int((float(i) / total_steps) * 100)
                self.progressBar.setValue(progress_value)#set the value
        else:
            i = 0 #counter variable for keeping track of iterations
            for widget in shaderWidgets:
                widget.createShader()

                #update progress bar
                i=i+1 #add the step counter
                progress_value = int((float(i) / total_steps) * 100)
                self.progressBar.setValue(progress_value)#set the value

        #define context
        context = hou.node("/mat")

        #layout children
        context.layoutChildren()

    def browseFolder(self):
        """
        This function creates a dialog for the user to choose their texture folder
        
        Args:
            None
        Returns:
            None
        """
        #get path from 
        self.path = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose Texture Folder" )
        #paste it in input field
        self.mainWindow.input_folderPath.setText(self.path)
            
    def findPrefixes(self):
        """
        This function finds the releavant prefixes and populates the shader widgets accordingly.
        Args:
            None
        Returns:
            None
        """
        self.clearWidgets() #clear all the widgets
        folder_path = self.mainWindow.input_folderPath.text() #get the text from folder
        if not folder_path:
            prefix = "aiStandardSurface"
            list = []
            folder_path = ""
            self.populate(prefix,list,folder_path="")
            return

        # Iterate through files in the folder
        prefix_files = {}
        for filename in os.listdir(folder_path):
            parts = filename.split('.')#split the ext
            ext = parts[-1]
            if ext == "exr": #get only exrs
                # Build full path
                full_path = os.path.join(folder_path, filename)

                #find the unique prefixes
                prefix = filename.split("_base")[0]
                # Add the file to the corresponding prefix list
                if prefix not in prefix_files:
                    prefix_files[prefix] = []
                prefix_files[prefix].append(full_path)
    
        # Populate the scroll area with each prefix and its list
        for prefix, files in prefix_files.items():
            for filename in files:
                # Check each suffix
                for suffix, var_name in SUFFIXES.items():
                    if suffix in filename:
                        isArnold = True
                for suffix,var_name in VP2SUFFIX.items():
                    if suffix in filename:
                        isArnold = False
                        
            if isArnold == True:
                self.populate(prefix, files,folder_path)
            if not isArnold:
                pass
        
        #reset the progress val
        self.progressBar.setValue(0)
            
    def populate(self,prefix,filesList,folder_path):
        """
        This function populates the Arnold shaderWidget instances on the scroll area
        
        Args:
            prefix: prefix to be set for the shaderNames and nodes
            filesList: list of files containing the same prefix
            folder_path: folderPath where the function iterates upon
        Returns:
            None
        """

        widget = ShaderCreator(prefix,filesList,folder_path,mtlx=self.isMtlx)
        self.scrollLayout.addWidget(widget)
        self.scrollArea.setFixedWidth(widget.width()) #set the scroll area according to contents

    def clearWidgets(self):
        """
        This Function clears all the shader widgets in the scroll area
        
        Args:
            None
        Returns:
            None
        """

        #if arnold widgets present
        shaderWidgets = self.findChildren(ShaderCreator)
        if shaderWidgets:
            for widget in shaderWidgets:
                widget.setVisible(False) #hide them
                widget.deleteShaderWidget() #delete the light
        
class ShaderCreator(QtWidgets.QWidget):  # Change to QWidget instead of QMainWindow

    """
    This is a ShaderCreator class that lets us create the ShaderWidget in the scroll area
    
    Methods:
        __init__: This is the Constructor function to initialize layout variables ,dict and also connections for each prefix found
        createShader: This function creates an arnold shader and calls the connectTextures() to assign textures to it. If assign and mesh is passed , then it will asign the shader to selected mesh
        createShaderAndAssign: This Function checks for any selected mesh. If there are any selected mesh, then an arnold shader will be created and assigned
        createMtlxShader: This function creates a mtlx shader and calls the connectTextures() to assign textures to it. If assign and mesh is passed , then it will asign the shader to selected mesh
        createMtlxShaderAndAssign:  This Function checks for any selected mesh. If there are any selected mesh, then a mtlx shader will be created and assigned
        connectTextures: This function checks the texturePaths dictionary and connects it to the passed shader if there are any paths
        connect_file_texture_to_shader: This functions creates a texture and connects it to the given shader based on the type of texture
        findTexturesPath: This function finds the relevant textures path from the given folder path
        deleteShaderWidget: This function deletes the widget from the parent UI
        updateShaderName: This function updates the shader name label based on the given input in the LineEdit Widget
        setBaseColorPath: This function makes a dialog for the User to pick the Base Color Texture path 
        setRoughPath: This function makes a dialog for the User to pick the Roughness Texture path 
        setMetalPath: This function makes a dialog for the User to pick the Metalness Texture path 
        setNormalPath: This function makes a dialog for the User to pick the Normal Texture path 
        setDispPath: This function makes a dialog for the User to pick the Displacement Texture path 

    """

    def __init__(self,prefix,filesList,folder_path,mtlx=False,parent =None):
        """
        This is the Constructor function to initialize layout variables ,dict and also connections for each prefix found.
        
        Args:
            prefix: prefix to be set for the shaderNames and nodes
            filesList: list of files containing the same prefix
            folder_path: folderPath where the function iterates upon
            mtlx: Boolean to determine whether or not a materialX shader has to be created
        Returns:
            None
        """
        super(ShaderCreator, self).__init__(parent=parent)
        ui_path = "QtUi/masterUIShaderCreator.ui"  # Replace with the path to your .ui file
        self.myUI = QtUiTools.QUiLoader().load(ui_path, parentWidget=self)

        self.myUI.standardSurfaceWidget.setVisible(True)
        
        #hide mainlayouts
        self.myUI.VP2Widget.setVisible(False)
        self.myUI.VP2Widget.deleteLater()
        self.myUI.btn_browse.setVisible(False)
        self.myUI.btn_browse.deleteLater()
        self.myUI.input_folderPath.setVisible(False)
        self.myUI.input_folderPath.deleteLater()
        self.myUI.label.setVisible(False)
        self.myUI.label.deleteLater()
        
        
        #initialize prefix
        self.prefix = prefix
        self.listOfFiles = filesList

        self.mtlx = mtlx #store the boolean for determining mtlx


        #CONNECTIONS
        if mtlx: #if materialX is ticked
            self.myUI.btn_create.setText("Create MaterialX Shader")
            self.myUI.btn_createAndAssign.clicked.connect(self.createMtlxShaderAndAssign)
            self.myUI.btn_create.clicked.connect(self.createMtlxShader)
        else:
            self.myUI.btn_createAndAssign.clicked.connect(self.createShaderAndAssign)
            self.myUI.btn_create.clicked.connect(self.createShader)
        
        
        self.myUI.input_shaderName.returnPressed.connect(self.updateShaderName)

        self.myUI.tb_baseColor.clicked.connect(self.setBaseColorPath)
        self.myUI.tb_roughness.clicked.connect(self.setRoughPath)
        self.myUI.tb_metalness.clicked.connect(self.setMetalPath)
        self.myUI.tb_normal.clicked.connect(self.setNormalPath)
        self.myUI.tb_displacement.clicked.connect(self.setDispPath)


        # Set minimum size based on adjusted size
        self.adjustSize()
        self.setMinimumSize(self.myUI.standardSurfaceWidget.sizeHint())


        #initalize dict for toolbuttons
        self.texturePaths = {
            "baseColor" : None,
            "specularRoughness" :None,
            "metalness" : None,
            "normalCamera" : None,
            "displacementShader" : None,
        }


        self.findTexturesPath(folder_path) #find textures and assign them


        self.myUI.lb_shaderName.setText(self.prefix.split("_primary")[0]+"_SHD") #set the name
        self.myUI.lb_shaderName.setToolTip(self.prefix.split("_primary")[0]+"_SHD") #set the tooltip
        #adjust the size of the label
        self.defaultFont = self.myUI.lb_shaderName.font()
        self.smallfont = QtGui.QFont()
        self.smallfont.setPointSize(10)
        self.smallfont.setBold(1)

        if (len(self.myUI.lb_shaderName.text()))>=27:
            self.myUI.lb_shaderName.setFont(self.smallfont)

    def createShader(self,assign = False, mesh = None):
        """
        This function creates an arnold shader and calls the connectTextures() to assign textures to it. If assign and mesh is passed , then it will assign the shader to selected mesh

        Args:
            assign: bool to check if shader needs to be assigned
            mesh: mesh to assign the shader to.
        Returns:
            None
        """
        #get the name
        shaderName = self.myUI.lb_shaderName.text()
        if shaderName.startswith(tuple("0123456789")):
            raise ValueError("Couldnt create your shader")

        current_directory = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd() #store the current working directory without any selection

        if current_directory.type().name() != "matnet": #check if current directory is a matnet
            current_directory = hou.node("/mat")

        context = current_directory

        #MAKING THE SHADER
        try:
            #create a material builder
            self.builder = context.createNode("arnold_materialbuilder",shaderName)

            #set the subcontext again
            context = self.builder

            self.shader = context.createNode("arnold::standard_surface",shaderName)#create shader
            self.outShader = context.node("OUT_material") #set the output node
            self.outShader.setName("OUT_"+shaderName)

            #connect SG and shader
            self.outShader.setInput(0,self.shader)

            #connect textures
            self.connectTextures() 
            
            #assign to a mesh
            if assign:
                sel = hou.selectedNodes()[0]
                sel.parm("shop_materialpath").set(self.builder.path())
            else:
                pass
            
            print("Successfully created "+ shaderName+ " at "+str(current_directory))

            #layout children
            context.layoutChildren()

        except:

            raise RuntimeError("Couldnt create your shader")

    def createShaderAndAssign(self):
        """
        This Function checks for any selected mesh. If there are any selected mesh, then an arnold shader will be created and assigned

        Args:
            None
        Returns:
            None
        """
        selection = hou.selectedNodes()
        if not selection:
            raise RuntimeError("Nothing is selected")
        else:
            self.createShader(assign=True,mesh=selection)
            context = hou.node("/mat")
            context.layoutChildren()

    def createMtlxShader(self,assign = False, mesh = None):
        """
        This function creates an arnold shader and calls the connectTextures() to assign textures to it. If assign and mesh is passed , then it will assign the shader to selected mesh

        Args:
            assign: bool to check if shader needs to be assigned
            mesh: mesh to assign the shader to.
        Returns:
            None
        """
        #get the name
        shaderName = self.myUI.lb_shaderName.text()
        if shaderName.startswith(tuple("0123456789")):
            raise ValueError("Couldnt create your shader")

        #define the parent context
        context = hou.node("/mat")

        #MAKING THE SHADER
        try:
            #create nodes
            self.builder = context.createNode("subnet",shaderName+"_X_SN") #creates a subnet with same name and a suffix

            #DEFINING Mtlx Surface Material
            self.shader = self.builder.createNode("mtlxsurfacematerial",shaderName)


            #DEFINE MATERIALX STANDARD
            self.stdSurface = self.builder.createNode("mtlxstandard_surface","SUR_"+shaderName) #mtlx standard surface
            self.shader.setInput(0,self.stdSurface) #connecting the nodes

            #define the output of subnet
            output = self.builder.node("suboutput1")
            output.setInput(0,self.shader)
            output.setName("OUT_"+shaderName)

            #connect textures
            self.connectTextures() 
            
            #assign to a mesh
            if assign:
                sel = hou.selectedNodes()[0]
                sel.parm("shop_materialpath").set(self.builder.path())
            else:
                pass
            
            print("Successfully created "+ shaderName)

            #layout children
            self.builder.layoutChildren()

        except:

            raise RuntimeError("Couldnt create your shader")

    def createMtlxShaderAndAssign(self):
        """
        This Function checks for any selected mesh. If there are any selected mesh, then an arnold shader will be created and assigned

        Args:
            None
        Returns:
            None
        """
        selection = hou.selectedNodes()
        if not selection:
            raise RuntimeError("Nothing is selected")
        else:
            self.createMtlxShader(assign=True,mesh=selection)
            context = hou.node("/mat")
            context.layoutChildren()

    def connectTextures(self):
        """
        This function checks the texturePaths dictionary and connects it to the passed shader if there are any paths

        Args:
            None
        Returns:
            None
        """
        for texType,path in self.texturePaths.items():
            if path:
                self.connect_file_texture_to_shader(texType,path) #call the function to connect texture to shader

            if not path:
                print("Skipping "+texType)
                continue
    
    def connect_file_texture_to_shader(self,textureType,texture_path):
        """
        This functions creates a texture and connects it to the given shader based on the type of texture

        Args:   
            textureType: type of texture
            texture_path: path of texture
        Returns:
            None
        """

        #define the context
        context = self.builder

        #add <UDIM> suffix
        texture_path = texture_path.rsplit('.', 2)[0] + ".<UDIM>.exr"

        # Create a file texture node
        texture_name = texture_path.split("/")[-1].split(".")[0]#get the name of the texture
        if self.mtlx:
            file_texture = context.createNode("mtlximage",texture_name+"_FTN")
            file_texture.parm("file").set(texture_path)
        else:
            file_texture = context.createNode("arnold::image",texture_name+"_FTN")     
            # Set the file path to the texture node and set it to UDIMS
            file_texture.parm("filename").set(texture_path)



        # Connect the file texture to the shader's attributes based on type

        ### DSP ###
        if textureType == "displacementShader":
            if self.mtlx: #if its a materialX
                #create a mtlx displacement node
                dsp_bridge = context.createNode("mtlxdisplacement",texture_name+"_MTD")
                #set the connections
                dsp_bridge.setInput(0,file_texture)
                #connect the displacemenet to shader
                self.shader.setInput(1,dsp_bridge)
            else:
                #connecting DSP nodes 
                # Create a multiply node
                mult_dsp = context.createNode("arnold::multiply",texture_name+"_MLT")
                # Connect the file texture to the disp_shader node
                mult_dsp.setInput(0,file_texture)
                #Connec the disp_shader to shader
                self.outShader.setInput(1,mult_dsp)
        
        ### DIF ###
        elif textureType == "baseColor":  
            if self.mtlx: #if its a materialX
                # Create a color correct node
                color_correct = context.createNode("mtlxcolorcorrect",texture_name+"_MTC")
                # Connect the file texture to the color correct node
                color_correct.setInput(0,file_texture)
                # Connect the color correct node to the shader
                self.stdSurface.setInput(1,color_correct)
            else:   
                #connecting DIF nodes        
                # Create a color correct node
                color_correct = context.createNode("arnold::color_correct",texture_name+"_AIC")
                # Connect the file texture to the color correct node
                color_correct.setInput(0,file_texture)
                # Connect the color correct node to the shader
                self.shader.setInput(1,color_correct)

        ### RGH ###
        elif textureType == "specularRoughness":
            if self.mtlx: #if its a materialX
                # Create an aiRange node
                mtlx_range = context.createNode("mtlxrange",texture_name+"_MTR")
                # Connect the file texture to the aiRange node
                mtlx_range.setInput(0,file_texture)
                #Connec the aiRange to shader
                self.stdSurface.setInput(6,mtlx_range)
            else:   
                #connecting RGH nodes   
                # Create an aiRange node
                ai_range = context.createNode("arnold::range",texture_name+"_AIR")
                # Connect the file texture to the aiRange node
                ai_range.setInput(0,file_texture)
                #Connec the aiRange to shader
                self.shader.setInput(6,ai_range,1)
        
        ### MTL ###
        elif textureType == "metalness":  
            if self.mtlx: #if its a materialX
                # Create an aiRange node
                mtlx_range = context.createNode("mtlxrange",texture_name+"_MTR")
                # Connect the file texture to the aiRange node
                mtlx_range.setInput(0,file_texture)
                #Connec the aiRange to shader
                self.stdSurface.setInput(3,mtlx_range)
            else:   
                #connecting MTL nodes      
                # Create an aiRange node
                ai_range = context.createNode("arnold::range",texture_name+"_AIR")
                # Connect the file texture to the aiRange node
                ai_range.setInput(0,file_texture)
                #Connec the aiRange to shader
                self.shader.setInput(3,ai_range,1)
        
        ### NRM ###
        elif textureType == "normalCamera":  
            if self.mtlx: #if its a materialX
                #connecting NRM nodes        
                # Create an aiNormal node
                mtlx_nrmal = context.createNode("mtlxnormalmap",texture_name+"_MTN")
                # Connect the file texture to the aiRange node
                mtlx_nrmal.setInput(0,file_texture)
                #Connec the normal to shader  
                self.stdSurface.setInput(40,mtlx_nrmal)
            else:
                #connecting NRM nodes        
                # Create an aiNormal node
                ai_normal = context.createNode("arnold::normal_map",texture_name+"_AIN")
                # Connect the file texture to the aiRange node
                ai_normal.setInput(0,file_texture)
                #Connec the normal to shader  
                self.shader.setInput(39,ai_normal)
   
    def findTexturesPath(self,folder_path):
        """
        This function finds the relevant textures path from the given folder path

        Args:
            folder_path: path of the folder to iterate upon.
        Returns:
            None
        """
        # Initialize variables for each texture type
        base_color_path = None
        roughness_path = None
        normal_path = None
        displacement_path = None
        metalness_path = None
 
        # Iterate through files in the folder
        for filename in self.listOfFiles:
            # Check each suffix
            for suffix, var_name in SUFFIXES.items():
                if suffix in filename:
                    # Extract the number and file extension
                    parts = filename.split('.')
                    try:
                        frame_number = int(parts[-2])
                        ext = parts[-1]
                    except ValueError:
                        continue
                    if ext == "exr": #get only exrs
                        # Build full path
                        full_path = os.path.join(folder_path, filename)
                        # Assign to appropriate variable
                        if var_name == 'base_color_path':
                            if base_color_path is None or frame_number < int(base_color_path.split('.')[-2]):
                                base_color_path = full_path
                        elif var_name == 'roughness_path':
                            if roughness_path is None or frame_number < int(roughness_path.split('.')[-2]):
                                roughness_path = full_path
                        elif var_name == 'normal_path':
                            if normal_path is None or frame_number < int(normal_path.split('.')[-2]):
                                normal_path = full_path
                        elif var_name == 'displacement_path':
                            if displacement_path is None or frame_number < int(displacement_path.split('.')[-2]):
                                displacement_path = full_path
                        elif var_name == 'metalness_path':
                            if metalness_path is None or frame_number < int(metalness_path.split('.')[-2]):
                                metalness_path = full_path  

        #assign the values for our dictionary
        self.texturePaths["baseColor"]=base_color_path
        self.texturePaths["specularRoughness"]=roughness_path
        self.texturePaths["metalness"]=metalness_path
        self.texturePaths["normalCamera"]=normal_path
        self.texturePaths["displacementShader"]=displacement_path

        #set the icons and label
        if base_color_path:
            self.myUI.tb_baseColor.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_baseColor.setText(base_color_path.split("/")[-1])
            #take out strike
            font = self.myUI.lb_baseColor.font()
            font.setStrikeOut(False)
            self.myUI.lb_baseColor.setFont(font)
        if not base_color_path:
            self.myUI.tb_baseColor.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_baseColor.setText("No Texture Found")
            #strike it
            font = self.myUI.lb_baseColor.font()  
            font.setStrikeOut(True)
            self.myUI.lb_baseColor.setFont(font)

        if roughness_path:
            self.myUI.tb_roughness.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_roughness.setText(roughness_path.split("/")[-1])
            #take out strike
            font = self.myUI.lb_roughness.font()
            font.setStrikeOut(False)
            self.myUI.lb_roughness.setFont(font)
        if not roughness_path:
            self.myUI.tb_roughness.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_roughness.setText("No Texture Found")
            #strike it
            font = self.myUI.lb_roughness.font()
            font.setStrikeOut(True)
            self.myUI.lb_roughness.setFont(font)

        if metalness_path:
            self.myUI.tb_metalness.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_metalness.setText(metalness_path.split("/")[-1])
            #take out strike
            font = self.myUI.lb_metalness.font()
            font.setStrikeOut(False)
            self.myUI.lb_metalness.setFont(font)
        if not metalness_path:
            self.myUI.tb_metalness.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_metalness.setText("No Texture Found")
            #strike it
            font = self.myUI.lb_metalness.font()
            font.setStrikeOut(True)
            self.myUI.lb_metalness.setFont(font)


        if normal_path:
            self.myUI.tb_normal.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_normal.setText(normal_path.split("/")[-1])
            #take out strike
            font = self.myUI.lb_normal.font()
            font.setStrikeOut(False)
            self.myUI.lb_normal.setFont(font)
        if not normal_path:
            self.myUI.tb_normal.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_normal.setText("No Texture Found")
            #strike it
            font = self.myUI.lb_normal.font()
            font.setStrikeOut(True)
            self.myUI.lb_normal.setFont(font)
            
        if displacement_path:
            self.myUI.tb_displacement.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_displacement.setText(displacement_path.split("/")[-1])
            #take out strike
            font = self.myUI.lb_displacement.font()
            font.setStrikeOut(False)
            self.myUI.lb_displacement.setFont(font)
        if not displacement_path:
            self.myUI.tb_displacement.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_displacement.setText("No Texture Found")
            #strike it
            font = self.myUI.lb_displacement.font()
            font.setStrikeOut(True)
            self.myUI.lb_displacement.setFont(font)

    def deleteShaderWidget(self):
        """
        This function deletes the widget from the parent UI

        Args:
            None
        Returns:
            None
        """
        self.setParent(None) #remove from the layout
        self.setVisible(False) #make it hidden
        self.deleteLater() #delete the UI as soon as it can
        
    def updateShaderName(self):
        """
        This function updates the shader name label based on the given input in the LineEdit Widget
        
        Args:
            None
        Returns:
            None
        """
        #get the name
        inputname = self.myUI.input_shaderName.text()
        name = inputname+"_SHD" #add suffix
        #update the text
        self.myUI.lb_shaderName.setText(name)
        self.myUI.lb_shaderName.setToolTip(name)#set the tooltip
        self.myUI.input_shaderName.clear()

        if (len(self.myUI.lb_shaderName.text()))>=27:
            self.myUI.lb_shaderName.setFont(self.smallfont)
        else:
            self.myUI.lb_shaderName.setFont(self.defaultFont)
    
    def setBaseColorPath(self):
        """
        This function makes a dialog for the User to pick the Base Color Texture path 
        
        Args:
            None
        Returns:
            None
        """
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Base Color Texture" ,dir = self.path)[0]
        except:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Base Color  Texture")[0]
        self.texturePaths["baseColor"]=file
        if file:
            self.myUI.tb_baseColor.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_baseColor.setText(file.split("/")[-1])
            #take out strike
            font = self.myUI.lb_baseColor.font()
            font.setStrikeOut(False)
            self.myUI.lb_baseColor.setFont(font)
        if not file:
            self.myUI.tb_baseColor.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_baseColor.setText("No Texture Selected")
            #strike it
            font = self.myUI.lb_baseColor.font()  
            font.setStrikeOut(True)
            self.myUI.lb_baseColor.setFont(font)

    def setRoughPath(self):
        """
        This function makes a dialog for the User to pick the Roughness Texture path 
        
        Args:
            None
        Returns:
            None
        """
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Roughness Texture" ,dir = self.path)[0]
        except:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Roughness Texture")[0]
        self.texturePaths["specularRoughness"]=file
        if file:
            self.myUI.tb_roughness.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_roughness.setText(file.split("/")[-1])
            #take out strike
            font = self.myUI.lb_roughness.font()
            font.setStrikeOut(False)
            self.myUI.lb_roughness.setFont(font)
        if not file:
            self.myUI.tb_roughness.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_roughness.setText("No Texture Selected")
            #strike it
            font = self.myUI.lb_roughness.font()
            font.setStrikeOut(True)
            self.myUI.lb_roughness.setFont(font)
      
    def setMetalPath(self):
        """
        This function makes a dialog for the User to pick the Metalness Texture path 
        
        Args:
            None
        Returns:
            None
        """
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Metalness Texture" ,dir = self.path)[0]
        except:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Metalness Texture")[0]
        self.texturePaths["metalness"]=file
        if file:
            self.myUI.tb_metalness.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_metalness.setText(file.split("/")[-1])
            #take out strike
            font = self.myUI.lb_metalness.font()
            font.setStrikeOut(False)
            self.myUI.lb_metalness.setFont(font)
        if not file:
            self.myUI.tb_metalness.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_metalness.setText("No Texture Selected")
            #strike it
            font = self.myUI.lb_metalness.font()
            font.setStrikeOut(True)
            self.myUI.lb_metalness.setFont(font)

    def setNormalPath(self):
        """
        This function makes a dialog for the User to pick the Normal Texture path 
        
        Args:
            None
        Returns:
            None
        """
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Normal Texture" ,dir = self.path)[0]
        except:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Normal Texture")[0]
        self.texturePaths["normalCamera"]=file
        if file:
            self.myUI.tb_normal.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_normal.setText(file.split("/")[-1])
            #take out strike
            font = self.myUI.lb_normal.font()
            font.setStrikeOut(False)
            self.myUI.lb_normal.setFont(font)
        if not file:
            self.myUI.tb_normal.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_normal.setText("No Texture Selected")
            #strike it
            font = self.myUI.lb_normal.font()
            font.setStrikeOut(True)
            self.myUI.lb_normal.setFont(font)

    def setDispPath(self):
        """
        This function makes a dialog for the User to pick the Displacement Texture path 
        
        Args:
            None
        Returns:
            None
        """
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Displacement Texture" ,dir = self.path)[0]
        except:
            file = QtWidgets.QFileDialog.getOpenFileName(self,"Choose Displacement Texture")[0]
        self.texturePaths["displacementShader"]=file
        if file:
            self.myUI.tb_displacement.setArrowType(QtCore.Qt.RightArrow)
            self.myUI.lb_path_displacement.setText(file.split("/")[-1])
            #take out strike
            font = self.myUI.lb_displacement.font()
            font.setStrikeOut(False)
            self.myUI.lb_displacement.setFont(font)
        if not file:
            self.myUI.tb_displacement.setArrowType(QtCore.Qt.NoArrow)
            self.myUI.lb_path_displacement.setText("No Texture Selected")
            #strike it
            font = self.myUI.lb_displacement.font()
            font.setStrikeOut(True)
            self.myUI.lb_displacement.setFont(font)

def createShaderCreatorWindow():
    """
    This function makes an instance of the Arnold Shader Creator Window

    Args:
        None
    Returns:
        None
    """

    arnold_shader_creatorWin = ShaderCreatorHoudiniWindow()
    arnold_shader_creatorWin.show()

createShaderCreatorWindow() #call the function to create the Window Class