from extraGame_001.Bottle import Bottle
from extraGame_001.Bullet import Bullet
from extraGame_001.Enemy import Enemy, coin_pics
from extraGame_001.shared_data import SharedData
from random import randint
from extraGame_001.bullet_design.bullet_summon import summon_bullet, summon_bullet_v3
from extraGame_001.bullet_design.bullet_move import bullet_move
from extraGame_001.enemy_design.enemy_summon import summon_enemy
from extraGame_001.enemy_design.enemy_move import enemy_move
import curses
import threading
import time
import queue

key_queue = queue.Queue() # 键盘采集队列
LAST_TIME = 60 # 小游戏总时长
SharedData.cur_left_time = 60 # 小游戏倒计时器
is_gameover = False # 游戏是否结束

class Bullets():
    bullets: list[Bullet] = []


class Enemies():
    enemies: list[Enemy] = []


def input_reader(stdscr):
    '''线程1：专门负责读取按键'''
    while True:
        key = stdscr.getch()
        if key != -1:
            key_queue.put(key)
        time.sleep(0.01)


def hit_check(lock: threading.Lock, normal_attack_stop_event: threading.Event):
    '''线程2：子弹与敌人的碰撞检测'''
    while not normal_attack_stop_event.is_set():
        with lock:
            new_enemy_list: list[Enemy] = []
            for i, enemy in enumerate(Enemies.enemies):
                bullet = enemy.hit_detect()
                # 如果碰到子弹（函数返回值是子弹不是False的情况）
                if bullet and bullet in Bullets.bullets:
                    SharedData.score += enemy.value
                    Bullets.bullets.remove(bullet)
                else:
                    new_enemy_list.append(enemy)
            Enemies.enemies[:] = new_enemy_list

def ultimate_hit_check(lock: threading.Lock, ultimate_attack_stop_event: threading.Event):
    '''线程3： 在瓶子开大招时子弹和敌人的碰撞检测'''
    while not ultimate_attack_stop_event.is_set():
        with lock:
            new_enemy_list: list[Enemy] = []
            for i, enemy in enumerate(Enemies.enemies):
                bullet = enemy.hit_detect()
                # 如果碰到子弹（函数返回值是子弹不是False的情况）
                if bullet and bullet in Bullets.bullets:
                    SharedData.score += enemy.value
                else:
                    new_enemy_list.append(enemy)
            Enemies.enemies[:] = new_enemy_list

def time_counter():
    global is_gameover
    '''线程4：计算游戏时间
        game_time: 当前用时'''

    while SharedData.cur_left_time >= 0:
        time.sleep(1)
        SharedData.cur_left_time -= 1

    is_gameover = True


def main(stdscr):
    global is_gameover

    curses.curs_set(0)
    stdscr.nodelay(True)

    height, width = stdscr.getmaxyx()
    x = width // 2
    y = height - 3

    e1 = Enemy(x + 2, 0, 1)
    e2 = Enemy(x - 10, 0, 1)
    e1.pic_list = coin_pics[-1]
    e1.width = 5
    e2.pic_list = coin_pics[-1]
    e2.width = 5
    Enemies.enemies.append(e1)
    Enemies.enemies.append(e2)
    
    player_bottle = Bottle(x, y)
    lock = threading.Lock()
    normal_stop_event = threading.Event()
    normal_attack_stop_event = threading.Event()
    ultimate_attack_stop_event = threading.Event()
    
    # 记录过去大招开始时间
    last_start_times = [0]
    # 大招开始时间，是否正在大招中
    start_time = 0
    is_ultimate_attack_on = False

    # 线程1：读取按键 
    # 线程2：子弹与敌人的碰撞检测
    thread_1 = threading.Thread(target=input_reader, args=(stdscr,))
    thread_2 = threading.Thread(target=hit_check, args=(lock, normal_attack_stop_event))
    thread_3 = threading.Thread(target = ultimate_hit_check, args=(lock, ultimate_attack_stop_event))
    thread_4 = threading.Thread(target = time_counter, args = ())
    thread_summon_bullet = threading.Thread(target=summon_bullet, args=(lock, normal_stop_event, player_bottle))
    thread_summon_bullet_v3 = threading.Thread(target=summon_bullet_v3, args=(lock, player_bottle))
    thread_bullet_move = threading.Thread(target=bullet_move, args=(stdscr, lock))
    thread_summon_enemy = threading.Thread(target=summon_enemy, args=(lock, width))
    thread_enemy_move = threading.Thread(target=enemy_move, args=(stdscr, lock, height))

    thread_1.daemon = True
    thread_2.daemon = True
    thread_3.daemon = True
    thread_4.daemon = True
    thread_summon_bullet.daemon = True
    thread_summon_bullet_v3.daemon = True
    thread_bullet_move.daemon = True
    thread_summon_enemy.daemon = True
    thread_enemy_move.daemon = True
    thread_1.start()
    thread_2.start()
    thread_4.start()
    thread_summon_bullet.start()
    thread_bullet_move.start()
    thread_summon_enemy.start()
    thread_enemy_move.start()

    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    right_button_held = False
    v3_bottle_start = False


    # 主线程循环
    while not is_gameover:
        # 将子弹，敌人列表，玩家瓶子数据写入shared_data中
        SharedData.bullets = Bullets.bullets
        SharedData.enemies = Enemies.enemies
        SharedData.player_bottle = player_bottle
        SharedData.is_ultimate_attack_on = is_ultimate_attack_on

        stdscr.clear()

        # 画瓶子    
        with lock:
            SharedData.player_bottle.draw(stdscr)

        # 画子弹
        with lock:
            for bullet in SharedData.bullets:
                bullet.draw(stdscr)

        # 画敌人
        with lock:
            for enemy in SharedData.enemies:
                enemy.draw(stdscr)

        # 画分数
        stdscr.addstr(1, 1, "Money:" + str(SharedData.score))

        # 画剩余时间
        stdscr.addstr(3, 1, "Time:" + str(SharedData.cur_left_time))

        stdscr.refresh()

        # 根据得分的不同，改变游戏数值
        if SharedData.score >= 30:
            SharedData.cur_bottle_level = 2
            SharedData.player_bottle.upgrade(2)
            SharedData.BULLET_SUMMON_SPEED = 8
            SharedData.BULLET_MOVE_SPEED = 80

            SharedData.ENEMY_SUMMON_SPEED = 5
            SharedData.ENEMY_MOVE_SPEED = 6
        
            SharedData.ENEMY_WIDE = 20

        if SharedData.score >= 100:
            SharedData.cur_bottle_level = 3
            SharedData.player_bottle.upgrade(3)
            SharedData.BULLET_SUMMON_SPEED = 12
            SharedData.BULLET_MOVE_SPEED = 100

            SharedData.ENEMY_SUMMON_SPEED = 10
            SharedData.ENEMY_MOVE_SPEED = 8
            SharedData.ENEMY_WIDE = 25  

            normal_stop_event.set()
            if not v3_bottle_start:
                thread_summon_bullet_v3.start()
                v3_bottle_start = True

        if SharedData.score >= 200:
            SharedData.cur_bottle_level = 4
            SharedData.player_bottle.upgrade(4)
            SharedData.BULLET_SUMMON_SPEED = 16
            SharedData.BULLET_MOVE_SPEED = 160

            SharedData.ENEMY_SUMMON_SPEED = 16
            SharedData.ENEMY_MOVE_SPEED = 10
            SharedData.ENEMY_WIDE = 30
            
            SharedData.COIN_1 = 0.9
            SharedData.COIN_5 = 0.1
        
        if SharedData.score >= 400:
            SharedData.player_bottle.upgrade(4)
            SharedData.BULLET_SUMMON_SPEED = 20
            SharedData.BULLET_MOVE_SPEED = 200

            SharedData.ENEMY_SUMMON_SPEED = 23
            SharedData.ENEMY_MOVE_SPEED = 15
            SharedData.ENEMY_WIDE = 35

            SharedData.COIN_1 = 0.7
            SharedData.COIN_5 = 0.2
            SharedData.COIN_10 = 0.1

        if SharedData.score >= 600:
            SharedData.ENEMY_SUMMON_SPEED = 30
            SharedData.ENEMY_MOVE_SPEED = 20
            SharedData.ENEMY_WIDE = 40
            SharedData.COIN_1 = 0.3
            SharedData.COIN_5 = 0.1
            SharedData.COIN_10 = 0.5
            SharedData.COIN_50 = 0.1
            #SharedData.COIN_100 = 0.1

        # 处理输入
        try:
            key = key_queue.get_nowait()
        except queue.Empty:
            key = None

        if key == curses.KEY_MOUSE:
            _, x, y, _, button_state = curses.getmouse()
            
            if button_state and curses.BUTTON3_PRESSED:
                right_button_held = True

            elif button_state and curses.BUTTON3_RELEASED:
                right_button_held = False

            if right_button_held:
                player_bottle.x = x
                # 画瓶子    
                with lock:
                    SharedData.player_bottle.draw(stdscr)

                stdscr.refresh()

        # 监测大招是否时间已到
        end_time = time.time()
        if is_ultimate_attack_on:
            if end_time - start_time >= SharedData.ULTIMATE_ATTACK_DURANCE:
                ultimate_attack_stop_event.set()
                is_ultimate_attack_on = False
                normal_attack_stop_event.clear()
                ultimate_attack_stop_event.clear()
                thread_2 = threading.Thread(target=hit_check, args=(lock, normal_attack_stop_event))
                thread_2.start()
                
                # 把数值改回来
                SharedData.BULLET_MOVE_SPEED /= 3
                SharedData.BULLET_SUMMON_SPEED /= 3

        if key == curses.KEY_LEFT and player_bottle.x > 0:
            player_bottle.x -= 1
        elif key == curses.KEY_RIGHT and player_bottle.x < width:
            player_bottle.x += 1
        elif key == ord(" "):  
            # 如果现在不处于大招，并且上一次开始大招时间距离现在已经过了CD，则可以再开启一次大招
            start_time = time.time()
            if not is_ultimate_attack_on and start_time - last_start_times[-1] > SharedData.ULTIMATE_ATTACK_CD:
                last_start_times.append(start_time)

                is_ultimate_attack_on = True
                normal_attack_stop_event.set()
                thread_3 = threading.Thread(target = ultimate_hit_check, args=(lock, ultimate_attack_stop_event))
                thread_3.start()

                # 更改数值
                SharedData.BULLET_MOVE_SPEED *= 3
                SharedData.BULLET_SUMMON_SPEED *= 3

            with lock:
                pass

    time.sleep(3)

def Main():
    curses.wrapper(main)

    return SharedData.score
