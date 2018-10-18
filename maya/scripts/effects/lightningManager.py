# coding=utf8
#version 1.0
import os
import time
from PySide2 import QtWidgets, QtCore, QtGui
import logging
import lightning

logging.basicConfig()
logger = logging.getLogger('LightningManager')
logger.setLevel(logging.DEBUG)
logger.debug('Using shiboken2')
# Again, this uses the correct naming so we just import without aliasing
from shiboken2 import wrapInstance
from PySide2.QtCore import Signal
from maya import OpenMayaUI as omui
from maya import OpenMaya as om
import pymel.core as pm
# Finally from the functional tools library we import partial that will be useful for craeting temporary functions
from functools import partial


class LightWidget(QtWidgets.QWidget):
    onSolo = Signal(bool)

    def __init__(self, light):
        super(LightWidget, self).__init__()
        if isinstance(light, basestring):
            logger.debug('Converting node to a PyNode')
            light = pm.PyNode(light)

        if isinstance(light, pm.nodetypes.Transform):
            self.start_point_tf = pm.ls("%s|start_point" % light)[0]
            self.start_point = self.start_point_tf.getShape()
            self.end_point_tf = pm.ls("%s|end_point" % light)[0]
            self.end_point = self.end_point_tf.getShape()
            self.guide_particle = pm.ls("%s|guide_curve|lightning_particle" % light)[0].getShape()
            self.extrude_circle = pm.ls("%s|circle_curve_transform|circle_curve" % light)[0]
            self.stroke_tf = pm.ls("%s|lightning_stroke_transform" % light)[0]
            self.stroke = pm.ls("%s|lightning_stroke_transform|lightning_stroke" % light)[0]
        # Then we store the pyMel node on this class
        self.light = light

        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        # total group
        self.name = name = QtWidgets.QCheckBox(str(self.light))
        name.setChecked(self.light.visibility.get())
        name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(name, 0, 0)

        # This will be our button to delete the light
        delete = QtWidgets.QPushButton('DELETE')
        delete.clicked.connect(self.deleteLight)
        delete.setMaximumWidth(500)
        layout.addWidget(delete, 0, 2)
        ####################################################################################################
        # start_locator
        self.startpoint_name = startpoint_name = QtWidgets.QCheckBox(str(self.start_point.getTransform()))
        startpoint_name.setChecked(self.start_point.visibility.get())
        startpoint_name.toggled.connect(lambda val: self.start_point.visibility.set(val))
        layout.addWidget(startpoint_name, 1, 0)

        startpoint_solo = QtWidgets.QPushButton('Select')
        start_point = self.start_point_tf
        startpoint_solo.clicked.connect(partial(self.selectLight, start_point))
        layout.addWidget(startpoint_solo, 1, 1)

        # start_locatot_positionX
        self.start_point_x = QtWidgets.QLineEdit("Translate_X")
        self.start_point_x.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.start_point_x, "source": self.start_point_tf.tx}))
        layout.addWidget(self.start_point_x, 2, 0)
        # start_locatot_positionY
        self.start_point_y = QtWidgets.QLineEdit("Translate_Y")
        self.start_point_y.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.start_point_y, "source": self.start_point_tf.ty}))
        layout.addWidget(self.start_point_y, 2, 1)
        # start_locatot_positionZ
        self.start_point_z = QtWidgets.QLineEdit("Translate_Z")
        self.start_point_z.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.start_point_z, "source": self.start_point_tf.tz}))
        layout.addWidget(self.start_point_z, 2, 2)

        self.start_key = QtWidgets.QPushButton("key")
        self.start_key.setMaximumWidth(20)
        self.start_key.setMaximumHeight(20)
        # self.setButtonColor()
        self.start_key.clicked.connect(partial(self.keyFrame, self.start_point_tf))
        layout.addWidget(self.start_key, 2, 3)

        ####################################################################################################

        # end_locator
        self.endpoint_name = endpoint_name = QtWidgets.QCheckBox(str(self.end_point.getTransform()))
        endpoint_name.setChecked(self.end_point.visibility.get())
        endpoint_name.toggled.connect(lambda val: self.end_point.visibility.set(val))
        layout.addWidget(endpoint_name, 3, 0)

        endpoint_solo = QtWidgets.QPushButton('Select')
        end_point = self.end_point_tf
        endpoint_solo.clicked.connect(partial(self.selectLight, end_point))
        layout.addWidget(endpoint_solo, 3, 1)

        # end_locatot_positionX
        self.end_point_x = QtWidgets.QLineEdit("Translate_X")
        self.end_point_x.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.end_point_x, "source": self.end_point_tf.tx}))
        layout.addWidget(self.end_point_x, 4, 0)
        # end_locatot_positionY
        self.end_point_y = QtWidgets.QLineEdit("Translate_Y")
        self.end_point_y.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.end_point_y, "source": self.end_point_tf.ty}))
        layout.addWidget(self.end_point_y, 4, 1)
        # end_locatot_positionZ
        self.end_point_z = QtWidgets.QLineEdit("Translate_Z")
        self.end_point_z.editingFinished.connect(
            partial(self.valueChanged, {"editline": self.end_point_z, "source": self.end_point_tf.tz}))
        layout.addWidget(self.end_point_z, 4, 2)

        self.end_key = QtWidgets.QPushButton("key")
        self.end_key.setMaximumWidth(20)
        self.end_key.setMaximumHeight(20)
        # self.setButtonColor()
        self.end_key.clicked.connect(partial(self.keyFrame, self.end_point_tf))
        layout.addWidget(self.end_key, 4, 3)
        ####################################################################################################
        # particle_system
        self.particle_shape = particle_shape = QtWidgets.QLabel(str("particle_system"))
        layout.addWidget(particle_shape, 5, 0)

        particle_shape_solo = QtWidgets.QPushButton('Select')
        guide_particle = self.guide_particle
        particle_shape_solo.clicked.connect(partial(self.selectLight, guide_particle))
        layout.addWidget(particle_shape_solo, 5, 1)

        particle_shape_expression = QtWidgets.QPushButton('Edit')
        particle_shape_expression.clicked.connect(partial(self.edit_expression, guide_particle))
        layout.addWidget(particle_shape_expression, 5, 2)
        ####################################################################################################
        # extrude_circle
        self.circle = circle = QtWidgets.QCheckBox(str("extrude_circle"))
        circle.setChecked(self.extrude_circle.visibility.get())
        circle.toggled.connect(lambda val: self.extrude_circle.visibility.set(val))
        layout.addWidget(circle, 6, 0)

        circle_solo = QtWidgets.QPushButton('Select')
        extrude_circle_shape = self.extrude_circle
        circle_solo.clicked.connect(partial(self.selectLight, extrude_circle_shape))
        layout.addWidget(circle_solo, 6, 1)

        ####################################################################################################
        # stroke
        self.stroke_shape = stroke = QtWidgets.QCheckBox(str("stroke"))
        stroke.setChecked(self.stroke_tf.visibility.get())
        stroke.toggled.connect(lambda val: self.stroke_tf.visibility.set(val))
        layout.addWidget(stroke, 7, 0)

        stroke_solo = QtWidgets.QPushButton('Select')
        stroke_shape = self.stroke
        stroke_solo.clicked.connect(partial(self.selectLight, stroke_shape))
        layout.addWidget(stroke_solo, 7, 1)
        # intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # intensity.setMinimum(1)
        # intensity.setMaximum(1000)
        # # intensity.setValue(self.light.intensity.get())
        # # intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        #
        # layout.addWidget(intensity, 1, 0, 1, 2)



        # Now this is a weird Qt thing where we tell it the kind of sizing we want it respect
        # We are saying that the widget should never be larger than the maximum space it needs
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.getValue()

    def disableLight(self, val):
        # This function takes a value, converts it to bool and then sets our checkbox to that value
        self.name.setChecked(not bool(val))

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()
        pm.delete(self.light)

    def selectLight(self, obj):
        pm.select(clear=True)
        pm.select(obj)

    def getValue(self):
        start_point_x = pm.getAttr(self.start_point_tf.tx)
        self.start_point_x.setText(str(start_point_x))
        start_point_y = pm.getAttr(self.start_point_tf.ty)
        self.start_point_y.setText(str(start_point_y))
        start_point_z = pm.getAttr(self.start_point_tf.tz)
        self.start_point_z.setText(str(start_point_z))

        end_point_x = pm.getAttr(self.end_point_tf.tx)
        self.end_point_x.setText(str(end_point_x))
        end_point_y = pm.getAttr(self.end_point_tf.ty)
        self.end_point_y.setText(str(end_point_y))
        end_point_z = pm.getAttr(self.end_point_tf.tz)
        self.end_point_z.setText(str(end_point_z))

    def edit_expression(self, particle_shape):
        pm.mel.eval("expressionEditor creation %s position" % particle_shape)

    def valueChanged(self, pack, *args):
        editline = pack["editline"]
        source = pack["source"]
        try:
            newValue = float(editline.text())
            pm.setAttr(source, newValue)
        except:
            self.getValue()

    def keyFrame(self, attr, *args):
        currentTime = pm.currentTime(query=True)
        pm.setKeyframe(attr, time=currentTime,breakdown=False)



        # def setColor(self):
        #     lightColor = self.light.color.get()
        #     color = pm.colorEditor(rgbValue=lightColor)
        #     r, g, b, a = [float(c) for c in color.split()]
        #     color = (r, g, b)
        #     self.light.color.set(color)
        #     self.setButtonColor(color)

        # def setButtonColor(self, color=None):
        #     if not color:
        #         # We use pymels methods to query the value
        #         color = self.light.color.get()
        #     assert len(color) == 3, "You must provide a list of 3 colors"
        #     r, g, b = [c * 255 for c in color]
        #     self.colorBtn.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0);' % (r, g, b))


class LightingManager(QtWidgets.QWidget):
    """
    This is the main lighting manager.
    To call it we just do

    LightingManager(dock=True) and it will display docked, otherwise dock=False will display it as a window

    """

    lightTypes = {
        "lightning_count50": lightning.build_50,
        "lightning_count100": lightning.build_100,
        "lightning_count150": lightning.build_150,
        "lightning_count200": lightning.build_200
    }

    def __init__(self, dock=False):
        if dock:
            parent = getDock()
        else:
            deleteDock()
            try:
                pm.deleteUI('lightingManager')
            except:
                logger.debug('No previous UI exists')

            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('lightingManager')
            parent.setWindowTitle('Lighting Manager')
            dlgLayout = QtWidgets.QVBoxLayout(parent)

        super(LightingManager, self).__init__(parent=parent)

        self.buildUI()

        self.populate()

        self.sel_id = om.MEventMessage.addEventCallback("DragRelease",self.refresh)
        # We then add ourself to our parents layout
        self.parent().layout().addWidget(self)

        # Finally if we're not docked, then we show our parent
        if not dock:
            parent.show()

    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QtGui.QCursor()
        print cursor.pos()
        self.refresh()

    def buildUI(self):
        # Like in the LightWidget we show our
        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            # We add the option to the combobox
            self.lightTypeCB.addItem(lightType)
        # Finally we add it to the layout in row 0, column 0
        # We tell it take 1 row and two columns worth of space
        layout.addWidget(self.lightTypeCB, 0, 0, 1, 2)

        # We create a button to create the chosen lights
        createBtn = QtWidgets.QPushButton('Create')
        createBtn.clicked.connect(self.createLight)
        layout.addWidget(createBtn, 0, 2)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # Then we give it a vertical layout because we want everything arranged vertically
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)

        # Finally we create a scrollArea that will be in charge of scrolling its contents
        scrollArea = QtWidgets.QScrollArea()
        # Make sure it's resizable so it resizes as the UI grows or shrinks
        scrollArea.setWidgetResizable(True)
        # Then we set it to use our container widget to scroll
        scrollArea.setWidget(scrollWidget)
        # Then we add this scrollArea to the main layout, at row 1, column 0
        # We tell it to take 1 row and 3 columns of space
        layout.addWidget(scrollArea, 1, 0, 1, 3)

        # We need a refresh button to manually force the UI to refresh on changes
        refreshBtn = QtWidgets.QPushButton('Refresh')
        # We'll connect this to the refresh method
        refreshBtn.clicked.connect(self.refresh)
        # Finally we add it to the layout at row 2, column 2
        layout.addWidget(refreshBtn, 2, 2)

    def refresh(self,*args):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()
        self.populate()

    def populate(self):
        for node in pm.ls():
            if node.startswith("lightning_group"):
                if not pm.listRelatives(node, parent=1):
                    print node
                    self.addLight(node)

    def getDirectory(self):
        # The getDirectory method will give us back the name of our library directory and create it if it doesn't exist
        directory = os.path.join(pm.internalVar(userAppDir=True), 'lightManager')
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def createLight(self, lightType=None, add=True):
        if not lightType:
            lightType = self.lightTypeCB.currentText()
        func = self.lightTypes[lightType]
        light = func()
        print add
        if add:
            self.addLight(light)

    def addLight(self, light):
        widget = LightWidget(light)
        widget.onSolo.connect(self.isolate)
        self.scrollLayout.addWidget(widget)

    def isolate(self, val):
        # This function will isolate a single light
        # First we find all our children who are LightWidgets
        lightWidgets = self.findChildren(LightWidget)
        # We'll loop through the list to perform our logic
        for widget in lightWidgets:
            # Every signal lets us know who sent it that we can query with sender()
            # So for every widget we check if its the sender
            if widget != self.sender():
                # If it's not the widget, we'll disable it
                print val
                if val:
                    pm.select(clear=True)
                    pm.select(widget.light)


def getMayaMainWindow():
    """
    Since Maya is Qt, we can parent our UIs to it.
    This means that we don't have to manage our UI and can leave it to Maya.

    Returns:
        QtWidgets.QMainWindow: The Maya MainWindow
    """
    # We use the OpenMayaUI API to get a reference to Maya's MainWindow
    win = omui.MQtUtil_mainWindow()
    # Then we can use the wrapInstance method to convert it to something python can understand
    # In this case, we're converting it to a QMainWindow
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    # Finally we return this to whoever wants it
    return ptr


def getDock(name='LightingManagerDock'):
    """
    This function creates a dock with the given name.
    It's an example of how we can mix Maya's UI elements with Qt elements
    Args:
        name: The name of the dock to create

    Returns:
        QtWidget.QWidget: The dock's widget
    """
    # First lets delete any conflicting docks
    deleteDock(name)
    # Then we create a workspaceControl dock using Maya's UI tools
    # This gives us back the name of the dock created
    ctrl = pm.workspaceControl(name, dockToMainWindow=('right', 1), label="Lighting Manager")

    # We can use the OpenMayaUI API to get the actual Qt widget associated with the name
    qtCtrl = omui.MQtUtil_findControl(ctrl)

    # Finally we use wrapInstance to convert it to something Python can understand, in this case a QWidget
    ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)

    # And we return that QWidget back to whoever wants it.
    return ptr


def deleteDock(name='LightingManagerDock'):
    """
    A simple function to delete the given dock
    Args:
        name: the name of the dock
    """
    # We use the workspaceControl to see if the dock exists
    if pm.workspaceControl(name, query=True, exists=True):
        # If it does we delete it
        pm.deleteUI(name)
