# -*- coding: utf-8 -*-
from .ProcessInterface import ProcessInterface
from wxpy import TEXT
import re
import requests
import json
from random import choice
import logging


class GetSentece(ProcessInterface):
    def __init__(self, blacklist=[]):
        self.blacklist = blacklist
        self.Hitokotoheaders = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        self.tablerandom = ["hitokoto", "chp"]
        logging.info('GetSentence initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return
        if any([x == msg.sender.name for x in self.blacklist]):
            return
        if re.search(r"^/random$", msg.text):
            if choice(self.tablerandom) == "hitokoto":
                msg.reply(self.getHitokotoSentence())
            else:
                msg.reply(self.getChpSentence())

    def getHitokotoSentence(self):
        url = "https://v1.hitokoto.cn/?encode=json"
        r = requests.get(url, headers=self.Hitokotoheaders)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        yiStc = json.loads(r.text)
        return yiStc['hitokoto']+"\n    -「"+yiStc['from']+"」"

    def getChpSentence(self):
        """ 彩虹屁 """
        url = "https://chp.shadiao.app/api.php"
        r = requests.get(url, headers=self.Hitokotoheaders)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return "「"+r.text+"」"


if __name__ == '__main__':
    print(GetSentece().getChpSentence())
