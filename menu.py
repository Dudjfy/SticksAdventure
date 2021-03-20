from render import *

# Huvudmenyn klassen
class Menu:

    def __init__(self):
        self.menu = ['Play', 'Settings', 'Exit']    # Menyns olika avdelningar

    # Skriver ut menyn
    def printMenu(self, screen):
        screen.clear()
        h, w = screen.getmaxyx()

        # Centrerar menyn vertikalt och horisontalt, varje nästa element skrivs ut på nästa rad
        for idx, row in enumerate(self.menu):
            x = w//2 - len(row)//2
            y = h//2 - len(self.menu)//2 + idx
            if idx == 0:
                screen.attron(curses.color_pair(1))
                screen.addstr(y, x, row)
                screen.attroff(curses.color_pair(1))

        screen.refresh()
