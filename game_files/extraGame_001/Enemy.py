from extraGame_001.shared_data import SharedData
import curses

coin_pics =  {500: ["╭────╮ ",
                    "│    ╰╮",
                    "│ 500 │",
                    "╰─────╯"], 
        100: ["╭──╮ ",
              "│  ╰╮",
              "│100│",
              "╰───╯"], 
        50:  ["╭─╮ ",
              "│ ╰╮",
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
              "╰─╯"],
        -1:  ["╭───╮",
              "│*_*│",
              "╰───╯"]}


class Enemy():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.pic_list = coin_pics[value]
        self.width = len(self.pic_list[0])
        self.height = len(self.pic_list)

    def draw(self, stdscr):
        try:
            for i, pic_line in enumerate(self.pic_list):
                stdscr.addstr(self.y + (i), self.x, pic_line)
        except curses.error:
            pass

    def move(self):
        '''向下移动一格'''
        self.y += 1

    def hit_detect(self): 
        '''判断是否碰到任意子弹，如有，返回撞到的那颗子弹'''
        for bullet in SharedData.bullets:
            if self.y + self.height - 3 <= bullet.y <= self.y + self.height - 2 and \
              self.x + self.width // 2 - (self.width - 1) // 2 <= bullet.x <= self.x + self.width // 2 + (self.width - 1) // 2:
                return bullet
        return False