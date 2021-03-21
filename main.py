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

for i in range(10):
    entityList.append(Monster(40 + i, 18, 'o', 'Orc', 2, True, hp=10, dmg=2))

entityList.sort(key=lambda x: x.order)

gameMap = GameMap()
gameMap.createGameMapFromFile()
gameMap = gameMap.gameMap

for tile in gameMap:
    if tile.name == 'Wall':
        for entity in entityList:
            if entity.x == tile.x and entity.y == tile.y:
                entityList.remove(entity)


while True:
    curHan.renderFrame(gameMap)
    curHan.renderFrame(entityList)
    curHan.renderPlayerStats(player)
    curHan.renderMessages('Orc - HP:{} DMG:{}'.format(orc.hp, orc.dmg))
    dx, dy = curHan.playerInput()
    player.move(entityList, gameMap, dx, dy)
    if player.hp <= 0:
        break

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()
# print('Game Over')

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
