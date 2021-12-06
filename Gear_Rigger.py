"""
Gear Rigger
Author: Brandon Bower

Instructions: Select driven gear(s), then shift select driver gear last, launch code 

Note: if you already know the ratio, it can be directly inputted 
as opposed to calculated through tooth numbers.
"""

import maya.cmds as cmds
    
WIDTH = 228 # Constant for window width    
    
def gearRig(*args):
    '''
    (*args) -> None
    
    gets values from ui fields, writes appropriate expression, 
    assigns expression to driven gear    
    '''
    obs = cmds.ls(sl=True) # Get the selected gears
    if(len(obs) > 1): # Make sure at least two gears have been selected
        ratio = cmds.floatField('fltFld', q=True, v=True) # Get ratio between the two gears
        drivenAxis = cmds.optionMenu('drivenAx', q=True, v=True) # Get axis selection for driven gear
        driverAxis = cmds.optionMenu('driverAx', q=True, v=True) # Get axis selection for driver gear
        if(drivenAxis != driverAxis):
            cmds.select(obs[-1])
            origin = cmds.xform(sp=True, q=True, ws=True)# Get position of driver gear
            getIndex = {'x': 0, 'y': 1, 'z': 2}
            d1 = getIndex[driverAxis.lower()]
            d2 = getIndex[drivenAxis.lower()]
        # set up expression
        for i in range(len(obs) - 1): # -1 to exclude driver gear
            cmds.select(obs[i])
            cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0) # Freeze transforms
            r = -ratio
            if(drivenAxis != driverAxis): 
                position = cmds.xform(sp=True, q=True, ws=True) # Get position of driven gear
                dist1 = position[d1] - origin[d1] 
                dist2 = position[d2] - origin[d2] # Find position of driven relative to driver
                if(dist1 * dist2 >= 0): # Check if the distances are the same polarity
                    r = ratio # Driven gears with same polarity dimensions spin same direction as the driver gear
            gearExp = "{}.rotate{} = ({}.rotate{} * {});".format(obs[i], drivenAxis, obs[-1], driverAxis, r)
            cmds.expression(s=gearExp, o=obs[i]) # apply expression to driven gear
    else:
        cmds.warning("Must select at least two gears")
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
    cmds.text('Teeth of driven gear(s):')
    cmds.intField('intFld1', w=WIDTH, v=1, cc=calcRatio) # Teeth count, driven
    cmds.optionMenu('drivenAx', label='Rotation Axis') # Axis select, driven
    cmds.menuItem(l='X')
    cmds.menuItem(l='Y')
    cmds.menuItem(l='Z')
    cmds.text(' ')
    # Driver gear ui items
    cmds.text('Teeth of driver gear:')
    cmds.intField('intFld2', w=WIDTH, v=1, cc=calcRatio) # Teeth count, driver
    cmds.optionMenu('driverAx', label='Rotation Axis') # Axis select, driver
    cmds.menuItem(l='X')
    cmds.menuItem(l='Y')
    cmds.menuItem(l='Z')
    cmds.text(' ')
    # Ratio ui items
    cmds.text('Rotation ratio (Driver Teeth / Driven Teeth):')
    cmds.floatField('fltFld', w=WIDTH, v=1.0, ann='Number of driven gear rotations per one driver rotation')
    # button to call gearRig function
    cmds.button(l='Rig', w=WIDTH, c=gearRig)

    cmds.showWindow('grWin')
    cmds.window('grWin', e=True, w=WIDTH, h=195)  
  

def main():
    '''Program Driver'''
    windowCall()
    
main()
    
