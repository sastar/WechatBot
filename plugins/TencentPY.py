from .ProcessInterface import ProcessInterface
import requests
from lxml import etree
import re
import os
import logging
import json
from retrying import retry
from wxpy import TEXT
import emoji
from time import time


class TencentPY(ProcessInterface):
    def __init__(self, blacklist=[]):
        self.blacklist = blacklist
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        self.proxies = ""
        self.pymap = {
            "真": emoji.emojize(":OK_hand:"),
            "假": emoji.emojize(":double_exclamation_mark: :warning:"),
            "疑": emoji.emojize(":question_mark:")
        }
        logging.info("Tencentpy initialized")

    @retry(stop_max_attempt_number=5, wait_fixed=1000)
    def _getSelector(self, url):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text

    def process(self, msg, type):
        if type != TEXT:
            return
        if any([x == msg.sender.name for x in self.blacklist]):
            return
        if re.search(r"^/py", msg.text):
            key = msg.text.split("py")[1].strip()
            if key == '':
                msg.reply('请输入您要查找的内容')
            logging.info("search py  {}".format(key))
            res = self.searchPY(key)
            msg.reply(res)

    def searchPY(self, title):
        url = "https://vp.fact.qq.com/searchresult?title={}&num=0&_={}".format(
            title, str(int(time()*1000)))
        text = self._getSelector(url)
        jsonp = json.loads(text)
        if jsonp['total'] == 0:
            return "未找到，按关键词查找"
        res = ""
        count = 0
        for c in jsonp['content']:
            if c['_score'] < 2.05 or count > 4:
                break
            sourceUrl = "https://vp.fact.qq.com/article?id={}&ADTAG=xw-1.jz".format(
                c['_id'])
            result = c['_source']['result'].split("-")
            result = result[0] + " " + result[1] + " " + self.pymap[result[0]]
            title = c['_source']['title']
            res += """{} {}
{}
""".format(result, title, sourceUrl)
            count += 1
        if res == "":
            return "无相关结果，请注意关键词"
        return res


if __name__ == "__main__":
    # dxs = DingxiangScrapy()
    # print(dxs.getTencentPY())
    pass
