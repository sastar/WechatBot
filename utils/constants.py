# -*- coding: utf-8-*-
import os

APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

PLUGIN_PATH = os.path.join(APP_PATH, "plugins")
CONFIG_PATH = os.path.join(APP_PATH, "")
BILI_PATH = os.path.join(APP_PATH, "bilipic")

def getConfigData(*fname):
    """
    获取配置目录下的指定文件的路径
    :param *fname: 指定文件名。如果传多个，则自动拼接
    :returns: 配置目录下的某个文件的存储路径
    """
    return os.path.join(CONFIG_PATH, *fname)


def getBiliPicData(*fname):
    return os.path.join(BILI_PATH, *fname)


def getPluginData(*fname):
    return os.path.join(PLUGIN_PATH, *fname)
