from utils.EarthQuake import EarthQuake
from utils.weiboHS import getWeiboHotSearch
from WechatBot.plugins.ToolsManager import ToolsManager
from apscheduler.schedulers.background import BackgroundScheduler
from .BaiduSignin import BaiduSignIn
import logging

class AutoLaunch(object):
    def __init__(self, **utilities):
        logging.getLogger('apscheduler').setLevel(logging.WARNING)
        self.baidusignin = BaiduSignIn()
        self.earthquake = EarthQuake()
        self.weibo = getWeiboHotSearch()
        self.tools = ToolsManager()
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
        self.bot = utilities['bot']
        self.filehelper = utilities['filehelper']

        logging.info("AutoLaunch initialized")

    def predictEarthQuake(self):
        """ 地震推送 """
        info = self.earthquake.getFristInfo()
        if info != None:
            self.filehelper.send(info)

    def handlerResou(self):
        """ 热搜推送 """
        info = self.weibo.handlerBreakingNews()
        if info != None:
            self.filehelper.send(info)

    def sendRainProbablitily(self):
        """ 推送天气更新 """
        res = self.tools.getRealtimeWeather(isadcode=False)
        if "未来两小时不会下雨" in res['forecast_keypoint']:
            return
        weather = """天气状况
【温度】:{}℃
【湿度】:{}%
【天气状况】:{}
【AQI指数】:{}
【紫外线】:{}
【出行建议】:{}""".format(res['realtime']['temperature'], res['realtime']['humidity']*100, self.skyconDict[res['realtime']['skycon']], res['realtime']['aqi'], res['realtime']['ultraviolet']['desc'], res['forecast_keypoint'])
        if res['alert']['content'] != []:
            weather += """
【预警】:{}""".format(res['alert']['content'][0]['description'])
        self.filehelper.send(weather)

    def launchTask(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.baidusignin.startSignIn, 'cron',
                          day_of_week='0-6', hour=0, minute=0, second=3, id="1")
        scheduler.add_job(self.predictEarthQuake, 'interval',
                          seconds=60, id="3")
        scheduler.add_job(self.handlerResou, 'interval',
                          seconds=30, id="4")
        scheduler.add_job(self.sendRainProbablitily,
                          trigger='cron', hour="*/2", id="7")
        scheduler.start()
        logging.info("auto task is running")


if __name__ == "__main__":
    pass
