import curses

# Klass som ansvarar för allt som har med curses att göra
class CursesHandler:

    def __init__(self, screen=None):
        self.screen = screen    # Använder screen i olika delar av klassen, därav en variabel här

    # Sätter upp curses
    def cursesSetup(self):
        self.screen = curses.initscr()      # screen initialization
        curses.curs_set(0)                  # Andra saker som har med curses sätts upp
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        # self.screen.nodelay(1)
        curses.start_color()

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)     # Färgpar


    # Curses avslutas, inställningar sätts tillbaka till
    def cursesEnd(self):
        self.screen.keypad(False)       # Curses avslutas, inställningar sätts som innan
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        # self.screen.nodelay(0)

        curses.endwin()

    # Render funktion mha curses
    def cursesRender(self, frame):
        # self.screen.attron(curses.color_pair(1))

        self.screen.clear()

        for tile in frame:
            self.screen.addstr(tile.y, tile.x, tile.char)

        self.screen.refresh()

        # self.screen.attroff(curses.color_pair(1))

    def cursesInput(self):
        self.screen.getch()
