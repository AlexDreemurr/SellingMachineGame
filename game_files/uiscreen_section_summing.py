# -*- coding: utf-8 -*-

from shared_userdata import UserData
from bottle import Bottle, MixedBottle, BasedBottle
from game_pics import bottle_pics
from useful_methods.space_counter import space_counter
from useful_methods.color_phrase import color_phrase, makeWordsColor, judgeEarnOrLose
from seller import Seller
from task import Task, TaskManager

import os
import sys
import json
import time


class uiscreenSectionSumming():
    def display(section, game_income):
        '''3回合结束，打印结算页，返回总盈利
            section: 章节数'''
        if section == 1:
            section_summing_page = """            ╭─────────────────────────────────────────────────────────╮
            │                                                         │
            │   ╭──╮┐              ┌┐            章 末 小 结          │
            │   │   ├─╮╭─╮┌─╮─┼─    │        ───────────────────      │
            │   ╰──╯┴ ┴╰─┴├─╯ └─   ─┴─          S U M M A R Y         │
            │             ┴                                           │
            │                                                         │
            │    在你巧夺天工的双手下，诞生了琳琅满目的地球饮料组合！ │
            │                                                         │
            │    顺利通过第一章！                                     │
            ╰─────────────────────────────────────────────────────────╯
    """
            print(section_summing_page)

            print("              【瓶子射手】附加游戏的奖金：", judgeEarnOrLose(game_income))
            print()
            summary_list = TaskManager.returnSummaryList()
            print("             \033[1;33m额外任务     完成度        完成状态      获得奖金\033[0m")
            time.sleep(1)
            total_sum = 0
            for summary in summary_list:
                print()
                summary: list
                name, percentage, status, salary = summary
                total_sum += salary

                print(f"             {space_counter(name, 14)}{space_counter((str(percentage) + '%'), 14)}{space_counter(status, 14)}{space_counter(judgeEarnOrLose(salary), 10)}")
                time.sleep(0.5)

            print()
            time.sleep(0.5)
            print("             任务总盈利：                                 ", judgeEarnOrLose(total_sum))
            print()
            print()
            input("             >>> 按回车进入下一章。")
            return total_sum

'''
a = BasedBottle("water")
b = BasedBottle("beer")
UserData.user_bottles = [a, b, MixedBottle(a, b)]
uiscreenSumming.display()
'''
#uiscreenSectionSumming.display()