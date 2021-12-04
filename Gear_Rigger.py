"""
Gear Rigger
Author: Brandon Bower

Instructions: Select driven gear, shift select driver gear, launch code 

Note: if you already know the ratio, it can be directly inputted 
as opposed to calculated through tooth numbers.
"""

import maya.cmds as cmds
    
WIDTH = 228 # Constant for window width    
    
def gearRig(*args):
    '''
    (*args) -> None
    
    gets values from ui fields, writes appropriate expression, 
    assigns expression to driver gear    
    '''
    obs = cmds.ls(sl=True) # Get the selected gears
    ratio = cmds.floatField('fltFld', q=True, v=True) # Get ratio between the two gears
    driverAxis = cmds.optionMenu('driverAx', q=True, v=True) # Get axis selection for driver gear
    drivenAxis = cmds.optionMenu('drivenAx', q=True, v=True) # Get axis selection for driven gear 
    # set up expression
    gearExp = "{}.rotate{} = ({}.rotate{} * -{});".format(obs[0], driverAxis, obs[1], drivenAxis, ratio)
    cmds.expression(s=gearExp, o=obs[0]) # apply expression to driver gear
    # cmds.deleteUI('grWin') # delete the '#' at the start if window deletion is desired

def calcRatio(*args):
    '''
    (*args) -> None
    
    calculates rotation ratio based on tooth count of both gears
    updates value in float field
    '''
    # Get teeth values of driven and driver gears
    drivenTeeth = cmds.intField('intFld1', q=True, v=True)
    driverTeeth = cmds.intField('intFld2', q=True, v=True)
    # calculate ratio, update float field with value
    cmds.floatField('fltFld', e=True, v=(driverTeeth/float(drivenTeeth))) 


def windowCall():
    '''
    () -> None
    
    creates Gear Rig window
    '''
    
    # check if window exists, if it does, delete it
    if(cmds.window('grWin', ex=True)):
        cmds.deleteUI('grWin')
             
    # Set up window and window layout         
    cmds.window('grWin', s=False, t='Gear Rig')    
    cmds.columnLayout()
    # Driven gear ui items
    cmds.text('Teeth of driven gear:')
    cmds.intField('intFld1', w=WIDTH, v=1, cc=calcRatio) # Teeth count, driven
    cmds.optionMenu('driverAx') # Axis select, driven
    cmds.menuItem(l='X')
    cmds.menuItem(l='Y')
    cmds.menuItem(l='Z')
    cmds.text(' ')
    # Driver gear ui items
    cmds.text('Teeth of driver gear:')
    cmds.intField('intFld2', w=WIDTH, v=1, cc=calcRatio) # Teeth count, driver
    cmds.optionMenu('drivenAx') # Axis select, driver
    cmds.menuItem(l='X')
    cmds.menuItem(l='Y')
    cmds.menuItem(l='Z')
    cmds.text(' ')
    # Ratio ui items
    cmds.text('Gear rotation value (Driver Teeth / Driven Teeth):')
    cmds.floatField('fltFld', w=WIDTH, v=1.0, ann='Number of driven gear rotations per one driver rotation')
    # button to call gearRig function
    cmds.button(l='Rig', w=WIDTH, c=gearRig)

    cmds.showWindow('grWin')
    cmds.window('grWin', e=True, w=WIDTH, h=195)  
  

def main():
    '''Program Driver'''
    windowCall()
    
main()
    
