import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import threading
import time
from extraGame_001.Bullet import Bullet
from extraGame_001.Bottle import Bottle
from extraGame_001.shared_data import SharedData


def summon_bullet(lock: threading.Lock, stop_event: threading.Event, player_bottle: Bottle):
    '''自动生成子弹'''
    while not stop_event.is_set():
        time.sleep(1 / SharedData.BULLET_SUMMON_SPEED)

        with lock:
            # 自动发射子弹
            bullet = Bullet(player_bottle.x + 1, player_bottle.y - 2)
            if SharedData.is_ultimate_attack_on:
                bullet.pic = "┃"
                
            SharedData.bullets.append(bullet)

def summon_bullet_v3(lock: threading.Lock, player_bottle: Bottle):
    '''自动生成三发子弹（3代瓶）'''
    while SharedData.cur_bottle_level == 3:
        time.sleep(1 / SharedData.BULLET_SUMMON_SPEED)

        with lock:
            # 自动发射子弹
            bullet1 = Bullet(player_bottle.x + 1, player_bottle.y - 2)
            bullet2 = Bullet(player_bottle.x + 2, player_bottle.y - 2)
            bullet3 = Bullet(player_bottle.x + 3, player_bottle.y - 2)
            if SharedData.is_ultimate_attack_on:
                bullet1.pic = "┃"
                bullet2.pic = "┃"
                bullet3.pic = "┃"

            SharedData.bullets.append(bullet1)
            SharedData.bullets.append(bullet2)
            SharedData.bullets.append(bullet3)

    while SharedData.cur_bottle_level >= 4:
        time.sleep(1 / SharedData.BULLET_SUMMON_SPEED)

        with lock:
            # 自动发射子弹
            bullet1 = Bullet(player_bottle.x + 2, player_bottle.y - 2)
            bullet2 = Bullet(player_bottle.x + 3, player_bottle.y - 2)
            bullet3 = Bullet(player_bottle.x + 4, player_bottle.y - 2)
            bullet4 = Bullet(player_bottle.x , player_bottle.y - 1)
            bullet5 = Bullet(player_bottle.x + 6, player_bottle.y - 1)
            if SharedData.is_ultimate_attack_on:
                bullet1.pic = "┃"
                bullet2.pic = "┃"
                bullet3.pic = "┃"
                bullet4.pic = "┃"
                bullet5.pic = "┃"

            SharedData.bullets.append(bullet1)
            SharedData.bullets.append(bullet2)
            SharedData.bullets.append(bullet3)
            SharedData.bullets.append(bullet4)
            SharedData.bullets.append(bullet5)

