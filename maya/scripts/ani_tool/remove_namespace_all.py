import pymel.core as pm
import maya.cmds as cmd
#only for maya verion higher than 2018(include 2018)
def main():
    all=pm.ls(long=True,dag=True,sns=True)
    clearlist=[]
    for file in all:
        print file
        if file.startswith(":"):
            ns=file[1:]
            print ns
            if ns and ns not in clearlist:

                clearlist.append(ns)

    clearlist.sort(key=len,reverse=True)
    for name_space in clearlist:
        pm.namespace(rm = "%s"%name_space,mnr=True)
