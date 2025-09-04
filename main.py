# -*- coding: utf-8 -*-

from coin import Coin
from coin_charger import Charger, MoneyNotEnoughError
from bottle import Bottle, MixedBottle, BasedBottle
from extraGame_001.main import Main as main_extraGame01
from game_pics import chapter_1_bonus_level_pic
from machine import Machine, ItemNotFindError, ItemNotEnoughError, CoinNotAvailableError, HaveNoMoneyToBuyError
from shared_machinedata import MachineData
from shared_userdata import UserData
from seller import Seller
from task import Task, TaskManager
from uiscreen import Uiscreen
from uiscreen_summing import uiscreenSumming
from uiscreen_section_summing import uiscreenSectionSumming
from uiscreen_introduction import uiscreenBeginning, uiscreenTitle, uiscreenTutorial
from useful_methods.price_round import price_round
from user import User, SpecificCoinNotExistError
import os 
import time

class PageNotFound(Exception):
    '''未找到对应页码'''
    pass

class PageError(Exception):
    '''页面格式错误'''
    pass


def clear():
    '''清屏'''
    os.system('cls' if os.name == 'nt' else 'clear')

def changePage(user_input):
    '''接受用户输入的内容，切换页面'''
    page = 1
    # 如果P后面为非数字
    try:
        page = int(user_input[1:])
    except:
        raise PageError()
    
    # 如果输入的页码数不存在 
    if page > Uiscreen.total_page_count or page <= 0:
        raise PageNotFound()
    
    player.page = page
    Uiscreen.page = player.page
    UserData.tip_information = ""




player = User("Alex")


'''开场界面'''
user_chosen = "玩法教程"
while True:
    clear()
    UserData.user_chosen = user_chosen
    uiscreenTitle.printTitle()

    print("            1：开始游戏  2：玩法教程")
    user = input("            >>> ")
    if user == "1":
        break
    elif user == "2":
        uiscreenTutorial.printTutorial()


'''游戏初始化变量'''
game_status = True
# 所在的回合数和阶段数，每3个回合为1章
game_round = 1
game_section = 1
# 当前回合结束
round_end = True
Machine.item_data = Machine.setMenuItem('1') # 初始是第一组5个饮料

# 开启第一张开头画面
if game_section == 1 and game_round == 1:
    clear()
    uiscreenTitle.sectionStartPage(1)

UserData.task_list = TaskManager.generate_tasks()
player.task_list = UserData.task_list
    
    

'''游戏主界面'''
while game_status:
    # 将玩家数据共享到shared_userdata中，方便uiscreen调用 
    UserData.user_coins = player.coins                                # 硬币列表
    UserData.user_saved_coins = player.saved_coins                    # 贮存硬币列表
    UserData.user_saved_100_coin_count = player.saved_coins_100_count # 贮存100的硬币数量
    UserData.user_saved_500_coin_count = player.saved_coins_500_count # 贮存500的硬币数量
    UserData.user_balance = player.balance                            # 玩家总余额
    UserData.user_saving_balance = player.saving_balance              # 玩家贮存硬币总余额
    UserData.user_bottles = player.bottles                            # 实时瓶子列表
    UserData.user_bottles_per_section = player.bottles_per_section    # 当前阶段瓶子列表
    UserData.user_history_bottles = player.history_bottles            # 历史所有瓶子列表
    UserData.task_list = player.task_list                             # 当前任务列表
    UserData.page = player.page                                       # 当前所处页码数
    UserData.game_round = game_round                                  # 游戏回合数
    UserData.game_section = game_section                              # 游戏阶段数 

    # 将售货机数据共享到shared_machinedata中
    MachineData.AVAILABLE_COINS_OUTPUT = Machine.AVAILBALE_COINS_OUTPUT          # 售货机可以吐出的硬币面额列表
    MachineData.ACCEPTABLE_COINS = Machine.ACCEPTABLE_COINS                      # 售货机支持的硬币面额列表
    MachineData.ACCEPTABLE_COINS_FOR_SAVE = Machine.ACCEPTABLE_COINS_FOR_SAVE    # 硬币贮存操作支持的硬币面额列表
    # 更新任务信息
    TaskManager.updateAll()

    # player.display()

    # 如果进入一个新的章节，则重置任务列表
    if game_round % 3 == 1 and round_end:
        # 删除原有任务列表
        UserData.task_list = []
        player.task_list = []
        # 创建新任务列表
        UserData.task_list = TaskManager.generate_tasks()
        player.task_list = UserData.task_list

    if game_round == 2:
        Machine.item_data = Machine.setMenuItem("1")
    if game_section == 2:
        # 切换到第二种
        Machine.item_data = Machine.setMenuItem("2")

    round_end = False

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

        if user_input[0] == "P":
                '''切换页面'''
                try:
                    changePage(user_input)
                except PageNotFound:
                    UserData.tip_information = "输入的页码有误。当前一共只有2页。"
                except PageError:
                    UserData.tip_information = "页码格式有误，请在P后面跟上页码数字（1/2）"

        # 第一页：混合、结算操作
        if player.page == 1:    
            if user_input == "结算":
                # 进入结算画面
                clear()
                earn = uiscreenSumming.display()

                # 给玩家加钱
                new_earned_coins = Charger.charger(earn)
                for coin in new_earned_coins:
                    player.addCoin(coin)
                
                # 清空本回合瓶子
                player.bottles = []

                # 售货机自动添加商品
                Machine.autoRefillItem(game_round)

                # 游戏货币通货膨胀
                Machine.autoRisePrice(game_round)

                UserData.tip_information = ""
                # 如果破产了游戏结束，否则回合数加一
                try:
                    Machine.checkIfPlayerCanBuyAny(player.balance)
                except HaveNoMoneyToBuyError:
                    game_status = False
                    continue
                else:
                    round_end = True

                    # 根据阶段数和回合数播放阶段小结画面
                    if game_section == 1 and game_round == 3:
                        clear()
                        print(chapter_1_bonus_level_pic)
                        input("            >>> 按回车开始奖励关：记得按鼠标移动瓶子哦~")
                        clear()
                        # 跳转至奖励关
                        extra_money = main_extraGame01()
                        task_money = uiscreenSectionSumming.display(1, extra_money)
                        # 给玩家加钱
                        extra_coins = Charger.charger(extra_money)
                        task_coins = Charger.charger(task_money)
                        for coin in extra_coins:
                            player.addCoin(coin)
                        for coin in task_coins:
                            player.addCoin(coin)


                    # 播放下一章开头动画
                    if game_section == 1 and game_round == 3:
                        clear()
                        uiscreenTitle.sectionStartPage(2)

                    # 根据回合数增加硬币支持
                    if game_round == 3:
                        MachineData.ACCEPTABLE_COINS.append(5)
                        UserData.tip_information = "现在售货机将支持面额为5的硬币投入。"
                    if game_round == 5:
                        MachineData.ACCEPTABLE_COINS.append(1)
                        UserData.tip_information = "现在售货机将支持面额为1的硬币投入。"

                    # 更新Seller的幸运瓶gap数值膨胀
                    Seller.gap = price_round(Seller.gap * 1.1)
                    print(Seller.gap)

                    # 更新阶段数
                    if game_round % 3 == 0:
                        game_section += 1
                    game_round += 1
                    continue

            try:
                a, b = user_input.split("+")
                bottle1 = player.bottles[int(a) - 1]
                bottle2 = player.bottles[int(b) - 1]
            except:
                UserData.tip_information = "你输入的混合信息有误，请用加号连接两杯饮料的序号。决定结束本回合请输入结算。"
                continue
        
            # 清屏
            UserData.tip_information = ""
            # 混合瓶子，添加新瓶子并删除旧瓶子
            player.addBottle(MixedBottle(bottle1, bottle2))
            player.deleteBottle(bottle1)
            player.deleteBottle(bottle2)

        # 第二页：查看任务、贮存金币
        elif player.page == 2:
            if user_input[0] == "S":
                '''贮存操作'''
                try:
                    value = int(user_input[1:])
                except:
                    UserData.tip_information = "格式错误，贮存请在S后输入你想贮存的硬币（支持100/500）"
                    continue
                else:
                    try:
                        '''存硬币'''
                        player.saveCoin(value)
                    except SpecificCoinNotExistError:
                        UserData.tip_information = "你没有这种面额的硬币。"
                        continue
                    except CoinNotAvailableError:
                        UserData.tip_information = "硬币贮存仅支持500/100硬币。"
                        continue
                    else:
                        UserData.tip_information = ""

            elif user_input[0] == "W":
                '''取钱操作'''
                try:
                    value = int(user_input[1:])
                except:
                    UserData.tip_information = "格式错误，取钱请在W后输入你想取出的硬币（支持100/500）"
                    continue
                else:
                    try:
                        '''取硬币'''
                        player.withdrawCoin(value)
                    except SpecificCoinNotExistError:
                        UserData.tip_information = "你没有这种面额的硬币。"
                        continue
                    except CoinNotAvailableError:
                        UserData.tip_information = "硬币存储系统仅支持500/100硬币。"
                        continue
                    else:
                        UserData.tip_information = ""
            else:
                UserData.tip_information = "未知输入。存钱请输入S+金额(100/500)，取钱请输入W+金额(100/500)，切换页面请输入P+页码数。"


    else:
        '''玩家还能继续购买'''

        # 刷屏
        clear()
        Uiscreen.display()
        # 用户输入
        user_input = input("Stage 1>>> ")

        if user_input == "":
            UserData.tip_information = "未知输入。投币请输入面额，购买商品请输入位置，切换页面请输入P+页码数，退币请输入退钱。"
            continue

        if user_input[0] == "P":
            '''切换页面'''
            try:
                changePage(user_input)
            except PageNotFound:
                UserData.tip_information = "输入的页码有误。当前一共只有2页。"
            except PageError:
                UserData.tip_information = "页码格式有误，请在P后面跟上页码数字（1/2）"
            finally:
                continue
        
        # 第一页：投币、购买、退钱操作
        if player.page == 1:
            try:
                '''尝试字符串变整数'''
                int(user_input)
                
            except ValueError:
                '''如果输入含有文字'''
                
                if user_input[0] in ["A", "B"]:
                    '''购买操作'''

                    pivot_position = user_input

                    # 找到要买的东西
                    try:
                        item_name = Machine.searchItem(pivot_position)
                    except ItemNotFindError:
                        UserData.tip_information = "你输入的商品位置有误。"
                        continue

                    # 计算找钱
                    try:
                        charged_coin_list = Charger.charge(Machine.current_input_coins, Machine.item_data[item_name]["price"])
                    except MoneyNotEnoughError:
                        UserData.tip_information = "你投入的金额不够。"
                        continue

                    # 贩卖机完成购买
                    try:
                        Machine.sell(item_name)
                    except ItemNotEnoughError:
                        UserData.tip_information = "该商品已售罄。"
                        continue
                    
                    '''这下面说明交易没有问题，可以交易'''
                    # 创建基底瓶子，添加到玩家瓶子序列中
                    new_bottle = BasedBottle(Machine.item_data[item_name]["tag"])
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

                elif user_input == "退钱":
                    for coin in Machine.current_input_coins:
                        player.addCoin(coin)
                    
                    Machine.clearCoin()
                    UserData.tip_information = ""


                else:
                    UserData.tip_information = "未知输入。投币请输入面额，购买商品请输入位置，切换页面请输入P+页码数，退币请输入退钱。"
                    continue


            else:
                '''输入为纯数字，代表投币操作'''
                try:
                    '''检测玩家是否拥有该面额硬币'''
                    pivot_coin = player.checkIfCoinExist(int(user_input))
                except SpecificCoinNotExistError:
                    UserData.tip_information = "你没有这种面额的硬币。"
                    continue
                
                else:
                    # 贩卖机完成投币后处理
                    try:
                        Machine.inputCoin(pivot_coin)
                    except CoinNotAvailableError:
                        UserData.tip_information = "售货机不支持该种硬币。"
                        continue

                    # 删除玩家钱序列里投入的硬币
                    player.deleteCoin(pivot_coin)
                    UserData.tip_information = ""
        
        # 第二页：查看任务、贮存硬币、取出硬币
        elif player.page == 2:
            if user_input[0] == "S":
                '''贮存操作'''
                try:
                    value = int(user_input[1:])
                except:
                    UserData.tip_information = "格式错误，贮存请在S后输入你想贮存的硬币（支持100/500）"
                    continue
                else:
                    try:
                        '''存硬币'''
                        player.saveCoin(value)
                    except SpecificCoinNotExistError:
                        UserData.tip_information = "你没有这种面额的硬币。"
                        continue
                    except CoinNotAvailableError:
                        UserData.tip_information = "硬币贮存仅支持500/100硬币。"
                        continue
                    else:
                        UserData.tip_information = ""

            elif user_input[0] == "W":
                '''取钱操作'''
                try:
                    value = int(user_input[1:])
                except:
                    UserData.tip_information = "格式错误，取钱请在W后输入你想取出的硬币（支持100/500）"
                    continue
                else:
                    try:
                        '''取硬币'''
                        player.withdrawCoin(value)
                    except SpecificCoinNotExistError:
                        UserData.tip_information = "你没有这种面额的硬币。"
                        continue
                    except CoinNotAvailableError:
                        UserData.tip_information = "硬币存储系统仅支持500/100硬币。"
                        continue
                    else:
                        UserData.tip_information = ""

            else:
                UserData.tip_information = "未知输入。存钱请输入S+金额(100/500)，取钱请输入W+金额(100/500)，切换页面请输入P+页码数。"


        
UserData.tip_information = f"游戏结束！你共计坚持了 {game_round} 个回合。"

# 刷屏
clear()
Uiscreen.display()

input(">>> 按回车以结束游戏")

'''
player.addBottle(Bottle("milk"))
player.addBottle(Bottle("coffee"))
UserData.user_bottles = player.bottles
uiscreenSumming.display()
'''
