import maya.cmds as cmds
import os

WIDTH = 250 # constant for width of window

def openRenderDelete(path, fbxFile):
    '''
    (string, string) -> none
    
    imports fbxFile, renders an image of the file,
    saves that image in the same folder as the file,
    then deletes all imported elements
    '''
    # Complete path to fbx file
    fName = f"{path}/{fbxFile}"
    imported = cmds.file(fName,  i=True, rnn=True)
    # render image
    cmds.render(cmds.listCameras()[0])
    # example.fbx gets saved as example.png
    fileSavePath = f"{path}/{os.path.splitext(fbxFile)[0]}"
    # save render image
    editor = 'renderView'
    cmds.renderWindowEditor(editor, e=True, writeImage=fileSavePath)
    # Select and delete all aspects of the imported meshes
    cmds.select(imported)
    cmds.Delete()
    return
    

def renderModels(*args):
    '''
    (*args) -> None
    
    Explores all sub-folders of the root folder. Renders a snapshot of all applicable
    models, and stores the images in the same folder as the object rendered
    
    Note that *args are passed in, as Maya requires it, but are not used
    '''
    
    # Query button label to get path to root folder
    path = cmds.button("pButton", q=True, l=True)
    # Walk through all sub-folders and files in root folder
    for (dirpath, dirnames, filenames) in os.walk(path):
        for name in filenames:
            # Only open fbx files
            if name.endswith('.fbx'):
                openRenderDelete(dirpath, name)
    cmds.deleteUI('Snapshot_Render')             
    return


def findPath(*args):
    '''
    (*args) -> None
    
    Finds path to first image in sequence, updates button label to that path
    called by windowCall
    
    Note that *args are passed in, as Maya requires it, but are not used
    '''
    #multipleFilters = "Compatible files (*.jpg *.jpeg *.png);;jpeg (*.jpeg *.jpg);;png (*.png);;All Files (*.*)"
    # Launch dialog to select root folder
    fPath = cmds.fileDialog2(cap='Select root folder', fm=2, ds=2)
    if(fPath is not None):
       # Update path button and enable the 'Go' button
       cmds.button("pButton", e=True ,l=fPath[0])
       cmds.button('Go', e=True, en=True)
    return 

def windowCall():
    '''
    () -> None
    Creates user interface window
    '''
    # Check that window doesn't already exist
    if cmds.window('Snapshot_Render', ex=True):
        cmds.deleteUI('Snapshot_Render') 
    cmds.window('Snapshot_Render')
    cmds.columnLayout("SnapRender_layout")
    # Button for selecting root folder
    pathButton = cmds.button("pButton", l='Select root folder of objects to be rendered', w=WIDTH)
    cmds.button(pathButton, e=True, c=findPath)
    # Button for starting script
    cmds.button('Go', en=False, w=250, c=renderModels)
    cmds.window('Snapshot_Render', e=True, h=20, w=WIDTH) 
    cmds.showWindow('Snapshot_Render')
    return

def main():
    '''function driver for program'''
    windowCall()
    return
    
if __name__ == "__main__":
    main()