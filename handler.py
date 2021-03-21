import curses
import time

# Klass som ansvarar för allt som har med curses att göra
class CursesHandler:

    def __init__(self, screen=None):
        self.screen = screen    # Använder screen i olika delar av klassen, därav en variabel här
        self.msgLst = ['', '', '', '']

    # Sätter upp curses
    def cursesSetup(self):
        self.screen = curses.initscr()      # screen initialization
        curses.curs_set(0)                  # Andra saker som har med curses sätts upp
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        # self.screen.nodelay(1)
        curses.start_color()

        curses.resize_term(40, 100)
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

        # Färgpar
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)      # Classic/player colors
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)      # Orc green colors
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)       # Sword light-blue colors
        curses.init_pair(4, 240, curses.COLOR_BLACK)                      # Wall dark-gray colors
        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)     # Inverted (classic) colors


    # Curses avslutas, inställningar sätts tillbaka till
    def cursesEnd(self):
        self.screen.keypad(False)       # Curses avslutas, inställningar sätts som innan
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        # self.screen.nodelay(0)

        curses.endwin()

    # Render funktion mha curses
    def renderFrame(self, frame):
        # self.screen.attron(curses.color_pair(1))

        # y, x = self.screen.getmaxyx()
        # self.screen.addstr('{} {}'.format(x, y))
        # self.screen.refresh()
        # time.sleep(3)

        # self.screen.clear()
        # self.screen.move(0, 0)

        for tile in frame:
            self.screen.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.color))

        # self.screen.refresh()

        # self.screen.attroff(curses.color_pair(1))
    def renderMessages(self, newMsg):
        self.msgLst.insert(0, newMsg)
        self.msgLst.pop()
        for i, msg in enumerate(self.msgLst):
            self.screen.addstr(25 - i, 30, msg)

    def renderPlayerStats(self, player):
        self.screen.addstr(22, 0, 'HP: {:<3}'.format(player.hp))
        self.screen.addstr(23, 0, 'DMG: {:<3}'.format(player.dmg))
        self.screen.addstr(24, 0, 'Level: {:<3}'.format(player.lvl))
        self.screen.addstr(25, 0, 'XP: {:<5}'.format(player.xp))

        self.screen.addstr(26, 0, ' ')

        self.screen.addstr(27, 0, 'X:{:<3} Y:{:<3}'.format(player.x, player.y))

    def playerInput(self):
        key = self.screen.getch()

        dx = 0
        dy = 0

        if key == 119:
            dy -= 1
        if key == 115:
            dy += 1
        if key == 97:
            dx -= 1
        if key == 100:
            dx += 1
        if key == 27:
            exit()

        return dx, dy
