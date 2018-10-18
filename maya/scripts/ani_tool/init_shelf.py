# coding=utf8
# if the shelf exist delete old button else create the shelf
import maya.cmds as cmds
import pymel.core as pm
jud = cmds.shelfLayout("tool_set", ex=True)
# if jud:
#    cmds.deleteUI("tool_set")
# sh1 = cmds.shelfLayout("tool_set", style="iconAndTextVertical",p="ShelfLayout",backgroundColor=(.1, .4, .2))

if not jud:
    sh1 = cmds.shelfLayout("tool_set", style="iconAndTextVertical", p="ShelfLayout", backgroundColor=(.1, .4, .2))
else:
    shelf_buttons = cmds.shelfLayout("tool_set", q=True, ca=True)
    if shelf_buttons:
        for shelf_button in shelf_buttons:
            cmds.deleteUI(shelf_button)
    sh1 = "tool_set"

sh1b1 = cmds.shelfButton(p=sh1, image="Wax.png",
                         label="abc_export2017", annotation="abc_export2017",
                         command="import ani_tool.dealnamespace_and_export_selection_abc as export_abc_re\nreload(export_abc_re)\nexport_abc_re.main()",
                         imageOverlayLabel="r2017abc",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))

sh1b2 = cmds.shelfButton(p=sh1, image1="Wax.png",
                         label="2017abc", annotation="2017abc",
                         command="import ani_tool.export_selection_abc as export_abc\nreload(export_abc)\nexport_abc.main()",
                         imageOverlayLabel="2017abc",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b3 = cmds.shelfButton(p=sh1, image="Wax.png",
                         label="abc_export2014", annotation="abc_export2014",
                         command="import ani_tool.dealnamespace_and_export_selection_abc_14 as export_abc_re\nreload(export_abc_re)\nexport_abc_re.main()",
                         imageOverlayLabel="r2014abc",
                         overlayLabelColor=(.8, .1, .4),
                         overlayLabelBackColor=(0.1, .1, .1, .8))

sh1b4 = cmds.shelfButton(p=sh1, image1="Wax.png",
                         label="2014abc", annotation="2014abc",
                         command="import ani_tool.export_selection_abc14 as export_abc\nreload(export_abc)\nexport_abc.main()",
                         imageOverlayLabel="2014abc",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b5 = cmds.shelfButton(p=sh1, image1="cameraAim.png",
                         label="view_reset", annotation="view_reset",
                         command="import ani_tool.reset_view as reset_view\nreload(reset_view)\nreset_view.main()",
                         imageOverlayLabel="view_reset",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b6 = cmds.shelfButton(p=sh1, image1="cameraAim.png",
                         label="ZoomPan", annotation="ZoomPan",
                         command="import pymel.core as pm\npm.mel.eval('PanZoomTool')\npm.mel.eval('ToggleToolSettings')",
                         imageOverlayLabel="ZoomPan",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b7 = cmds.shelfButton(p=sh1, image1="playblast.png",
                         label="playblast", annotation="playblast",
                         command="import ani_tool.play_blast as play_blast\nreload(play_blast)\nplay_blast.main()",
                         imageOverlayLabel="playblast",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b8 = cmds.shelfButton(p=sh1, image1="rename.png",
                         label="remove_namespace_all", annotation="remove_namespace_all",
                         command="import ani_tool.remove_namespace_all as rename\nreload(rename)\nrename.main()",
                         imageOverlayLabel="remove_namespace_all",
                         overlayLabelColor=(.1, .1, .9),
                         overlayLabelBackColor=(1, .25, .25, .5))

sh1b9 = cmds.shelfButton(p=sh1, image="Wax.png",
                         label="2017", annotation="2017exportselection",
                         command="import ani_tool.sel_abc2017 as sel_abc2017\nreload(sel_abc2017)\nsel_abc2017.main()",
                         imageOverlayLabel="r2017selection",
                         overlayLabelColor=(.3, .1, .4),
                         overlayLabelBackColor=(0.1, 1, .1, .8))

sh1b10 = cmds.shelfButton(p=sh1, image="Wax.png",
                         label="2014", annotation="2014exportselection",
                         command="import ani_tool.sel_abc2014 as sel_abc2014\nreload(sel_abc2014)\nsel_abc2014.main()",
                         imageOverlayLabel="r2014selection",
                         overlayLabelColor=(.3, .1, .4),
                         overlayLabelBackColor=(0.1, 1, .1, .8))

sh1b11 = cmds.shelfButton(p=sh1, image="zoom.png",
                         label="clip_far", annotation="clip_far",
                         command="""import pymel.core as pm\npm.mel.eval('setAttr "perspShape.farClipPlane" 10000000')""",
                         imageOverlayLabel="clip_far",
                         overlayLabelColor=(.3, .1, .4),
                         overlayLabelBackColor=(0.1, 1, .95, .1))

sh1 = cmds.shelfLayout("tool_set", q=True, fpn=True)
tempDir = cmds.internalVar(ush=True)

cmds.saveShelf(sh1, (tempDir + 'shelf_tool_set'))

