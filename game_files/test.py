# -*- coding: utf-8 -*-

from coin import Coin
from bottle import Bottle
from useful_methods.color_phrase import makeWordsColor
from useful_methods.space_counter import space_counter, my_len

a = "牛逼"
b = "100%"
colored = makeWordsColor(a, "green")
colored_b = makeWordsColor(b, "grey")
print(space_counter(colored, 10) + "|")


print(my_len(colored), my_len(colored_b))


















'''
coin_list = [Coin(500), Coin(500), Coin(100), Coin(100), Coin(50), Coin(10)]

coin_pics = {500: [" ╭───╮ ",
                   "╭╯'*'╰╮",
                   "│ 500 │",
                   "╰─────╯"], 
             100: [" ╭─╮ ",
                   "╭╯*╰╮",
                   "│100│",
                   "╰───╯"], 
             50:  [" ╭╮ ",
                   "╭╯╰╮",
                   "│50│",
                   "╰──╯"],
             10:  ["╭──╮",
                   "│10│",
                   "╰──╯"],
             5:   ["╭─╮",
                   "│5│",
                   "╰─╯"],
             1:   ["╭─╮",
                   "│1│",
                   "╰─╯"]}
coin_height = {500: 4, 
               100: 4, 
               50: 4, 
               10: 3, 
               5: 3,
               1: 3}

coin_linelists = ["" for i in range(max(list(coin_height.values())))]
for coin in coin_list:
    if coin_height[coin.value] == 4:
        coin_linelists[0] += coin_pics[coin.value][0]
for i in range(1, max(list(coin_height.values()))):
    for coin in coin_list:
        if coin_height[coin.value] == 4:
            coin_linelists[i] += coin_pics[coin.value][i]
        elif coin_height[coin.value] == 3:
            coin_linelists[i] += coin_pics[coin.value][i - 1]

for line in coin_linelists:
    print(line)

'''


bottle_list = [Bottle("water"), Bottle("milk"), Bottle("tea"), Bottle("coffee")]

bottle_pics = {"common": ["╭o╮", 
                          "│ │",
                          "╰─╯"], 
               "small": ["╭o╮",
                         "╰─╯"], 
               "long": ["╭o╮",
                        "│ │",
                        "│ │",
                        "╰─╯"],
               "giant": ["╭〇╮",
                         "│  │",
                         "│  │",
                         "╰──╯"],
               "commonM": ["╭o╮", 
                           "│M│",
                           "╰─╯"], 
               "longM": ["╭o╮",
                         "│M│",
                         "│ │",
                         "╰─╯"],
               "giantM": ["╭〇╮",
                          "│ M│",
                          "│  │",
                          "╰──╯"], 
               "commonT": ["╭o╮", 
                           "│T│",
                           "╰─╯"], 
               "longT": ["╭o╮",
                         "│T│",
                         "│ │",
                         "╰─╯"],
              "giantT": ["╭〇╮",
                         "│ T│",
                         "│  │",
                         "╰──╯"], 
              "commonÉ": ["╭o╮", 
                          "│É│",
                          "╰─╯"], 
              "longÉ": ["╭o╮",
                        "│É│",
                        "│ │",
                        "╰─╯"],
              "giantÉ": ["╭〇╮",
                         "│ É│",
                         "│  │",
                         "╰──╯"],
              "common~": ["╭o╮", 
                          "│~│",
                          "╰─╯"], 
              "long~": ["╭o╮",
                        "│~│",
                        "│~│",
                        "╰─╯"],
              "giant~": ["╭〇╮",
                         "│ ~│",
                         "│~ │",
                         "╰──╯"],
              "common#": ["╭o╮", 
                          "│#│",
                          "╰─╯"], 
              "long#": ["╭o╮",
                        "│#│",
                        "│ │",
                        "╰─╯"],
              "giant#": ["╭〇╮",
                         "│ #│",
                         "│# │",
                         "╰──╯"], 
              "smallcappuccino": ["____ ",
                                  "│‾‾├╮",
                                  "│fé├╯",
                                  "╰──╯ "], 
              "commoncappuccino": ["______ ",
                                   "│‾‾‾‾├╮",
                                   "│café├╯",
                                   "╰────╯ "],
              "giantcappuccino":  ["_______ ",
                                   "│‾‾‾‾‾├╮",
                                   "│     ││",
                                   "│ café├╯",
                                   "╰─────╯ "], 
              "commonmilktea": ["___╱_",
                                "│‾╱‾│",
                                "│╱oo│",
                                "╰───╯"],
              "giantmilktea": ["____╱╱_",
                               "│‾‾╱╱‾│",
                               "│o╱╱oo│",
                               "│╱╱ooo│",
                               "╰─────╯"], 
              "commonmilkshake": ["___╱_",
                                  "│‾╱‾│",
                                  "│╱~~│",
                                  "╰───╯"],
              "giantmilkshake": ["____╱╱_",
                                 "│‾‾╱╱‾│",
                                 "│`╱╱~`│",
                                 "│╱╱~`~│",
                                 "╰─────╯"], 
              "commonfruittea":  ["___││__",
                                  "│‾‾││‾│",
                                  " ╲~~~╱ ",
                                  "  ‾‾‾  "],
              "giantfruittea":  ["____││___",
                                 "│‾‾‾││‾‾│",
                                 " ╲~C┤│~╱ ",
                                 "  ╲~~~╱  ",
                                 "   ‾‾‾   "], 
              "smallpoison": ["____",
                              "│~~│",
                              "│@@│",
                              "╰──╯"], 
              "commonpoison": ["______",
                               "│~~~~│",
                               "│@@@@│",
                               "╰────╯"], 
              "giantpoison": ["_______",
                              "│~~~~~│",
                              "│~~~~~│",
                              "│@@@@@│",
                              "╰─────╯"]}
'''

bottle_linelists = ["" for i in range(4)]
for bottle in bottle_list:
    if len(bottle_pics[bottle.label]) == 4:
        bottle_linelists[0] += bottle_pics[bottle.label][0]
    else:
        bottle_linelists[0] += "   "

for bottle in bottle_list:
    if len(bottle_pics[bottle.label]) == 4:
        bottle_linelists[1] += bottle_pics[bottle.label][1]
    elif len(bottle_pics[bottle.label]) == 3:
        bottle_linelists[1] += bottle_pics[bottle.label][0]
    else:
        bottle_linelists[1] += "   "

for i in range(2, 4):
    for bottle in bottle_list:  
        bottle_linelists[i] += bottle_pics[bottle.label][i - (4 - len(bottle_pics[bottle.label]))]

for line in bottle_linelists:
    print(line)

'''
'''


small
____
│‾‾├╮
│fé├╯ 
╰──╯


common
______
│‾‾‾‾├╮
│café├╯
╰────╯
giant
_______
│‾‾‾‾‾├╮
│     ││ 
│ café├╯
╰─────╯


small
    
 ┬─╱─┬
 │╱~*│
 ╰───╯
     
giant

 ┬───╱─┬
 │*~╱~*│
 │~╱*~~│
 │╱~~*~│
 ╰─────╯

 common

 ┬──╱─┬
 │*╱~*│
 │╱~*~│
 ╰────╯
fruittea

___││__
│‾‾││‾│ 
 ╲~~~╱
  ╰─╯

____││___
│‾‾‾││‾‾│
 ╲~C┤│~╱ 
  ╲~~~╱
   ╰─╯

  
fruittea
   _|_
 ╭─╯│╰╮
 │ψ ┼o│
 ╰────╯

    _|_
 ╭──╯│╰╮
 │  o┼o│
 │ψ  ┼o│
 ╰─────╯


poison
______
│    │
│╳╳╳╳│
╰────╯
____
│  │
│╳╳│ 
╰──╯

_______
│     │
│     │ 
│╳╳╳╳╳│
╰─────╯

longlongmysterious

longlongdoublemysterious
╭o╮╭o╮
│?├┤?│
│ ├┤ │
│ ├┤ │
╰─╯╰─╯

longdoublemysterious
╭o╮╭o╮
│?├┤?│
│ ├┤ │
╰─╯╰─╯
doublemysterious
╭o╮╭o╮
│?├┤?│
╰─╯╰─╯

smallalcohol
╭o╮
╰─╯

commonalcohol
╭o╮
│Å│
╰─╯
longalcohol
╭o╮
│Å│
│ │
╰─╯
giantalcohol
╭〇╮
│ Å│
│  │
╰──╯

smallwine
╰┬╯
 ┴

commonwine
│ │
╰┬╯
 ┴

longwine
│ │
│ │
╰┬╯
 ┴ 

giantwine
│   │
│   │
╰─╥─╯
 ─╨─

giantlongwine
│   │
│   │
│   │
╰─╥─╯
 ─╨─

smallbeer
╭┬─╮
│╰─┤
│ ʙ│
╰──╯

commonbeer
╭┬──╮
│╰──┤
│  ʙ│
│   │
╰───╯

giantbeer
 ╭─╮
 ├-┤
╭╯ ╰╮
│ ʙɛ│
│ ɛʀ│
│   │
╰───╯


smallyogurt
┌/┐
╰─╯

commonyogurt
┌─╱┐
╰──╯

longyogurt
┌─╱┐
│  │
╰──╯
giantyogurt
┌──╱┐
│ ╱ │
│   │
╰───╯

commonjuiceyogurt
┌─╱┐
│╱D│
╰──╯

longjuiceyogurt
┌─╱┐
│╱D│
│D │
╰──╯

giantjuiceyogurt
┌──╱┐
│D╱D│
│ D │
╰───╯


commonsweetwine
┌───│╮
│....│
╰────╯

longsweetwine
┌───│╮
│...││
│.o..│
╰────╯

giantsweetwine
┌─────│╮
│.....││
│.oo..││
│.O..o.│
╰──────╯

A C E J M T ~

cocacola
╭o╮
│C│
╰─╯
__
‾‾
···. ·...·.·.. .· ·...··..· ·..·.。



cocktail      
  ╮__.╭
  │._·│
  │_·_│
  ╰─╥─╯
  ──╨──

  ╮ ╭
  │-│
  │ │
  │ │
  ╰─╯

  ╮ ╭
  │+│
  │ │
  │ │
  ╰─╯

⎩⎧⎨
╭ ╮ ╯ ╰
    

  ├──────┤  
│╱│    │╱│
├─┼─┬─┬┤ │
│ ├─├─┤│─┤
│╱  ├─┤│╱ 
├───┼─┼┤
    └─┘


      ├────────────┤  
    │╱│          │╱│
    ├─┼───────┬─┬┤ │
    │ ├───────├─┤│─┤
    │╱        ├─┤│╱ 
    ├─────────┼─┼┤
              └─┘



 ├─
 ├─
╭┴╮
╰─╯

    ╭──────┐
╭──╮├──────┴┬───────┐
│:)├┤       ├───────┤
╰──╯├──────┬┴───────┘
    ╰──────┘
        
    

      ├────────────────────────────┤  
     ╱├───────────────────────────╱│
    ╱╱│                          ╱╱│
   │╱ │                         │╱ │
  ╱│  │                        ╱│  │
│╱╱│  │______________________│╱╱│__│
├───────────────────┬─────┬──┤╱ │  │
│  │ ╱│             ├─────┤  │  │ ╱│
│  │╱ ├─────────────├─────┤──│──│╱─│
│  │ ╱│             ├─────┤  │  │ ╱│                              
│ ╱│╱               ├─────┤  │ ╱│╱ 
│╱ │                ├─────┤  │╱ │  
│‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│ ╱│
│╱                  ├─────┤  │╱
├───────────────────├─────┤──┤
│                   ├─────┤  │

              
      │                            │
     ╱├───────────────────────────╱│
    ╱ ├──────────────────────────╱ │
   ╱ ╱                          ╱ ╱│
  ╱│╱                          ╱│╱ │
│╱ │                         │╱ │  │
├────────────────────────────│ ╱│  │
├───────────────────┬─────┬──┤╱ │  │
│  │ ╱│‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│  │ ╱│
│  │╱ │‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│  │╱ │
│  │ ╱├─────────────├─────┤──│  │ ╱│                              
│ ╱│╱ │             ├─────┤  │ ╱│╱ │
│╱ ╱                ├─────┤  │╱ │  
│‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│ ╱│
│‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│╱
├───────────────────├─────┤──┤
│                   ├─────┤  │

      │                            │
     ╱├───────────────────────────╱│
    ╱ ├──────────────────────────╱ │
   ╱ ╱                          ╱ ╱│
  ╱│╱                          ╱│╱ │
│╱ │                         │╱ │  │
├───────────────────┬─────┬──│ ╱│  │
├───────────────────├─────┤──┤╱ │  │
│  │ ╱│‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│  │ ╱│
│  │╱ │|│|│|│|│|│|│|├─────┤|││  │╱ │
│  │ ╱└─────────────├─────┤──│  │ ╱│                              
│ ╱│╱               ├─────┤  │ ╱│╱ │
│╱ ╱                ├─────┤  │╱ │  
│‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾├─────┤‾‾│ ╱│
│|│|│|│|│|│|│|│|│|│|├─────┤|││╱
├───────────────────├─────┤──┤
│                   ├─────┤  │





┌──────────────────────────────────┐
│ ╭─╮╭─╮╭─╮╭─╮╭─╮╭─╮   POST        │
│ ╰─╯╰─╯╰─╯╰─╯╰─╯╰─╯        CARD   │
│  To ________                     │
│                                  │
│                                  │
│                                  │
│                                  │
│                                  │
│                                  │
│ ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ │
│                                  │
│  _____________________________   │
│  _____________________________   │
│  _____________________________   │
│  _____________________________   │
│  _____________________________   │
│                                  │
│                                  │
│                       ________   │
└──────────────────────────────────┘
'''

