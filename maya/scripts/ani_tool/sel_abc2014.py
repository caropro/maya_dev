# coding=utf8

import os
import pymel.core as pm
import maya.cmds as cmds


def main():
    objs = pm.ls(sl=True)
    
    #use the current filepath as the clue to query the destination
    current_path = pm.mel.eval("file -q -sn")
    filename = os.path.basename(current_path)
    abc_name = os.path.splitext(filename)[0] + "_plug"+".abc"

    rp_code = os.path.dirname(current_path).split("/")[-1]

    dirname = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "abc")

    abc_name = os.path.normpath(os.path.join(dirname, abc_name))

    sel_frameRange = str(pm.playbackOptions(q=True, minTime=True)-10) + " " + str(pm.playbackOptions(q=True, maxTime=True)+10)

    geo=""
    for obj in objs:
        geo+="-root %s "%obj

    pm.AbcExport(
        j="-frameRange {frameRange} -uvWrite -worldSpace -writeVisibility -dataFormat hdf {file} -file {path}".format(
            frameRange=sel_frameRange, file=geo, path=abc_name))

