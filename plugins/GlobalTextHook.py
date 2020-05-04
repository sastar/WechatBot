from wxpy import TEXT
from .ProcessInterface import ProcessInterface
import re
import logging


class GlobalTextHook(ProcessInterface):
    def __init__(self, subdict={}, blacklist=[]):
        self.dict = subdict
        self.blacklist = blacklist
        self.areIsat = False

        logging.info('GlobalTextHook initialized.')

    def process(self, msg, type):
        if type != TEXT:
            return
        # 如果有在黑名单里面有群，则跳过
        if any([x == msg.sender.name for x in self.blacklist]):
            if re.search(r'^/help$', msg.text):
                msg.reply("""/help 查看帮助信息
/dx 最新消息
/yq [省市区名] 所在区的疫情情况""")
                return
                
        for k in self.dict:
            if re.search(k, msg.raw['Content']):
                v = self.dict[k]
                # logging.info('{0} => {1}'.format(msg.raw['Content'], v))
                msg.reply(v)
