"""
State:          Lightsattach
State type:     lightsattach
Description:    Lightsattach
Author:         waranr
Date Created:   June 27, 2024 - 14:56:52
"""


import hou
import viewerstate.utils as su

class State(object):
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer


    def onSelection(self, kwargs):
        """ Called when a selector has selected something
        """        
        selection = kwargs["selection"]
        state_parms = kwargs["state_parms"]
        
        node = kwargs["node"]  #store the node of the mesh connected
        geo = node.geometry()  #store the geometry of the connected node

        context = hou.node("/obj") #set the context
        sel = selection.selections() #stores a tuple of the selection
        selectedPoints = sel[0].points(geo)#return the points in the selection

        path = node.path() #storing the full path of the node
        offsetParmPath = node.parm("offsetY").path()

        lgtlist = [] #lights list

        for pt in selectedPoints: #iterate through ponits
            num = pt.number() #store the number of point
            light = context.createNode("hlight::2.0",str(node)+"_lgt_"+str(num)) #create lights 
            
            lgtlist.append(light) #append the lights
            
            attrib = "P" #attribute to set expression 

            #set Expression for each parameters of the light
            light.parm("tx").setExpression("point('{0}',{1},{2},0)".format(path,num,attrib))
            light.parm("ty").setExpression("point('{0}',{1},{2},1)+ch('{3}')".format(path,num,attrib,offsetParmPath))
            light.parm("tz").setExpression("point('{0}',{1},{2},2)".format(path,num,attrib))

        lgtsubnet = context.collapseIntoSubnet(lgtlist,str(node)+"_LIGHTS") #collapse into subnets

        lgtsubnet.layoutChildren() #lay it out

        # Must return True to accept the selection
        return False


def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = kwargs["type"].definition().sections()["DefaultState"].contents()
    state_label = "Lightsattach"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon(kwargs["type"].icon())

    template.bindGeometrySelector(
        name = "pointselect",
        prompt = "Select the Points on which you want to attach lights",
        quick_select = False,
        use_existing_selection = True,
        geometry_types = [hou.geometryType.Points],
        allow_other_sops = False,
        secure_selection = hou.secureSelectionOption.Off)


    return template
