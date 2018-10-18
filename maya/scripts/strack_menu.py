# coding=utf8
# Copyright (c) 2017 CineUse
import logging
import imp
import os

import maya.cmds as mc

from std_log import std_log
from std_strack import list_strack_actions
from strack_globals import StrackGlobals
from std_config.get_custom_dir import get_custom_dir

logger = std_log(level=logging.INFO)

DEFAULT_ITEMS = [
    {
        "name": "change_project",
        "label": "SelectProject",
        "command": "from my_project_list.MyProjectList import MyProjectList;\
                    from std_qt.get_main_window import get_main_window;\
                    project_list=MyProjectList(get_main_window('maya'));project_list.show()"
    },
    {
        "name": "strack_panel",
        "label": "StrackPanel",
        "command": "from strack_panel import StrackPanel;\
                    from std_maya.show_as_panel import show_as_panel;\
                    st_panel=StrackPanel();show_as_panel(st_panel)"
    },
    {
        "name": "asset_keeper",
        "label": "AssetKeeper",
        "command": "from asset_keeper import AssetKeeper;\
                    from std_qt.get_main_window import get_main_window;\
                    st_asset_keeper=AssetKeeper(get_main_window('maya'));st_asset_keeper.show()"
    },
    {
        "name": "divider",
    },
    {
        "name": "About",
        "label": "About Strack",
        "command": "from strack_about_info import strack_about_info;\
                   strack_about_info()"
    },
]


class StrackMenu(object):
    def __init__(self, project_info, entity_info):
        # get maya win
        maya_main_win = "MayaWindow"
        # make menu
        strack_menu_name = "strack_menu"
        strack_menu_label = "Strack"
        try:
            mc.deleteUI(strack_menu_name)
        except RuntimeError, e:
            logger.warning("%s" % e)
        strack_menu = mc.menu(strack_menu_name, label=strack_menu_label, tearOff=True, parent=maya_main_win)
        # get project info
        project_id = project_info.get("id")

        # make action sub menu
        self.action_menu = mc.menuItem("Actions", sm=1, label="Actions", tearOff=True, parent=strack_menu)
        self.update_action_menu(project_id, entity_info)
        # default menu items
        mc.menuItem("", divider=1, parent=strack_menu)
        for item_info in DEFAULT_ITEMS:
            name = item_info.get("name")
            if name == "divider":
                mc.menuItem("", divider=1, parent=strack_menu)
                continue
            label = item_info.get("label")
            command = item_info.get("command")
            mc.menuItem(name, label=label, parent=strack_menu, command=command)

    @staticmethod
    def _get_actions(project_id, entity_info):
        # get task actions of this project, maya actions
        engine = "maya"
        entity_type = entity_info.get("type")
        action_entity_list = list_strack_actions(StrackGlobals.st, project_id, engine, entity_type) or []
        action_list = []
        for action_info, _ in action_entity_list:
            action_list.append(action_info)
        return action_list

    def update_action_menu(self, project_id, entity_info):
        action_list = self._get_actions(project_id, entity_info)
        logger.debug("action_list >> %s" % action_list)
        # clear old items
        mc.menu(self.action_menu, edit=True, deleteAllItems=True)
        # add new items
        for action_info in action_list:
            name = action_info.get("name")
            logger.debug("action_info >> %s" % action_info)
            label = action_info.get("label") or action_info.get("name")
            script_name = action_info.get("register", {}).get("command", "")
            custom_dir = get_custom_dir()
            script_dir = os.path.join(custom_dir, "actions", "scripts")
            script_dir = script_dir.replace("\\", "/")
            try:
                fn_, path, desc = imp.find_module(script_name, [script_dir])
            except:
                continue
            mod = imp.load_module(script_name, fn_, path, desc)
            try:
                mc.menuItem(name, label=label, parent=self.action_menu, c=mod.main)
            except:
                pass    # ignore errors

