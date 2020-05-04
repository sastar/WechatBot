# -*- coding: utf-8 -*-
from wxpy import TEXT
from .ProcessInterface import ProcessInterface
import re
import requests
import json
import logging


class SearchGarbage(ProcessInterface):
    def __init__(self, blacklist=[]):
        self.blacklist = blacklist
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept": "*/*",
            "Content-Length": "79"
        }
        logging.info('SearchGarbage initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return
        if any([x == msg.sender.name for x in self.blacklist]):
            return
        if re.match(r"^/laji", msg.text):
            key = msg.text.split("laji")[1].strip()
            logging.info("search garbage classify {}".format(key))
            Laji = self.getGarbageClassify(key)
            if Laji == "":
                Laji = key + " 不是垃圾！"
            msg.reply(Laji)

    def get_content_length(self, data):
        length = len(data.keys()) * 2 - 1
        total = ''.join(list(data.keys()) + list(data.values()))
        length += len(total)
        return length

    def getGarbageClassify(self, key):
        url = "http://www.atoolbox.net/Api/GetRefuseClassification.php"
        d = {"ref": key}
        logging.info(self.headers['Content-Length'])
        r = requests.post(url, headers=self.headers, data=d)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        logging.info(r.text)
        classifyInfoNums = json.loads(r.text)
        classifyInfo = ""
        for x in classifyInfoNums:
            classifyInfo += classifyInfoNums[x]['name'] + \
                " - 属于 - "+classifyInfoNums[x]['type']+"\n"
        return classifyInfo


if __name__ == '__main__':
    pass
