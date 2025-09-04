# -*- coding: utf-8 -*-

from coin import Coin
from shared_machinedata import MachineData
from machine import Machine, CoinNotAvailableError

class SpecificCoinNotExistError(Exception):
    pass

class User():
    def __init__(self, name):
        self.name = name

        # 当前所处的页码数
        self.page = 1

        # 初始给2枚500硬币
        self.coins = [Coin(500), Coin(500)]
        # 贮存的硬币、500硬币的量、100硬币的量
        self.saved_coins = []
        self.saved_coins_500_count = 0
        self.saved_coins_100_count = 0
        # 用户的总余额
        self.balance = 1000
        # 用户贮存的总余额
        self.saving_balance = 0

        # 获得的瓶子
        self.bottles = []
        # 每个阶段获得的瓶子
        self.bottles_per_section = []
        # 历史上获得的所有瓶子
        self.history_bottles = []

        # 任务列表
        self.task_list = []
        
    def updateBalance(self):
        '''更新self.balance的余额数值'''
        self.balance = 0
        self.saving_balance = 0
        for coin in self.coins:
            self.balance += coin.value
        for coin in self.saved_coins:
            self.balance += coin.value
            self.saving_balance += coin.value

    def display(self):
        for i in range(len(self.coins)):
            print(i+1, str(self.coins[i].value) + "円", self.coins[i].eraname + str(self.coins[i].erayear) + "年")

    def displayBottleNames(self):
        result = ""
        for bottle in self.bottles:
            result += bottle.tag + " "

        return result

    def sumMoneyAvailableForMachine(self):
        result = 0
        for coin in self.coins:
            if coin.value in Machine.ACCEPTABLE_COINS:
                result += coin.value
        return result

    def saveCoin(self, value):
        '''给定硬币面额（必须在硬币列表中存在），存入贮存硬币列表、并从原硬币列表中删除'''
        if value not in MachineData.ACCEPTABLE_COINS_FOR_SAVE:
            raise CoinNotAvailableError()
        coin = self.checkIfCoinExist(value)
        self.saved_coins.append(coin)
        self.deleteCoin(coin)

        if value == 500:
            self.saved_coins_500_count += 1
        elif value == 100:
            self.saved_coins_100_count += 1

        self.coins = Coin.sort(self.coins)

    def withdrawCoin(self, value):
        '''给定硬币面额（必须在贮存硬币列表中存在），从贮存硬币中拿出、添加到硬币列表'''
        if value not in MachineData.ACCEPTABLE_COINS_FOR_SAVE:
            raise CoinNotAvailableError()
        coin = self.checkIfCoinExistInSavedCoins(value)
        self.coins.append(coin)
        self.deleteCoin(coin, list_type = "saved_coins")

        if value == 500:
            self.saved_coins_500_count -= 1
        elif value == 100:
            self.saved_coins_100_count -= 1

        self.coins = Coin.sort(self.coins)
        
    def addCoin(self, coin, list_type = "coins"):
        '''给定硬币，向用户硬币序列中添加
            coins: 玩家硬币序列
            saved_coins: 玩家贮存硬币序列'''
        if list_type == "coins":
            self.coins.append(coin)
            self.coins = Coin.sort(self.coins)
        elif list_type == "saved_coins":
            self.saved_coins.append(coin)
            self.saved_coins = Coin.sort(self.saved_coins)
        self.updateBalance()

    def deleteCoin(self, pivot_coin, list_type = "coins"):
        '''给定硬币，将其从用户硬币序列中删除
            coins: 玩家硬币序列
            saved_coins: 玩家贮存硬币序列'''
        if list_type == "coins":
            for i in range(len(self.coins)):
                if self.coins[i] == pivot_coin:
                    self.coins.remove(pivot_coin)
                    break
            self.coins = Coin.sort(self.coins)
        elif list_type == "saved_coins":
            for i in range(len(self.saved_coins)):
                if self.saved_coins[i] == pivot_coin:
                    self.saved_coins.remove(pivot_coin)
                    break
            self.saved_coins = Coin.sort(self.saved_coins)
        self.updateBalance()

    def addBottle(self, bottle):
        '''给定瓶子，向用户瓶子序列中添加'''
        self.bottles.append(bottle)
        self.bottles_per_section.append(bottle)
        self.history_bottles.append(bottle)
    
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
    
    def checkIfCoinExistInSavedCoins(self, value):
        '''检测玩家是否有给定面额的硬币在贮存硬币中，如果有则返回该硬币，没有则返回SpecificCoinNotExistError()'''
        for coin in self.saved_coins:
            if coin.value == value:
                return coin
        
        raise SpecificCoinNotExistError()
        