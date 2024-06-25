import hou
import toolutils


class TurnTabler():


    def __init__(self):
        
        if not hou.selectedNodes():
            raise ValueError("Nothing is selected! Please select something")
        
        self.selected_node = hou.selectedNodes()[0] #save selected node
        button_index, (self.startframe ,self.turntableTime,self.lightspinTime) = hou.ui.readMultiInput("Set the Turntabler Attributes Below",("Start Frame","Turntable Duration","Light Spin Duration"),initial_contents = ("1001","50","50"),buttons = ("Create TurnTable","Cancel"),default_choice = 0 , close_choice = 1)

        #convert given inputs into Integers
        self.startframe = int(self.startframe)
        self.turntableTime = int(self.turntableTime)
        self.lightspinTime = int(self.lightspinTime) 

        if button_index == 0: #if Okay is pressed
            self.createTT() #call the function
        else:
            pass            


    def createTT(self):

        setEnvMap = hou.ui._selectFile(start_directory = "/jobs/tvcResources/bangComms/waranr/Downloads_Server/HDRI",title= "Select your HDRI") #store HDRI path


        #Load the file with Spheres and chart
        file_path = "/usr/people/waranr/Desktop/test/geo1.py" #file path
        openfile = hou.readFile(file_path) #open file 
        exec(openfile) #execute the file


        #store the nodes
        name_node = self.selected_node.name() #save the name of the node
        tt_node = hou.node("/obj/geo1") #save the imported node
        context = self.selected_node.parent() #save the context
        
        #subnetize model and imported file
        subnet = context.collapseIntoSubnet((self.selected_node,tt_node),"Turntable_"+ name_node) #store the subnet


        tt_node = hou.node(subnet.path()+"/geo1") #store tt_node again
        self.selected_node = hou.node(subnet.path()+"/"+name_node)  #store selected geo again
        
        #set transform for the imported geo
        myTTpos = (-0.045,0.035,-0.2)
        myTTscale = 0.01
        myTTrot = -90
        tt_node.parmTuple("t").set(myTTpos)
        tt_node.parm("scale").set(myTTscale)
        tt_node.parm("ry").set(myTTrot)

        #create cam
        cam = subnet.createNode("cam","TT_cam_"+name_node)
        tt_node.setInput(0,cam) #set inputs


        #look through the camera
        viewer = toolutils.sceneViewer().curViewport() #store viewport
        viewer.lockCameraToView(True) #lock cam
        self.selected_node.setSelected(1,clear_all_selected = True) #set selection
        viewer.frameSelected() #frame selected
        viewer.home() #home selected

        #transfer the view to cam
        viewer.saveViewToCamera(cam) #save the cam pos
        viewer.setCamera(cam) #change the current cam

        #set cam parameters again
        cam.parm("focal").set(50)
        cam.parm("aperture").set(41)
        tupleVal = cam.parmTuple("t").eval()
        tx,ty,tz = tupleVal
        cam.parmTuple("t").set((tx+1,ty+1,tz+1))

        #create a null to rotate model
        ctrl_node = subnet.createNode("null","CTRL_"+name_node)
        self.selected_node.setInput(0,ctrl_node) #parent it to null
        ctrl_node.setDisplayFlag(0)

        #create an env light
        env_node = subnet.createNode("envlight","HDRI")

        #########DEFINE KEYFRAMES ##############

        #startframe turntableTime lightspinTime

        startTT = self.startframe 
        endTT = self.startframe+self.turntableTime
        startSpin = endTT+1
        endSpin = startSpin+self.lightspinTime

        #set time ranges of the scene
        hou.playbar.setFrameRange(startTT,endSpin) #setframe range
        hou.playbar.setFrameRange(startTT,endSpin) #set playback

        #assigning values for the parameter purpose
        dictValueTT = {
            startTT : 0,
            endTT : 360
        }

        dictValueSpin = {
            startSpin : 0,
            endSpin : 360
        }

        #iterating and setting keyframes
        for item in dictValueTT:
            key = hou.Keyframe()
            key.setFrame(item)
            key.setValue(dictValueTT.get(item))
            ctrl_node.parm("ry").setKeyframe(key)

        for item in dictValueSpin:
            key = hou.Keyframe()
            key.setFrame(item)
            key.setValue(dictValueSpin.get(item))
            env_node.parm("ry").setKeyframe(key)

        #set environment map    
        env_node.parm("env_map").set(setEnvMap)


        #########ROP Render (Arnold) ##############
        rop = subnet.createNode("ropnet","RenderOUT") #create a ROP Net
        arnold = rop.createNode("arnold","RenderProperties") #create a renderer Node

        #arnold properties
        arnold.parm("camera").set(cam.path())#set the camera of the renderer

        options = arnold.parm("trange").menuItems() #store the drop down options
        arnold.parm("trange").set(options[1]) #set the option

        #force only selected objects and light to render
        arnold.parm("vobject").set(subnet.name())
        arnold.parm("alights").set(subnet.name() + "/" + env_node.name())

        #cleaner node pos
        subnet.layoutChildren()


obj = TurnTabler()
