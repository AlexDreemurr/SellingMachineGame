# -*- coding: utf-8 -*-

from useful_methods.price_round import price_round
from bottle import Bottle, MixedBottle
import random
import os
import sys
import json

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "sell_price.json"), "r", encoding="utf-8") as f:
    PRICE_CHART_0 = json.loads(f.read())

class Seller():
    PRICE_CHART = PRICE_CHART_0
    gap = 400

    def __volumePercentage(bottle):
        bottletype = bottle.bottletype
        if bottletype == "small":
            return 0.6
        elif bottletype == "common":
            return 1.0
        elif bottletype == "long":
            return 1.25
        elif bottletype == "giant":
            return 1.5
        elif bottletype == "longlong":
            return 1.5
        elif bottletype == "longlonglong":
            return 2.0
        else:
            return 1.0
        
    def sell(bottle: Bottle | MixedBottle):
        '''提供饮料，返回可卖出的价格（末位保留0/5'''

        if bottle.tag == "mysterious":
            '''average: 幸运瓶子价格的期望值(平均)
               gap：    间隔
               如 average=100 gap=400 代表从-300~500随机生成一个数字'''
            
            average = Seller.PRICE_CHART[bottle.tag]
            return price_round(random.randint(average - Seller.gap, average + Seller.gap) * Seller.__volumePercentage(bottle))
        
        elif bottle.tag == "doublemysterious":
            '''average: 双重幸运瓶子价格的期望值(平均)
               gap：    间隔
               如 average=200 gap=400 代表从-600~1120随机生成一个数字'''
            
            average = Seller.PRICE_CHART[bottle.tag]
            return price_round(random.randint(average - Seller.gap * 2, average + Seller.gap * 2.2) * Seller.__volumePercentage(bottle))
        
        return price_round(Seller.PRICE_CHART[bottle.tag] * Seller.__volumePercentage(bottle))
    
