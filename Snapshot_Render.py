import maya.cmds as cmds
import os

WIDTH = 250 # constant for width of window

def renderModels(*args):
    path = cmds.button("pButton", q=True, l=True)
    for (dirpath, dirnames, filenames) in os.walk(path):
        print(dirpath)
        print(dirnames)
        print(filenames)
    pass


def findPath(*args):
       '''
       (str, bool) -> None
       Finds path to first image in sequence, updates button label to that path
       called by windowCall
       '''
       #multipleFilters = "Compatible files (*.jpg *.jpeg *.png);;jpeg (*.jpeg *.jpg);;png (*.png);;All Files (*.*)"
       fPath = cmds.fileDialog2(cap='Select root folder', fm=2, ds=2)
       if(fPath is not None):
           cmds.button("pButton", e=True ,l=fPath[0])
           cmds.button('Go', e=True, en=True)
       return 

def windowCall():
    '''
    () -> None
    Creates user interface window
    '''
    if cmds.window('Snapshot_Render', ex=True):
        cmds.deleteUI('Snapshot_Render') 
    cmds.window('Snapshot_Render')
    cmds.columnLayout("SnapRender_layout")
    pathButton = cmds.button("pButton", l='Select root folder of objects to be rendered', w=WIDTH)
    cmds.button(pathButton, e=True, c=findPath)
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