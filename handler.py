# -*- coding: utf-8 -*-
import curses
import time
import math

# Klass som ansvarar för allt som har med curses att göra


class CursesHandler:

    def __init__(self, screen=None):
        self.screen = screen    # Använder screen i olika delar av klassen, därav en variabel här
        self.msgLst = ['You may leave after defeating the Boss!', 'Here you will find Monsters and Loot',
                       'Let your adventure begin with WASD', 'Welcome To The Dungeon, Stick!']

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
        # self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

        # Färgpar
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)       # Classic white fg, black bg
        curses.init_pair(2, 240, curses.COLOR_BLACK)                      # Wall dark-gray fg, black bg
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)       # Orc green fg, black bg
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)        # Sword blue fg, black bg
        curses.init_pair(5, 11, curses.COLOR_BLACK)                       # Player cyan fg, black bg
        curses.init_pair(100, curses.COLOR_BLACK, curses.COLOR_WHITE)     # Inverted (classic) colors

        # curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)      # Classic white fg, yellow bg
        # curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)      # Orc green fg, yellow bg
        # curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)       # Sword blue fg, yellow bg
        # curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)       # Wall dark-gray fg, yellow bg
        # curses.init_pair(10, 11, curses.COLOR_BLACK)                     # Player cyan fg, yellow bg


    # Curses avslutas, inställningar sätts tillbaka till
    def cursesEnd(self):
        self.screen.keypad(False)       # Curses avslutas, inställningar sätts som innan
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        # self.screen.nodelay(0)

        curses.endwin()

    # Render funktion mha curses
    def renderGameMap(self, gameMap, exploredGameMap, player, rad=5):
        for tile in exploredGameMap.values():
            self.screen.addstr(tile.y, tile.x, tile.charDark, curses.color_pair(tile.dark))

        rays = 360
        steps = 5
        for ray in range(rays):
            x = rad * math.cos(ray)
            y = rad * math.sin(ray)
            for step in range(1, steps + 1):
                tile = gameMap.get((player.x + round(x / steps * step), player.y + round(y / steps * step)))
                if tile == None:
                    break
                if tile not in exploredGameMap:
                    exploredGameMap.update({(player.x + round(x * step), player.y + round(y * step)) : tile})

                self.screen.addstr(tile.y, tile.x, tile.charLight, curses.color_pair(tile.light))
                if tile.blocksMovement:
                    break

        # for tile in gameMap.values():
        #     # Pythagoras Theorem for distance
        #     distance = round(math.sqrt(abs(player.x - tile.x) ** 2 + abs(player.y - tile.y) ** 2))
        #     if distance <= rad:
        #         if tile not in exploredGameMap:
        #             exploredGameMap[(tile.x, tile.y)] = tile
        #         self.screen.addstr(tile.y, tile.x, tile.charLight, curses.color_pair(tile.light))
        #     else:
        #         if tile in exploredGameMap.values():
        #             self.screen.addstr(tile.y, tile.x, tile.charDark, curses.color_pair(tile.dark))


    def renderEntityList(self, entityList, itemList, player, rad=5):
        tempList = []
        newEntityList = list(entityList.values())
        newEntityList.extend(list(itemList.values()))
        newEntityList.sort(key=lambda x: x.order)

        # rays = 360
        # for ray in range(len(rays)):
        #     x = round(5 * math.cos(ray))
        #     y = round(5 * math.sin(ray))
        #     for step in range(1, rad + 1):
        #         if


        for tile in newEntityList:
            # Pythagoras Theorem for distance
            distance = round(math.sqrt(abs(player.x - tile.x) ** 2 + abs(player.y - tile.y) ** 2))
            if distance <= rad:
                self.screen.addstr(tile.y, tile.x, tile.char, curses.color_pair(tile.light))

    def renderMessages(self, newMsg, update=False):
        if update:
            self.msgLst.insert(0, '{:<40}'.format(newMsg))
            self.msgLst.pop()
        for i, msg in enumerate(self.msgLst):
            self.screen.addstr(25 - i, 20, msg)

    def renderPlayerStats(self, player):
        self.screen.addstr(22, 0, 'HP: {:<3}'.format(player.hp))
        self.screen.addstr(23, 0, 'DMG: {:<3}'.format(player.dmg))
        self.screen.addstr(24, 0, 'Level: {:<3}'.format(player.lvl))
        self.screen.addstr(25, 0, 'XP: {:<6}'.format(player.xp))

        self.screen.addstr(26, 0, ' ')

        self.screen.addstr(27, 0, 'X:{:<3} Y:{:<3}'.format(player.x, player.y))

    def playerInput(self, player, entityList, gameMap):
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
        if key == curses.KEY_UP:
            player.xp += 10
            player.calcLevel(entityList)
        if key == curses.KEY_DOWN:
            player.heal()

        if key == 27:
            return False

        player.move(entityList, gameMap, dx, dy)
        if player.hp <= 0:
            return False

        return True
