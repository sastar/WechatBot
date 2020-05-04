# -*- coding: utf-8 -*-
from .ProcessInterface import ProcessInterface
from WechatBot.utils.utilities import config,mongo_client
from WechatBot.utils import weiboHS
import requests
import json
import time
import random
import logging
import re
from wxpy import TEXT
from lxml import etree


class ToolsManager(ProcessInterface):
    """
    工具类
    各种需要实现的api
    """

    def __init__(self):
        self.resou = weiboHS.getWeiboHotSearch()
        self.codeDB = mongo_client['citycode']
        self.caiyun_token = config['caiyun_token']
        self.juhe_apikey = config['juhe_apikey']
        self.geo_point = config['geo_point']
        self.skyconDict = {
            'CLEAR_DAY': '晴（白天）',
            'CLEAR_NIGHT': '晴（夜间）',
            'PARTLY_CLOUDY_DAY': '多云（白天）',
            'PARTLY_CLOUDY_NIGHT': '多云（夜间）',
            'CLOUDY': '阴',
            'WIND': '大风',
            'HAZE': '雾霾',
            'RAIN': '雨',
            'SNOW': '雪'
        }
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Host": "wufazhuce.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

        logging.info("Toolmanager initialized")

    def process(self, msg, type):
        shallRunObj = self.isRun(msg, type)
        if shallRunObj['shallRun'] != True:
            return
        if shallRunObj['resou']:
            msg.reply(self.resou.startParsed())
        if shallRunObj['today']:
            address = msg.text.split("today")[1].strip()
            weather = self.getRealtimeWeather(address)
            todayhis = self.todayHistory()
            oneword = self.getOneWord()
            msg.reply(weather+"\n"+todayhis+"\n"+oneword)

    # def starLuck(self,)

    def todayHistory(self):
        '''
        历史上的今天
        '''
        today = time.localtime(time.time())
        month = today[1]
        day = today[2]
        url = 'http://api.juheapi.com/japi/toh?v=1.0&month=' + str(month) + \
            '&day=' + str(day) + '&key=' + self.juhe_apikey
        todayHistory = json.loads(requests.get(url).text)['result']
        return "【历史上的今天】:"+todayHistory[random.randint(0, len(todayHistory)-1)]['des']

    def getRealtimeWeather(self, address=None, isadcode=True):
        if isadcode:
            direct = self.codeDB['code'].find(
                {"formatted_address": {'$regex': address}})
            if direct.count() == 0:
                return "无结果\n输入全名,检查错别字或扩大查找范围"
            direct = direct[0]
            req_url = "http://api.caiyunapp.com/v2/{}/weather?adcode={}&lang=zh_CN&alert=true&unit=metric:v1".format(
                self.caiyun_token, direct['adcode'])
        else:
            # 默认请求
            req_url = "https://api.caiyunapp.com/v2/{}/{}/weather?lang=zh_CN&alert=true&unit=metric:v1".format(
                self.caiyun_token, self.geo_point)
        logging.info(req_url)
        r = requests.get(req_url)
        r.raise_for_status()
        res = r.json().get('result')
        if isadcode:
            res['formatted_address'] = direct['formatted_address']
        else:
            return res
        weather = """{} 天气状况
【温度】:{}℃
【湿度】:{}%
【天气状况】:{}
【AQI指数】:{}
【紫外线】:{}
【出行建议】:{}""".format(res['formatted_address'], res['realtime']['temperature'], res['realtime']['humidity']*100, self.skyconDict[res['realtime']['skycon']], res['realtime']['aqi'], res['realtime']['ultraviolet']['desc'], res['forecast_keypoint'])
        if res['alert']['content'] != []:
            weather += """
【预警】:{}""".format(res['alert']['content'][0]['description'])
        return weather

    def getOneWord(self):
        url = "http://wufazhuce.com/"
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        selector = etree.HTML(r.text)
        words = selector.xpath('//*[@class="fp-one-cita"]/a/text()')
        return "【One-一个】:"+words[0]

    def isRun(self, msg, type):
        if type != TEXT or 'Content' not in msg.raw:
            return {'shallRun': False}
        if re.search(r'^/today', msg.raw['Content']):
            return {'shallRun': True, 'today': True, 'resou': False}
        if re.search(r'^/resou$', msg.raw['Content']):
            return {'shallRun': True, 'today': False, 'resou': True}
        return {'shallRun': False}


if __name__ == '__main__':
    pass
