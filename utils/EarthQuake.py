from lxml import etree
import requests
import time
import logging
import sys
sys.path.append("..")
from WechatBot.utils.utilities import mongo_client


class EarthQuake():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            "Host": "news.ceic.ac.cn",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.listDB = mongo_client['list']
        self.Coll = self.listDB['earthquakelist']
        self.earthquakelist = self.Coll.find_one() == None and "" or self.Coll.find_one()

        self.url = "http://news.ceic.ac.cn/index.html"

    def checkData(self, datetime):
        query_dict = {"O_TIME": datetime}
        doc = self.Coll.find(query_dict)
        try:
            if doc.count() == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)

    def getFristInfo(self):
        url = 'http://news.ceic.ac.cn/index.html?time={}'.format(
            int(time.time()))
        r = requests.get(url, headers=self.headers)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        res = html.xpath('normalize-space(//*[@id="news"]//tr[2])').split()
        datetime = res[1]+" "+res[2]
        code = self.checkData(datetime)
        if code:
            return None
        elif float(res[0]) >= 6.0 and self.earthquakelist != res[1]+" "+res[2]:
            logging.info("{},发生了{}级地震".format(res[1]+" "+res[2], res[0]))
            self.earthquakelist = res[1]+" "+res[2]
            self.Coll.insert_one(
                {"O_TIME": datetime, "EPI_LAT": res[3], "EPI_LON": res[4], "EPI_DEPTH": res[5], "M": res[0], "LOCATION_C": res[6]})
            # ['6.4', '2020-01-09', '16:38:10', '62.35', '170.95', '10', '俄罗斯西伯利亚东部']
            return f'北京时间:{res[1]+" "+res[2]},在纬度:{res[3]} ,经度{res[4]} 处发生了{res[0]}级地震,震源深度{res[5]}千米,参考位置:{res[6]}'


if __name__ == "__main__":
    print(EarthQuake().getFristInfo())
