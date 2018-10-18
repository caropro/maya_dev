#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/7/23'
# version     :
# usage       :
# notes       :

# Built-in modules

# Third-party modules
import maya.OpenMayaUI as mui

# Studio modules

# Local modules


def get_maya_win(module="mayaUI"):
    """
    get a QMainWindow Object of maya main window
    :param module (optional): string "PySide"(default) or "PyQt4"
    :return main_window: QWidget or QMainWindow object
    """
    prt = mui.MQtUtil.mainWindow()
    if module == "Qt":
        import Qt
        if "PyQt" in Qt.__binding__:
            import sip
            import PyQt4.QtCore as QtCore
            main_window = sip.wrapinstance(long(prt), QtCore.QObject)
        elif Qt.__binding__ == "PySide":
            import shiboken
            import PySide.QtGui as QtGui
            main_window = shiboken.wrapInstance(long(prt), QtGui.QWidget)
        elif Qt.__binding__ == "PySide2":
            import shiboken2
            import PySide2.QtWidgets as QtWidgets
            main_window = shiboken2.wrapInstance(long(prt), QtWidgets.QWidget)
        else:
            raise ValueError('Qt Binding Not supported...')
    elif module == "PyQt4":
        import sip
        import PyQt4.QtCore as QtCore
        main_window = sip.wrapinstance(long(prt), QtCore.QObject)
    elif module == "PySide":
        import shiboken
        import PySide.QtGui as QtGui
        main_window = shiboken.wrapInstance(long(prt), QtGui.QWidget)
    elif module == "PySide2":
        import shiboken2
        import PySide2.QtWidgets as QtWidgets
        main_window = shiboken2.wrapInstance(long(prt), QtWidgets.QWidget)
    elif module == "mayaUI":
        main_window = "MayaWindow"
    else:
        raise ValueError('param "module" must be "mayaUI" "PyQt4" "PySide" "PySide2" or "Qt"')
    return main_window
