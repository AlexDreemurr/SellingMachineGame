# -*- coding: utf-8 -*-

from coin import Coin
from machine import Machine

class SpecificCoinNotExistError(Exception):
    pass

class User():
    def __init__(self, name):
        self.name = name

        # 初始给2枚500硬币
        self.coins = [Coin(500), Coin(500)]

        # 获得的瓶子
        self.bottles = []

    def display(self):
        for i in range(len(self.coins)):
            print(i+1, str(self.coins[i].value) + "円", self.coins[i].eraname + str(self.coins[i].erayear) + "年")

    def displayBottleNames(self):
        result = ""
        for bottle in self.bottles:
            result += bottle.tag + " "

        return result
    
    def sortCoin(self):
        '''将用户的硬币序列按金额从大到小的顺序排序'''
        self.coins = Coin.sort(self.coins)

    def sumMoneyAvailableForMachine(self):
        result = 0
        for coin in self.coins:
            if coin.value in Machine.ACCEPTABLE_COINS:
                result += coin.value
        return result


    def deleteCoin(self, pivot_coin):
        '''给定硬币，将其从用户硬币序列中删除'''
        for i in range(len(self.coins)):
            if self.coins[i] == pivot_coin:
                self.coins.remove(pivot_coin)
                break
        self.sortCoin()

    def addCoin(self, coin):
        '''给定硬币，向用户硬币序列中添加'''
        self.coins.append(coin)
        self.sortCoin()

    def addBottle(self, bottle):
        '''给定瓶子，向用户瓶子序列中添加'''
        self.bottles.append(bottle)

    def deleteBottle(self, pivot_bottle):
        '''给定瓶子，将其从用户瓶子序列中删除'''
        for i in range(len(self.bottles)):
            if self.bottles[i] == pivot_bottle:
                self.bottles.remove(pivot_bottle)
                break

    def checkIfCoinExist(self, value):
        '''检测玩家是否有给定面额的硬币，如果有则返回该硬币，没有则返回SpecificCoinNotExistError()'''
        for coin in self.coins:
            if coin.value == value:
                return coin
        
        raise SpecificCoinNotExistError()
        