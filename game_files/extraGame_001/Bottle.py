import curses

bottle_pic = {1: ["╭o╮",
                  "│ │",
                  "╰─╯"], 
              2: ["╭o╮",
                  "│2│",
                  "╰─╯"],
              3: ["╭ooo╮",
                  "│ 3 │",
                  "╰───╯"],
              4: [" ╭ooo╮ ",
                  "╳│   │╳",
                  "╰┤ 4 ├╯",
                  " ╰───╯ "], 
              5: ["",
                  "",
                  "",
                  ""]}

class Bottle():
    '''底部的射击瓶子'''
    def __init__(self, x, y, bottle_num = 1):
        self.x = x
        self.y = y
        self.bottle_num = bottle_num
        self.bottle_pic = bottle_pic[self.bottle_num]

    def upgrade(self, bottle_num):
        '''输入指定等级，将瓶子贴图改为对应等级贴图'''
        self.bottle_num = bottle_num
        self.bottle_pic = bottle_pic[self.bottle_num]

    def draw(self, stdscr):
        try:
            for i, line_pic in enumerate(self.bottle_pic):
                stdscr.addstr(self.y + i - 1, self.x, line_pic)
        except curses.error:
            pass

'''

╭ooo╮
│ 4 │
╰───╯
  ╭ooo╮
 ╳│   │╳
 ╰┤ 4 ├╯
  ╰───╯

'''