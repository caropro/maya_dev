import pymel.core as pm
import os

def run():
    current_path = pm.mel.eval("file -q -sn")
    filename = os.path.basename(current_path)
    render_name = os.path.splitext(filename)[0]

    if "." in render_name:
        render_name = render_name.split(".")[0]
    else:
        render_name = render_name.split("_e")[0]

    rp_code = os.path.dirname(current_path).split("/")[-1]
    renderlayer=pm.ls(type="renderLayer")
    layercount=len(renderlayer)
    if layercount==1:
        renderdir = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "render", render_name)
    else:
        renderdir = os.path.join(os.path.dirname(current_path)[:-len(rp_code)], "render", render_name,"<RenderLayer>")

    renderpath = os.path.join(renderdir, render_name).replace("\\", "/").replace(":", ":/")

    pm.mel.eval('setAttr -type "string" defaultRenderGlobals.imageFilePrefix "%s"'% renderpath)