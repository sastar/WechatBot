import requests
import logging
import time
import json
from .utilities import config

class Caiyun(object):
    def __init__(self):
        self.token = config['caiyun_token']
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
        logging.info("Caiyun initialized")

    def getRealtimeWeather(self, geo_point):
        realTimeUrl = "https://api.caiyunapp.com/v2/" + \
            self.token+"/"+geo_point+"/realtime?lang=zh_CN&unit=metric:v1"
        realTimeWeather = json.loads(
            requests.get(realTimeUrl).content.decode())
        result = realTimeWeather['result']
        skycon = result['skycon']            # 主要天气现象
        temperature = result['temperature']  # 温度
        humidity = result['humidity']        # 湿度
        aqi = result['aqi']                  # aqi
        confortDesc = result['comfort']['desc']  # 舒适度
        localPrecIntensity = result['precipitation']['local']['intensity']
        ultravioletLevel = result['ultraviolet']['desc']
        return ("""{}
温度 {}℃,湿度 {}%, {},舒适度 {},紫外线强度 {}
aqi指数: {},本地降水强度: {}"""
                .format(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(realTimeWeather['server_time'])),
                        temperature, humidity, self.skyconDict[skycon], confortDesc, ultravioletLevel,
                        aqi, localPrecIntensity))

    def hasLocalRain(self, geo_point):
        """ 
        判断最近是否下雨 和 是否有预警信息
        """
        minutelyRainUrl = "https://api.caiyunapp.com/v2/" + \
            self.token+"/"+geo_point+"/weather?lang=zh_CN&alert=true&unit=metric:v1"
        minutelyRain = json.loads(requests.get(
            minutelyRainUrl).content.decode())
        logging.info(minutelyRainUrl)
        rainForecast = ""
        result = minutelyRain['result']
        forecast_keypoint = result['forecast_keypoint']
        if "未来两小时不会下雨，放心出门吧" in forecast_keypoint:
            return ""
        probability = result['minutely']['probability']
        for index in range(len(probability)):
            if probability[index] < 0.03:
                probability[index] = "无雨 "+str(probability[index])
            elif probability[index] >= 0.03 and probability[index] < 0.25:
                probability[index] = "小雨 "+str(probability[index])
            elif probability[index] >= 0.25 and probability[index] < 0.35:
                probability[index] = "中雨 "+str(probability[index])
            elif probability[index] >= 0.35 and probability[index] < 0.48:
                probability[index] = "大雨 "+str(probability[index])
            elif probability[index] >= 0.48:
                probability[index] = "暴雨 "+str(probability[index])
        rainForecast = ("""{}
{}
未来2小时，逐半小时，雷达降水概率预报:
{},  {},  {},  {}""".format(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(minutelyRain['server_time'])),
                            forecast_keypoint, probability[0], probability[1], probability[2], probability[3]))

        alertContent = result['alert']['content']
        alertWords = ""
        if len(alertContent) == 0:
            return rainForecast
        for content in alertContent:
            alertWords += """\n{} {} 发布
状态: {},  {}, 
具体信息: {} """.format(content['location'], time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(content['pubtimestamp'])),
                    content['status'], content['title'], content['description'])

        return rainForecast+"\n"+alertWords


if __name__ == "__main__":
    pass
