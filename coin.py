# -*- coding: utf-8 -*-

import random
import copy

class RandomDecider():
    def yearDecide():
        years_range = (1960, 2025)
        years_percentage = {0.00: (1960, 1960),
                            0.05: (1960, 1970),
                            0.12: (1971, 1980),
                            0.23: (1981, 1990),
                            0.40: (1991, 2000),
                            0.60: (2001, 2010),
                            0.92: (2011, 2020),
                            1.00: (2021, 2025)}
        randomer = random.random()
        for i in range(len(years_percentage)):
            if list(years_percentage.keys())[i] < randomer < list(years_percentage.keys())[i + 1]:
                a, b = years_percentage[list(years_percentage.keys())[i + 1]]
                return random.randint(a, b)

class Coin():
    VALUE = (1, 5, 10, 50, 100, 500)
    def __init__(self, value):
        if value not in Coin.VALUE:
            TypeError("不支持这种面额的硬币。")
            
        self.value = value
        self.year = RandomDecider.yearDecide()
        
        if 1926 <= self.year <= 1988:
            self.eraname = "昭和"
            self.erayear = self.year - 1925
        elif 1989 <= self.year <= 2019:
            self.eraname = "平成"
            self.erayear = self.year - 1988
        elif 2020 <= self.year:
            self.eraname = "令和"
            self.erayear = self.year - 2018

    # 这是求和工具方法
    def sum(coin_list):
        '''提供全部为coin的list，返回coin总金额'''
        result = 0
        for coin in coin_list:
            result += coin.value
        return result
    
    def sort(coin_list, reverse = False):
        '''不改变原来硬币序列，返回一个硬币按面额默认从大到小排序序列'''
        new_coin_list = []
        local_coin_list = copy.deepcopy(coin_list) 
        
        cur_max, cur_max_coin = 0, Coin(0)
        
        while len(local_coin_list) != 0:
            for coin in local_coin_list:
                if cur_max <= coin.value:
                    cur_max = coin.value
                    cur_max_coin = coin
            new_coin_list.append(cur_max_coin)
            local_coin_list.remove(cur_max_coin)
            cur_max = 0
            
        return new_coin_list

            
    

