# -*- coding: utf-8 -*-

from machine import Machine
from coin import Coin
from game_pics import bottle_pics, coin_pics

class Uiscreen():

    def display():
        '''显示游戏画面'''

        '''瓶子的显示状态：
            1：在售、投入的钱不够 -> 小数字靠下
            2：在售、投入的钱足够 -> 大数字
            3：被选中
            0：已售罄'''

        # 数字字体
        small_number_under = "₁₂₃₄₅₆₇₈₉"
        small_number_above = "¹²³⁴⁵⁶⁷⁸⁹"
        large_number = "123456789"

        # 根据Machine信息设置每个瓶子的状态列表
        bottle_statuses = [1 for i in range(14)] 
        pivot = 0
        cur_status = 1
        for name in Machine.item_data:
            cur_status = 1
            for i in range(len(Machine.item_data[name]["position"])):
                if Machine.item_data[name]["count"] <= 0:
                    cur_status = 0
                elif Machine.caculateInputSum() >= Machine.item_data[name]["price"]:
                    cur_status = 2
                bottle_statuses[pivot] = cur_status
                pivot += 1

        # 不同状态下瓶子显示的图案
        def bottle_display(number, status):
            if status == 1:
                return large_number[number - 1]
            elif status == 2:
                return "\033[6m" + large_number[number - 1] + "\033[0m"
            elif status == 0:
                return "\033[31m" + "╳" + "\033[0m"
            elif status == 3:
                return "O"
        b = bottle_statuses
        bs = bottle_display

        # 商品信息列表（添加于售货机右侧）
        info_linelists = []
        for i in Machine.item_data:
            info_linelists.append("{:<16}{:<9}{:<8}{:<4}".format(i.replace("_", " "), Machine.item_data[i]["price"],  Machine.item_data[i]["count"], " ".join(Machine.item_data[i]["position"])))
        
        # 将硬币信息转化成图示，按行得到图示列表以备打印
        from shared_userdata import UserData
        coin_linelists = ["" for i in range(4)]
        for i in range(3, -1, -1):
            for coin in UserData.user_coins:  
                if (4 - i) > len(coin_pics[coin.value]):
                    coin_linelists[i] += " " * len(coin_pics[coin.value][0])
                else:
                    coin_linelists[i] += coin_pics[coin.value][i - 4]

        # 将瓶子信息转化成图示，按行得到图示列表以备打印
        bottle_linelists = ["" for i in range(5)]
        for i in range(4, -1, -1):
            for bottle in UserData.user_bottles:  
                if (5 - i) > len(bottle_pics[bottle.label]):
                    bottle_linelists[i] += " " * len(bottle_pics[bottle.label][0])
                else:
                    bottle_linelists[i] += bottle_pics[bottle.label][i - 5]


        # 售货机图案
        MACHINE_PIC = f'''
  +—————————————————————+
 ╱/////////////////////╱|
+—————————————————————+ |
|  Selling  Machine   |╱|
|_____________________| |
|╭o╮╭o╮╭o╮╭o╮╭o╮╭o╮╭o╮|A|
|│{bs(1, b[0])}││{bs(2, b[1])}││{bs(3, b[2])}││{bs(4, b[3])}││{bs(5, b[4])}││{bs(6, b[5])}││{bs(7, b[6])}│| |
|╰─╯╰─╯╰─╯╰─╯╰─╯╰─╯╰─╯|╱|
|─────────────────────| |
|╭o╮╭o╮╭o╮╭o╮╭o╮╭o╮╭o╮|B|
|│{bs(1, b[7])}││{bs(2, b[8])}││{bs(3, b[9])}││{bs(4, b[10])}││{bs(5, b[11])}││{bs(6, b[12])}││{bs(7, b[13])}│| |
|╰─╯╰─╯╰─╯╰─╯╰─╯╰─╯╰─╯|╱|
|‾‾‾‾‾‾‾‾‾│‾‾‾‾‾‾‾‾‾‾‾| |
| IN \033[90m{Machine.caculateInputSum():04}\033[0m │  ╭╮   ╭╮  | |
|—————————│  ╰╯   ╰╯  | +
|OUT \033[90m{Machine.caculateLastChargeSum():04}\033[0m │Coin Charge|╱|
+—————————+———————————+ |
|   ┌─────────────┐   | |
|   │             │   | |
|   │             │   | +
|   └─────────────┘   |╱
+—————————————————————+
'''
        machine_pic = MACHINE_PIC.split("\n")[1:]

        # 逐行打印售货机图案以及售货机右侧的商品信息、硬币图示、购买的瓶子图示、提示信息
        for i in range(len(machine_pic)):
            print(machine_pic[i], end = "")
            if i == 2:
                print(" " * 22 + "Round" , str(UserData.game_round), end = "")
            if 3 <= i <= 3 + len(info_linelists):
                print(" " * 5, end = "")
                if i == 3:
                    print("Name         Price    Left      Position", end = "")
                else:
                    print(info_linelists[i - 4], end = "")

            if 9 < i <= 9 + len(coin_linelists):
                print(" " * 5, end = "")
                print(coin_linelists[i - 10], end = "")

            if 14 < i <= 14 + len(bottle_linelists):
                print(" " * 5, end = "")
                print(bottle_linelists[i - 15], end = "")

            if i == 21:
                print(" " * 7, end = "")
                print(UserData.tip_information, end = "")
            print()



'''
 ╭─╮    O
╭╯*╰╮  ╭╯╰╮
│100│  │50│  
╰───╯  ╰──╯
   ╭─╮ 
 ╭─╯*╰─╮
 │ 500 │
 ╰─────╯   
╭──╮
│10│
╰──╯
╭─╮
│5│
╰─╯
╭─╮
│1│
╰─╯

 ⌂⏒±※‗‖‡
__
‾‾
₅₆₇₈₉₁₀₂₃₄
⁰¹²³⁴⁵⁶⁷⁸⁹

Name           Price   Vol   Left   Position
pure water       120   500ml   15   [11, 12, 13]
instant coffee   140   400ml   10   [14, 15]
apple juice      150   280ml   8    [16, 17]
peach juice      160   350ml   10   [21, 22, 23]
wheat tea        140   600ml   15   [24, 25, 26, 27]
'''

