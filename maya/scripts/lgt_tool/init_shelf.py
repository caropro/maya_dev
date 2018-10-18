# coding=utf8
# if the shelf exist delete old button else create the shelf
import maya.cmds as cmds
import pymel.core as pm
jud = cmds.shelfLayout("lgt_tool_set", ex=True)

if not jud:
    sh1 = cmds.shelfLayout("lgt_tool_set", style="iconAndTextVertical", p="ShelfLayout", backgroundColor=(.1, .1, .4))
else:
    shelf_buttons = cmds.shelfLayout("lgt_tool_set", q=True, ca=True)
    if shelf_buttons:
        for shelf_button in shelf_buttons:
            cmds.deleteUI(shelf_button)
    sh1 = "lgt_tool_set"

sh1b1 = cmds.shelfButton(p=sh1, image="lightBulb.png",
                         label="4lights", annotation="4lights",
                         command="import lgt_tool.create_default_light as cdl\nreload(cdl)\ncdl.run()",
                         imageOverlayLabel="4lights",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))

sh1b2 = cmds.shelfButton(p=sh1, image1="render.png",
                         label="render_setting", annotation="render_setting",
                         command="import lgt_tool.default_render_setting as drs\nreload(drs)\ndrs.run()",
                         imageOverlayLabel="render_setting",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b3 = cmds.shelfButton(p=sh1, image="setKeyOnAnim.png",
                         label="render_path", annotation="render_path",
                         command="import lgt_tool.set_renderpath as srp\nreload(srp)\nsrp.run()",
                         imageOverlayLabel="render_path",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))

sh1b4 = cmds.shelfButton(p=sh1, image="render_blendTwoAttr.png",
                         label="Convert_phong", annotation="Convert_phong",
                         command="import lgt_tool.convert_mtl as cm\nreload(cm)\ncm.convert()",
                         imageOverlayLabel="Convert_phong",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))
sh1b5 = cmds.shelfButton(p=sh1, image="render_blendTwoAttr.png",
                         label="t_m", annotation="Convert_t_m",
                         command="import lgt_tool.t_to_m as t_to_m\nreload(t_to_m)\nt_to_m.convert()",
                         imageOverlayLabel="Convert_t_to_m",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))
sh1b6 = cmds.shelfButton(p=sh1, image="render_blendTwoAttr.png",
                         label="PATH", annotation="PATH",
                         command="import lgt_tool.asset_re_path as rp\nreload(rp)\nrp.main()",
                         imageOverlayLabel="RP",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))

sh1 = cmds.shelfLayout("lgt_tool_set", q=True, fpn=True)
tempDir = cmds.internalVar(ush=True)

cmds.saveShelf(sh1, (tempDir + 'lgt_shelf_tool_set'))

