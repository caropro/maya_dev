# coding=utf8

import os
import pymel.core as pm
import maya.cmds as cmds


def get_next(child):
    for child_next in pm.listRelatives(child, children=True, fullPath=True):
        child_next_type = pm.objectType(child_next)
        if child_next_type == "transform":
            print
            child_next
            return get_next(child_next)
        elif child_next_type == "mesh":
            print
            child_next
            return child
        else:
            print
            child_next
            return None


def get_top(obj):
    """
    Args:
        obj:
    Returns:
            the function to get the top level of the selection
    """
    parent_node = pm.listRelatives(obj, children=True, fullPath=True, allParents=True)
    if parent_node:
        return get_top(parent_node)
    else:
        result = obj
        print
        "final one %s" % result
        return result


def main(*args):
    # get the top one
    if not cmds.ls(sl=True):
        cmds.select(all=True)
    objs = pm.ls(sl=True, references=True)
    if not objs:
        return pm.inViewMessage(smg="select object first", pos="midCenterTop", bkc=0x00FF1010, fade=True)
    pm.select(clear=True)
    for obj in objs:
        parent_node = pm.listRelatives(obj, children=True, fullPath=True, allParents=True)
        if parent_node:
            final = get_top(obj)[0]
        else:
            final = obj

        file_path = pm.referenceQuery("%s" % final, filename=True)

        if file_path.startswith("T:"):
            new_version_file = file_path.replace("T:", "m:")

            cmds.file(new_version_file, loadReference="%s" % final, type="mayaAscii", options="v=0")
            pm.inViewMessage(smg="Update Done", pos="midCenterTop", bkc=0x00FF1010, fade=True)
