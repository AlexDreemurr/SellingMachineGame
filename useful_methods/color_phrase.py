# -*- coding: utf-8 -*-
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "color_item_list.json"), "r", encoding="utf-8") as f:
    COLOR_ITEM_LIST = json.loads(f.read())

with open(os.path.join(BASE_DIR, "item_translation.json"), "r", encoding="utf-8") as f:
    ITEM_TRANSLATION = json.loads(f.read())

def color_phrase(word):
    '''输入一个英文饮品名称，如果是彩色字返回彩色中文译名，否则返回中文译名'''
    trans_word = ITEM_TRANSLATION[word]
    if word in COLOR_ITEM_LIST.keys():
        color = COLOR_ITEM_LIST[word]

        if color == "yellow":
            return f"\033[33m{trans_word}\033[0m"
        elif color == "lightyellow":
            return f"\033[93m{trans_word}\033[0m"
    else:
        return trans_word
    
def phrase(word):
    '''输入英文饮品名称，返回中文译名'''
    return ITEM_TRANSLATION[word]

def makeWordsColor(word, color = "yellow"):
    '''输入一个字符串和颜色名，提供彩色字符串码'''
    if color == "yellow":
        return f"\033[33m{word}\033[0m"
    elif color == "green":
        return f"\033[32m{word}\033[0m"
    elif color == "red":
        return f"\033[31m{word}\033[0m"
    elif color == "grey":
        return f"\033[90m{word}\033[0m"
    
def judgeEarnOrLose(balance):
    '''输入一个金额，如果>0则返回该金额的绿色字符串(带加号），=0为灰色，<0为红色'''
    if balance == 0:
        return makeWordsColor(balance, "gray")
    elif balance > 0:
        return makeWordsColor("+" + str(balance), "green")
    else:
        return makeWordsColor(balance, "red")
