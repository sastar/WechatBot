# -*- coding: utf-8 -*-
import logging
logging.basicConfig(
    format='%(asctime)s :%(levelname)s: %(filename)s > %(funcName)s %(message)s', level=logging.INFO)
from emoji import demojize
from wxpy import TEXT, FRIENDS, embed, Bot
from utils.utilities import config
from utils.AutoLaunch import AutoLaunch
from plugins.ProcessInterface import ProcessInterface
from plugins.GlobalTextHook import GlobalTextHook
from plugins.ToolsManager import ToolsManager
from plugins.SearchGarbage import SearchGarbage
from plugins.GetSentence import GetSentece
from plugins.Duiduilian import DuiDuilian
from plugins.TencentPY import TencentPY
from plugins.GetBiliPic import GetBiliPic

bot = Bot(cache_path=True, console_qr=2)
allFri = bot.friends()

help_msg = """/help 查看帮助信息
/today [城市] 获取今日天气
/random 随机一句
/dui [上联] 对对联
/resou 查看微博热搜
/getbli [B站URL] 获取B站封面
/py [短消息] 查找短消息是否是谣言"""

mps = []
for mp in config['mps']:
    mps.append(bot.mps().search(mp)[0])

# Some global switches for debugging use only
isDebug = config['debug']

AutoLaunch(bot=bot, filehelper=bot.file_helper).launchTask()

plugins = [
    GlobalTextHook({'^/help$': help_msg}),
    ToolsManager(),
    SearchGarbage(),
    GetSentece(),
    DuiDuilian(),
    TencentPY(),
    GetBiliPic()
]
for plugin in plugins:
    if not isinstance(plugin, ProcessInterface):
        logging.error(
            'One of the plugins are not a subclass of ProcessInterface.')
        exit(-1)

bot.file_helper.send(help_msg)

# 命令循环
@bot.register([bot.file_helper], except_self=False)
def handlerPush(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg, msg.type)
        except Exception as e:
            logging.error(e)

# 自动接收好友申请
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    new_friend = msg.card.accept()
    new_friend.set_remark_name("BotFrient-"+demojize(new_friend.nick_name))
    new_friend.send("""[自动同意好友申请]
你好ヾ(≧▽≦*)o""")

# 公众号监听
@bot.register(mps)
def forward_mps(msg):
    msg.forward(bot.file_helper, prefix="来自"+msg.sender.name)


embed(banner="""
\t\t\t\t############################
\t\t\t\t#   WELCOME TO WeChatBot   #
\t\t\t\t############################
""")
