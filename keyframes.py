"""Keyframing in Houdini using asCode"""

import hou

mynode = hou.selectedNodes()[0] #first selected node

myparm = mynode.parm("tx") #save the parameter

print(myparm.asCode())

"""set Keyframes manually"""

import hou

cnode = hou.selectedNodes()[0]

myparm = cnode.parm("tx")

#FIRST FRAME

#create a key

key1 = hou.Keyframe()

#set value and frame for the key
key1.setFrame(1)
key1.setValue(20)

#set the key to that parameter
myparm.setKeyframe(key1)


#SECOND FRAME

#create a key

key2 = hou.Keyframe()

#set value and frame for the key
key2.setFrame(1100)
key2.setValue(0)

#set the key to that parameter
myparm.setKeyframe(key2)


"""Return keyframes"""

import hou

cnode = hou.selectedNodes()[0]

myparm = cnode.parm("tx")

print(myparm.keyframes())