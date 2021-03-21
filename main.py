# -*- coding: utf-8 -*-
import time

from entity import *
from handler import *
from menu import *
from gameMap import *
import curses

"""
    OBS! Replits inbyggda konsol fungerar väldigt dåligt, så kör uppguften från shell med:
    python3 main.py
    
    Projektet var gjord i PyCharm så det finns ett par extra filer, dessutom användes github
    för att kunna göra ändringar både på replit och min egna lokala miljö. Git användes då för
    versionskontroll. Utöver detta bör projektens filer vara tillgångliga som vanligt.
"""


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

player = Player(78, 19, '@', 'Player', 2, 5, True, baseHp=30, baseDmg=4)
orc = Monster(69, 18, 'o', 'Orc', 2, 3, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}')
sword = Item(60, 18, '/', 'Sword', 2, 4, False)
test = Entity(5, 2)



entityList = [player, orc, sword, test]

# Orcs test
# [entityList.append(Monster(40 + i, 18, 'o', 'Orc' + str(i), 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}'))
#  for i in range(12)]

# Orcs random over whole map
Monster().createRandomMonsters(entityList, orc, 100)

entityList.sort(key=lambda x: x.order)

gameMap = GameMap()
gameMap.createGameMapFromFile()
gameMap = gameMap.gameMap

# Entities map collision detection
for tile in gameMap:
    if tile.name == 'Wall':
        for entity in entityList:
            if entity.x == tile.x and entity.y == tile.y:
                entityList.remove(entity)

# Entities entity collision detection
for i, entity1 in enumerate(entityList):
    for entity2 in entityList[i + 1:]:
        if entity1.x == entity2.x and entity1.y == entity2.y:
            entityList.remove(entity2)

# List comprehension version
# [[entityList.remove(entity) for entity in entityList if entity.x == tile.x and entity.y == tile.y]
#  for tile in gameMap if tile == 'Wall']

rad = 5         # Radius of light
gameOn = True

exploredGameMap = set()
while gameOn:
    curHan.screen.clear()
    curHan.renderFrame(gameMap, player, rad, exploredGameMap)
    curHan.renderFrame(entityList, player, rad)
    curHan.renderPlayerStats(player)

    attackedMonster = Monster().returnAttackedMonster(entityList)

    curHan.renderMessages(attackedMonster.attackedMsg\
        .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg) if \
        isinstance(attackedMonster, Monster) else '', isinstance(attackedMonster, Monster))
    # if isinstance(attackedMonster, Monster):
    #     curHan.renderMessages(attackedMonster.attackedMsg
    #                           .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg))

    gameOn = curHan.playerInput(player, entityList, gameMap)

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()

