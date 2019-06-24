# coding=utf8

import os
import pymel.core as pm
import maya.cmds as cmds


def get_next(child):
    for child_next in pm.listRelatives(child, children=True, fullPath=True):
        child_next_type = pm.objectType(child_next)
        if child_next_type == "transform":
            print child_next
            return get_next(child_next)
        elif child_next_type == "mesh":
            print child_next
            return child
        else:
            print child_next
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
        print "final one %s" % result
        return result


def main(*args):
    # get the top one
    cmds.select(all=True)
    objs = pm.ls(sl=True)
    if not objs:
        return pm.inViewMessage(smg="select object first", pos="midCenterTop", bkc=0x00FF1010, fade=True)
    pm.select(clear=True)
    for obj in objs:
        parent_node = pm.listRelatives(obj, children=True, fullPath=True, allParents=True)
        if parent_node:
            final = get_top(obj)[0]
        else:
            final = obj
        ref_jud = pm.referenceQuery("%s" % final, isNodeReferenced=True)

        if ref_jud:
            try:
                file_path = pm.referenceQuery("%s" % final, filename=True)
                print file_path
                current_filename = os.path.splitext(os.path.basename(file_path))[0]
                file_dir = os.path.join(os.path.dirname(file_path).split("maya")[0], "maya")
                current_version = os.path.dirname(file_path).split("/")[-2]
                print file_dir, current_version
                version_list = [folder for folder in os.listdir(file_dir) if
                                os.path.isdir(os.path.join(file_dir, folder)) and not folder.startswith(".")]
                print version_list
                version_max = max(version_list)
                print version_max
                if not version_max == current_version:
                    print "update"
                    new_version_dir = os.path.join(file_dir, version_max, "rig_maya")
                    new_version_file = os.listdir(new_version_dir)[0]
                    print new_version_file
                    ref_name = current_filename + "RN"
                    ref_file = os.path.join(new_version_dir, new_version_file)
                    print ref_name, ref_file
                    cmds.file(ref_file, loadReference=ref_name, type="mayaAscii", options="v=0")
                    pm.inViewMessage(smg="Update Done", pos="midCenterTop", bkc=0x00FF1010, fade=True)
                    return
            except:
                continue