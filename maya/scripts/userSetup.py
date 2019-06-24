# coding=utf8
# Copyright (c) 2016 Strack
import os
import json
import logging
import pymel.core as pm
from strack_api import strack
from strack_globals import StrackGlobals
import std_log
from strack_menu import StrackMenu

log = std_log.std_log(level=logging.INFO)


def bootstrap_strack():
    # get login_info
    strack_info_str = os.getenv("strack_info")
    if not strack_info_str:
        log.warning("could not get strack info")
        return
    strack_info = json.loads(strack_info_str)
    login_info = strack_info.get("login_info")
    # set engine info
    StrackGlobals.engine = "maya"
    # init st
    StrackGlobals.st = strack.Strack(base_url=login_info.get('base_url'),
                                     login=login_info.get('login'),
                                     password=login_info.get('password'))
    log.info("Strack initialized, get strack api object StrackGlobals.st")
    StrackGlobals.current_project = strack_info.get("current_project")
    StrackGlobals.current_entity = strack_info.get("entity_info")
    if StrackGlobals.current_entity.get("type") == "task":
        StrackGlobals.selected_task = strack_info.get("entity_info")
    # setup strack menu
    project_info = strack_info.get("current_project")
    entity_info = strack_info.get("entity_info")
    pm.evalDeferred("StrackMenu(%s, %s)" % (project_info, entity_info))

log.info("STD_Maya initializing...")
bootstrap_strack()
log.info("STD_Maya initialized...")
