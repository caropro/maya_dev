import pymel.core as pm
import maya.cmds as cmds

light_type_list = ["aiSkyDomeLight","pointLight","aiAreaLight","areaLight","directionalLight","spotLight"]
def get_next(child,light_type_list):
    for child_next in pm.listRelatives(child,children=True,fullPath=True):
        child_next_type=pm.objectType(child_next)
        print pm.objectType(child_next)
        if child_next_type in light_type_list:
            # print child_next
            return child_next
        elif child_next_type=="transform":
            # print child_next
            return get_next(child_next,light_type_list)
        else:
            # print child_next
            return None
def main():            
    current_selection = pm.ls(sl=True, long=True,dag=True)
    light_shape_list=[]
    for obj in current_selection:
        print obj
        lgt_shape = None
        children = pm.listRelatives(obj, children=True, fullPath=True)
        if len(children)==1 and pm.objectType(children) in light_type_list:
            lgt_shape = children[0]
            light_shape_list.append(lgt_shape)
            continue
    result = cmds.promptDialog(
                    title='aiAOV Light Group',
                    message='Enter Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
    if result == 'OK':
            input_value = cmds.promptDialog(query=True, text=True)        
    if input_value:
        for light_shape in light_shape_list:
            pm.setAttr("%s.aiAov"%light_shape,input_value)  
