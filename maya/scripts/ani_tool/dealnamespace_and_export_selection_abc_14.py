# coding=utf8

import os
import pymel.core as pm
import maya.cmds as cmds

def get_next(child):
    for child_next in pm.listRelatives(child,children=True,fullPath=True):
        child_next_type=pm.objectType(child_next)
        if child_next_type=="transform":
            print child_next
            return get_next(child_next)
        elif child_next_type=="mesh":
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


def main():
    cmds.loadPlugin("AbcExport.mll")
    # get the top one
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
        # judge the selection is ref or not
        ref_jud = pm.referenceQuery("%s" % final, isNodeReferenced=True)

        if ref_jud:
            file_path = pm.referenceQuery("%s" % final, filename=True)
            print file_path
            name_space = pm.referenceQuery("%s" % final, namespace=True)
            print name_space

            pm.mel.eval('file -importReference "%s"' % file_path)
            # remove the namespace
            pm.mel.eval('namespace -mv "%s" ":" -force' % name_space)
            # trying to get the shape group(filter of the curve and rig)
        pm.select(final, add=True)

    #deal with the samename node after import the reference readonly
    obj_list = cmds.ls(sl=True,long=True, dag=True)
    obj_list.sort(key=len, reverse=True)
    renamedict = {}
    namelist = []
    for obj in obj_list:
        obj_name = obj.split("|")[-1]
        print obj_name
        if not namelist.count(obj_name):
            namelist.append(obj_name)
            renamedict[obj_name] = [obj]
        else:
            renamedict[obj_name].append(obj)

    for name in namelist:
        paths=renamedict[name]
        paths.sort(key=len, reverse=True)
        if len(paths) == 1:
            continue
        print name, paths
        index = 1
        for path in paths:
            new_name = "%s_%s" % (name, index)
            index += 1
            cmds.rename(path, new_name)
            
    # pm.select(clear=True)
    # pm.select(final, add=True)
    objs = pm.ls(sl=True, long=True)

    geo_list = []
    for obj in objs:
        print obj
        geo = None
        children = pm.listRelatives(obj, children=True, fullPath=True)
        for child in children:
            print pm.objectType(child)
            if "geo" in child.name() or "Geo" in child.name():
                geo = child
                geo_list.append(geo)
                break
            else:
                geo = None
        if not geo:
            if len(children) == 1 and pm.objectType(children) == "mesh":
                geo = obj
                geo_list.append(geo)
                continue
            else:
                for child in children:
                    if get_next(child):
                        geo = child
                        geo_list.append(geo)


    pm.select(clear=True)
    pm.select(geo_list, add=True)
    print(666666666666666666666666666666666666666666666666666)
    # use the current filepath as the clue to query the destination

    current_path = pm.mel.eval("file -q -sn")
    filename = os.path.basename(current_path)
    abc_name = os.path.splitext(filename)[0] + ".abc"

    rp_code = os.path.dirname(current_path).split("/")[-1]

    dirname = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "abc")

    abc_name = os.path.normpath(os.path.join(dirname, abc_name))

    sel_frameRange = str(pm.playbackOptions(q=True, minTime=True)-10) + " " + str(pm.playbackOptions(q=True, maxTime=True)+10)

    root_geo=""
    for obj in geo_list:
        root_geo+="-root %s "%obj

    print root_geo
    pm.AbcExport(
        j="-frameRange {frameRange} -uvWrite -worldSpace -writeVisibility -dataFormat hdf {file} -file {path}".format(
            frameRange=sel_frameRange, file=root_geo, path=abc_name))


