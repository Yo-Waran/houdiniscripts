"""
Script Name: materialXConverter.py
Author: Ram Yogeshwaran
Company: The Mill
Contact: Ram.Yogeshwaran@themill.com
Description: This script generates a materialX Shader with all the textures connected from a Princpled Shader in Houdini.
"""


"""Converting Principled Shaders to MaterialX"""

import hou

class materialXConverter():
    """
    This is a converter class that converts a selected node into another shader.
     
    Methods:
        __init__: Initializes the converter class.
        convertSelected : Generates a materialX shader node from a selected Principled Shader node
    """
    def __init__(self):
        pass

    def convertSelected(self):
        """
        This function generates a materialX shader node from a selected Principled Shader node. This works only on Principled shader nodes.

        Args:
            none

        Returns:
            None
        """
        if not hou.selectedNodes(): 
            raise ValueError("Nothing is selected ! Please select an appropriate shader") #Erroring out Early in the program

        mysel = hou.selectedNodes()[0] #selecting only one node 

        context = mysel.parent() #returns a context of selected node

        matxsubnet = context.createNode("subnet",mysel.name()+"_materialX") #creates a subnet with same name and a suffix

        #DEFINING SURFACE OUTPUT
        surfaceoutput = matxsubnet.createNode("subnetconnector","surface_output") #creating similar output node

        #setting its parameters similar to materialX
        surfaceoutput.parm("parmname").set("surface")
        surfaceoutput.parm("parmlabel").set("Surface")
        surfaceoutput.parm("parmtype").set("surface")
        surfaceoutput.parm("connectorkind").set("output")

        #DEFINING DISP OUTPUT
        dispoutput = matxsubnet.createNode("subnetconnector","displacement_output") #creating similar output node

        #setting its parameters similar to materialX
        dispoutput.parm("parmname").set("displacement")
        dispoutput.parm("parmlabel").set("Displacement")
        dispoutput.parm("parmtype").set("displacement")
        dispoutput.parm("connectorkind").set("output")

        #DEFINE MATERIALX STANDARD
        mtlx = matxsubnet.createNode("mtlxstandard_surface","mtlxstandard_surface1") #mtlx standard surface
        surfaceoutput.setInput(0,mtlx) #connecting the nodes

        #REPLICATE BASECOLOR If present
        if mysel.parm("basecolor_useTexture").eval() == 1:
            colorpath = mysel.parm("basecolor_texture").eval() #querying and storing DIF path
            colortexture = matxsubnet.createNode("mtlximage","COLOR") #creating Texture node
            colortexture.parm("file").set(colorpath)  #setting the node path
            mtlx.setInput(1,colortexture) #connecting the nodes

        else:
            print("Skipping Base Color")

        #REPLICATE RGHNESS If present
        if mysel.parm("rough_useTexture").eval()==1:
            rghpath = mysel.parm("rough_texture").eval() #querying and storing RGH path
            rghtexture = matxsubnet.createNode("mtlximage","ROUGHNESS") #creating Texture node
            rghtexture.parm("file").set(rghpath)  #setting the node path
            rghtexture.parm("signature").set("0") #setting a 'signature' paramter for RGH
            mtlx.setInput(6,rghtexture) #connecting the nodes

        else:
            print("Skipping Roughness")

        #REPLICATE OPACITY IF present

        if mysel.parm("opaccolor_useTexture").eval()==1: #checks if the 'useTexture' is ticked
            opapath = mysel.parm("opaccolor_texture").eval() #querying and storing file path
            opatexture = matxsubnet.createNode("mtlximage","OPACITY") #creating Texture node
            opatexture.parm("file").set(opapath)  #setting the node path
            opatexture.parm("signature").set("0") #setting a 'signature' paramter for RGH
            mtlx.setInput(38,opatexture) #connecting the nodes
        else:
            print("Skipping Opacity")    

        #REPLICATE NORMAL If Present
        if mysel.parm("baseBumpAndNormal_enable").eval()==1: #checks if the 'useTexture' is ticked
            nrmpath = mysel.parm("baseNormal_texture").eval() #querying and storing file path
            nrmtexture = matxsubnet.createNode("mtlximage","NORMAL") #creating Texture node
            nrmtexture.parm("file").set(nrmpath)  #setting the node path
            nrmBridge = matxsubnet.createNode("mtlxnormalmap","mtlxnormalmap1") #creating the bridge Normal node
            nrmBridge.setInput(0,nrmtexture)  #connecting the texture
            mtlx.setInput(40,nrmBridge) #connecting the bridge to the shader
        else:
            print("Skipping Normal")    

        #REPLICATE DISPLACEMENT If Present
        if mysel.parm("dispTex_enable").eval()==1: #checks if the 'useTexture' is ticked
            disppath = mysel.parm("dispTex_texture").eval() #querying and storing file path
            disptexture = matxsubnet.createNode("mtlximage","DISPLACEMENT") #creating Texture node
            disptexture.parm("file").set(disppath)  #setting the node path
            dispBridge = matxsubnet.createNode("mtlxdisplacement","mtlxdisplacement1") #creating the bridge Displacement node
            dispBridge.setInput(0,disptexture)  #connecting the texture
            disptexture.parm("signature").set("0")#setting a 'signature' paramter for DSP
            dispoutput.setInput(0,dispBridge) #connecting the bridge to the shader
        else:
            print("Skipping Displacement")    


        matxsubnet.layoutChildren() #layout nodes

obj1= materialXConverter()        
obj1.convertSelected()