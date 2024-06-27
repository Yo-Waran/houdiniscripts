import hou
import os

class SmartSaver():

    def __init__(self):
        self.basename = hou.hipFile.basename() #store the filename

        path = hou.hipFile.path().split("/")
        if self.basename == "untitled.hip" or path[-3] != "scenes": #check if filename is a saved file or in our context
            self.initValues()
        else:
            self.getValues()
        
        self.description = "" #inital value

        self.main()

    def initValues(self):
        #initial values for the fields
        self.dir = "/usr/people/waranr/Desktop/test/"
        self.project = "untitled"
        self.ass_shot = "untitled"
        self.dept = "assets"
        self.version = "v1"
        self.layer = ""
        

    def getValues(self):

        #get file path
        path = hou.hipFile.path()
        path = path.split("/") #split the string
        self.project = path[-5] #getting only the specific folder name
        directoryPath = path[:-5] #slicing the list
        self.dir = ("/").join(directoryPath) + "/" #join the directory

        #get file name
        values = self.basename.split("_") 
        self.ass_shot = values[0] #save first element of file name
        self.dept = values[1] #save second element

        if len(values)==3: #if layer not present
            self.layer = "" 

        elif len(values) == 4: #if layer present
            self.layer = values[2]
        
        
        self.version = values[-1].split(".")[0] #get the last element of name for version  number


    def main(self):
        #creating the fields
        self.button_idx , (self.dir , self.project, self.ass_shot,self.dept,self.version,self.layer,self.description) = hou.ui.readMultiInput(
            "Save/Version Up your file",
            ("Directory","Project","Asset/Shot","Department","Version","Layer","Description"),
            initial_contents = (self.dir , self.project, self.ass_shot,self.dept,self.version,self.layer,self.description),
            title = "Smart Save Tool",
            buttons = ("Save","VersionUp","Cancel"),
            default_choice = 0, close_choice = 2,
        )
        self.fileNameConstruct()
        self.filePathConstruct()
        self.saveScene()



    def fileNameConstruct(self):
        ext = ".hip" #extension
        if self.layer: #if layer exists
            varList = [self.ass_shot,self.dept,self.layer,self.version] #make a list of var
        else: #if layer doesnt exist
            varList = [self.ass_shot,self.dept,self.version] #make a list of var
            
        self.filename = "_".join(varList) #add the variables
        self.filename = self.filename + ext #add extension


    def filePathConstruct(self):
        #creating the path
        self.filepath = self.dir+self.project+"/houdini/scenes/"+self.dept+"/" #making the full path to save on 

    def saveScene(self):
        #making directory if it doesnt exist
        if os.path.exists(self.filepath) == 0:
            os.makedirs(self.filepath)

        if self.button_idx == 0: #if save button is clicked
            hou.hipFile.save(self.filepath+self.filename)
            print("File saved!")
        elif self.button_idx == 1:
            version = list(self.version) #make it into a list (v1 into ['v','1'])
            newval = int(version[-1])+1 #add one to the last element
            version[-1] = str(newval) #make it into a string again
            self.version = "".join(version) #join it with previous value
            self.fileNameConstruct() #change the filename again
            hou.hipFile.save(self.filepath+self.filename) #save the file
            print("File Versioned Up")


obj = SmartSaver()
