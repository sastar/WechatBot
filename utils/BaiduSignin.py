# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from .utilities import config
import logging


class BaiduSignIn():
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'Cookie': config['baidu_cookie'],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }

    def match_bar_name(self, soup):
        '''
        函数match_bar_name用来获取
        1、当前页
        2、关注贴吧名字和链接，返回列表数据，格式[{'name':'abc','link':'www.asdfaf.asdfasdf'},'name':'abc','link':'www.asdfaf.asdfasdf'}]，
        '''
        list = []
        for i in soup.find_all('a'):
            if i.has_attr('href') and not i.has_attr('class') and i.has_attr('title'):
                if i.string != 'lua':
                    list.append(
                        {'name': i.string, 'link': 'http://tieba.baidu.com/'+i.get('href')+'&fr=home'})
        return list

    def get_bar_link(self):  # 遍历所有页，直到最后一页
        '''
        函数get_bar_link用来获取
        1、所有页
        2、关注贴吧
        3、名字和链接
        '''
        url = r'http://tieba.baidu.com/f/like/mylike?pn=%d'
        pg = 1
        tieba_list = []
        while 1:
            res = self.s.get(url % pg, headers=self.headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            tieba_list.extend(self.match_bar_name(soup))
            if '下一页' in str(soup):
                pg += 1
            else:
                return tieba_list

    def check(self, name, link):  # 获取每个关注贴吧 提交数据tbs，然后签到，并返回签到结果
        '''
        name: 贴吧名字
        link：贴吧链接
        '''
        try:
            res = self.s.post(link)
            tbs = re.compile('\'tbs\': "(.*?)"')
            find_tbs = re.findall(tbs, res.text)
            if not find_tbs:  # 　没有查找到tbs,跳过这个吧的签到
                return -2
            data = {
                'ie': 'utf-8',
                'kw': name,
                'tbs': find_tbs[0],
            }
            url = 'http://tieba.baidu.com/sign/add'
            res = self.s.post(url, data=data, headers=self.headers)  # 签到 post
            return int(res.json()['no'])  # 返回提交结果
        except:
            return -1

    def SignIn(self, data):
        try:
            res = self.check(data['name'], data['link'])
            if res == 0:
                logging.info(data['name'] + '吧签到成功')
                return True
            elif res == 1101:
                logging.info(data['name'] + '吧已经签过')
                return True
            elif res == 1102:
                logging.info(data['name'] + '吧，签到太快，重新签到本吧')
                time.sleep(10)
                return False
            else:
                logging.info(res)
                logging.info('未知返回值，重新签到' + data['name']+'吧')
                return False
        except:
            logging.info('未知报错 重新签到' + data['name']+'吧')
            return False

    def startSignIn(self):
        for i in self.get_bar_link():  # 根据签到的返回值处理结果,利用count做最多三次异常重复签到
            flag = False
            count = 0
            while flag == False:
                flag = self.SignIn(i)
                time.sleep(0.7)  # 控制签到速度
                count = count + 1
                if count >= 3:
                    logging.info(i['name']+'吧异常，无法签到，已经跳过')
                    break


if __name__ == "__main__":
    BaiduSignIn().startSignIn()
