# coding=utf-8
# author:Jonathon Woo
# version:1.0.0
import pymel.core as pm
import maya.cmds as cmds
import mtoa.ui.ae.utils as aeUtils
import maya

class LODWindow(object):
    """A pymel class for an level-of-detail editing window"""
    ## unique handle for the window
    WINDOW_NAME = 'light Attribute'

    def __init__(self):
        all_light = cmds.ls(lt=True)
        current_selection = cmds.ls(sl=True, dag=True)
        self.current_selected_lights = [x for x in current_selection if x in all_light]

    def create(self):
        # destroy the window if it already exists
        try:
            pm.deleteUI(self.WINDOW_NAME, window=True)
        except:
            pass
        # draw the window
        with pm.window(self.WINDOW_NAME) as res_window:
            with pm.columnLayout(adjustableColumn=True):
                cmds.checkBox(label='Use Color Temperature', onCommand=pm.Callback(self.test, True),
                              offCommand=pm.Callback(self.test, False))
                self.canvasName = cmds.canvas(rgbValue=(1, 0, 1), width=100, height=20)
                self.tempertaure = cmds.intSliderGrp(field=True, label='Temperature', minValue=0, maxValue=15000,
                                                     fieldMinValue=1000,
                                                     fieldMaxValue=100000000376832, value=6500, enable=False,
                                                     changeCommand=pm.Callback(self.set_aiColorTemperature))
                pm.separator(style='in', height=4)
                self.exposure = cmds.floatSliderGrp(label='Exposure', field=True, minValue=-5.0, maxValue=5.0,
                                                    fieldMinValue=-100.0,
                                                    fieldMaxValue=100.0, value=5,
                                                    changeCommand=pm.Callback(self.set_float_attr, exposure=True))

                pm.separator(style='in', height=4)
                self.sample = cmds.intSliderGrp(field=True, label='Samples', minValue=0, maxValue=10,
                                                fieldMinValue=0,
                                                fieldMaxValue=20, value=1,
                                                changeCommand=pm.Callback(self.set_int_attr, sample=True))
                self.radius = cmds.floatSliderGrp(label='Radius', field=True, minValue=0, maxValue=10.0,
                                                  fieldMinValue=0,
                                                  fieldMaxValue=100.0, value=0,
                                                  changeCommand=pm.Callback(self.set_float_attr, radius=True))
                cmds.checkBox(label='Normalize',value=True, onCommand=pm.Callback(self.checkbox,"n",True),
                              offCommand=pm.Callback(self.checkbox,"n", False))

                pm.separator(style='in', height=4)
                cmds.checkBox(label='Cast Shadows',value=True, onCommand=pm.Callback(self.checkbox,"cs",True),
                              offCommand=pm.Callback(self.checkbox,"cs", False))
                self.shadow_density = cmds.floatSliderGrp(label='Shadow Density', field=True, minValue=0, maxValue=1,
                                    fieldMinValue=0, fieldMaxValue=1, value=1.0,
                                                          changeCommand=pm.Callback(self.set_float_attr, shadow_density=True))

                pm.separator(style='in', height=4)
                cmds.checkBox(label='Cast Volumetric Shadows',value=True, onCommand=pm.Callback(self.checkbox,"cvs",True),
                              offCommand=pm.Callback(self.checkbox,"cvs", False))
                self.volumeSamples = cmds.intSliderGrp(field=True, label='Volume Sample', minValue=0, maxValue=10,
                                                fieldMinValue=0,
                                                fieldMaxValue=20, value=2,changeCommand=pm.Callback(self.set_int_attr, volumeSamples=True))

                self.status_line = pm.textField(editable=False)
                cmds.button(label=u"刷新选择",command=pm.Callback(self.refresh))
                pm.text(label=u'此面板参数一经修改，就会影响所选灯光中含有对应属性的数值')
            res_window.setWidthHeight((500, 400))
    def refresh(self):
        all_light = cmds.ls(lt=True)
        current_selection = cmds.ls(sl=True, dag=True)
        self.current_selected_lights = [x for x in current_selection if x in all_light]
    def checkbox(self,type,value):
        if type=="n":
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiNormalize" % light, value)
                except:
                    continue
        if type=="cs":
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiCastShadows" % light, value)
                except:
                    continue
        if type=="cvs":
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiCastVolumetricShadows" % light, value)
                except:
                    continue
    def test(self, switch):
        if switch:
            cmds.intSliderGrp(self.tempertaure, q=True, edit=True, enable=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiUseColorTemperature" % light, True)
                except:
                    continue
        else:
            cmds.intSliderGrp(self.tempertaure, q=True, edit=True, enable=False)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiUseColorTemperature" % light, False)
                except:
                    continue

    def set_float_attr(self, exposure=False, radius=False, shadow_density=False):
        if shadow_density:
            aiShadowDensity = cmds.floatSliderGrp(self.shadow_density, q=True, value=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiShadowDensity" % light, aiShadowDensity)
                except:
                    continue
        if radius:
            aiRadius = cmds.floatSliderGrp(self.radius, q=True, value=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiRadius" % light, aiRadius)
                except:
                    continue
        if exposure:
            aiExposure = cmds.floatSliderGrp(self.exposure, q=True, value=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiExposure" % light, aiExposure)
                except:
                    continue

    def set_int_attr(self, sample=False,volumeSamples=False):
        if sample:
            aiSamples = cmds.intSliderGrp(self.sample, q=True, value=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiSamples" % light, aiSamples)
                except:
                    continue
        if volumeSamples:
            aiVolumeSamples = cmds.intSliderGrp(self.volumeSamples, q=True, value=True)
            for light in self.current_selected_lights:
                try:
                    cmds.setAttr("%s.aiVolumeSamples" % light, aiVolumeSamples)
                except:
                    continue

    def set_aiColorTemperature(self):
        print(self.tempertaure)
        temperature = cmds.intSliderGrp(self.tempertaure, q=True, value=True)
        colorTemp = cmds.arnoldTemperatureToColor(temperature)
        displayColor = colorTemp
        if maya.mel.eval("exists \"colorManagementConvert\""):
            displayColor = cmds.colorManagementConvert(toDisplaySpace=colorTemp)

        displayColor[0] = min(max(displayColor[0], 0.0), 1.0)
        displayColor[1] = min(max(displayColor[1], 0.0), 1.0)
        displayColor[2] = min(max(displayColor[2], 0.0), 1.0)
        cmds.canvas(self.canvasName, edit=True, rgbValue=displayColor)
        for light in self.current_selected_lights:
            try:
                cmds.setAttr("%s.aiColorTemperature" % light, temperature)
            except:
                continue

def run():
    LODWindow().create()
