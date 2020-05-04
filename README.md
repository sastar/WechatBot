# WechatBot

基于[wxpy](https://github.com/youfou/wxpy)的微信机器人



## 注意

**网页版微信地址：<https://wx.qq.com/>。 请尝试登陆此网页微信，若不能登陆，则无法使用本项目**

**强烈建议仅小号运行**

**强烈建议仅小号运行**

**强烈建议仅小号运行**



## 测试环境

* 系统: Debian 9.12 stretch

* Python版本： 3.7.7

> 未在Windows下测试

## 功能

- [x] 凌晨自动贴吧打卡，两小时自动发送配置地址的天气预报及天气预警
- [x] 支持命令查询形式的工具助手
- [x] 监听公众号，若有更新则发送到文件传输助手
- [x] 地震信息推送，爆点热搜推送
- [x] 获取B站视频封面图
- [ ] 通过配置文件，配置朋友自动回复
- [ ] 接入人工智能机器人
- [ ] 九宫图和GIF分解



## 下载运行说明

> 本项目不是面向最终用户,配置时可能需要修改源码进行配置，使用本项目需要基础的调试技巧 (再加上一点点运气（￣︶￣）↗　)

* 依赖：运行前请安装好**mongodb数据库**和**python3.5**及以上，MongoDB安装请自行谷歌，Python建议使用Anaconda进行安装

```shell
git clone https://github.com/sastar/WechatBot #下载项目
cd WechatBot
cp config.yml.example config.yml # 配置文件
pip3 install -r requirements.txt  #安装python依赖包
python3 main.py # 进入之后扫描命令行二维码码登陆
# 之后才文件传输助手中发送命令进行交互
```



## 退出程序
组合键 ```Ctrl+C``` 或 组合键 ```Ctrl+D``` 或 ```Ctrl+4```



## 配置说明

```yaml
# 微信消息打印开关
debug: True

# 图灵apikey 暂未用到
# tuling_apikey: 'api key'

# 彩云token 彩云天气api token 
# 彩云天气token 注册平台 https://dashboard.caiyunapp.com/v1/token/
caiyun_token: "CaiYun token"

# 聚合api key
# 前往https://www.juhe.cn/ucenter/datacenter 申请 AppKey
juhe_apikey: "juhe appkey"

# location: "广州"

# 地理位置 经度在前, 纬度在后
# 彩云天气需要用到，用于具体位置的天气信息的获取
geo_point: "104.0837670000,30.6303190000" 

# 百度贴吧cookie 用于贴吧自动签到
baidu_cookie: "Tieba cookie"

# 公众号监听
# 需要订阅公众号，若无，会抛出异常
mps:
  - "赤戟的书荒救济所"

# mongodb 配置
mongodb:
  host: "localhost"
  port: 27017

# 朋友 *保留位置，为完成*
friends:

```



## 数据来源

#### 1. 微博热搜

https://s.weibo.com/

#### 2. One-一个

http://wufazhuce.com/

#### 3. 聚合数据

http://juhe.cn

#### 4. 彩云天气API

https://open.caiyunapp.com/Main_Page

#### 5. Hitokoto

https://hitokoto.cn/

#### 6. 彩虹屁生成器

https://chp.shadiao.app/



## 其他

微信斗图功能请参考[鸭哥的项目](https://github.com/grapeot/WechatForwardBot)配置

微博订阅功能参考微博[爬虫项目](https://github.com/dataabc/weiboSpider)



## 捐助


| Wechat |
| :------: |
| <img width="150" src="./docs/donate/wechat.jpg"> |


## LICENSE
[MIT License](https://github.com/sastar/WechatBot/blob/master/LICENSE)