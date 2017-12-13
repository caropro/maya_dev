#coding=utf-8
import pymel.core as pm
import mtoa.utils as mutils

print("ready for creating lights")
def run():
    amb_lgt = mutils.createLocatorWithName("aiSkyDomeLight", nodeName="amb_lgt", asLight=True)
    pm.setAttr('%s.aiAov' % amb_lgt[0], "amb", type="string")
    pm.setAttr('%s.aiSamples' % amb_lgt[0], 3)

    fill_lgt = pm.directionalLight(name="fill_lgt")
    pm.setAttr('%s.aiAov' % fill_lgt, "fill", type="string")
    pm.setAttr('%s.aiSamples' % fill_lgt, 3)

    rim_lgt = pm.directionalLight(name="rim_lgt")
    pm.setAttr('%s.aiAov' % rim_lgt, "rim_lgt", type="string")
    pm.setAttr('%s.aiSamples' % rim_lgt, 3)

    key_lgt = pm.directionalLight(name="key_lgt")
    pm.setAttr('%s.aiAov' % key_lgt, "key_lgt", type="string")
    pm.setAttr('%s.aiSamples' % key_lgt, 3)
    return
