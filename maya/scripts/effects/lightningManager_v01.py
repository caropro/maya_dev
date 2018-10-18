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
            self.start_point = pm.ls("%s|start_point"%light)[0].getShape()
            self.end_point= pm.ls("%s|end_point"%light)[0].getShape()
        # Then we store the pyMel node on this class
        self.light = light

        self.buildUI()
 
    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)
        self.name = name = QtWidgets.QCheckBox(str(self.light))
        print self.light,666666666666666666666
        name.setChecked(self.light.visibility.get())
        name.toggled.connect(lambda val: self.light.visibility.set(val))
        layout.addWidget(name, 0, 0)
        self.startpoint_name = startpoint_name = QtWidgets.QCheckBox(str(self.start_point.getTransform()))
        startpoint_name.setChecked(self.start_point.visibility.get())
        startpoint_name.toggled.connect(lambda val: self.start_point.visibility.set(val))
        layout.addWidget(startpoint_name, 1, 0)
        self.endpoint_name = endpoint_name = QtWidgets.QCheckBox(str(self.end_point.getTransform()))
        endpoint_name.setChecked(self.end_point.visibility.get())
        endpoint_name.toggled.connect(lambda val: self.end_point.visibility.set(val))
        layout.addWidget(endpoint_name, 2, 0)

        startpoint_solo = QtWidgets.QPushButton('Select')
        start_point=self.start_point
        startpoint_solo.clicked.connect(partial(self.selectLight,start_point))
        layout.addWidget(startpoint_solo, 1, 1)

        endpoint_solo = QtWidgets.QPushButton('Select')
        end_point = self.end_point
        endpoint_solo.clicked.connect(partial(self.selectLight,end_point))
        layout.addWidget(endpoint_solo, 2, 1)

        # This will be our button to delete the light
        delete = QtWidgets.QPushButton('X')
        delete.clicked.connect(self.deleteLight)
        delete.setMaximumWidth(10)
        layout.addWidget(delete, 0, 2)


        # intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # intensity.setMinimum(1)
        # intensity.setMaximum(1000)
        # # intensity.setValue(self.light.intensity.get())
        # # intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        #
        # layout.addWidget(intensity, 1, 0, 1, 2)

        self.colorBtn = QtWidgets.QPushButton()
        self.colorBtn.setMaximumWidth(20)
        self.colorBtn.setMaximumHeight(20)
        # self.setButtonColor()
        # self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn, 1, 2)

        self.colorBtn2 = QtWidgets.QPushButton()
        self.colorBtn2.setMaximumWidth(20)
        self.colorBtn2.setMaximumHeight(20)
        # self.setButtonColor()
        # self.colorBtn.clicked.connect(self.setColor)
        layout.addWidget(self.colorBtn2, 2, 2)

        # Now this is a weird Qt thing where we tell it the kind of sizing we want it respect
        # We are saying that the widget should never be larger than the maximum space it needs
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

    def disableLight(self, val):
        # This function takes a value, converts it to bool and then sets our checkbox to that value
        self.name.setChecked(not bool(val))

    def deleteLight(self):
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()
        pm.delete(self.light)

    def selectLight(self,obj):
        pm.select(clear=True)
        pm.select(obj)
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
        "lightning": lightning.main
    }

    def __init__(self, dock=False):
        # So first we check if we want this to be able to dock
        if dock:
            # If we should be able to dock, then we'll use this function to get the dock
            parent = getDock()
        else:
            # Otherwise, lets remove all instances of the dock incase it's already docked
            deleteDock()
            # Then if we have a UI called lightingManager, we'll delete it so that we can only have one instance of this
            # A try except is a very important part of programming when we don't want an error to stop our code
            # We first try to do something and if we fail, then we do something else.
            try:
                pm.deleteUI('lightingManager')
            except:
                logger.debug('No previous UI exists')


            parent = QtWidgets.QDialog(parent=getMayaMainWindow())
            parent.setObjectName('lightingManager')
            parent.setWindowTitle('Lighting Manager')
            dlgLayout = QtWidgets.QVBoxLayout(parent)

        # Now we are on to our actual widget
        # We've figured out our parent, so lets send that to the QWidgets initialization method
        super(LightingManager, self).__init__(parent=parent)

        # We call our buildUI method to construct our UI
        self.buildUI()

        # Now we can tell it to populate with widgets for every light
        self.populate()

        # We then add ourself to our parents layout
        self.parent().layout().addWidget(self)

        # Finally if we're not docked, then we show our parent
        if not dock:
            parent.show()

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

    def refresh(self):
        # This is one of the rare times I use a while loop
        # It could be done in a for loop, but I want to show you how a while loop would look

        # We say that while the scrollLayout.count() gives us any Truth-y value we will run the logic
        # count() tells us how many children it has
        while self.scrollLayout.count():
            # We take the first child of the layout, and ask for the associated widget
            # Taking the child, means that it is no longer under the care of its parent
            widget = self.scrollLayout.takeAt(0).widget()
            # Some objects don't have widgets, so we'll only run this for objects with a widget
            if widget:
                # We set the visibility to False because there is a period where it will still be alive
                widget.setVisible(False)
                # Then we tell it to kill the widget when it can
                widget.deleteLater()

        # Finally we tell it to populate again
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
        # This function creates lights. Duh.
        # First we get the text of the combobox if we haven;t been given a light
        if not lightType:
            lightType = self.lightTypeCB.currentText()

        # Then we look up the lightTypes dictionary to find the function to call
        func = self.lightTypes[lightType]
        print func,22222222222222222222222
        # All our functions are pymel functions so they'll return a pymel object
        light = func()
        print light,888888888888888888888
        # We wil pass this to the addLight method if the method has been told to add it
        if add:
            self.addLight(light)

    def addLight(self, light):
        # This will create a LightWidget for the given light and add it to the UI
        # First we create the LightWidget
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
