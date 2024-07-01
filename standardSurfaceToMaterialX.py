#iterating through a standard surface!
import hou

selSubnet = hou.selectedNodes()[0]

list = selSubnet.children()

for item in list:
    if item.type().name() == "arnold::standard_surface":
        sel = item
    
    elif item.type().name() == "subnetconnector" and item.parm("parmtype").eval() == 25:
        dispNode = item



if sel.type().name() != "arnold::standard_surface":
    raise ValueError("Selected Subnet doesnt have a Standard surface shader !")

parentPath = selSubnet.parent().path()

context = hou.node(parentPath)

matxsubnet = context.createNode("subnet",sel.name()+"_materialX") #creates a subnet with same name and a suffix

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



# if base color connected
if sel.input(1):
    dif_node = sel.input(1)
    dif_path = dif_node.parm("filename").eval()
    colortexture = matxsubnet.createNode("mtlximage","COLOR") #creating Texture node
    colortexture.parm("file").set(dif_path)  #setting the node path
    mtlx.setInput(1,colortexture) #connecting the nodes

else:
    print("Skipping Base Color")

#if metal connected
if sel.input(3):
    mtl_node = sel.input(3)
    mtl_path = mtl_node.parm("filename").eval()
    mtltexture = matxsubnet.createNode("mtlximage","METALNESS") #creating Texture node
    mtltexture.parm("file").set(mtl_path)  #setting the node path
    mtlx.setInput(3,mtltexture) #connecting the nodes

else:
    print("Skipping Metalness")


#if roughness connected
if sel.input(6):
    rgh_node = sel.input(6)
    rgh_path = rgh_node.parm("filename").eval()
    rghtexture = matxsubnet.createNode("mtlximage","ROUGHNESS") #creating Texture node
    rghtexture.parm("file").set(rgh_path)  #setting the node path
    rghtexture.parm("signature").set("0") #setting a 'signature' paramter for RGH
    mtlx.setInput(6,rghtexture) #connecting the nodes

else:
    print("Skipping Roughness")



#if normal connected
if sel.input(39):
    nrm_node = sel.input(39)
    nrm_path = nrm_node.parm("filename").eval()
    nrmtexture = matxsubnet.createNode("mtlximage","NORMAL") #creating Texture node
    nrmtexture.parm("file").set(nrm_path)  #setting the node path
    nrmBridge = matxsubnet.createNode("mtlxnormalmap","mtlxnormalmap1") #creating the bridge Normal node
    nrmBridge.setInput(0,nrmtexture)  #connecting the texture
    mtlx.setInput(40,nrmBridge) #connecting the bridge to the shader

else:
    print("Skipping Normal")

#if displacement connected

#layoutStuffs
matxsubnet.layoutChildren()
selSubnet.parent().layoutChildren()

