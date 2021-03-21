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
orc = Monster(69, 18, 'o', 'Orc', 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}')
sword = Item(60, 18, '/', 'Sword', 3, False)
test = Entity(5, 2)



entityList = [player, orc, sword, test]


[entityList.append(Monster(40 + i, 18, 'o', 'Orc' + str(i), 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}'))
 for i in range(12)]

entityList.sort(key=lambda x: x.order)

gameMap = GameMap()
gameMap.createGameMapFromFile()
gameMap = gameMap.gameMap

for tile in gameMap:
    if tile.name == 'Wall':
        for entity in entityList:
            if entity.x == tile.x and entity.y == tile.y:
                entityList.remove(entity)

# List comprehension version
# [[entityList.remove(entity) for entity in entityList if entity.x == tile.x and entity.y == tile.y]
#  for tile in gameMap if tile == 'Wall']

while True:
    curHan.renderFrame(gameMap)
    curHan.renderFrame(entityList)
    curHan.renderPlayerStats(player)
    attackedMonster = Monster().returnAttackedMonster(entityList)
    if isinstance(attackedMonster, Monster):
        curHan.renderMessages(attackedMonster.attackedMsg
                              .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg))
    # [curHan.renderMessages(entity.attackedMsg.format(entity.name, entity.hp, entity.dmg))
    #  for entity in entityList if isinstance(entity, Monster) and entity.attacked]

    dx, dy = curHan.playerInput()
    player.move(entityList, gameMap, dx, dy)
    if player.hp <= 0:
        break

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()

