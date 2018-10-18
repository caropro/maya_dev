#coding=utf-8
#author:Jonathon Woo
#version:1.0.0

import mtoa
import pymel.core as pm
import os

def convert():
    textures = pm.ls(type="file")
    for texture in textures:
        print
        dir(texture)
        old_path = texture.getAttr("fileTextureName")
        new_path = old_path.replace("T:","m:")
        texture.setAttr("fileTextureName", new_path)
