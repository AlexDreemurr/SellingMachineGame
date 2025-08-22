# -*- coding: utf-8 -*-

import json
import os
import sys
import random
from coin import Coin
from coin_charger import Charger
from shared_machinedata import MachineData
from useful_methods.price_round import price_round
from seller import Seller

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "item_data.json"), "r", encoding="utf-8") as f:
    ITEM_DATA = json.loads(f.read())
 
class ItemNotExistError(Exception):
    pass

class CoinNotAvailableError(Exception):
    pass

class ItemNotEnoughError(Exception):
    pass
    
class ItemNotFindError(Exception):
    pass

class HaveNoMoneyToBuyError(Exception):
    pass

class Machine():
    # 可接受的硬币 和 自动找钱用的硬币种类
    ACCEPTABLE_COINS = [10, 50, 100, 500]
    AVAILBALE_COINS_OUTPUT = sorted([1, 5, 10, 50, 100, 500], reverse = True)

    # 贩卖机商品信息
    item_data = ITEM_DATA
    # 总共累计盈利金额
    total_earned = 0
    # 钱币增长倍率
    rise_percentage = 0.1
    # 当前投入硬币列表
    current_input_coins = []
    # 上次找钱硬币列表
    last_charge_coins = []
    
    def searchItem(position):
        '''通过位置返回商品名'''
        for name in Machine.item_data:
            if position in Machine.item_data[name]["position"]:
                return name
        
        # 没有找到商品
        raise ItemNotFindError()

    def caculateInputSum():
        '''返回目前向贩卖机投入的硬币总额'''
        return Coin.sum(Machine.current_input_coins)
    
    def caculateLastChargeSum():
        '''返回上次找钱的金额'''
        return Coin.sum(Machine.last_charge_coins)
    
    def caculateTotalItem():
        '''返回售货机现在售卖的商品总数'''
        count = 0
        for item in Machine.item_data:
            count += Machine.item_data[item]["count"]
        return count

    def delete(item_name):
        '''删除贩卖机的某项商品信息'''
        del Machine.item_data[item_name]

    def inputCoin(coin):
        '''投入硬币，如不支持，则报出CoinNotAvailableError()'''
        # 判断硬币是否支持
        if coin.value not in MachineData.ACCEPTABLE_COINS:
            raise CoinNotAvailableError()

        Machine.current_input_coins.append(coin)
        
    def checkIfPlayerCanBuyAny(player_money):
        '''判断玩家是否还能买得起最便宜的商品，如不能，则报出HaveNoMoneyError()'''

        cheapest_price = 99999999

        for item in Machine.item_data:
            # 找到最便宜的商品，且目前还有货
            if Machine.item_data[item]["price"] < cheapest_price and Machine.item_data[item]["count"] > 0:
                cheapest_price = Machine.item_data[item]["price"]
            
        if player_money + Coin.sum(Machine.current_input_coins) < cheapest_price:
            raise HaveNoMoneyToBuyError()

    def clearCoin():
        '''清空贩卖机内存储的硬币'''
        Machine.current_input_coins = []

    def autoRefillItem(game_round):
        '''一个回合结束后根据回合数随机补充物品'''
        total_item_count = Machine.caculateTotalItem()
        total_add_count = 0
        add_chance = 0

        if 0 <= total_item_count <= 10:
            each_add = 4
            add_chance = 3
        elif 11 <= total_item_count <= 20:
            each_add = 1
            add_chance = 2
        elif 21 <= total_item_count:
            each_add = 1
            add_chance = 1
        
        already_items = []
        item = ""
        for i in range(add_chance):
            item = random.choice(list(Machine.item_data.keys()))
            while item in already_items:
                item = random.choice(list(Machine.item_data.keys()))
            already_items.append(item)

        for item in already_items:
            Machine.item_data[item]["count"] += each_add
        

        '''
        added_item_list = [-1, ]
        random_cursor = -1
        cur_count = 0
        for i in range(add_chance):
            while random_cursor not in added_item_list:
                random_cursor = random.randint(0, len(Machine.item_data) - 1)
            added_item_list.append(random_cursor)

            random_count = random.randint(1, total_add_count - 1)

            Machine.item_data[list(Machine.item_data.keys())[random_cursor]]["count"] += random_count
            cur_count += random_count
            if cur_count >= total_add_count:
                break
        '''

    def autoRisePrice(game_round):
        '''根据回合数自动将商品涨价，同时售卖价格也会增加'''
        
        if game_round % 3 == 0:
            Machine.rise_percentage += 0.05

        # 增加幸运瓶子的gap值
        Seller.gap = price_round(Seller.gap * (1 + Machine.rise_percentage))

        # 增加物价
        for item in Machine.item_data:
            Machine.item_data[item]["price"] = price_round(Machine.item_data[item]["price"] * (1 + Machine.rise_percentage))

        # 增加回收价格
        for name in Seller.PRICE_CHART:
            Seller.PRICE_CHART[name] = price_round(Seller.PRICE_CHART[name] * (1 + Machine.rise_percentage))

    def sell(item_name):
        # 判断商品是否存在
        if item_name not in Machine.item_data.keys():
            raise ItemNotExistError()

        if Machine.item_data[item_name]["count"] <= 0:
            raise ItemNotEnoughError()
        
        # 计算总盈利，剩余商品数减一
        Machine.total_earned += Machine.item_data[item_name]["price"]
        Machine.item_data[item_name]["count"] -= 1

        # 售货机存储硬币清空
        Machine.clearCoin()
        '''
        # 售货机内玩家的钱减去商品的价格
        Machine.current_input_coins = Charger.charge(Machine.current_input_coins, Machine.item_data[item_name]["price"])
        '''
        '''
        # 如果商品卖光则删除该物品信息
        if Machine.item_data[item_name]["count"] <= 0:
            Machine.delete(item_name)
        '''
    
        


        



