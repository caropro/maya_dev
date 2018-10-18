#coding=utf-8
#author:Jonathon Woo
#version:1.0.0

import mtoa
import pymel.core as pm
import os
from mtoa.convertShaders import *


def convertAiStandard(inShd):
    if ':' in inShd:
        aiName = inShd.rsplit(':')[-1] + '_new'
    else:
        aiName = inShd + '_new'

    # print 'creating '+ aiName
    outNode = cmds.shadingNode('aiStandardSurface', name=aiName, asShader=True)

    convertAttr(inShd, 'Kd', outNode, 'base')
    convertAttr(inShd, 'color', outNode, 'baseColor')
    convertAttr(inShd, 'diffuseRoughness', outNode, 'diffuseRoughness')

    convertAttr(inShd, 'Ks', outNode, 'specular')
    convertAttr(inShd, 'KsColor', outNode, 'specularColor')
    convertAttr(inShd, 'specularRoughness', outNode, 'specularRoughness')

    convertAttr(inShd, 'specularAnisotropy', outNode, 'specularAnisotropy', anisotropyRemap)

    convertAttr(inShd, 'specularRotation', outNode, 'specularRotation', rotationRemap)
    convertAttr(inShd, 'Kt', outNode, 'transmission')

    convertAttr(inShd, 'KtColor', outNode, 'transmissionColor')  # not multiplying by transmittance

    # transmission_depth => (transmittance == AI_RGB_WHITE) ? 0.0 : 1.0
    convertAttr(inShd, 'dispersionAbbe', outNode, 'transmissionDispersion')  # not multiplying by transmittance

    # transmission_extra_roughness => refraction_roughness - specular_roughness

    convertAttr(inShd, 'Ksss', outNode, 'subsurface')
    convertAttr(inShd, 'KsssColor', outNode, 'subsurfaceColor')
    convertAttr(inShd, 'sssRadius', outNode, 'subsurfaceRadius')

    convertAttr(inShd, 'Kr', outNode, 'coat')
    convertAttr(inShd, 'KrColor', outNode, 'coatColor')
    cmds.setAttr(outNode + '.coat_roughness', 0)

    convertAttr(inShd, 'emission', outNode, 'emission')
    convertAttr(inShd, 'emissionColor', outNode, 'emissionColor')
    convertAttr(inShd, 'opacity', outNode, 'opacity')

    # caustics => enable_glossy_caustics || enable_reflective_caustics || enable_refractive_caustics
    convertAttr(inShd, 'enable_internal_reflections', outNode, 'internal_reflections')
    convertAttr(inShd, 'indirect_diffuse', outNode, 'indirect_diffuse')
    convertAttr(inShd, 'indirect_specular', outNode, 'indirect_specular')
    # exit_to_background => reflection_exit_use_environment || refraction_exit_use_environment

    convertAttr(inShd, 'normalCamera', outNode, 'normalCamera')  # not multiplying by transmittance
    print ("Converted %s to aiStandardSurface" % inShd)
    return outNode

def convert():
    phongs = pm.ls(type="phong")
    for phong in phongs:
        phong_name = phong.getName()
        new_mtl = convertAiStandard(phong)
        mtoa.convertShaders.assignToNewShader(phong_name, new_mtl)
        mtoa.convertShaders.setValue("%s.specular" % phong_name, 0)

    textures = pm.ls(type="file")
    for texture in textures:
        print
        dir(texture)
        old_path = texture.getAttr("fileTextureName")
        filename = os.path.basename(old_path)
        new_path = os.path.join(r"T:\24h\assets\jingansi\publish\texture\jingansi", filename)
        texture.setAttr("fileTextureName", new_path)