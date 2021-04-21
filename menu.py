# -*- coding: utf-8 -*-s
from handler import *

# This class in not currently used, except for game over screen
class Menu:

    def __init__(self):
        self.menu = ['Play', 'Settings', 'Exit']
        self.curRow = 0

    # Prints menu
    def printMenu(self, screen):
        screen.clear()
        h, w = screen.getmaxyx()

        # Centers menu depending on game size
        for idx, row in enumerate(self.menu):
            x = w//2 - len(row)//2
            y = h//2 - len(self.menu)//2 + idx
            if idx == self.curRow:
                screen.attron(curses.color_pair(1))
                screen.addstr(y, x, row)
                screen.attroff(curses.color_pair(1))
            else:
                screen.addstr(y, x, row)

        screen.refresh()

    # Menu input
    def inputMenu(self, screen):
        key = screen.getch()

        if key == curses.KEY_UP and self.curRow > 0:
            self.curRow -= 1
        elif key == curses.KEY_DOWN and self.curRow < len(self.menu) - 1:
            self.curRow += 1
        # elif key == curses.KEY_ENTER and self.menu[self.curRow] == 'Exit':

    # Game over screen
    def gameOver(self, screen):
        h, w = screen.getmaxyx()
        screen.clear()
        msg = 'Game Over'
        screen.addstr(h//2, w//2 - len(msg)//2, msg)
        screen.refresh()
        time.sleep(5)

# class MenuButton:
#     def