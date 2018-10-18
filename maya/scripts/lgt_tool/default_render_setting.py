#coding=utf-8
import json
import os
import pymel.core as pm
import mtoa.aovs as aovs
from pymel import versions

maya_version=versions.current()
if "2017" in str(maya_version):
    config=os.path.join(os.path.dirname(__file__), "config_2017.json")
    version_code="2017"
elif "2018" in str(maya_version):
    config = os.path.join(os.path.dirname(__file__), "config.json")
    version_code="2018"
else:
    config = os.path.join(os.path.dirname(__file__), "config.json")
    version_code="old"
with open(config, 'r') as f:
    data = json.load(f)
    print (data)
arnold=data["arnold"]

def run(default_setting=arnold,version_code=version_code):
    pm.mel.eval('unifiedRenderGlobalsWindow')
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
        pm.inViewMessage(smg="%s Render Setting Done\nthe error list show on the script editor" % version_code,
                         pos="midCenter", bkc=0x00FF1010, fade=True)
        return pm.inViewMessage(smg="aov created",pos="midCenterTop",bkc=0x00FF1060,fade=True)
    else:
        print errolist
        pm.inViewMessage(smg="%s Render Setting Done\nthe error list show on the script editor" % version_code,
                         pos="midCenter", bkc=0x00FF1010, fade=True)
        return pm.inViewMessage(smg="aov-create failed", pos="midCenterTop", bkc=0x00FF1010, fade=True)


def create_aov():
    print "create_aov"

    try:
        aov_dict={"N":"rgb","P":"vector","Z":"float","diffuse":"rgb","diffuse_albedo":"rgb","diffuse_direct_amb":"rgb","diffuse_fill":"rgb","diffuse_indirect_amb":"rgb","diffuse_key":"rgb","diffuse_rim":"rgb","emission":"rgb","motionvector":"rgb","specular":"rgb","specular_albedo":"rgb","specular_amb":"rgb","specular_direct_amb":"rgb","specular_fill":"rgb",
                  "specular_indirect_amb":"rgb","specular_key":"rgb","specular_rim":"rgb","sss":"rgb","sss_albedo":"rgb","transmission":"rgb"}
        for name,type in aov_dict.items():
            aovs.AOVInterface().addAOV(name,type)

        return 1
    except:
        return False
