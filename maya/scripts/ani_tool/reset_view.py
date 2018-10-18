#coding=utf-8
import maya.cmds as cmds
def main():
    pan = cmds.getPanel(withFocus=True)
    sel_camera = cmds.modelPanel(pan, q=True, camera=True)
    cmds.panZoom(sel_camera, abs=True, z=1, d=0, l=0, r=0, u=0)
    return
