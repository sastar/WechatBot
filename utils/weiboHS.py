#!/usr/bin/python3
# coding=utf-8
import json
import time
import requests
import re
import json
import emoji
import logging
import sys
from .utilities import mongo_client


class getWeiboHotSearch(object):
    def __init__(self):
        self.headers = {
            "Host": "s.weibo.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

        self.listDB = mongo_client['list']
        self.Coll = self.listDB['breakingNews']
        self.lastbreaking = self.Coll.find_one() == None and {
            'note': ''} or self.Coll.find_one()

        logging.info("weiboHS initialized")

    def analysedJsonp(self, jsonpText):
        """
        解析jsonp返回的数据，返回json
        """
        res = re.search(r"\((.*)\)\}", jsonpText).group(1)
        res = json.loads(res)
        return res

    def getHSDict(self):
        currTimeStamp = int(round(time.time() * 1000) + 100)
        url = 'https://s.weibo.com/ajax/jsonp/gettopsug?uid=&ref=PC_topsug&url=https%3A%2F%2Fs.weibo.com%2Ftop%2Fsummary%3Fcate%3Drealtimehot&Mozilla=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F78.0.3904.108%20Safari%2F537.36&_cb=STK_{0}3'.format(
            str(currTimeStamp))
        jsonp = requests.get(url, headers=self.headers)
        weiboDict = self.analysedJsonp(jsonp.text)['data']['list']
        return weiboDict

    def handlerBreakingNews(self):
        weiboDict = self.getHSDict()
        if weiboDict[0]['flag'] == "4" and self.lastbreaking['note'] != weiboDict[0]['note']:
            self.lastbreaking = weiboDict[0]
            self.Coll.insert_one(weiboDict[0])
            return """{}
{}  {}""".format(weiboDict[0]['note'], weiboDict[0]['num'], emoji.emojize("爆:red_circle:"))
        else:
            return None

    def ParsedDicttoPrint(self, weiboDict):
        HSstr = "最新热搜:\n"
        for i in range(0, 5):
            weibostr = """{} 
热度：{}  """.format(weiboDict[i]['note'], weiboDict[i]['num'])
            if weiboDict[i]['flag'] == "1":
                weibostr += emoji.emojize("新:green_circle:")+"\n"
            elif weiboDict[i]['flag'] == "0":
                weibostr += ""+"\n"
            elif weiboDict[i]['flag'] == "2":
                weibostr += emoji.emojize("热:yellow_circle:")+"\n"
            elif weiboDict[i]['flag'] == "16":
                weibostr += emoji.emojize("沸:orange_circle:") + "\n"
            elif weiboDict[i]['flag'] == "4":
                weibostr += emoji.emojize("爆:red_circle:")+"\n"
            else:
                weibostr += ""+"\n"
            HSstr += weibostr
        return HSstr

    def startParsed(self):
        HSDict = self.getHSDict()
        return self.ParsedDicttoPrint(HSDict)


if __name__ == "__main__":
    print(getWeiboHotSearch().startParsed())
