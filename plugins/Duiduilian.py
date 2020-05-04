# -*- coding: utf-8 -*-
from wxpy import TEXT
from .ProcessInterface import ProcessInterface
import re
import requests
import logging


class DuiDuilian(ProcessInterface):
    def __init__(self, blacklist=[]):
        self.blacklist = blacklist
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            "Host": "ai-backend.binwang.me",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        logging.info('Duilian initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return
        if any([x == msg.sender.name for x in self.blacklist]):
            return
        if re.match(r"^/dui", msg.text):
            key = msg.text.split("dui")[1].strip()
            logging.info("duiduilian {}".format(key))
            output = self.getDuilian(key)
            if output == "您的输入太长了":
                msg.reply("太长了 不对")
            else:
                msg.reply(output)

    def getDuilian(self, key):
        url = "https://ai-backend.binwang.me/chat/couplet/{}".format(key)
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()['output']


if __name__ == '__main__':
    print(DuiDuilian().getDuilian(""))
