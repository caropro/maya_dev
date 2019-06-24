# coding=utf-8
# author:Jonathon Woo
# version:1.0.0
import pymel.core as pm
import maya.cmds as cmds
import maya
import os
from PySide2 import QtWidgets

class LODWindow(object):
    """A pymel class for an level-of-detail editing window"""
    ## unique handle for the window
    WINDOW_NAME = 'Proxy Attribute'
    OVERRIDE = ['Use Global Settings','Use Local Settings','Bounding Box',"Disable Draw","Disable Load"]
    MODE = ['Bounding Box','Per Object Bounding Box','Polywire',"Wireframe","Point Cloud","Shaded Polywire","Shaded"]
    def __init__(self):
        self.current_selected_arStandIn = cmds.ls(sl=True, dag=True, type="aiStandIn")
        self.use_filesequence_status = False
    def create(self):
        # destroy the window if it already exists
        try:
            pm.deleteUI(self.WINDOW_NAME, window=True)
        except:
            pass
        # draw the window
        with pm.window(self.WINDOW_NAME) as res_window:
            with pm.columnLayout(adjustableColumn=True) as col:
                # part1_a#####################################################################################
                pm.rowLayout(numberOfColumns=2)
                self.input_path = cmds.textFieldGrp(label='Path', text='', editable=True,changeCommand=pm.Callback(self.path_input))
                cmds.iconTextButton(style='iconOnly', image1='folder-open.png', label='folder',command=pm.Callback(self.path_view))
                cmds.setParent(col)
                # part1_b#####################################################################################
                pm.columnLayout(adjustableColumn=True)
                self.viewport_override = cmds.optionMenuGrp(label='Viewport Override', columnWidth=(5, 20),changeCommand=pm.Callback(self.change_override))
                cmds.menuItem(label='Use Global Settings')
                cmds.menuItem(label='Use Local Settings')
                cmds.menuItem(label='Bounding Box')
                cmds.menuItem(label="Disable Draw")
                cmds.menuItem(label="Disable Load")
                self.viewport_draw_mode = cmds.optionMenuGrp(label='Viewport Draw Mode', columnWidth=(7, 20),changeCommand=pm.Callback(self.changedraw_mode))
                cmds.menuItem(label='Bounding Box')
                cmds.menuItem(label='Per Object Bounding Box')
                cmds.menuItem(label='Polywire')
                cmds.menuItem(label="Wireframe")
                cmds.menuItem(label="Point Cloud")
                cmds.menuItem(label="Shaded Polywire")
                cmds.menuItem(label="Shaded")
                pm.separator(style='in', height=4)
                # p2#####################################################################################
                cmds.checkBox(label='Use File Sequence', value=False, onCommand=pm.Callback(self.use_fileseq,True),
                              offCommand=pm.Callback(self.use_fileseq,False))
                self.frame_loop = cmds.checkBox(label='FrameLoop', value=False,enable=False,
                                                      onCommand=pm.Callback(self.seq_loop, True),
                                                      offCommand=pm.Callback(self.seq_loop, False))
                self.frame = cmds.floatFieldGrp(numberOfFields=1, label='Frame', value1=1,changeCommand=pm.Callback(self.frame_change))
                self.timeoffset = cmds.floatFieldGrp(numberOfFields=1, label='Frame Offset', value1=0.00,changeCommand=pm.Callback(self.time_offset))
                pm.separator(style='in', height=4)
                # p3#####################################################################################
                cmds.checkBox(label='RenderState', value=True,
                              onCommand=pm.Callback(self.checkbox, "RenderState", True),
                              offCommand=pm.Callback(self.checkbox, "RenderState", False))
                cmds.checkBox(label='Visibility', value=True, onCommand=pm.Callback(self.checkbox, "Visibility", True),
                              offCommand=pm.Callback(self.checkbox, "Visibility", False))
                self.status_line = pm.textField(editable=False)
                cmds.textScrollList("Current_selection", numberOfRows=8, allowMultiSelection=True,
                                    append=self.current_selected_arStandIn, showIndexedItem=4,
                                    selectCommand=pm.Callback(self.refresh, True))
                cmds.button(label=u"刷新选择", command=pm.Callback(self.refresh))
                pm.text(label=u'此面板参数一经修改，就会影响所选ArnoldStandIn中含有对应属性的数值')
            res_window.setWidthHeight((500, 400))

    def refresh(self,use_selection=False):
        if use_selection:
            cmds.select(clear=True)
            current_selected_items = cmds.textScrollList( "Current_selection",q=True,selectItem=True)
            cmds.select(current_selected_items)
            self.current_selected_arStandIn = current_selected_items
        else:
            cmds.textScrollList("Current_selection",e=True,removeAll=True)
            self.current_selected_arStandIn = cmds.ls(sl=True, dag=True, type="aiStandIn")
            cmds.textScrollList("Current_selection", e=True, append=self.current_selected_arStandIn)
    def path_input(self):
        current_path = cmds.textFieldGrp(self.input_path, q=True, text=True)
        for proxy_node in self.current_selected_arStandIn:
            cmds.setAttr("%s.dso" % proxy_node, current_path, type='string')
    def path_view(self):
        src_path = src_path = pm.fileDialog2(fileMode=1,fileFilter="Proxy Files (*.ass *.ass.gz)")[0]
        for proxy_node in self.current_selected_arStandIn:
            cmds.setAttr("%s.dso" % proxy_node, src_path, type='string')

    def change_override(self):
        current_index = self.OVERRIDE.index(cmds.optionMenuGrp(self.viewport_override,q=True,value=True))
        for proxy_node in self.current_selected_arStandIn:
            cmds.setAttr("%s.standInDrawOverride" % proxy_node, current_index)

    def changedraw_mode(self):
        current_index = self.MODE.index(cmds.optionMenuGrp(self.viewport_draw_mode,q=True,value=True))
        for proxy_node in self.current_selected_arStandIn:
            cmds.setAttr("%s.mode" % proxy_node, current_index)

    def use_fileseq(self,value):
        self.use_filesequence_status = value
        cmds.checkBox(self.frame_loop, e=True, enable=value)
        if value:
            cmds.floatFieldGrp(self.frame, edit=True, enable=False)
            for proxy_node in self.current_selected_arStandIn:
                cmds.setAttr("%s.useFrameExtension" % proxy_node, 1)
        else:
            cmds.floatFieldGrp(self.frame, edit=True, enable=True)
            for proxy_node in self.current_selected_arStandIn:
                cmds.setAttr("%s.useFrameExtension" % proxy_node, 0)

    def seq_loop(self,value):
        if value:
            for proxy_node in self.current_selected_arStandIn:
                proxy_node_file = cmds.getAttr("%s.dso"% proxy_node)
                proxy_node_filedir = os.path.dirname(proxy_node_file)
                proxy_node_filename = os.path.basename(proxy_node_file).split(".")[0]
                frame_count = len([f for f in os.listdir(proxy_node_filedir) if f.startswith(proxy_node_filename) and ".ass" in f])
                current_expression = cmds.listConnections("%s.frameNumber"%proxy_node, type="expression")
                if current_expression:
                    current_expression=current_expression[0]
                    cmds.expression(current_expression, e=True, s="{}.frameNumber=frame%{}".format(proxy_node,frame_count), o=proxy_node, ae=1, uc=all)
                else:
                    cmds.expression(s="{}.frameNumber=frame%{}".format(proxy_node,frame_count), o=proxy_node, ae=1, uc=all)
        else:
            for proxy_node in self.current_selected_arStandIn:
                current_expression = cmds.listConnections(proxy_node, type="expression")
                if current_expression:
                    current_expression = current_expression[0]
                    cmds.expression(current_expression, e=True, s="{}.frameNumber=frame".format(proxy_node), o=proxy_node, ae=1, uc=all)

    def frame_change(self):
        frame = cmds.floatFieldGrp(self.frame,q=True,value=True)[0]
        expression_attention = False
        for proxy_node in self.current_selected_arStandIn:
            current_expression = cmds.listConnections(proxy_node, type="expression")
            if not current_expression:
                cmds.setAttr("%s.frameNumber" % proxy_node, frame)
            else:
                expression_attention=True
        if expression_attention:
            pm.inViewMessage(smg=u"有表达式连接在frame节点！！！！！！", pos="midCenterTop", bkc=0x00FF1010, fade=True)

    def time_offset(self):
        offset = cmds.floatFieldGrp(self.timeoffset, q=True, value=True)[0]
        for proxy_node in self.current_selected_arStandIn:
            cmds.setAttr("%s.frameOffset" % proxy_node, offset)
    def checkbox(self, trigger_name, value):
        if trigger_name == "RenderState":
            for proxy_node in self.current_selected_arStandIn:
                cmds.setAttr("%s.primaryVisibility"%proxy_node,value)
        else:
            for proxy_node in self.current_selected_arStandIn:
                cmds.setAttr("%s.visibility"%proxy_node,value)


def run():
    LODWindow().create()
