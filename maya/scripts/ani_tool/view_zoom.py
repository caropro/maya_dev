#coding=utf-8
import maya.cmds as cmds
import pymel.core as pm
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class win(QDialog):
    #create a tool panel
    def __init__(self,parent=None):
        super(win, self).__init__(parent,Qt.WindowStaysOnTopHint)
        self.setWindowTitle("viewZoom%Pan")
        self.build_UI()
        self.function()
        self.show()
    #build the slider , checker , button
    def build_UI(self):
        layout_main=QVBoxLayout()
        self.quit_btn=QPushButton("Quit")
        self.reset_btn=QPushButton("reset")
        layout_main.addWidget(self.reset_btn)
        layout_main.addWidget(self.quit_btn)
        self.setLayout(layout_main)
    #deal with the connection between the tool and function
    def function(self):
        self.reset_btn.clicked.connect(self.reset_view)
        self.quit_btn.clicked.connect(self.close)
    #function
    def zoom(self):
        pass
    def reset_view(self):
        pan=cmds.getPanel( withFocus=True )
        sel_camera=pm.modelPanel(pan,q=True,camera=True)
        cmds.panZoom( sel_camera,abs=True, z=1,d=0,l=0,r=0,u=0 )
    def pan(self):
        pass
so=win()
so.show()

