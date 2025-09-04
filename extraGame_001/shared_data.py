from random import random, randint
from extraGame_001.Bottle import Bottle

class SharedData():
    bullets = []
    enemies = []
    player_bottle: Bottle = None
    # 玩家的分数
    score = 0
    
    # 游戏倒计时
    cur_left_time = 120

    # 玩家瓶子的当前等级
    cur_bottle_level = 1

    # 是否正在大招
    is_ultimate_attack_on = False
    
    # 大招持续时间和CD
    ULTIMATE_ATTACK_DURANCE = 5
    ULTIMATE_ATTACK_CD = 10

    # 子弹的生成速度和移动速度
    BULLET_SUMMON_SPEED = 3
    BULLET_MOVE_SPEED = 30

    # 敌人的生成速度和移动速度
    ENEMY_SUMMON_SPEED = 2
    ENEMY_MOVE_SPEED = 4
    
    # 敌人的x轴生成广度
    ENEMY_WIDE = 15

    # 各种硬币的概率（加起来总和一定为1）
    COIN_1 = 1
    COIN_5 = 0
    COIN_10 = 0
    COIN_50 = 0
    COIN_100 = 0

    def returnRandomCoinValue():
        fun = random()
        cur_sum = 0
        if 0 <= fun <= SharedData.COIN_1:
            return 1
        cur_sum += SharedData.COIN_1
        if cur_sum <= fun <= cur_sum + SharedData.COIN_5:
            return 5
        cur_sum += SharedData.COIN_5
        if cur_sum <= fun <= cur_sum + SharedData.COIN_10:
            return 10
        cur_sum += SharedData.COIN_10
        if cur_sum <= fun <= cur_sum + SharedData.COIN_50:
            return 50