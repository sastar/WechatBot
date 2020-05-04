# -*- coding: utf-8 -*-
import logging
import yaml
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)

def checkConfig():
    with open('config.yml', 'r', encoding='UTF-8') as f:
        _config = yaml.safe_load(f)
    for key in ['caiyun_token', 'mps', 'geo_point']:
        if key not in _config:
            logging.warn(key + " not in config")
    return _config


config = checkConfig()
logging.info(config['friends'])
