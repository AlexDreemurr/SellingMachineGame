# -*- coding: utf-8 -*-
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(sys.executable)) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "json/color_item_list.json"), "r", encoding="utf-8") as f:
    COLOR_ITEM_LIST = json.loads(f.read())

with open(os.path.join(BASE_DIR, "json/item_translation.json"), "r", encoding="utf-8") as f:
    ITEM_TRANSLATION = json.loads(f.read())

def if_colored(word):
    '''检查一个字符串有没有彩色字编码，返回True/False'''
    if word[0] == "\033":
        return True
    return False

def get_color(word):
    '''检查一个字符串的彩色字的颜色是什么'''
    color_num = int(word.split("\033")[1][1: word.split("\033")[1].find("m")])
    if color_num == 33:
        return "yellow"
    elif color_num == 32:
        return "green"
    elif color_num == 90:
        return "grey"
        
def remove_color(word):
    '''去除一个字符串的彩色字编码'''
    if if_colored(word):
        return word.split("\033")[1][word.split("\033")[1].find("m") + 1:]

    return word

def color_phrase(word, color = ""):
    '''输入一个英文饮品名称，如果是彩色字返回彩色中文译名，否则返回中文译名'''

    if if_colored(word):
        color = get_color(word)
        word = remove_color(word)
        
        trans_word = ITEM_TRANSLATION[word]
        trans_word = makeWordsColor(trans_word, color)
    
    else:
        trans_word = ITEM_TRANSLATION[word]

    if word in COLOR_ITEM_LIST.keys():
        color = COLOR_ITEM_LIST[word]
        if color != "":
            return makeWordsColor(trans_word, color=color)
        else:
            return makeWordsColor(trans_word, word)
    
    else:
        return trans_word
    
def makeWordsColor(word, color = "yellow"):
    '''输入一个字符串和颜色名，提供彩色字符串码'''
    if color == "yellow":
        return f"\033[33m{word}\033[0m"
    elif color == "lightyellow":
        return f"\033[93m{word}\033[0m"
    elif color == "green":
        return f"\033[32m{word}\033[0m"
    elif color == "red":
        return f"\033[31m{word}\033[0m"
    elif color == "grey":
        return f"\033[90m{word}\033[0m"
    
def judgeEarnOrLose(balance):
    '''输入一个金额，如果>0则返回该金额的绿色字符串(带加号），=0为灰色，<0为红色'''
    if balance == 0:
        return makeWordsColor(balance, "grey")
    elif balance > 0:
        return makeWordsColor("+" + str(balance), "green")
    else:
        return makeWordsColor(balance, "red")
