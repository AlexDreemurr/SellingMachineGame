import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import threading
import time
from Bullet import Bullet
from extraGame_001.shared_data import SharedData

def bullet_move(stdscr, lock: threading.Lock):
    '''子弹移动'''
    while True:
        with lock:
            new_bullet_list: list[Bullet] = []
            for i, bullet in enumerate(SharedData.bullets):
                bullet: Bullet

                bullet.move()
                if bullet.y > 0:
                    new_bullet_list.append(bullet)
                
            # 切片赋值
            SharedData.bullets[:] = new_bullet_list
        time.sleep(round(1 / SharedData.BULLET_MOVE_SPEED, 2))

    