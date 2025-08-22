# -*- coding: utf-8 -*-

from shared_machinedata import MachineData
from coin import Coin

class MoneyNotEnoughError(Exception):
    def __init__(self, given_money, price):
        self.given_money = given_money
        self.price = price

    def __str__(self):
        return f"You only paid {self.given_money} while the price is {self.price}!"

class Charger():
    def charger(to_be_charged):
        '''输入需要找的金额，返回硬币序列'''
        if to_be_charged < 0:
            return []
        result_coin_list = []
        for coin_value in MachineData.AVAILABLE_COINS_OUTPUT:
            cur_coin_count = to_be_charged // coin_value
            for i in range(cur_coin_count):
                result_coin_list.append(Coin(coin_value))
            to_be_charged -= cur_coin_count * coin_value
        return result_coin_list
        
    def charge(coin_list, price):
        '''输入投入的硬币序列和商品价格，返回找钱的硬币序列'''
        user_paid = Coin.sum(coin_list)
        if user_paid < price:
            raise MoneyNotEnoughError(user_paid, price)
        
        to_be_charged = user_paid - price
        charge_coin_list = Charger.charger(to_be_charged)

        return charge_coin_list
        
            
