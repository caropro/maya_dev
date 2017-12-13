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
    errolist = []
    for setting_dic in default_setting.values():
        for parm,value in setting_dic.items():
            if not value==None:
                try:
                    pm.setAttr(parm,value)
                    print parm, value, type(value)
                except:
                    errolist.append((parm,value))
                    continue

    current_path = pm.mel.eval("file -q -sn")
    filename = os.path.basename(current_path)
    render_name = os.path.splitext(filename)[0]

    rp_code = os.path.dirname(current_path).split("/")[-1]
    renderdir = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "render", render_name)

    renderpath = os.path.join(renderdir, render_name).replace("\\", "/").replace(":", ":/")

    pm.mel.eval('setAttr -type "string" defaultRenderGlobals.imageFilePrefix "%s"'% renderpath)
    if create_aov():
        print errolist
        pm.inViewMessage(smg="Render Setting Done\nthe error list show on the script editor" % errolist,
                         pos="midCenter", bkc=0x00FF1010, fade=True)
        return pm.inViewMessage(smg="aov created",pos="midCenterTop",bkc=0x00FF1060,fade=True)
    else:
        print errolist
        pm.inViewMessage(smg="Render Setting Done\nthe error list show on the script editor" % errolist,
                         pos="midCenter", bkc=0x00FF1010, fade=True)
        return pm.inViewMessage(smg="aov-create failed", pos="midCenterTop", bkc=0x00FF1010, fade=True)


def create_aov():
    print "create_aov"
    try:
        pm.mel.eval("AEnewNonNumericMultiAddNewItem")
        pm.mel.eval("AEnewNonNumericMultiAddNewItem")
    except:
        pass
    try:
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
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % N)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % N, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % N, f=True)
        pm.connectAttr('%s.message' % N, 'defaultArnoldRenderOptions.aovList[0]', f=True)
        # position node
        P = pm.createNode("aiAOV", name="aov_P")
        pm.setAttr("%s.name" % P, "P")
        pm.setAttr("%s.type" % P, 7)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % P)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % P, f=True)
        pm.connectAttr('%s.message' % closest_filter, '%s.outputs[0].filter' % P, f=True)
        pm.connectAttr('%s.message' % P, 'defaultArnoldRenderOptions.aovList[1]', f=True)
        # depth_z node
        Z = pm.createNode("aiAOV", name="aov_Z")
        pm.setAttr("%s.name" % Z, "Z")
        pm.setAttr("%s.type" % Z, 4)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % Z)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % Z, f=True)
        pm.connectAttr('%s.message' % closest_filter, '%s.outputs[0].filter' % Z, f=True)
        pm.connectAttr('%s.message' % Z, 'defaultArnoldRenderOptions.aovList[2]', f=True)
        # diffuse
        diffuse = pm.createNode("aiAOV", name="aov_diffuse")
        pm.setAttr("%s.name" % diffuse, "diffuse")
        pm.setAttr("%s.type" % diffuse, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse, f=True)
        pm.connectAttr('%s.message' % diffuse, 'defaultArnoldRenderOptions.aovList[3]', f=True)
        # diffuse_albedo
        diffuse_albedo = pm.createNode("aiAOV", name="aov_diffuse_albedo")
        pm.setAttr("%s.name" % diffuse_albedo, "diffuse_albedo")
        pm.setAttr("%s.type" % diffuse_albedo, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_albedo)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_albedo, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_albedo, f=True)
        pm.connectAttr('%s.message' % diffuse_albedo, 'defaultArnoldRenderOptions.aovList[4]', f=True)
        # diffuse_direct_amb
        diffuse_direct_amb = pm.createNode("aiAOV", name="aov_diffuse_direct_amb")
        pm.setAttr("%s.name" % diffuse_direct_amb, "diffuse_direct_amb")
        pm.setAttr("%s.type" % diffuse_direct_amb, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_direct_amb)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_direct_amb, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_direct_amb, f=True)
        pm.connectAttr('%s.message' % diffuse_direct_amb, 'defaultArnoldRenderOptions.aovList[5]', f=True)
        # diffuse_fill
        diffuse_fill = pm.createNode("aiAOV", name="aov_diffuse_fill")
        pm.setAttr("%s.name" % diffuse_fill, "diffuse_fill")
        pm.setAttr("%s.type" % diffuse_fill, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_fill)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_fill, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_fill, f=True)
        pm.connectAttr('%s.message' % diffuse_fill, 'defaultArnoldRenderOptions.aovList[6]', f=True)
        # diffuse_indirect_amb
        diffuse_indirect_amb = pm.createNode("aiAOV", name="aov_diffuse_indirect_amb")
        pm.setAttr("%s.name" % diffuse_indirect_amb, "diffuse_indirect_amb")
        pm.setAttr("%s.type" % diffuse_indirect_amb, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_indirect_amb)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_indirect_amb, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_indirect_amb, f=True)
        pm.connectAttr('%s.message' % diffuse_indirect_amb, 'defaultArnoldRenderOptions.aovList[7]', f=True)
        # diffuse_key
        diffuse_key = pm.createNode("aiAOV", name="aov_diffuse_key")
        pm.setAttr("%s.name" % diffuse_key, "diffuse_key")
        pm.setAttr("%s.type" % diffuse_key, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_key)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_key, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_key, f=True)
        pm.connectAttr('%s.message' % diffuse_key, 'defaultArnoldRenderOptions.aovList[8]', f=True)
        # diffuse_rim
        diffuse_rim = pm.createNode("aiAOV", name="aov_diffuse_rim")
        pm.setAttr("%s.name" % diffuse_rim, "diffuse_rim")
        pm.setAttr("%s.type" % diffuse_rim, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % diffuse_rim)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % diffuse_rim, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % diffuse_rim, f=True)
        pm.connectAttr('%s.message' % diffuse_rim, 'defaultArnoldRenderOptions.aovList[9]', f=True)
        # emission
        emission = pm.createNode("aiAOV", name="aov_emission")
        pm.setAttr("%s.name" % emission, "emission")
        pm.setAttr("%s.type" % emission, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % emission)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % emission, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % emission, f=True)
        pm.connectAttr('%s.message' % emission, 'defaultArnoldRenderOptions.aovList[10]', f=True)
        # motionvector
        motionvector = pm.createNode("aiAOV", name="aov_motionvector")
        pm.setAttr("%s.name" % motionvector, "motionvector")
        pm.setAttr("%s.type" % motionvector, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % motionvector)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % motionvector, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % motionvector, f=True)
        pm.connectAttr('%s.message' % motionvector, 'defaultArnoldRenderOptions.aovList[11]', f=True)
        # specular
        specular = pm.createNode("aiAOV", name="aov_specular")
        pm.setAttr("%s.name" % specular, "specular")
        pm.setAttr("%s.type" % specular, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular, f=True)
        pm.connectAttr('%s.message' % specular, 'defaultArnoldRenderOptions.aovList[12]', f=True)
        # specular_albedo
        specular_albedo = pm.createNode("aiAOV", name="aov_specular_albedo")
        pm.setAttr("%s.name" % specular_albedo, "specular_albedo")
        pm.setAttr("%s.type" % specular_albedo, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_albedo)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_albedo, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_albedo, f=True)
        pm.connectAttr('%s.message' % specular_albedo, 'defaultArnoldRenderOptions.aovList[13]', f=True)
        # specular_amb
        specular_amb = pm.createNode("aiAOV", name="aov_specular_amb")
        pm.setAttr("%s.name" % specular_amb, "specular_amb")
        pm.setAttr("%s.type" % specular_amb, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_amb)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_amb, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_amb, f=True)
        pm.connectAttr('%s.message' % specular_amb, 'defaultArnoldRenderOptions.aovList[14]', f=True)
        # specular_direct_amb
        specular_direct_amb = pm.createNode("aiAOV", name="aov_specular_direct_amb")
        pm.setAttr("%s.name" % specular_direct_amb, "specular_direct_amb")
        pm.setAttr("%s.type" % specular_direct_amb, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_direct_amb)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_direct_amb, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_direct_amb, f=True)
        pm.connectAttr('%s.message' % specular_direct_amb, 'defaultArnoldRenderOptions.aovList[15]', f=True)
        # specular_fill
        specular_fill = pm.createNode("aiAOV", name="aov_specular_fill")
        pm.setAttr("%s.name" % specular_fill, "specular_fill")
        pm.setAttr("%s.type" % specular_fill, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_fill)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_fill, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_fill, f=True)
        pm.connectAttr('%s.message' % specular_fill, 'defaultArnoldRenderOptions.aovList[16]', f=True)
        # specular_indirect_amb
        specular_indirect_amb = pm.createNode("aiAOV", name="aov_specular_indirect_amb")
        pm.setAttr("%s.name" % specular_indirect_amb, "specular_indirect_amb")
        pm.setAttr("%s.type" % specular_indirect_amb, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_indirect_amb)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_indirect_amb, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_indirect_amb, f=True)
        pm.connectAttr('%s.message' % specular_indirect_amb, 'defaultArnoldRenderOptions.aovList[17]', f=True)
        # specular_key
        specular_key = pm.createNode("aiAOV", name="aov_specular_key")
        pm.setAttr("%s.name" % specular_key, "specular_key")
        pm.setAttr("%s.type" % specular_key, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_key)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_key, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_key, f=True)
        pm.connectAttr('%s.message' % specular_key, 'defaultArnoldRenderOptions.aovList[18]', f=True)
        # specular_rim
        specular_rim = pm.createNode("aiAOV", name="aov_specular_rim")
        pm.setAttr("%s.name" % specular_rim, "specular_rim")
        pm.setAttr("%s.type" % specular_rim, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % specular_rim)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % specular_rim, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % specular_rim, f=True)
        pm.connectAttr('%s.message' % specular_rim, 'defaultArnoldRenderOptions.aovList[19]', f=True)
        # sss
        sss = pm.createNode("aiAOV", name="aov_sss")
        pm.setAttr("%s.name" % sss, "sss")
        pm.setAttr("%s.type" % sss, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % sss)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % sss, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % sss, f=True)
        pm.connectAttr('%s.message' % sss, 'defaultArnoldRenderOptions.aovList[20]', f=True)
        # sss_albedo
        sss_albedo = pm.createNode("aiAOV", name="aov_sss_albedo")
        pm.setAttr("%s.name" % sss_albedo, "sss_albedo")
        pm.setAttr("%s.type" % sss_albedo, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % sss_albedo)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % sss_albedo, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % sss_albedo, f=True)
        pm.connectAttr('%s.message' % sss_albedo, 'defaultArnoldRenderOptions.aovList[21]', f=True)
        # transmission
        transmission = pm.createNode("aiAOV", name="aov_transmission")
        pm.setAttr("%s.name" % transmission, "transmission")
        pm.setAttr("%s.type" % transmission, 5)
        pm.mel.eval('AEnewNonNumericMultiAddNewItem("%s","outputs")' % transmission)
        pm.connectAttr('defaultArnoldDriver.message', '%s.outputs[0].driver' % transmission, f=True)
        pm.connectAttr('defaultArnoldFilter.message', '%s.outputs[0].filter' % transmission, f=True)
        pm.connectAttr('%s.message' % transmission, 'defaultArnoldRenderOptions.aovList[22]', f=True)
        return 1
    except:
        return False