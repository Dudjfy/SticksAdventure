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
    
    ESC = komma ut ur programmet, viktigt då man kör i konsolen
    arrow UP = xp cheat, +10 XP
    arrow DOWN = healing cheat, +20% of Max HP
    
"""


curHan = CursesHandler()
menu = Menu()

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



# entityList = [player, orc, sword, test]
entityList = {}
itemList = {}
entityList[(player.x, player.y)] = player
entityList[(orc.x, orc.y)] = orc
itemList[(sword.x, sword.y)] = sword
entityList[(test.x, test.y)] = test

# Orcs test
# [entityList.append(Monster(40 + i, 18, 'o', 'Orc' + str(i), 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}'))
#  for i in range(12)]

# entityList.sort(key=lambda x: x.order)

gameMap = GameMap().createGameMapFromFile()

# Orcs random over whole map
Monster().createRandomMonsters(entityList, gameMap, orc, 100)

exploredGameMap = {}

for tile in gameMap.values():
    if tile.x == 0 or tile.x == 81 or tile.y == 0 or tile.y == 21:
        exploredGameMap[(tile.x, tile.y)] = tile

rad = 3         # Radius of light
rays = 360
steps = rad
gameOn = True

while gameOn:
    # curHan.screen.clear()
    curHan.renderFrame(gameMap, exploredGameMap, entityList, itemList, player, rad, rays, steps)

    curHan.renderPlayerStats(player)

    attackedMonster = Monster().returnAttackedMonster(entityList)

    curHan.renderMessages(attackedMonster.attackedMsg\
        .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg) if \
        isinstance(attackedMonster, Monster) else '', isinstance(attackedMonster, Monster))

    # curHan.screen.refresh()
    # time.sleep(1)
    gameOn = curHan.playerInput(player, entityList, gameMap)

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()

