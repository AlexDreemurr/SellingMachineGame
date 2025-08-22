# -*- coding: utf-8 -*-

from coin import Coin
from coin_charger import Charger, MoneyNotEnoughError
from bottle import Bottle, MixedBottle
from machine import Machine, ItemNotFindError, ItemNotEnoughError, CoinNotAvailableError, HaveNoMoneyToBuyError
from shared_machinedata import MachineData
from shared_userdata import UserData
from seller import Seller
from uiscreen import Uiscreen
from uiscreen_summing import uiscreenSumming
from user import User, SpecificCoinNotExistError
import os 
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


player = User("Alex")
game_status = True
game_round = 1

while game_status:
    time.sleep(0.5)

    # 将玩家金钱和瓶子列表共享到shared_userdata中，方便uiscreen调用
    UserData.user_coins = player.coins
    UserData.user_bottles = player.bottles
    UserData.game_round = game_round
    MachineData.AVAILABLE_COINS_OUTPUT = Machine.AVAILBALE_COINS_OUTPUT
    MachineData.ACCEPTABLE_COINS = Machine.ACCEPTABLE_COINS
    # player.display()

    try:
        '''检测玩家是否还有钱能继续购买'''
        Machine.checkIfPlayerCanBuyAny(player.sumMoneyAvailableForMachine())

    except HaveNoMoneyToBuyError:
        '''玩家不能继续购买'''

        # 刷屏
        clear()
        Uiscreen.display()

        # 用户输入
        user_input = input("Stage 2>>> ")

        if user_input == "done":
            # 进入结算画面
            clear()
            earn = uiscreenSumming.display()

            # 给玩家加钱
            new_earned_coins = Charger.charger(earn)
            for coin in new_earned_coins:
                player.addCoin(coin)
            player.sortCoin()

            # 清空本回合瓶子
            player.bottles = []

            # 售货机自动添加商品
            Machine.autoRefillItem(game_round)

            # 游戏货币通货膨胀
            Machine.autoRisePrice(game_round)

            UserData.tip_information = ""
            # 如果破产了游戏结束，否则回合数加一
            try:
                Machine.checkIfPlayerCanBuyAny(player.sumMoneyAvailableForMachine())
            except HaveNoMoneyToBuyError:
                game_status = False
                continue
            else:
                game_round += 1
                if game_round == 3:
                    MachineData.ACCEPTABLE_COINS.append(5)
                    UserData.tip_information = "Now The 5-Coin is available for use."
                if game_round == 5:
                    MachineData.ACCEPTABLE_COINS.append(1)
                    UserData.tip_information = "Now The 1-Coin is available for use."
                continue
        
        try:
            a, b = user_input.split("+")
            bottle1 = player.bottles[int(a) - 1]
            bottle2 = player.bottles[int(b) - 1]
        except:
            UserData.tip_information = "Your entry is illegal. To mix two drinks, type like'1+2'.\n                                                     Enter 'done' to end this turn."
            continue
        
        # 混合瓶子，添加新瓶子并删除旧瓶子
        player.addBottle(MixedBottle(bottle1, bottle2))
        player.deleteBottle(bottle1)
        player.deleteBottle(bottle2)

    else:
        '''玩家还能继续购买'''

        # 刷屏
        clear()
        Uiscreen.display()

        # 用户输入
        user_input = input("Stage 1>>> ")

        try:
            '''尝试字符串变整数'''
            int(user_input)
            
        except ValueError:
            '''如果输入含有文字'''
            if user_input == "":
                UserData.tip_information = "Unknown entry. For inserting coins, enter the value of the coin like '500'. \n                                             For Buying drinks, enter the position like 'A1'. \n                                             For Refunding the coins off the machine, enter 'refund'"
                continue
            
            if user_input[0] in ["A", "B"]:
                '''购买操作'''

                pivot_position = user_input

                # 找到要买的东西
                try:
                    item_name = Machine.searchItem(pivot_position)
                except ItemNotFindError:
                    UserData.tip_information = "You've entered the wrong position."
                    continue

                # 计算找钱
                try:
                    charged_coin_list = Charger.charge(Machine.current_input_coins, Machine.item_data[item_name]["price"])
                except MoneyNotEnoughError:
                    UserData.tip_information = "Inserted coins are not enough to pay for it."
                    continue

                # 贩卖机完成购买
                try:
                    Machine.sell(item_name)
                except ItemNotEnoughError:
                    UserData.tip_information = "This drink has sold out."
                    continue
                
                '''这下面说明交易没有问题，可以交易'''
                # 创建瓶子，添加到玩家瓶子序列中
                new_bottle = Bottle(Machine.item_data[item_name]["tag"])
                player.addBottle(new_bottle)

                # 清除上次售货机的找钱金额记录
                Machine.last_charge_coins = []

                # 把找的钱添加到玩家钱序列中
                for coin in charged_coin_list:
                    player.addCoin(coin)

                # 售货机记录找钱金额
                Machine.last_charge_coins = charged_coin_list
                
                # 刷屏，显示找钱金额
                UserData.tip_information = ""

            elif user_input == "refund":
                for coin in Machine.current_input_coins:
                    player.addCoin(coin)
                
                Machine.clearCoin()

            else:
                UserData.tip_information = "Unknown entry. For inserting coins, enter the value of the coin like '500'. \n                                             For Buying drinks, enter the position like 'A1'. \n                                             For Refunding the coins off the machine, enter 'refund'"


        else:
            '''输入为纯数字，代表投币操作'''
            try:
                '''检测玩家是否拥有该面额硬币'''
                pivot_coin = player.checkIfCoinExist(int(user_input))
            except SpecificCoinNotExistError:
                UserData.tip_information = "You do not have that type of coin."
                continue
            
            else:
                # 贩卖机完成投币后处理
                try:
                    Machine.inputCoin(pivot_coin)
                except CoinNotAvailableError:
                    UserData.tip_information = "The Selling Machine does not support this coin currently."
                    continue

                # 删除玩家钱序列里投入的硬币
                player.deleteCoin(pivot_coin)
                UserData.tip_information = ""
        
UserData.tip_information = f"GAME OVER! You have lasted {game_round} Rounds!"

# 刷屏
clear()
Uiscreen.display()

input(">>> Press enter to quit the game.")

'''
player.addBottle(Bottle("milk"))
player.addBottle(Bottle("coffee"))
UserData.user_bottles = player.bottles
uiscreenSumming.display()
'''