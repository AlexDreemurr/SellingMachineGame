# -*- coding: utf-8 -*-

from shared_userdata import UserData
from shared_machinedata import MachineData
from useful_methods.color_phrase import color_phrase, makeWordsColor, if_colored,  get_color, remove_color
from copy import deepcopy
import os
import sys
import json

BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "json/bottletype_translation.json"), "r", encoding="utf-8") as f:
    BOTTLETYPE_TRANSLATION = json.loads(f.read())

class Task():
    '''任务类父类'''

    def __init__(self, name, type, salary):
        ''' name: 任务的中文名称
            content: 任务内容的中文介绍
            type: 任务类型：
                    实时  --> 实时任务（必须在某一时刻拥有条件里的所有瓶子，如果之前有过但在达成任务之前没有了不行）
                    累计  --> 累计任务 (获得的瓶子只要累计达成就算达成）

            salary: 完成后的奖金金额
            complete_percentag: 项目完成度
            is_completed: 项目是否已完成（如果为True，将不再调用更新完成度的方法，因为有的任务是检查实时的瓶子情况，防止再变回False）'''
        self.name = name
        self.content = ""
        self.type = type
        self.salary = salary
        self.complete_percentage = 0
        self.is_completed = False

    def generateContent(self):
        '''生成任务内容介绍文字'''
        raise NotImplementedError()

    def updateCompletePercentage(self):
        '''自动计算并更新项目完成度'''
        raise NotImplementedError()
    
    @staticmethod
    def getItemTranslation(item_tag):
        '''提供一个英文tag名，返回其中文译名'''
        return color_phrase(item_tag)
        
    @staticmethod
    def getItemListTranslation(item_list):
        '''提供一个英文tag名列表，返回对应的中文译名列表（有彩色字的要带彩色ansi编码)'''
        translated_list = []
        for item in item_list:
            translated_list.append(color_phrase(item))
        return translated_list

    @staticmethod
    def getBottletypeListTranslation(bottletype_list):
        '''提供一个英文bottletype列表，返回对应中文译名列表'''
        translated_list = []
        for item in bottletype_list:
            color = ""
            if if_colored(item):
                color = get_color(item)
                item = remove_color(item)

            new_item = BOTTLETYPE_TRANSLATION[item]

            if color != "":
                new_item = makeWordsColor(new_item, color)
            
            translated_list.append(new_item)

        return translated_list

class TaskManager():
    '''任务分配管理器'''
    def generate_tasks():
        '''根据当前阶段数，返回一个任务列表'''
        task_list = []
        if UserData.game_section == 1:
            cur_task = AllCollectPerSectionTask("瓶瓶俱到", 300, ["water", "coffee", "juice", "tea", "milk"])
            cur_task2 = getSpecificBottlesTask("奶牛之家", 500, "milk", 5)
            cur_task3 = GetDifferentSizesTask("水漫金山", 1000, "water", ["small", "common", "long", "giant"])
            task_list.append(cur_task)
            task_list.append(cur_task2)
            task_list.append(cur_task3)
        
        elif UserData.game_section == 2:
            cur_task = AllCollectPerSectionTask("调酒师", 600, ["alcohol", "wine", "beer", "sweetwine"])
            cur_task2 = getSpecificBottlesTask("幸运狗", 1200, "doublemysterious", 2)
            #cur_task3 = GetDifferentSizesTask("水漫金山", 1000, "water", ["small", "common", "long", "giant"])
            task_list.append(cur_task)
            task_list.append(cur_task2)
            #task_list.append(cur_task3)

        return task_list
    
    def returnSummaryList():
        '''返回包含任务名，完成进度，是否已完成，奖金(0或者完成之后有数字)列表的列表'''
        result_list = []
        for task in UserData.task_list:
            task: Task
            if not task.is_completed:
                result_list.append([task.name, task.complete_percentage, "未完成", 0])
            else:
                result_list.append([task.name, task.complete_percentage, "已完成", task.salary])

        return result_list
    
    def updateAll():
        '''更新UserData任务列表中的所有任务状态（仅在未完成任务的情况下）'''
        for task in UserData.task_list:
            task: Task
            if not task.is_completed:
                task.updateCompletePercentage()

class AllCollectPerSectionTask(Task):
    '''累计：1个部分（3回合），每种在需求列表中的瓶子至少获得1个，以完成任务'''

    def __init__(self, name, salary, needed_bottle_list):
        '''needed_bottle_list: 完成任务需要收集的饮料tag名
           history_bottle_list: 历史上已经收集的饮料tag名'''

        super().__init__(name, '累计', salary)

        self.needed_bottle_list = needed_bottle_list
        self.history_bottle_list = []

        translated_list = Task.getItemListTranslation(self.needed_bottle_list)
        stringed_list = "、".join(translated_list)
        self.content = f"以下每种至少获得过1瓶：{stringed_list}"

    def __updateContent(self):
        translated_list = Task.getItemListTranslation(self.needed_bottle_list)
        stringed_list = "、".join(translated_list)
        self.content = f"以下每种至少获得过1瓶：{stringed_list}"

    def updateCompletePercentage(self):
        target_count = len(self.needed_bottle_list)
        for needed_bottle_name in self.needed_bottle_list:
            for user_bottle in UserData.user_bottles_per_section:
                if needed_bottle_name == user_bottle.tag and needed_bottle_name not in self.history_bottle_list:
                    self.history_bottle_list.append(needed_bottle_name)
                    # 已经完成的瓶子，显示绿色字
                    for i in range(len(self.needed_bottle_list)):
                        if self.needed_bottle_list[i] == needed_bottle_name:
                            self.needed_bottle_list[i] = makeWordsColor(self.needed_bottle_list[i], "green")
                            self.__updateContent()

        self.complete_percentage = int(round(len(self.history_bottle_list) / target_count, 2) * 100)
        if self.complete_percentage == 100:
            self.is_completed = True


class getSpecificBottlesTask(Task):
    '''累计：获得某个特定的瓶子若干个，以完成任务'''

    def __init__(self, name, salary, bottle_tag, count):
        '''bottle_tag: 完成任务所需瓶子种类
           count: 所需瓶子数量'''
        
        super().__init__(name, "累计", salary)

        self.needed_bottle_tag = bottle_tag
        self.count = count
        self.current_count = 0

        translated_name = Task.getItemTranslation(self.needed_bottle_tag)
        self.content = f"收集{self.count}杯{translated_name}饮料"

    def __updateContent(self):
        translated_name = Task.getItemTranslation(self.needed_bottle_tag)
        self.content = f"收集{self.count}杯{translated_name}饮料"

    def updateCompletePercentage(self):
        current_count = 0
        for user_bottle in UserData.user_bottles_per_section:
            if user_bottle.tag == self.needed_bottle_tag:
                current_count += 1

        if current_count > self.current_count:
            self.current_count = current_count
            self.updateCompletePercentage()

        self.complete_percentage = int(round(self.current_count / self.count, 2) * 100)
        if self.complete_percentage == 100:
            self.is_completed = True

class GetDifferentSizesTask(Task):
    '''即时：同时获得一种瓶子的若干尺寸'''

    def __init__(self, name, salary, bottle_tag, bottletype_list):
        '''bottle_tag: 瓶子tag名
           bottletype_list: 瓶子的bottletype列表'''
        
        super().__init__(name, "即时", salary)

        self.bottle_tag = bottle_tag
        self.bottletype_list = bottletype_list
        self.current_count = 0

        translated_name = Task.getItemTranslation(self.bottle_tag)
        translated_list = Task.getBottletypeListTranslation(self.bottletype_list)
        translated_list_str = "、".join(translated_list)
        self.content = f"同时拥有{translated_name}饮料的以下尺寸：{translated_list_str}"

    def __updateContent(self, current_bottletypes):
        translated_name = Task.getItemTranslation(self.bottle_tag)
        translated_list = Task.getBottletypeListTranslation(current_bottletypes)
        translated_list_str = "、".join(translated_list)
        self.content = f"同时拥有{translated_name}饮料的以下尺寸：{translated_list_str}"

    def updateCompletePercentage(self):
        current_count = 0
        current_bottletypes = deepcopy(self.bottletype_list)
        target_count = len(self.bottletype_list)

        for bottletype in self.bottletype_list:
            for user_bottle in UserData.user_bottles:
                if user_bottle.tag == self.bottle_tag and user_bottle.bottletype == bottletype:
                    current_count += 1
                    for i in range(len(current_bottletypes)):
                        if current_bottletypes[i] == bottletype:
                            current_bottletypes[i] = makeWordsColor(current_bottletypes[i], "green")
                    break
        
        self.__updateContent(current_bottletypes)
        self.complete_percentage = int(round(current_count / target_count, 2) * 100)
        if self.complete_percentage == 100:
            self.is_completed = True
        


class GetBottlesTask(Task):
    '''获得某几种瓶子各几个，以完成任务'''

    def __init__(self, name, salary, needed_bottle_dict):
        '''needed_bottle_dict: 完成任务需要收集的 (饮料tag名：饮料数) 键值对构成的字典'''

        super().__init__(salary)

        self.name = name
        self.needed_bottle_dict = needed_bottle_dict

        translated_list = Task.getItemListTranslation(list(self.needed_bottle_dict.keys()))
        stringed_list = "、".join(translated_list)
        self.content = f"收集以下饮料，每种至少获得过1个：{stringed_list}"

    def updateCompletePercentage(self):
        current_count = 0
        target_count = sum(self.needed_bottle_dict.values())

        for needed_bottle_name in self.needed_bottle_dict:
            for user_bottle in UserData.user_bottles_per_section:
                if needed_bottle_name == user_bottle.tag and self.needed_bottle_:
                    current_count += 1
                    continue

        self.complete_percentage = int(round(current_count / target_count, 2) * 100)
        if self.complete_percentage == 100:
            self.is_completed = True