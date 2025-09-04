import curses

class Bullet():
    def __init__(self, x, y, pic = "|"):
        self.x: int = x
        self.y: int = y
        self.pic: str = pic

    def move(self):
        '''向上移动一格'''
        self.y -= 1

    def draw(self, stdscr):
        try:
            stdscr.addstr(self.y, self.x, self.pic)
        except curses.error:
            pass
