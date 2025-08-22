# -*- coding: utf-8 -*-

from shared_userdata import UserData
from bottle import Bottle, MixedBottle
from game_pics import bottle_pics
from useful_methods.space_counter import space_counter
from useful_methods.color_phrase import color_phrase, makeWordsColor, judgeEarnOrLose, phrase
from seller import Seller
import os
import sys
import json
import time

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "item_translation.json"), "r", encoding="utf-8") as f:
    ITEM_TRANSLATION = json.loads(f.read())

with open(os.path.join(BASE_DIR, "bottletype_translation.json"), "r", encoding="utf-8") as f:
    BOTTLETYPE_TRANSLATION = json.loads(f.read())

class uiscreenSumming():
    def display():
        '''一个回合结束，打印结算页，返回总盈利'''
        info_linelists = []
        total_sum = 0

        print(f"                       Round {UserData.game_round} Settlement                          ")
        print()
        print("   Draw     Name                 Volume(ml)       Size       Profit")
        #print()
        time.sleep(1)
        for bottle in UserData.user_bottles:
            '''一行中包含：
                    瓶子字符画列表   中文名称   瓶子体积   瓶子体积种类   单项盈利'''

            bottle_pic = bottle_pics[bottle.label]
            chinese_name = (color_phrase(bottle.tag), phrase(bottle.tag))
            bottle_volume = bottle.volume
            bottle_bottletype = BOTTLETYPE_TRANSLATION[bottle.bottletype]
            bottle_earn = Seller.sell(bottle)

            total_sum += bottle_earn
            info_linelists.append([bottle_pic, chinese_name, bottle_volume, bottle_bottletype, bottle_earn])

        for line in info_linelists:
            for i in range(len(line[0])):

                if i == len(line[0]) // 2:
                    print(space_counter(line[0][i], 12, mode="middle") + space_counter(line[1][0], 22, length=len(line[1][1])), space_counter(str(line[2]), 12), space_counter(line[3], 12),  space_counter(judgeEarnOrLose(line[4]), 8), end = "")
                else:
                    print(space_counter(line[0][i], 12, mode="middle"), end = "")
                print()
            time.sleep(0.5)

        time.sleep(0.5)
        print()
        print("   Total Profit：                                           ", judgeEarnOrLose(total_sum))
        print()
        print()
        input(">>> press enter for the next round.")
        return total_sum

'''
a = Bottle("mysterious")
b = Bottle("coffee")
UserData.user_bottles = [a, b, MixedBottle(a, b)]
uiscreenSumming.display()
'''
