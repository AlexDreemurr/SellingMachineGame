import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import threading
import time
from extraGame_001.Enemy import Enemy
from extraGame_001.shared_data import SharedData

def enemy_move(stdscr, lock: threading.Lock, height):
    '''线程3：更新敌人'''
    while True:
        with lock:
            new_enemy_list: list[Enemy] = []
            for i, enemy in enumerate(SharedData.enemies):
                enemy: Enemy

                enemy.move()
                # 如果没出界，则保留
                if 0 < enemy.y < height - 3:
                    new_enemy_list.append(enemy)

            # 切片赋值
            SharedData.enemies[:] = new_enemy_list
        time.sleep(1 / SharedData.ENEMY_MOVE_SPEED)