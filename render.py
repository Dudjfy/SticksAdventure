import curses

class cursesRender():

    def __init__(self, screen=None):
        self.screen = screen


    def cursesSetup(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        # self.screen.nodelay(1)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def cursesEnd(self):
        self.screen.keypad(False)
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        # self.screen.nodelay(0)

        curses.endwin()
    def cursesRender(self):
        self.screen.attron(curses.color_pair(1))
        key = self.screen.getch()

        self.screen.clear()

        if key == curses.KEY_UP:
            self.screen.addstr(0, 0, "Upp")
        elif key == curses.KEY_DOWN:
            self.screen.addstr(0, 0, "Down")

        self.screen.refresh()

        self.screen.attroff(curses.color_pair(1))