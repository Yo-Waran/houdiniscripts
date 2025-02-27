"""
Script Name: houdini_material_QC_mod.py
Author: Ram Yogeshwaran
Company: The Mill
Contact: Ram.Yogeshwaran@themill.com
Description: This module contains all the necessary QC functions for the Houdini QC Tool .
"""

import hou

def update_all_material_networks(self):
    """
    This function updates the self.all_matnet with all the material networks available in the scene.

    Note:
        This function also skips the below mentioned matnets since they are part of the mill pipeline 
        globalMaterials : present inside rop node
        matnet1 : present inside Adv import nodes of assets
    Args:
        self: object of a class that is calling this function
    Returns:
        None
    """

    self.all_matnet = [] #empty list to store all the matnets
    
    # Include the /mat context if it exists (since it's a material network itself)
    mat_context = hou.node("/mat")
    if mat_context is not None:
        self.all_matnet.append(mat_context)


    # Iterate over all nodes in the scene
    for node in hou.node('/').allSubChildren():
        # Check if the node is of type 'matnet' (Material Network)
        if node.type().name() == 'matnet':
            if(node.parent().parent().type().name()=="tvcHoudiniTools::adv_import::0.2") : #go two steps above and check parent type
                continue
            elif node.name()=="globalMaterials":#skip the global material from the Template's rop
                continue
            else:
                self.all_matnet.append(node)

def naming_convention_QC(self,refresh = False ):
    """
    QC for checking the naming convention of all the Shaders and returns the wrong ones

    Note:
        This function also skips the below mentioned node if it contains only Arnold image nodes
        TEXTURES: node that contatins all the textures 

    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries 
    Returns:
        incorrectShaders : list of all the shaders with incorrect names
    """

    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self) 
        self.ui.lb_errorMessage.setText("Updated Naming Convention QC ") #update label
    else:
        pass
    
    #for collecting results
    self.incorrectShaders = []

    #check for matnets first
    if self.all_matnet:
        #iterate and check for naming conventions
        total_steps = len(self.all_matnet) #total steps for calculating percentage
        i = 0 #counter variable for keeping track of iterations
        for matnet in self.all_matnet:
            #check for suffixes and append accordingly
            for shd in matnet.children():
                if not shd.name().endswith("_MAT") and not shd.name().endswith("_SHD"): #shd check condition
                    if shd.name() == "TEXTURES": #check if the file is textures node
                        valid = True
                        for node in shd.children():
                            if not node.type().name() == "arnold::image":
                                valid = False
                        
                        if not valid:
                            self.incorrectShaders.append(shd)
                    else:
                        self.incorrectShaders.append(shd)

            #update progress bar
            i=i+1 #add the counter
            progress_value = int((float(i) / total_steps) * 100)
            self.ui.pBar_namingConvention.setValue(progress_value) #set the value
    else:
        print("No Matnets found")
        self.ui.pBar_namingConvention.setValue(100) #set the value of progress bar

    #setting the icon in UI
    if self.incorrectShaders :
        self.setStatusRed(self.ui.lb_statusNamingConvention,self.ui.btn_selectNamingConvention) #set the icon to red and enable select
    else:
        self.setStatusGreen(self.ui.lb_statusNamingConvention,self.ui.btn_selectNamingConvention) #set the icon to green and disable select


    #populate the error widget with the text on ui and return values
    if refresh:
        print("Populating error widget with Update")
        self.populateErrorWidget(self.ui.lb_labelNamingConvention.text(), returnVal1 = self.incorrectShaders,update=True) 
    else:
        print("Populating error widget without Update")
        self.populateErrorWidget(self.ui.lb_labelNamingConvention.text(), returnVal1 = self.incorrectShaders) 

    #enabling the refresh button
    self.ui.btn_refreshNamingConvention.setEnabled(True)

    return self.incorrectShaders 

def kept_in_adv_shaders_QC(self,refresh = False):
    """
    QC for checking if the shaders assigned to assets , are inside the adv shaders

    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries 
    Returns:
        nodes_not_in_adv : list of all the shaders with incorrect names
    """

    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self) 
        self.ui.lb_errorMessage.setText("Updated Kept in Adv Shaders QC ") #update label
    else:
        pass

    #for collecting results
    self.nodes_not_in_adv = []

    #check for matnets first
    if self.all_matnet:
            #iterate and check for the place
            total_steps = len(self.all_matnet) #total steps for calculating percentage
            i = 0 #counter variable for keeping track of iterations
            for matnet in self.all_matnet:
                if not matnet.parent().type().name() == "tvcHoudiniTools::adv_shaders::0.1": #if the parent's type is not adv shaders
                    for node in matnet.children(): #add all the nodes in the matnet
                        self.nodes_not_in_adv.append(node)
                #update progress bar
                i=i+1 #add the counter
                progress_value = int((float(i) / total_steps) * 100)
                self.ui.pBar_assignAdvShaders.setValue(progress_value) #set the value
    else:
        print("No Matnets found")
        self.ui.pBar_assignAdvShaders.setValue(100) #set the value of progress bar
    

    #setting the icon in UI
    if self.nodes_not_in_adv: #if results found
        self.setStatusRed(self.ui.lb_statusAssignAdvShaders,self.ui.btn_selectAssignAdvShaders) #set the icon to red and enable select
    else: #if no results found
        self.setStatusGreen(self.ui.lb_statusAssignAdvShaders,self.ui.btn_selectAssignAdvShaders) #set the icon to green and disable select

    #populate the error widget with the text on ui and return values
    if refresh:
        self.populateErrorWidget(self.ui.lb_labelAssignAdvShaders.text(), returnVal1 = self.nodes_not_in_adv,update=True) 

    else:
        self.populateErrorWidget(self.ui.lb_labelAssignAdvShaders.text(), returnVal1 = self.nodes_not_in_adv) 

    #enabling the refresh button
    self.ui.btn_refreshAssignAdvShaders.setEnabled(True)

    return self.nodes_not_in_adv

def unused_nodes_QC(self,refresh = False):
    """
    QC for checking the unused nodes in the Adv shaders

    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries 
    Returns:
        unused_nodes : a list containing all the unused shaders in the scene
    """
    
    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self)
        self.ui.lb_errorMessage.setText("Updated Unused Nodes QC ") #update label
    else:
        pass

    #List to store unused Textures
    self.unused_nodes = []    


    #check for matnets first
    if self.all_matnet:

        total_steps = len(self.all_matnet) #total steps for calculating percentage
        i = 0 #counter variable for keeping track of iterations

        for matnet in self.all_matnet:

            if matnet.parent().type().name() == "tvcHoudiniTools::adv_shaders::0.1": #if the parent's name is adv shaders
                adv_node = matnet.parent() #store the adv node

                #get the shader with no assignments
                shader_assignments = {} #empty to get the shader and assignments dict

                number_of_materials = adv_node.parm("num_materials").eval()

                for j in range(number_of_materials): #iterate through the materials parameter
                    shd_name = adv_node.parm("material_name{0}".format(j+1)).eval() #get the shader name
                    geo_selection = adv_node.parm("material_selection{0}".format(j+1)).eval() #get the geo
                    shader_assignments[shd_name] = geo_selection #append it to the dict

                unused_shader_names = [] #to collect shaders with no assignments

                for shader_name, assignment in shader_assignments.items():
                    if not assignment:
                        unused_shader_names.append(shader_name)

                #append the hou node of the the same namer
                for shd in matnet.children():
                    if shd.name() in unused_shader_names:
                        self.unused_nodes.append(shd)
            else:
                pass

            #update progress bar
            i=i+1 #add the counter
            progress_value = int((float(i) / total_steps) * 100)
            self.ui.pBar_unusedNodes.setValue(progress_value) #set the value

    else:
        print("No Matnets found")
        self.ui.pBar_unusedNodes.setValue(100) #set the value of progress bar

    
    #setting the icon in UI
    if self.unused_nodes:
        self.setStatusRed(self.ui.lb_statusUnusedNodes,self.ui.btn_selectUnusedNodes) #set the icon to red and enable select
    else:
        self.setStatusGreen(self.ui.lb_statusUnusedNodes,self.ui.btn_selectUnusedNodes) #set the icon to green and disable select

    #populate the error widget with the text on ui and return values
    if refresh:
        self.populateErrorWidget(self.ui.lb_labelUnusedNodes.text(),returnVal1=self.unused_nodes,update=True) 
    else:
        self.populateErrorWidget(self.ui.lb_labelUnusedNodes.text(),returnVal1=self.unused_nodes) 

    #enabling the refresh button
    self.ui.btn_refreshUnusedNodes.setEnabled(True)

    return self.unused_nodes

def check_for_textures(shader):
    """ 
    This function checks for textures in the given shaders.
    
    Args:
        shader: shader to check textures for
    Returns:
        textures_list : list containing all the textures and the texture paths in the given shader
    """

    textures_list= [] #empty list to collect all the texture nodes

    for node in shader.children(): #iterate through te shader
        if node.type().name() == "arnold::image": #if its an image
            textures_list.append(node) #append it to the dict

    return textures_list

def textures_in_current_job(self, refresh = False):
    """
    This function checks if all the textures that are present inside the shaders are in current job

    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries
    Returns:
        incorrectJobTextures : a dict containing all the textures that are not in the current job
    """    

    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self)
        self.ui.lb_errorMessage.setText("Updated Texture in Current Job QC ") #update label
    else:
        pass

    job = self.currentJob

    #empty list to collect incorrect Job textures
    self.incorrectJobTextures = []

    #self.setStatusYellow(self.ui.lb_statusCurrentJob) #set the icon to red and enable select

    #check for matnets first
    if self.all_matnet:
            #iterate and check for naming conventions
            total_steps = len(self.all_matnet) #total steps for calculating percentage
            i = 0 #counter variable for keeping track of iterations
            for matnet in self.all_matnet:
                #check for suffixes and append accordingly
                for shd in matnet.children():
                    textures_in_shd = check_for_textures(shd) #call the function 
                    if not textures_in_shd: #pass if there are no textures
                        continue
                    #iterate through the found textures
                    for texture in textures_in_shd: 
                        file_path = texture.parm("filename").eval() #get the file path parameter
                        if not job in file_path: #if there's no job string
                            self.incorrectJobTextures.append(texture) #append it to the dict
                        
                #update progress bar
                i=i+1 #add the counter
                progress_value = int((float(i) / total_steps) * 100)
                self.ui.pBar_currentJob.setValue(progress_value) #set the value
    else:
        print("No Matnets found")
        self.ui.pBar_currentJob.setValue(100) #set the value of progress bar

    #setting the icon in UI
    if self.incorrectJobTextures: #if results found
        self.setStatusRed(self.ui.lb_statusCurrentJob,self.ui.btn_selectCurrentJob) #set the icon to red and enable select
    else: #if no results found
        self.setStatusGreen(self.ui.lb_statusCurrentJob,self.ui.btn_selectCurrentJob) #set the icon to green and disable select

    #populate the error widget with the text on ui and return values
    if refresh:
        self.populateErrorWidget(self.ui.lb_labelCurrentJob.text(), returnVal1 = self.incorrectJobTextures,update=True) 

    else:
        self.populateErrorWidget(self.ui.lb_labelCurrentJob.text(), returnVal1 = self.incorrectJobTextures) 

    #enabling the refresh button
    self.ui.btn_refreshCurrentJob.setEnabled(True)

    return self.incorrectJobTextures

def published_textures_QC(self, refresh = False) : 
    """
    This function checks if all the textures that are present inside the shaders are published
    
    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries 
    Returns:
        unpublishedTextures : a list of all the textures that are not published 
    """

    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self)
        self.ui.lb_errorMessage.setText("Updated Published Textures QC ")#update label
    else:
        pass

    #empty list to collect the unpublished Textures
    self.unpublishedTextures = []

    #check for matnets first
    if self.all_matnet:
            #iterate and check for naming conventions
            total_steps = len(self.all_matnet) #total steps for calculating percentage
            i = 0 #counter variable for keeping track of iterations
            for matnet in self.all_matnet:
                #check for suffixes and append accordingly
                for shd in matnet.children():
                    textures_in_shd = check_for_textures(shd) #call the function 
                    if not textures_in_shd: #pass if there are no textures
                        continue
                    #iterate through the found textures
                    for texture in textures_in_shd: 
                        file_path = texture.parm("filename").eval() #get the file path parameter
                        if not "release" in file_path: #if there's no job string
                            self.unpublishedTextures.append(texture) #append it to the dict
                        
                #update progress bar
                i=i+1 #add the counter
                progress_value = int((float(i) / total_steps) * 100)
                self.ui.pBar_publishedTextures.setValue(progress_value) #set the value
    else:
        print("No Shaders to check for Textures")
        self.ui.pBar_publishedTextures.setValue(100) #set the value of progress bar
    

    #setting the icon in UI
    if self.unpublishedTextures:  #if results found
        self.setStatusRed(self.ui.lb_statusPublishedTextures,self.ui.btn_selectPublishedTextures) #set the icon to red and enable select
    else:  #if no results found
        self.setStatusGreen(self.ui.lb_statusPublishedTextures,self.ui.btn_selectPublishedTextures) #set the icon to green and disable select    
    
    #populate the error widget with the text on ui and return values
    if refresh:
        self.populateErrorWidget(self.ui.lb_labelPublishedTextures.text(), returnVal1 = self.unpublishedTextures,update=True) 
    else:
        self.populateErrorWidget(self.ui.lb_labelPublishedTextures.text(), returnVal1 = self.unpublishedTextures) 

    #enabling the refresh button
    self.ui.btn_refreshPublishedTextures.setEnabled(True)

    return self.unpublishedTextures

def duplicate_textures_QC(self, refresh = False):
    """
    This function checks if there are any texture duplicates in the scene
    
    Args:
        self: object of a class that is calling this function
        refresh : boolean value to refresh the dictionaries
    Returns:
        duplicateTextures : a list of all the textures that are duplicated 
    """
    
    #update dictionaries if refresh is True
    if refresh:
        update_all_material_networks(self)
        self.ui.lb_errorMessage.setText("Updated Duplicated Textures QC ") #update label
    else:
        pass

    self.duplicateTextures = []   #empty list to collect the unpublished Textures



    #check for matnets first
    if self.all_matnet:
            #iterate and check for naming conventions
            total_steps = len(self.all_matnet) #total steps for calculating percentage
            i = 0 #counter variable for keeping track of iterations
            for matnet in self.all_matnet:
                #check for suffixes and append accordingly
                for shd in matnet.children():

                    all_paths = [] #collecting all the paths
                    duplicateTexturePaths = [] #collecting all the duplicate texture paths

                    textures_in_shd = check_for_textures(shd) #call the function 
                    if not textures_in_shd: #pass if there are no textures
                        continue
                    #iterate through the found textures
                    for texture in textures_in_shd: 
                        file_path = texture.parm("filename").eval() #get the file path parameter
                        all_paths.append(file_path)
                    
                    #check the occurences of each texture paths
                    occurences = {}
                    
                    for path in all_paths:
                        if path in occurences:
                            occurences[path] +=1
                        else:
                            occurences[path] = 1
                    
                    for path,count in occurences.items():
                        if count>1:
                            duplicateTexturePaths.append(path)
                        
                    for texture in textures_in_shd:
                        file_path = texture.parm("filename").eval() #get the file path parameter

                        if file_path in duplicateTexturePaths:
                            self.duplicateTextures.append(texture)

                #update progress bar
                i=i+1 #add the counter
                progress_value = int((float(i) / total_steps) * 100)
                self.ui.pBar_duplicateTextures.setValue(progress_value) #set the value
    else:
        print("No Shaders to check for Textures")
        self.ui.pBar_duplicateTextures.setValue(100) #set the value of progress bar

    #setting the icon in UI
    if self.duplicateTextures:
        self.setStatusRed(self.ui.lb_statusDuplicateTextures,self.ui.btn_selectDuplicateTextures) #set the icon to red and enable select
    else:
        self.setStatusGreen(self.ui.lb_statusDuplicateTextures,self.ui.btn_selectDuplicateTextures) #set the icon to green and disable select    
    
    #populate the error widget with the text on ui and return values
    if refresh:
        self.populateErrorWidget(self.ui.lb_labelDuplicateTextures.text(), returnVal1 = self.duplicateTextures,update=True) 
    else:
        self.populateErrorWidget(self.ui.lb_labelDuplicateTextures.text(), returnVal1 = self.duplicateTextures) 

    #enabling the refresh button
    self.ui.btn_refreshDuplicateTextures.setEnabled(True)

    return self.duplicateTextures
