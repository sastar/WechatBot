from wxpy import TEXT
from WechatBot.utils.constants import getBiliPicData
import requests
import re
import os
import logging
from .ProcessInterface import ProcessInterface
import sys
import sys
sys.path.append("..")


class GetBiliPic(ProcessInterface):
    def __init__(self, blacklist=[]):
        self.blacklist = blacklist
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        self.urlMatch = re.compile(r'video\/(.*)$')
        self.imgPath = getBiliPicData()
        if not os.path.exists(self.imgPath):
            os.makedirs(self.imgPath)
        logging.info("GetBiliPic initialized")

    def process(self, msg, type):
        if type != TEXT:
            return
        if any([x == msg.sender.name for x in self.blacklist]):
            return
        if re.search(r"^/getbli", msg.text):
            key = msg.text.split("getbli")[1].strip()
            if key == '':
                msg.reply('请输入您要查找的内容')
            logging.info("get bili  {}".format(key))
            res = self.getBiliPic(key)
            msg.reply(res)

    def getRealUrl(self, url):
        res = requests.head(url)
        url = res.headers.get('location')
        return url

    def getBiliPic(self, url):
        if "b23" in url:
            url = self.getRealUrl(url)
            url = url[0:url.index("?")]
        vid = self.urlMatch.findall(url)
        if vid == []:
            return "url不正确"
        vid = vid[0]
        if vid[0:2] == "BV":
            url = "https://api.bilibili.com/x/web-interface/view?bvid="+vid[2:]
        elif vid[0:2] == "av":
            url = "https://api.bilibili.com/x/web-interface/view?aid="+vid[2:]
        else:
            return "不存在此视频"
        r = requests.get(url, headers=self.headers)
        r.encoding = r.apparent_encoding
        res = r.json()
        if res['code'] != 0:
            return "获取失败，请检查网络"
        data = res['data']
        name = data['title']
        picurl = data['pic']
        return "@img@"+self.saveCaipuPic(picurl, name)

    def saveCaipuPic(self, url, filename):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        file_suffix = os.path.splitext(url)[1]
        img = r.content
        imgPath = getBiliPicData(filename+file_suffix)
        with open(imgPath, 'wb') as f:
            f.write(img)
        return imgPath
