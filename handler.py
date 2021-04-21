# -*- coding: utf-8 -*-
import curses
import string
import math
import time

from player import *

# Handler class using curses
class CursesHandler:
    def __init__(self, screen=None):
        self.screen = screen    # Använder screen i olika delar av klassen, därav en variabel här
        self.msgList = [('{:<35}'.format('Should I approach him? (use WASD)'), (28, 29, 30, 31)),
                       ('{:<35}'.format('He.. looks like.. A Wizard?..'), ()),
                       ('{:<35}'.format("Looks like there's someone close.."), ()),
                       ('{:<35}'.format('Ahgg... Whe- Where.. am I??.'), ())]

        self.keyList = {}
        for value, letter in enumerate(string.ascii_lowercase):
            self.keyList[letter] = value + 97
        self.renderMode = True

    # Curses setup
    def cursesSetup(self):
        # screen initialization and setup
        self.screen = curses.initscr()
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        # self.screen.nodelay(1)
        curses.start_color()

        # Extra screen size just in case
        curses.resize_term(40, 100)
        # self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')

        # Colorpairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)       # Classic white fg, black bg
        curses.init_pair(2, 240, curses.COLOR_BLACK)                      # Wall dark-gray fg, black bg
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)       # Orc green fg, black bg
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)        # Sword blue fg, black bg
        curses.init_pair(5, 11, curses.COLOR_BLACK)                       # Player/XP-bar cyan fg, black bg
        curses.init_pair(6, 13, curses.COLOR_BLACK)                       # Fountain pink fg, black bg
        curses.init_pair(7, 5, curses.COLOR_BLACK)                        # Wizard purple fg, black bg
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)         # HP-bar red fg, red bg
        curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_BLACK)      # HP-bar red fg, red bg
        curses.init_pair(100, curses.COLOR_BLACK, curses.COLOR_WHITE)     # Inverted (classic) colors

    # Ends curses, returns to normal settings
    def cursesEnd(self):
        self.screen.keypad(False)
        curses.curs_set(1)
        curses.echo()
        curses.nocbreak()
        # self.screen.nodelay(0)

        curses.endwin()

    # The main game rendering function
    def renderFrame(self, gameMapObj, entityList, itemList, player, rad=4, rays=360, steps=4):
        # Rendering mode check
        if self.renderMode:
            # Renders explored tiles
            for tile in gameMapObj.exploredGameMap.values():
                self.screen.addstr(tile.y, tile.x, tile.charDark, curses.color_pair(tile.dark))

            # Complex self made raytracing mechanism and rendering, entities only rendered when inside player range
            for ray in range(rays):
                x = rad * math.cos(ray)
                y = rad * math.sin(ray)
                for step in range(0, steps + 1):
                    cords = (player.x + round(x / steps * step), player.y + round(y / steps * step))
                    tile = gameMapObj.gameMap.get(cords)
                    if tile == None:
                        break
                    if tile not in gameMapObj.exploredGameMap:
                        gameMapObj.exploredGameMap.update({cords : tile})

                    item = itemList.get(cords)
                    entity = entityList.get(cords)
                    if not entity == None:
                        self.screen.addstr(entity.y, entity.x, entity.char, curses.color_pair(entity.light))
                    elif not item == None:
                        self.screen.addstr(item.y, item.x, item.char, curses.color_pair(item.light))
                    else:
                        self.screen.addstr(tile.y, tile.x, tile.charLight, curses.color_pair(tile.light))

                    if tile.blocksMovement:
                        break
        # Cheat-mode rendering
        else:
            for tile in gameMapObj.gameMap.values():
                self.screen.addstr(tile.y, tile.x, tile.charDark, curses.color_pair(tile.dark))

            for item in itemList.values():
                self.screen.addstr(item.y, item.x, item.char, curses.color_pair(item.light))

            for entity in entityList.values():
                self.screen.addstr(entity.y, entity.x, entity.char, curses.color_pair(entity.light))

    # Renders messages, the middle column
    def renderMessages(self, newMsg='', update=False, highlightPosList=None):
        # If update to the message list needed
        if update:
            if highlightPosList != None:
                self.msgList.insert(0, ('{:<35}'.format(newMsg), highlightPosList))
            else:
                self.msgList.insert(0, ('{:<35}'.format(newMsg), ()))
            self.msgList.pop()

        # Renders messages
        for i, msg in enumerate(self.msgList):
            for j, letter in enumerate(msg[0]):
                if j in msg[1]:
                    self.screen.addstr(25 - i, 26 + j, letter, curses.color_pair(5))
                else:
                    self.screen.addstr(25 - i, 26 + j, letter)

    # Renders player stats, left column
    def renderPlayerStats(self, player):
        # Special char for hp and xp bar
        barChar = '■'
        # Math related calculations for hp
        hpBarLevel = math.ceil(player.hp / (player.maxHp / 10))
        hpShown = '{:>4}/{:<4}'.format(player.hp, player.maxHp).strip()
        # Rendering och result
        self.screen.addstr(22, 0, 'HP:|{:10}| {:<9}'.format('', hpShown))
        self.screen.addstr(22, 4, barChar * hpBarLevel, curses.color_pair(8))
        self.screen.addstr(23, 0, 'DMG: {:<9}'.format(
            '{}(+{})'.format(player.dmg + (0 if player.weapon == None else player.weapon.dmg),
                             0 if player.weapon == None else player.weapon.dmg)))
        self.screen.addstr(23, 15, 'DEF: {:<3}'.format(player.defence))
        self.screen.addstr(24, 0, 'Level: {:<3}'.format(player.lvl))

        # More math for xp
        curLevelXp = (player.lvl / player.xpConst) ** 2
        nextLevelXp = ((player.lvl + 1) / player.xpConst) ** 2
        playerXpDif = round(player.xp - curLevelXp) if player.lvl > 1 else round(player.xp - curLevelXp + 25)
        nextLevelXpDif = round(nextLevelXp - curLevelXp) if player.lvl > 1 else 100
        xpBarLevel = math.ceil(playerXpDif / (nextLevelXpDif / 10))

        # Final rendering of the rest
        xpShown = '{:>4}/{:<4}'.format(playerXpDif, nextLevelXpDif).strip()
        self.screen.addstr(25, 0, 'XP:|{:10}| {:<9}'.format('', xpShown))
        self.screen.addstr(25, 4, barChar * xpBarLevel, curses.color_pair(4))

        self.screen.addstr(26, 0, ' ')

        self.screen.addstr(27, 0, 'X:{:<3} Y:{:<3}'.format(player.x, player.y))

    # Rendering of inventory, the right column
    def renderInventory(self, inventory, player):
        # Clears the previous star
        for y in range(inventory.visibleSize):
            self.screen.addstr(22 + y, 62, ' ')

        # Renders inventory if any items
        if len(inventory.itemList) > 0:
            # Clears
            for itemIdx in range(inventory.visibleSize):
                self.screen.addstr(22 + itemIdx, 62, '{:>20}'.format(' '))

            # Renders results
            for itemIdx in range(inventory.visibleSize):
                if itemIdx < len(inventory.itemList):
                    if inventory.itemList[inventory.startPos + itemIdx] == player.weapon \
                            or inventory.itemList[inventory.startPos + itemIdx] == player.armor:
                        self.screen.addstr(22 + itemIdx, 62, '*', curses.color_pair(1))

                    if itemIdx == inventory.curVisibleIdx:
                        self.screen.addstr(22 + itemIdx, 62, '*', curses.color_pair(100))

                    msg = '{:>18}'.format('{} x{:>2}'.format(inventory.itemList[inventory.startPos + itemIdx].name,
                                                             inventory.itemList[inventory.startPos + itemIdx].amount))
                    self.screen.addstr(22 + itemIdx, 64, msg)

        # If no items displays message
        else:
            self.screen.addstr(22, 62, '{:^20}'.format('Inventory Empty'))

    # Renders dividers between columns
    def renderDividers(self, devLen):
        for y in range(devLen):
            self.screen.addstr(22 + y, 25, '|')
        for y in range(devLen):
            self.screen.addstr(22 + y, 61, '|')

    # Takes player input
    def playerInput(self, player, inventory, entityList, itemList, gameMapObj):
        # Gets the input
        key = self.screen.getch()

        # Change in y and x
        dx = 0
        dy = 0

        # Movement
        if key == self.keyList.get('w'):
            dy -= 1
        if key == self.keyList.get('s'):
            dy += 1
        if key == self.keyList.get('a'):
            dx -= 1
        if key == self.keyList.get('d'):
            dx += 1

        # Inventory related

        # Pickup with E
        if key == self.keyList.get('e'):
            item = itemList.get((player.x, player.y))
            if item != None:
                if inventory.addItem(item.invItem):
                    itemList.pop((item.x, item.y))
                else:
                    self.renderMessages("You can only hold 10 items at once!".format(item.name), True)

        # Use in inventory with F
        if key == self.keyList.get('f'):
            inventory.useItem(player)
            self.renderInventory(inventory, player)

        # I or C for item desc
        if key == self.keyList.get('i') or key == self.keyList.get('c'):
            if len(inventory.itemList) > 0:
                item = inventory.itemList[inventory.startPos + inventory.curVisibleIdx]
                inventory.createMsg(item.desc)

        # Item dropping with Q
        if key == self.keyList.get('q'):
            # Checks if any items in inventory
            if len(inventory.itemList) > 0:
                item = inventory.itemList[inventory.startPos + inventory.curVisibleIdx]

                # Can't drop key
                if isinstance(item, Key):
                    self.renderMessages("Key's too important, can't drop it".format(item.name), True)
                    return True

                # Rendering asking to drop item in case of accidental Q press
                self.renderMessages('Dropping {}? (Y/N)'.format(item.name), True, (12 + len(item.name), 14 + len(item.name)))

                self.screen.addstr(player.y, player.x, player.char, curses.color_pair(100))

                # While loop waits until user accepts or declines dropping
                while True:
                    key = self.screen.getch()

                    if key == self.keyList.get('y'):
                        # Dropping message rendering
                        self.renderMessages('Dropped item: {}'.format(item.name), True)
                        if isinstance(item, Weapon) or isinstance(item, Armor):
                            if item == player.weapon or item == player.armor:
                                item.use(player)

                        # Dropping of item
                        if len(inventory.itemList) > 0:
                            if inventory.startPos == 0:
                                if inventory.curVisibleIdx > len(inventory.itemList) - 2:
                                    inventory.curVisibleIdx -= 1
                            elif inventory.startPos + inventory.visibleSize > len(inventory.itemList) - 1:
                                inventory.startPos -= 1
                        self.renderInventory(inventory, player)

                        inventory.itemList.remove(item)
                        break
                    elif key == self.keyList.get('n'):
                        break

                return True

        # Up Down keys for inventory scrolling
        if key == curses.KEY_UP:
            inventory.nextItem(-1)
        if key == curses.KEY_DOWN:
            inventory.nextItem(1)

        # Cheat codes

        # -
        if key == 45:
            # +10 xp
            player.xp += 10
            player.calcLevel(entityList)
        # =
        if key == 61:
            # +1/5 max xp
            player.heal()
        # 0
        if key == 48:
            # Changes rendering mode for main game
            self.renderMode = not self.renderMode
            self.screen.clear()
            self.renderMessages()

        # ESC key, ends game
        if key == 27:
            return False

        # Moves player
        player.move(entityList, gameMapObj, inventory, dx, dy)

        # Ends game if hp 0 or less
        if player.hp <= 0:
            return False

        # Continues in other cases
        return True
