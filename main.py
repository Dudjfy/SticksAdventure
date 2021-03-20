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

player = Player(78, 19, '@', 'Player', 'white', True)
orc = Monster(69, 18, 'o', 'Orc', 'green', True, hp=10, dmg=2)
sword = Item(60, 18, '/', 'Sword', 'light_blue', False)
test = Entity(5, 2)

entityList = [player, orc, sword, test]
# entityList = [orc, sword, test, player]
entityList.sort(key=lambda x: x.order)
# entityList = Entity().sortEntityListInOrder(entityList)

gameMap = GameMap()
gameMap.createGameMapFromFile()
gameMap = gameMap.gameMap

while True:
    curHan.cursesRender(gameMap)
    curHan.cursesRender(entityList)
    curHan.cursesRenderMessages('Player - X:{} Y:{} HP:{} DMG:{}      Orc - HP:{} DMG:{}'
                                .format(player.x, player.y, player.hp, player.dmg, orc.hp, orc.dmg))
    dx, dy = curHan.cursesPlayerInput()
    if not player.collisionDetection(entityList, dx, dy) and not player.collisionDetection(gameMap, dx, dy):
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
