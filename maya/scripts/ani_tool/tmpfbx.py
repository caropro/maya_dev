#coding=utf-8
#author:Jonathon Woo
#version:1.0.0
import pymel.core as pm
import maya.cmds as cmds
import os


def remove_namespace():
    all = pm.ls(long=True, dag=True, sns=True)
    clearlist = []
    for file in all:
        # print file
        if file.startswith(":"):
            ns = file[1:]
            # print ns
            if ns and ns not in clearlist:
                clearlist.append(ns)
    clearlist.sort(key=len, reverse=True)
    for name_space in clearlist:
        pm.namespace(rm="%s" % name_space, mnr=True)


def get_next(child):
    for child_next in pm.listRelatives(child, children=True, fullPath=True):
        child_next_type = pm.objectType(child_next)
        if child_next_type == "transform":
            # print child_next
            return get_next(child_next)
        elif child_next_type == "mesh":
            # print child_next
            return child
        else:
            # print child_next
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


def deal_with_name():
    # deal with the samename node after import the reference readonly
    obj_list = cmds.ls(sl=True, long=True, dag=True)
    obj_list.sort(key=len, reverse=True)
    renamedict = {}
    namelist = []
    for obj in obj_list:
        obj_name = obj.split("|")[-1]
        # print obj_name
        if not namelist.count(obj_name):
            namelist.append(obj_name)
            renamedict[obj_name] = [obj]
        else:
            renamedict[obj_name].append(obj)

    for name in namelist:
        paths = renamedict[name]
        paths.sort(key=len, reverse=True)
        if len(paths) == 1:
            continue
        # print name, paths
        index = 1
        for path in paths:
            new_name = "%s_%s" % (name, index)
            index += 1
            cmds.rename(path, new_name)


def func():
    remove_namespace()
    # 找出带有关键字的骨骼根节点
    key_world = "Root_M"
    all_nodes = cmds.ls(type="joint", l=True)
    for node in all_nodes:
        print node
        if str(node).endswith("Root_M") and "DeformationSystem" in str(node):
            pm.select(node)
            break
    print("hahahaha")
    current_select = pm.ls(sl=True)
    if not current_select:
        return
    # 判断是不是代理文件，并处理命名空间
    final = get_top(current_select)[0]
    # judge the selection is ref or not
    ref_jud = pm.referenceQuery("%s" % final, isNodeReferenced=True)
    if ref_jud:
        file_path = pm.referenceQuery("%s" % final, filename=True)
        print file_path
        pm.mel.eval('file -importReference "%s"' % file_path)
        # 导入之后重新选择节点
        all_nodes = cmds.ls(type="joint", l=True)
        for node in all_nodes:
            print node
            if str(node).endswith("Root_M") and "DeformationSystem" in str(node):
                pm.select(node)
                break
        print("hahahaha")
    current_select = pm.ls(sl=True)
    # 将这套骨骼从组中提出
    cmds.parent(current_select, world=True)
    # 选择根骨骼层级下的所有骨骼
    pm.select(current_select, hierarchy=True)
    all_sk = pm.ls(sl=True)
    # 获取当前起止帧数
    start = pm.playbackOptions(q=True, minTime=True)
    end = pm.playbackOptions(q=True, maxTime=True)
    # 进行动画烘焙
    pm.bakeResults(all_sk, simulation=True, hierarchy="below", t=(start, end))
    # 导出所选骨骼，包含所有层级，为fbx文件
    # 先选中骨骼
    pm.select(current_select)
    # 反选并删除其余内容，因为工程没整理，批量导出会有残余
    pm.mel.eval("invertSelection")
    pm.delete(pm.ls(sl=True))
    # 再选择导出的骨骼
    pm.select(current_select, hierarchy=True)
    # 输出路径
    current_path = pm.mel.eval("file -q -sn")
    fbxpath = os.path.splitext(current_path)[0] + ".fbx"
    pm.mel.eval('file -force -options "v=1;" -typ "FBX export" -pr -es "%s"' % fbxpath)


