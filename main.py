import time

from entity import *
from handler import *
from menu import *
from gameMap import *
import curses

curHan = CursesHandler()
menu = Menu()

# gameMap = GameMap()
# gameMap.createGameMapFromFile()
# gameMap = gameMap.gameMap
#
# for i in gameMap:
#     print(i.x, i.y, i.name)
#     break

""" Curses setup """
curHan.cursesSetup()

# Menu loop
# while True:
#     menu.printMenu(ren.screen)
#     menu.inputMenu(ren.screen)

player = Player(78, 19, '@', 'Player', 1, True)
orc = Monster(69, 18, 'o', 'Orc', 2, True, hp=10, dmg=2)
sword = Item(60, 18, '/', 'Sword', 3, False)
test = Entity(5, 2)

entityList = [player, orc, sword, test]
# entityList = [orc, sword, test, player]
entityList.sort(key=lambda x: x.order)
# entityList = Entity().sortEntityListInOrder(entityList)

gameMap = GameMap()
gameMap.createGameMapFromFile()
gameMap = gameMap.gameMap

while True:
    curHan.renderFrame(gameMap)
    curHan.renderFrame(entityList)
    curHan.renderPlayerStats(player)
    curHan.renderMessages('Orc - HP:{} DMG:{}'.format(orc.hp, orc.dmg))
    dx, dy = curHan.playerInput()
    if not player.collisionDetectionEntityList(entityList, dx, dy) and \
            not player.collisionDetectionMap(gameMap, dx, dy):
        player.move(dx, dy)

""" Curses End """
curHan.cursesEnd()


# while True:
#     # Represents render/draw
#     for entity in entityList:
#         print('X:{} Y:{} Char:{} Name:{} Color:{} Blocks Movement:{}'.format(
#             entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))
#
#     # Represents movement
#     inp = input('>>> ').strip().lower()
#     for letter in inp:
#         if letter == 'w':
#             player.y -= 1
#         if letter == 's':
#             player.y += 1
#         if letter == 'a':
#             player.x -= 1
#         if letter == 'd':
#             player.x += 1
