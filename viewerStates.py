"""Basics of Viewerstates"""

    def onEnter(self,kwargs):
        """ Called on node bound states when it starts
        """
        current_node = kwargs["node"]
        state_parms = kwargs["state_parms"]

        # print kwargs in the viewer state console if "Debug log" is 
        # enabled
        current_node.node("switch1").parm("input").set(1) #set the switch node's value to 1
        self.log("onEnter= Smooth the Pig",kwargs)

    def onExit(self,kwargs):
        """ Called when the state terminates
        """
        current_node = kwargs["node"]
        state_parms = kwargs["state_parms"]
        current_node.node("switch1").parm("input").set(0)#set the switch node's value to 0
        self.log("onExit= Reduce the Pig",kwargs)
        

"""Mouse Events on ViewerStates"""

    def onMouseEvent(self, kwargs):
        """ Process mouse events
        """
        current_node = kwargs["node"] #store current node
        ui_event = kwargs["ui_event"]
        dev = ui_event.device()
        self.log("Mouse:", dev.mouseX(), dev.mouseY(), dev.isLeftButton(),dev.isRightButton(),dev.isCtrlKey())
        
        #print(dev)
        totalparm = current_node.node("copy1").parm("ncy") #store the copyTo Node
        totalNum = totalparm.eval() #store its value
        if dev.isLeftButton(): #if button is clicked
            totalparm.set(totalNum+1) #increase the value by 1
        if dev.isRightButton(): #similarly for right button
            totalparm.set(totalNum-1) #decrease the value by 1
        # Must return True to consume the event
        return False

    def onMouseWheelEvent(self, kwargs):
        """ Process a mouse wheel event
        """
        current_node = kwargs["node"] #store current node
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]
        dev = ui_event.device() #store the device        
        scroll = dev.mouseWheel() #store the mousewheel value
        
        #MORE CONDITIONS 
        if dev.isCtrlKey(): #one ctrl key is pressed
            direction = "ty"
        else: #default is translateX
            direction = "tx"
        if dev.isCtrlKey() and dev.isShiftKey(): #both keys are pressed
            direction = "tz"

        #CHANGE TRANSLATES
        txparm = current_node.node("copy1").parm(direction) #store the tx parm in the copyTo Node 
        txNum = txparm.eval() #store its value
        
        
        txparm.set(txNum+scroll) #add the value be +1 or -1
        self.log("MouseWheel:", scroll)
        
        # Must return True to consume the event
        return False

"""ViewerStates Reason"""

    def onMouseEvent(self, kwargs):
        """ Process mouse events
        """
        current_node = kwargs["node"] #store current node
        ui_event = kwargs["ui_event"]
        dev = ui_event.device()
        self.log("Mouse:", dev.mouseX(), dev.mouseY(), dev.isLeftButton(),dev.isRightButton(),dev.isCtrlKey())
        
            
        button = "some" #default reason value
        totalparm = current_node.node("copy1").parm("ncy") #store the copyTo Node
        totalNum = totalparm.eval() #store its value
        if dev.isLeftButton(): #if button is clicked
            totalparm.set(totalNum+1) #increase the value by 1
            button = "Left"
            input = 1 #set input of switch and store it
            
        
        if dev.isRightButton(): #similarly for right button
            totalparm.set(totalNum-1) #decrease the value by 1
            button = "Right"
            input = 2 #set input of switch and store it
            
        #REASONS
        reason = ui_event.reason() #stores the reason value 
        if reason == hou.uiEventReason.Picked:
            print(button + "Button is Clicked")
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Start:
            print( button + "Button is pressed Down")
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Active:
            print(button +"Dragged with button press")
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Changed:
            print(button + "Button Released")
            current_node.node("switch1").parm("input").set(0) #default switch should be 0 
        
        # Must return True to consume the event
        return False

"""ViewerStates Keyboard Presses"""  

def onKeyEvent(self, kwargs):
        """ Called for processing a keyboard event
        """
        currentNode = kwargs["node"]
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]
        self.log("key pressed->",ui_event.device().keyString())
        
        self.key_pressed = ui_event.device().keyString() #store the pressed key
        
        #store the transform Parameters
        tx = currentNode.node("transform1").parm("tx")
        ty = currentNode.node("transform1").parm("ty")
        tz = currentNode.node("transform1").parm("tz")
        
        step = currentNode.parm("Step").eval() #value to increase/decrease by
        

        #check the key and assign values
        #X_AXIS_CONTROLS
        if self.key_pressed == "Shift+UpArrow": #if uparrow pressed
            currentVal = tx.eval() #store the current value
            tx.set(currentVal+step) #add the value to it
        if self.key_pressed == "Shift+DownArrow":
            currentVal = tx.eval()
            tx.set(currentVal-step)
        #Y_AXIS_CONTROLS
        if self.key_pressed == "Shift+LeftArrow":
            currentVal = tz.eval()
            tz.set(currentVal-step)
        if self.key_pressed == "Shift+RightArrow":
            currentVal = tz.eval()
            tz.set(currentVal+step)
        #Z_AXIS_CONTROLS
        if self.key_pressed == "Ctrl+UpArrow":
            currentVal = ty.eval()
            ty.set(currentVal+step)
        if self.key_pressed == "Ctrl+DownArrow":
            currentVal = ty.eval()
            ty.set(currentVal-step)

"""ViewerStates Context Menu"""
....#class State rest of the code 
    def onMenuAction(self, kwargs):
        current_node = kwargs["node"] #store the current node
        selected = kwargs["menu_item"] #store the current selection
        if selected == "first": #check the selection
            val = 0 #assign a value
        if selected == "second": #check the selection
            val = 1 #assign a value
        if selected == "third": #check the selection
            val = 2 #assign a value
        if selected == "four": #check the selection
            val = 3 #assign a value
        current_node.node("switch2").parm("input").set(val)  #set the value of the switch node
   
   
def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = kwargs["type"].definition().sections()["DefaultState"].contents()
    state_label = "Waranr::subnet::1.0"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon(kwargs["type"].icon())
    
    #create Bind Context Menu
    menu = hou.ViewerStateMenu("bend menu", "Bend")
    menu.addActionItem("first","Input One")
    menu.addActionItem("second","Input Two")
    menu.addActionItem("third","Input Three")
    menu.addActionItem("four","Input Four")
    template.bindMenu(menu)



    return template


"""SuperClone HDA ViewerState Definition"""


import hou
import viewerstate.utils as su

class State(object):
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer


    def onMouseEvent(self, kwargs):
        """ Process mouse events
        """
        current_node = kwargs["node"] #store current node
        ui_event = kwargs["ui_event"]
        dev = ui_event.device()
        self.log("Mouse:", dev.mouseX(), dev.mouseY(), dev.isLeftButton(),dev.isRightButton(),dev.isCtrlKey())

        totalparm = current_node.node("copy1").parm("ncy") #store the copyTo Node
        totalNum = totalparm.eval() #store its value
        if dev.isLeftButton(): #if button is clicked
            totalparm.set(totalNum+1) #increase the value by 1
            input = 1 #set input of switch and store it
            
        
        if dev.isLeftButton() and dev.isCtrlKey(): #red color switch
            totalparm.set(totalNum-1) #decrease the value by 1
            input = 2 #set input of switch and store it
            
        #REASONS
        reason = ui_event.reason()
        if reason == hou.uiEventReason.Picked:
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Start:
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Active:
            current_node.node("switch1").parm("input").set(input) #set switch
            
        elif reason == hou.uiEventReason.Changed:
            current_node.node("switch1").parm("input").set(0) #default switch should be 0 
        
        # Must return True to consume the event
        return False
        

    def onMouseWheelEvent(self, kwargs):
        """ Process a mouse wheel event
        """
        current_node = kwargs["node"] #store current node
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]
        dev = ui_event.device() #store the device        
        scroll = dev.mouseWheel() #store the mousewheel value
        
        #MORE CONDITIONS 
        if dev.isCtrlKey(): #one ctrl key is pressed
            direction = "ty"
        else: #default is translateX
            direction = "tx"
        if dev.isCtrlKey() and dev.isShiftKey(): #both keys are pressed
            direction = "tz"

            

        #CHANGE TRANSLATES
        txparm = current_node.node("copy1").parm(direction) #store the tx parm in the copyTo Node 
        txNum = txparm.eval() #store its value
        
        
        txparm.set(txNum+scroll) #add the value be +1 or -1
        self.log("MouseWheel:", scroll)
        
        # Must return True to consume the event
        return False

    def onMenuAction(self, kwargs):
        current_node = kwargs["node"] #store the current node
        selected = kwargs["menu_item"] #store the current selection
        if selected == "first": #check the selection
            val = 0 #assign a value
        if selected == "second": #check the selection
            val = 1 #assign a value
        if selected == "third": #check the selection
            val = 2 #assign a value
        if selected == "four": #check the selection
            val = 3 #assign a value
        current_node.node("switch2").parm("input").set(val)  #set the value of the switch node
   
   
def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = kwargs["type"].definition().sections()["DefaultState"].contents()
    state_label = "Waranr::subnet::1.0"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon(kwargs["type"].icon())
    
    #create Bind Context Menu
    menu = hou.ViewerStateMenu("bend menu", "Bend")
    menu.addActionItem("first","Input One")
    menu.addActionItem("second","Input Two")
    menu.addActionItem("third","Input Three")
    menu.addActionItem("four","Input Four")
    template.bindMenu(menu)



    return template

