"""
2D Texture Rigger
Author: Brandon Bower

Rigs 2D textures onto an object so that textures can be changed with an attribute to animate the texture.
Select object, then control, before running
"""
import maya.cmds as cmds
import re
from functools import partial

WIDTH = 250 # constant for width of window

def getSurfaceShader(objName):
    '''
    (str) -> list
    
    gets name of material and shading group attached to object, returns that in a list
    
    Code by mark_wilkins, found at: https://simplymaya.com/forum/showthread.php?t=3181
    This assumes you want ONLY the shape node at the selected level of the
    hierarchy, for the object whose transform name is passed in as the argument.
    '''
    myShapeNode = cmds.listRelatives(objName, children=True, shapes=True)
    mySGs = cmds.listConnections(myShapeNode[0], type='shadingEngine') 
    surfaceShader = cmds.listConnections(mySGs[0] + '.surfaceShader')
    return [surfaceShader[0], mySGs[0]]

def connectTex(p2dTexture, fName):
    '''
    (str, str) -> None
    creates all relevant connections between a place2dTexture node and a file node
    '''
    attrs = ['coverage', 'translateFrame', 'rotateFrame', 'mirrorU', 'mirrorV', 'stagger',\
            'wrapU', 'wrapV', 'repeatUV', 'offset', 'rotateUV', 'noiseUV',\
            'vertexUvOne', 'vertexUvTwo', 'vertexUvThree', 'vertexCameraOne']
    for i in range(len(attrs)):     
        cmds.connectAttr(p2dTexture + '.' + attrs[i], fName + '.' + attrs[i], f=True);
    cmds.connectAttr(p2dTexture + '.outUV', fName + '.uv', f=True);
    cmds.connectAttr(p2dTexture + '.outUvFilterSize', fName + '.uvFilterSize', f=True);
    return

def rigHandler(*args):
    '''
    (bool) -> None
    iterates over all texture-relevant ui elements, queries them,
    and sets up the rig with that information
    called by windowCall
    '''
    selectList = cmds.ls(sl=True)
    uiList = cmds.scrollLayout('sub_fields', q=True, ca=True)
    cmds.shadingNode('place2dTexture', asUtility=True, n = 'p2dT')
    cmds.shadingNode('layeredTexture', asTexture=True, n='lT')
    index = 0
    for i in range(0,len(uiList),3): # iterate over list, step by 3 for the 3 info elements of each texture         
        path = cmds.button(uiList[i], q=True, l=True)
        if(path == "Select first image in sequence"):
            continue # Skip paths that were not specified
        names = cmds.textField(uiList[i+1], q=True, tx=True)
        enum = cmds.checkBox(uiList[i+2], q=True, v=True)
        
        fName = 'file_' + str(index)
        cmds.shadingNode('file', asTexture=True, n = fName) # create file node for texture
        connectTex('p2dT', fName) # connect to place2dTexture
        cmds.setAttr(fName + '.fileTextureName', path, type = 'string') # load file
        cmds.setAttr('lT.inputs[' + str(index) + '].blendMode', 1)
        cmds.connectAttr(fName + '.outColor', 'lT.inputs[' + str(index) + '].color', f=True)
        cmds.connectAttr(fName + '.outAlpha', 'lT.inputs[' + str(index) + '].alpha', f=True) # connect nodes, set lT attributes
        
        pathList = path.split('/')
        texName = pathList.pop() # split-up path, pop off end item, as that is the name of the texture
        path = '/'.join(pathList) + '/' # join path back, to get path to folder
        namesList = names.split(',') # get names for attribute name as well as enum, if relevant
        attrName = namesList[0].strip()
        if (attrName == '' or attrName == "Name Attribute"): 
            attrName = 'attr' + str(index + 1) # auto-name for if user didn't input any names
        number = re.findall('[\d]+', texName) # find sequence number
        items = texName.split(number[-1]) # get texture name and file type
        numbSearch = '?' * len(number[-1]) # create string of '?' same length as sequence number
        files = cmds.getFileList(folder=path, filespec=items[0] + numbSearch + items[1]) # all sequence numbers, for length calculations
        fLength = len(files)  
        if (enum):
            enumNames = ''
            nLength = len(namesList)
            for j in range(fLength):
                # for loop to set up enum names
                if (j + 1 < nLength and namesList[1] != " separate with comma for Enum"):
                    enumNames += namesList[j + 1].strip() + ':' # user defined names
                else:
                    enumNames += str(j + 1) + ':' # in case user didn't define enough names
            enumNames = enumNames[:-1] # strip off end ':'    
            cmds.addAttr(selectList[1], ln=attrName, at='enum', en=enumNames)
            cmds.setAttr(selectList[1] + '.' + attrName, e=True, keyable=True) # create attribute, make it keyable
            for j in range(fLength):
                cmds.setAttr(selectList[1] + '.' + attrName, j)
                cmds.setAttr(fName + '.frameExtension', j + 1)
                cmds.setDrivenKeyframe(fName + '.frameExtension', cd=selectList[1] + '.' + attrName) # set up driven key 
        else:
            # create attr, have it drive frameExtension of the file
            cmds.addAttr(selectList[1], ln=attrName, at='long', min=1, max=fLength, dv=1)
            cmds.setAttr(selectList[1] + '.' + attrName, e=True, keyable=True)
            cmds.connectAttr(selectList[1] + '.' + attrName, fName + '.frameExtension', f=True) 
        cmds.setAttr(fName + '.useFrameExtension', 1)
        index += 1    

    surfShaders = getSurfaceShader(selectList[0])
    if(cmds.checkBox('mnm', q=True, v=True)): # New material
        cmds.duplicate(surfShaders[1], upstreamNodes=True, n=surfShaders[0] + '_copySG') # copy old material
        surfShaders[1] = surfShaders[0] + '_copySG' 
        surfShaders[0] = cmds.listConnections(surfShaders[1] + '.surfaceShader')[0] # update list values with new material names
        cmds.select(selectList[0])
        cmds.hyperShade(assign=surfShaders[1]) # assign new material to selsected object
    cmds.setAttr('lT.inputs[' + str(index) + '].blendMode', 0) 
    cmds.connectAttr(surfShaders[0] + '.outColor', 'lT.inputs[' + str(index) + '].color', f=True)
    cmds.connectAttr('lT.outColor', surfShaders[1] + '.surfaceShader', f=True) # splice lT between mat and shading group

def findPath(*args):
       '''
       (str, bool) -> None
       Finds path to first image in sequence, updates button label to that path
       called by windowCall
       '''
       multipleFilters = "Compatible files (*.jpg *.jpeg *.png);;jpeg (*.jpeg *.jpg);;png (*.png);;All Files (*.*)"
       fPath = cmds.fileDialog2(cap='First image in sequence', fm=1, ff=multipleFilters, ds=2)
       if(fPath is not None):
           cmds.button(args[0], e=True ,l=fPath[0])
           cmds.button('Rig', e=True, en=True)
       return 


def makeButtons(n):
    '''
    (int) -> None (creates ui elements as a side effect)
    recursively calls itself to create needed ui elements
    called by changeHandler
    calls itself recursively
    '''
    if n == 0:
        return
    else:
        pathButton = cmds.button(l='Select first image in sequence', w=WIDTH)
        cmds.button(pathButton, e=True, c=partial(findPath, pathButton))
        cmds.textField(w=WIDTH,\
        ann="If using Enum, separate names with a comma. \n First name written will be used as name of the attribute.",\
        tx="Name Attribute, separate with comma for Enum")
        cmds.checkBox(l='Enum')
        makeButtons(n - 1)
        return

def changeHandler(n):
    '''
    (int) -> None (creates sublayout for buttons created by makeButtons)
    Handles when initial int field is changed
    deletes previous layout
    creats new column or scroll layout, based on number of textures to be rigged
    called by windowCall
    calls makeButtons to create needed ui elements
    '''
    if cmds.scrollLayout('sub_fields', ex=True):
        cmds.deleteUI('sub_fields')
        cmds.window('Rig_Texture_2D', e=True, h=20)
    if (n == 0):
        return
    if (n <= 4):
        cmds.scrollLayout('sub_fields', w=WIDTH+4, h=n*68)
        cmds.window('Rig_Texture_2D', e=True, w=WIDTH+4, h=n*68 + 60)
    else:
        cmds.scrollLayout('sub_fields', w=WIDTH+18, h=240)
    cmds.button('Rig', en=False, edit=True) # Disable rig button
    makeButtons(n)
    return
    

def windowCall():
    '''
    () -> None
    Creates user interface window
    '''
    if cmds.window('Rig_Texture_2D', ex=True):
        cmds.deleteUI('Rig_Texture_2D') 
    cmds.window('Rig_Texture_2D')
    cmds.columnLayout()
    cmds.intField(w=WIDTH/4, cc=changeHandler) # intField to determine number of textures to be rigged
    cmds.checkBox('mnm', l='Make New Material?')
    cmds.button('Rig', en=False, w=WIDTH, c=rigHandler)
    cmds.window('Rig_Texture_2D', e=True, h=20, w=WIDTH) 
    cmds.showWindow('Rig_Texture_2D')
    return

def main():
    '''function driver for program'''
    windowCall()
    return
    
main()
