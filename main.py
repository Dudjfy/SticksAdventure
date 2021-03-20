import time

from entity import *
from handler import *
from menu import *
import curses

curHan = CursesHandler()
menu = Menu()

""" Curses setup """
curHan.cursesSetup()

# Menu loop
# while True:
#     menu.printMenu(ren.screen)
#     menu.inputMenu(ren.screen)

player = Creature(10, 10, '@', 'Player', 'white', True)
orc = Creature(15, 10, 'o', 'Orc', 'green', True)
sword = Entity(15, 15, '/', 'Sword', 'light_blue', False)
test = Entity()

entityList = [player, orc, sword, test]
entityBlockingCordsList = []
for entity in entityList:
    if entity.blocksMovement and entity != player:
        entityBlockingCordsList.append([entity.y, entity.x])

while True:
    curHan.cursesRender(entityList)
    dx, dy = curHan.cursesPlayerInput()

    player.move(dx, dy)

""" Curses End """
curHan.cursesEnd()


while True:
    # Represents render/draw
    for entity in entityList:
        print('X:{} Y:{} Char:{} Name:{} Color:{} Blocks Movement:{}'.format(
            entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))

    # Represents movement
    inp = input('>>> ').strip().lower()
    for letter in inp:
        if letter == 'w':
            player.y -= 1
        if letter == 's':
            player.y += 1
        if letter == 'a':
            player.x -= 1
        if letter == 'd':
            player.x += 1
