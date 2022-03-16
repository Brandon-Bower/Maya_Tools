import maya.cmds as cmds
import os

def renderModels():
    pass


def windowCall():
    '''
    () -> None
    Creates user interface window
    '''
    if cmds.window('Snapshot_Render', ex=True):
        cmds.deleteUI('Snapshot_Render') 
    cmds.window('Snapshot_Render')
    cmds.columnLayout()
    cmds.button('Go', en=False, w=250, c=renderModels)
    cmds.window('Snapshot_Render', e=True, h=20, w=250) 
    cmds.showWindow('Snapshot_Render')
    return

def main():
    '''function driver for program'''
    windowCall()
    return
    
if __name__ == "__main__":
    main()