# -*- coding: utf-8 -*-
from shared_userdata import UserData
import random
import math
import os
import sys
import json

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "json/bottle_mix_chart.json"), "r", encoding="utf-8") as f:
    BOTTLE_MIX_CHART = json.loads(f.read())

with open(os.path.join(BASE_DIR, "json/bottle_upgrade_chart.json"), "r", encoding="utf-8") as f:
    BOTTLE_UPGRADE_CHART = json.loads(f.read())

with open(os.path.join(BASE_DIR, "json/bottletype_mix_chart.json"), "r", encoding="utf-8") as f:
    BOTTLETYPE_MIX_CHART = json.loads(f.read())

with open(os.path.join(BASE_DIR, "json/base_volume_bottletype_relationship.json"), "r", encoding="utf-8") as f:
    BASE_VOLUME_BOTTLETYPE_RELATIONSHIP = json.loads(f.read())

with open(os.path.join(BASE_DIR, "json/base_or_mixture.json"), "r", encoding="utf-8") as f:
    BASE_OR_MIXTURE = json.loads(f.read())

'''fun值和bottle的关系：
        fun       bottle
         '''

def get_luckybottle_probability(x: int) -> float:
    '''输入当前回合数，返回生成幸运瓶子的概率'''
    # 已知前6个回合
    fixed = {
        1: 0.04,
        2: 0.07,
        3: 0.11,
        4: 0.12,
        5: 0.13,
        6: 0.14,
    }

    if x in fixed:
        return fixed[x]

    # 从第7回合开始，用指数函数逼近 0.20
    # 公式: p = limit - (limit - base) * decay^(x-6)
    limit = 0.20  # 趋近的上限
    base = 0.14   # 第6回合的概率
    decay = 0.7   # 衰减系数，调节收敛速度

    p = limit - (limit - base) * (decay ** (x - 6))
    return round(p, 4)  # 保留4位小数

def get_wordshow_probability(x: int) -> float:
    '''输入当前回合数，返回基底瓶子上有字的概率'''
    # 前10个回合的固定值
    fixed = {
        1: 1.00,
        2: 0.80,
        3: 0.70,
        4: 0.60,
        5: 0.55,
        6: 0.50,
        7: 0.475,
        8: 0.45,
        9: 0.425,
        10: 0.40,
    }

    if x in fixed:
        return fixed[x]

    # 从第11回合开始趋近 0.20
    # 公式: p = limit + (base - limit) * decay^(x-10)
    limit = 0.20   # 下限
    base = 0.40    # 第10回合的概率
    decay = 0.9    # 衰减系数，越接近1越慢

    p = limit + (base - limit) * (decay ** (x - 10))
    return round(p, 4)

class MixtureGroupNotFound(Exception):
    pass

class BottletypeNotFound(Exception):
    pass

class Bottle():
    '''这是所有瓶子类的父类
        创建瓶子实例时请用子类BasedBottle或MixedBottle'''

    def __init__(self, tag, volume = 0, bottletype = ""):
        '''tag:    json商品标签，有water, juice等
           label:  uiscreen对应显示的瓶子样式编号'''
        
        # 初始化父类属性：所有的瓶子都有这些属性
        self.tag = tag
        self.volume = volume
        self.bottletype = bottletype
        self.label = self.bottletype + self.tag
        self.fun = random.randint(1, 100)

        appear_word_percentage = get_wordshow_probability(UserData.game_round)
        small_percentage = 0.20 * (1 - math.exp(-0.35*(UserData.game_round-1)))

        self.isWordAppear = random.random() <= appear_word_percentage
        self.isSmall = random.random() <= small_percentage
        self.lucky_bottle_percentage = get_luckybottle_probability(UserData.game_round) # 幸运瓶概率 4%~20%
        '''
        # 设定uiscreen显示的瓶子编号label，按照一个数学函数的概率上面有字
        self.label = self.bottletype
        if self.tag == "mysterious":
            # 如果是幸运瓶子，百分百上面都有问号
            self.label = self.bottletype + self.tag
        elif self.isWordAppear and self.bottletype != "small":
            self.label = self.bottletype + self.tag
        '''

class BasedBottle(Bottle):
    '''BasedBottle专用于基底瓶子属性的类，父类为Bottle'''

    def __init__(self, tag, volume = 0, bottletype = ""):
        '''tag: 饮料标签(water, milk...)'''
        # 调用父类初始化函数
        super().__init__(tag, volume=volume, bottletype=bottletype)

        # 随机设定volume和bottletype的值
        '''随机生成瓶子属性开始'''
        if self.isSmall:
            self.bottletype = "small"
        else:
            if 1 <= self.fun <= 40:        self.bottletype = "common"
            elif 41 <= self.fun <= 60:     self.bottletype = "long"
            elif 61 <= self.fun <= 80:     self.bottletype = "giant"
            elif 80 <= self.fun <= 80 + self.lucky_bottle_percentage * 100:
                self.bottletype = "common"
                self.tag = "mysterious"
                self.volume = 500
            else:
                self.bottletype = "common"

        if self.tag != "mysterious":
            self.volume = BASE_VOLUME_BOTTLETYPE_RELATIONSHIP[self.bottletype]
        '''随机生成瓶子属性结束'''

        # 随机决定有没有字
        self.label = self.bottletype
        if self.tag == "mysterious":
            # 如果是幸运瓶子，百分百上面都有问号
            self.label = self.bottletype + self.tag
        elif self.isWordAppear and self.bottletype != "small":
            # 如果不是幸运瓶子，但是概率抽到能生成字，并且不是最小的瓶子
            self.label = self.bottletype + self.tag
        
        if self.tag == "yogurt":
            # 如果是酸奶，则不会生成普通无字瓶子
            self.label = self.bottletype + self.tag

class MixedBottle(Bottle):
    '''MixedBottle专指表示混合瓶子的类，父类为Bottle'''

    def __init__(self, bottle1, bottle2, volume = 0, bottletype = ""):
        '''tag: 饮料标签(water, milk...)
           bottle1: 混合前的饮料1
           bottle2: 混合前的饮料2'''
        self.bottle1, self.bottle2 = bottle1, bottle2

        volume = self.bottle1.volume + self.bottle2.volume
        tag = MixedBottle.decide_tag(bottle1, bottle2)
        bottletype = MixedBottle.decide_bottletype(tag, volume)

        super().__init__(tag, volume, bottletype)


    def decide_tag(bottle1, bottle2):
        '''输入两个瓶子，返回他们融合后瓶子的tag'''
        tag_name = ""
        target_group = [bottle1.tag, bottle2.tag]

        for tag_name in BOTTLE_MIX_CHART:
            for group in BOTTLE_MIX_CHART[tag_name]:
                if set(group) == set(target_group):
                    return tag_name

        # 如果找不到组合，就变成毒药
        return "poison"   
         
        # raise MixtureGroupNotFound()

    def decide_bottletype(tag, volume):
        '''输入瓶子tag和volume，返回这个融合瓶子的bottletype'''
        json_tag = tag
        for tag_name in BASE_OR_MIXTURE:
            if tag_name == tag and BASE_OR_MIXTURE[tag_name] == 1:
                json_tag = "base"

        for bottletype in BOTTLETYPE_MIX_CHART[json_tag]:
            min_vol = BOTTLETYPE_MIX_CHART[json_tag][bottletype][0]
            max_vol = BOTTLETYPE_MIX_CHART[json_tag][bottletype][1]

            if min_vol <= volume <= max_vol:
                return bottletype
        
        return BottletypeNotFound()




