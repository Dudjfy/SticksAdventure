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
orc = Monster(68, 18, 'o', 'Orc', 2, 3, True, baseHp=10, baseDmg=2, attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=15)
troll = Monster(69, 18, 'T', 'Troll', 2, 3, True, baseHp=20, baseDmg=1, attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=40)
goblin = Monster(70, 18, 'G', 'Goblin', 2, 3, True, baseHp=4, baseDmg=6, attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=50)
sword = Item(60, 18, '/', 'Sword', 2, 4, False)
fountain = NPC(61, 18, '*', 'Health Fountain', 2, 6, True, healAmount=3, healedTimes=0, healTimeMax=3,
               npcMsgList=['Healed player {0} HP', 'Player already at max HP!'])
wizard = NPC(80, 19, 'W', 'Wizard', 2, 7, True,
             npcMsgList=['Welcome To The Dungeon, Stick!', 'Let your adventure begin with WASD',
                         'to move, interact or attack Monster!', "Use E to pick up Items of Loot",
                         'You may leave after defeating the Boss!', 'Good luck with your adventure, Stick!'])
test = Entity(5, 2)

# entityList = [player, orc, sword, test]
entityList = {}
itemList = {}
entityList[(player.x, player.y)] = player
entityList[(orc.x, orc.y)] = orc
entityList[(troll.x, troll.y)] = troll
entityList[(goblin.x, goblin.y)] = goblin
itemList[(sword.x, sword.y)] = sword
entityList[(fountain.x, fountain.y)] = fountain
entityList[(wizard.x, wizard.y)] = wizard
entityList[(test.x, test.y)] = test

# Orcs test
# [entityList.append(Monster(40 + i, 18, 'o', 'Orc' + str(i), 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}'))
#  for i in range(12)]

# entityList.sort(key=lambda x: x.order)

gameMap = GameMap().createGameMapFromFile()
forbiddenTiles = GameMap().addForbiddenTiles([], 57, 17, 80, 20)


# Orcs random over whole map
Monster().spawnRandomMonsters(entityList, gameMap, forbiddenTiles, orc, 50)
Monster().spawnRandomMonsters(entityList, gameMap, forbiddenTiles, troll, 20)
Monster().spawnRandomMonsters(entityList, gameMap, forbiddenTiles, goblin, 10)

exploredGameMap = {}

for tile in gameMap.values():
    if tile.x == 0 or tile.x == 81 or tile.y == 0 or tile.y == 21:
        exploredGameMap[(tile.x, tile.y)] = tile

rad = 3         # Radius of light
rays = 360
steps = rad
gameOn = True

curHan.renderMessages()

while gameOn:
    # curHan.screen.clear()
    # curHan.renderFrame(gameMap, exploredGameMap, entityList, itemList, player, rad, rays, steps)

    curHan.renderPlayerStats(player)

    attackedMonster = Monster().returnAttackedMonster(entityList)

    if isinstance(attackedMonster, Monster):

        curHan.renderMessages(attackedMonster.attackedMsg\
            .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg),
                              isinstance(attackedMonster, Monster))

        if attackedMonster.hp <= 0:
            entityList.pop((attackedMonster.x, attackedMonster.y))

    if fountain.msgFlag:
        curHan.renderMessages(fountain.npcMsgList[1] if player.healedHp == 0 else
                              fountain.npcMsgList[0].format(player.healedHp), True)
        fountain.msgFlag = False
        if fountain.healedTimes >= fountain.healTimesMax:
            fountain.respawnNpc(entityList, itemList, gameMap, forbiddenTiles)

    for entity in entityList.values():
        if isinstance(entity, NPC) and entity.msgFlag:
            curHan.renderMessages(entity.npcMsgList[entity.curMsgIndex], entity.msgFlag)
            entity.loopMsgs()
            entity.msgFlag = False
            break

    curHan.renderFrame(gameMap, exploredGameMap, entityList, itemList, player, rad, rays, steps)

    gameOn = curHan.playerInput(player, entityList, gameMap)

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()

