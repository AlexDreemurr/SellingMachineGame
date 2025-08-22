# -*- coding: utf-8 -*-
from shared_userdata import UserData
import random
import math

'''fun值和bottle的关系：
        fun       bottle
         '''

class Bottle():
    LEVEL_SINGLE = ("small", "common", "long", "giant")
    LEVEL_MIXTURE = {"1": ("common", "giant"),
                     "2": ("small", "common", "giant")}
    LEVEL_MIXTURE_TYPE = {"cappuccino": "2", 
                          "fruittea": "1",
                          "milktea": "2", 
                          "milkshake": "2", 
                          "poison": "2"}

    def __init__(self, tag, volume = 0, bottletype = "", label = "", isMixedBottle = False):
        '''tag:    json商品标签，有water, juice等
           label:  uiscreen对应显示的瓶子样式编号'''
        
        self.tag = tag

        self.fun = random.randint(1, 100)
        appear_word_percentage = 0.35 + 0.55 * math.exp(-0.5*(UserData.game_round-1))
        small_percentage = 0.20 * (1 - math.exp(-0.35*(UserData.game_round-1)))

        self.isWordAppear = random.random() <= appear_word_percentage
        self.isSmall = random.random() <= small_percentage

        if not isMixedBottle:
            # 如果不是混合瓶子
            # 随机设定volume和bottletype的值

            if self.isSmall:
                self.bottletype = "small"
                self.volume = 250
            else:
                if 1 <= self.fun <= 55:
                    self.bottletype = "common"
                    self.volume = 500
                elif 56 <= self.fun <= 70:
                    self.bottletype = "long"
                    self.volume = 750
                elif 71 <= self.fun <= 85:
                    self.bottletype = "giant"
                    self.volume = 1000
                elif 86 <= self.fun <= 100:
                    self.bottletype = "common"
                    self.tag = "mysterious"
                    self.volume = 500

        # 如果volume和bottletype有设定值，那么按照设定值来，否则系统随机生成
        if volume != 0:
            self.volume = volume
            self.tag = tag
        if bottletype != "":
            self.bottletype = bottletype
            self.tag = tag

        # 设定uiscreen显示的瓶子编号label，按照一个数学函数的概率上面有字
        self.label = self.bottletype
        if self.tag == "mysterious":
            # 如果是幸运瓶子，百分百上面都有问号
            self.label = self.bottletype + self.tag
        elif self.isWordAppear and self.bottletype != "small":
            self.label = self.bottletype + self.tag
        
        # 如果label有设定值，那么按照设定值来，否则系统按照volume和bottletype赋值
        if label != "":
            self.label = label


        
class MixedBottle(Bottle):
    MIXTURE = ("cappuccino", "milktea", "milkshake", "fruittea", "poison")

    def __init__(self, bottle1, bottle2, volume = 0, bottletype = "", label = ""):
        '''tag: 饮料标签 water, milk...
           bottle1: 混合前的饮料1
           bottle2: 混合前的饮料2'''
        
        self.bottle1, self.bottle2 = bottle1, bottle2
        mix_set = {self.bottle1.tag, self.bottle2.tag}
        volume = self.bottle1.volume + self.bottle2.volume

        MixedBottle.__milkTeaCounter = MixedBottle.__milkShakeCounter = MixedBottle.__poisonCounter = MixedBottle.__milkCoffeeCounter
        if mix_set == {"milk", "coffee"}:   tag = "cappuccino"; bottletype = MixedBottle.__milkCoffeeCounter(volume)
        elif mix_set == {"milk", "tea"}:    tag = "milktea"   ; bottletype = MixedBottle.__milkTeaCounter(volume)
        elif mix_set == {"milk", "juice"}:  tag = "milkshake" ; bottletype = MixedBottle.__milkShakeCounter(volume)
        elif mix_set == {"tea", "juice"}:  tag = "fruittea" ; bottletype = MixedBottle.__fruitTeaCounter(volume)
        elif mix_set in ({"coffee", "tea"}, {"coffee", "juice"}): tag = "poison"; bottletype = MixedBottle.__poisonCounter(volume)
        elif mix_set == {"mysterious"}:
            # 两边全是幸运问号瓶，直接变成双拼问号瓶
            tag = "doublemysterious"
            bottletype = MixedBottle.__doubleMysteriousCounter(self.bottle1, self.bottle2)
        
        elif "doublemysterious" in mix_set:
            # 一方是双拼问号瓶，保留双拼问号瓶属性，容量增大
            tag = "doublemysterious"
            bottletype = MixedBottle.___mysteriousCounter(self.bottle1, self.bottle2)
            
        elif "mysterious" in mix_set:
            # 一方是幸运问号瓶，保留幸运问号瓶属性，容量增大
            tag = "mysterious"
            bottletype = MixedBottle.___mysteriousCounter(self.bottle1, self.bottle2)

        elif "water" in mix_set:
            # 一方是水，保留另一方属性，稀释
            tag = self.bottle1.tag if self.bottle1.tag != "water" else self.bottle2.tag
            bottletype = MixedBottle.__waterOtherCounter(volume)

        elif (self.bottle1.tag in MixedBottle.MIXTURE or self.bottle2.tag in MixedBottle.MIXTURE) and not (self.bottle1.tag in MixedBottle.MIXTURE and self.bottle2.tag in MixedBottle.MIXTURE):
            # 如果两边只有一边是混合物
            mixture_bottle = self.bottle1 if self.bottle1.tag in MixedBottle.MIXTURE else self.bottle2
            single_bottle = self.bottle1 if self.bottle1.tag not in MixedBottle.MIXTURE else self.bottle2

            if single_bottle.tag in (mixture_bottle.bottle1.tag, mixture_bottle.bottle2.tag):
                # 如果另一个单独的饮料是混合饮料的组成成分，就扩大混合饮料的容量
                tag = mixture_bottle.tag
                try:
                    index = Bottle.LEVEL_MIXTURE_TYPE[mixture_bottle.tag]
                    bottletype_list = Bottle.LEVEL_MIXTURE[index]
                    real_index = MixedBottle.__mixtureCounter(volume, index)
                    bottletype = bottletype_list[real_index + 1]
                except:
                    bottletype = mixture_bottle.bottletype
            else:
                # 如果不是，说明是乱混合，变成毒药
                tag = "poison"
                max_bottle = self.bottle1 if self.bottle1.volume > self.bottle2.volume else self.bottle2
                bottletype = max_bottle.bottletype

        elif self.bottle1.tag == self.bottle2.tag and (self.bottle1.tag not in MixedBottle.MIXTURE and self.bottle2.tag not in MixedBottle.MIXTURE):
            # 两边是一样的非混合后的东西，比如两边都是牛奶
            tag = self.bottle1.tag
            min_volume = min(bottle1.volume, bottle2.volume)
            index = MixedBottle.__singleCounter(min_volume)
            try:
                bottletype = Bottle.LEVEL_SINGLE[index + 1]
            except:
                bottletype = self.bottle1.bottletype if self.bottle1.volume < self.bottle2 else self.bottle2.bottletype

        elif self.bottle1.tag in MixedBottle.MIXTURE and self.bottle2.tag in MixedBottle.MIXTURE:
            # 如果两边全是混合饮料
            if self.bottle1.tag != self.bottle2.tag:
                # 如果混合饮料的种类不相同，变成大号毒药
                tag = "poison"
                bottletype = "giant"
            else:
                # 如果相同，则扩大容量
                tag = self.bottle1.tag
                max_bottle = self.bottle1 if self.bottle1.volume > self.bottle2.volume else self.bottle2
                try:
                    index = Bottle.LEVEL_MIXTURE_TYPE[self.bottle1.tag]
                    bottletype_list = Bottle.LEVEL_MIXTURE[index]
                    real_index = MixedBottle.__mixtureCounter(volume, index)
                    bottletype = bottletype_list[real_index + 1]
                except:
                    bottletype = max_bottle.bottletype


        label = bottletype + tag

        super().__init__(tag, volume, bottletype, label, isMixedBottle=True)

    def __singleCounter(volume):
        '''小瓶饮料输入容量返回bottletype的排位号（0 1 2 3）'''
        if volume == 250:
            return 0
        elif volume == 500:
            return 1
        elif volume == 750:
            return 2
        else:
            return 3

    def __mixtureCounter(volume, type):
        '''混合饮料输入容龄和饮料类编号返回bottletype的排位号'''
        if type == "1":
            if 500 <= volume <= 1000:
                return 0
            else:
                return 1
            
        elif type == "2":
            if 500 <= volume <= 750:
                return 0
            elif 750 <= volume <= 1500:
                return 1
            else:
                return 2
        
    def __waterOtherCounter(volume):
        if volume == 500:
            return "common"
        elif 500 < volume <= 750:
            return "long"
        else:
            return "giant"

    def __milkCoffeeCounter(volume):
        if 500 <= volume <= 750:
            return "small"
        elif 750 <= volume <= 1500:
            return "common"
        else:
            return "giant"
        
    def __fruitTeaCounter(volume):
        if 500 <= volume <= 1000:
            return "common"
        else:
            return "giant"

    def __doubleMysteriousCounter(bottleA, bottleB):
        return bottleA.bottletype if bottleA.volume < bottleB.volume else bottleB.bottletype

    def ___mysteriousCounter(bottleA, bottleB):
        mysterious_bottle = bottleA if bottleA.tag == "mysterious" else bottleB

        bottletype = mysterious_bottle.bottletype
        if bottletype == "common":
            return "long"
        elif bottletype == "long":
            return "longlong"
        elif bottletype == "longlong":
            return "longlonglong"
        else:
            return bottletype



