# coding=utf8
# Copyright (c) 2017 CineUse
import pymel.core as pm


def get_current_file_name(full_path=False):
    if full_path:
        return str(pm.sceneName().abspath())
    return str(pm.sceneName().basename())


if __name__ == "__main__":
    get_current_file_name()
