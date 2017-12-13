#coding=utf-8
import json
import os
import pymel.core as pm
config=os.path.join(os.path.dirname(__file__), "config.json")
with open(config, 'r') as f:
 data = json.load(f)
 print (data)
arnold=data["arnold"]

def run(default_setting=arnold):
    create_aov()
    print 666666666666666666666666666
    connect_aov()
    return


def create_aov():
    print "create_aov"
    # create filter
    # default_filter
    pm.setAttr("defaultArnoldFilter.aiTranslator", 'gaussian')
    # closest_filter
    closest_filter = pm.createNode('aiAOVFilter', name="closest_filter")
    pm.setAttr("%s.aiTranslator" % closest_filter, 'closest')

    # normal node
    N = pm.createNode("aiAOV", name="aov_N")
    pm.setAttr("%s.name" % N, "N")
    pm.setAttr("%s.type" % N, 5)


def connect_aov():
    pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % "aov_N")
    pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % "aov_N", f=True)
    pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % "aov_N", f=True)
    pm.connectAttr('%s.message' % "aov_N", 'defaultArnoldRenderOptions.aovList[0]', f=True)
