import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import threading
import time
from random import randint
from extraGame_001.Enemy import Enemy
from extraGame_001.shared_data import SharedData


def summon_enemy(lock: threading.Lock, width):
    '''线程5：敌人的自动生成'''
    while True:
        time.sleep(1 / SharedData.ENEMY_SUMMON_SPEED)

        with lock:
            x = width // 2 + randint(-SharedData.ENEMY_WIDE, SharedData.ENEMY_WIDE)
            value = SharedData.returnRandomCoinValue()

            new_enemy = Enemy(x, 0, value)
            SharedData.enemies.append(new_enemy)