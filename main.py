# -*- coding: utf-8 -*-
import time

from entity import *
from player import *
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
# player = Player(6, 2, '@', 'Player', 2, 5, True, baseHp=30, baseDmg=4)
orc = Monster(68, 18, 'o', 'Orc', 2, 3, True, baseHp=10, baseDmg=2,
              attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=15)
troll = Monster(69, 18, 'T', 'Troll', 2, 3, True, baseHp=20, baseDmg=1,
                attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=40)
goblin = Monster(70, 18, 'G', 'Goblin', 2, 3, True, baseHp=4, baseDmg=6,
                 attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=50)
boss = Boss(5, 2, 'B', 'Boss', 2, 9, True, hp=120, dmg=20,
            attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='Boss died. You won, Stick!')
fountain = Fountain(61, 18, '*', 'Health Fountain', 2, 6, True, healAmount=3, healedTimes=0, healTimeMax=3,
               npcMsgList=['Healed player {0} HP', 'Player already at max HP!'])
wizard = Wizard(80, 19, 'W', 'Wizard', 2, 7, True,
             npcMsgList=['Welcome To The Dungeon, Stick!', 'Let your adventure begin with WASD',
                         'to move, interact or attack others!', "Use E to pick up Items of Loot",
                         'You may leave if the Boss falls!', 'Good luck on your adventure, Stick!'])
# bossDoor = Door(5, 5, '-', 'Boss Door', True)
# test = Entity(5, 2)

# entityList = [player, orc, weapon, test]
entityList = {}
entityList[(player.x, player.y)] = player
entityList[(orc.x, orc.y)] = orc
entityList[(troll.x, troll.y)] = troll
entityList[(goblin.x, goblin.y)] = goblin
entityList[(fountain.x, fountain.y)] = fountain
entityList[(wizard.x, wizard.y)] = wizard
# entityList[(bossDoor.x, bossDoor.y)] = bossDoor
entityList[(boss.x, boss.y)] = boss

key = Item(57, 17, '<', 'Key', 2, 4, False, invItem=Key('Key', 1, 'Key, opens locked doors', 1, False))

leatherArmor = Item(57, 18, '%', 'Leather Armor', 2, 4, False, weight=3,
                   invItem=LeatherArmor('Leather Armor', 1, 'Leather Armor, DEF + 1', 1, False, defence=1))
ironArmor = Item(58, 18, '%', 'Iron Armor', 2, 4, False, weight=1,
                   invItem=IronArmor('Iron Armor', 1, 'Iron Armor, DEF + 3', 1, False, defence=3))
dagger = Item(59, 18, '/', 'Dagger', 2, 4, False, weight=3,
             invItem=Dagger('Dagger', 1, 'Dagger, deals 2 DMG', 1, False, dmg=2))
sword = Item(60, 18, '/', 'Sword', 2, 4, False, weight=1,
             invItem=Dagger('Sword', 1, 'Sword, deals 4 DMG', 1, False, dmg=4))
normalPotion = Item(62, 19, '~', 'Potion', 2, 4, False, weight=6,
             invItem=NormalPotion('Potion', 99, 'Potion, heals 1/5 of max HP', 1, True, healPart=0.2))
maxPotion = Item(63, 19, '~', 'Max Potion', 2, 4, False, weight=1,
             invItem=MaxPotion('Max Potion', 99, 'Max Potion, heals max HP', 1, True, healPart=1))
falseItem = Item(name='Empty', weight=85)

itemList = {}
itemPresets = []

itemPresets.append(dagger)
itemPresets.append(sword)
itemPresets.append(leatherArmor)
itemPresets.append(ironArmor)
itemPresets.append(normalPotion)
itemPresets.append(maxPotion)
itemPresets.append(falseItem)

itemList[(key.x, key.y)] = key
itemList[(dagger.x, dagger.y)] = dagger
itemList[(sword.x, sword.y)] = sword
itemList[(leatherArmor.x, leatherArmor.y)] = leatherArmor
itemList[(ironArmor.x, ironArmor.y)] = ironArmor
itemList[(normalPotion.x, normalPotion.y)] =normalPotion
itemList[(maxPotion.x, maxPotion.y)] = maxPotion

# Orcs test
# [entityList.append(Monster(40 + i, 18, 'o', 'Orc' + str(i), 2, True, hp=10, dmg=2, attackedMsg='{} - HP:{:>3} DMG:{:>3}'))
#  for i in range(12)]

# entityList.sort(key=lambda x: x.order)

gameMapObj = GameMap()
gameMapObj.createGameMapFromFile()
gameMapObj.addForbiddenTiles(57, 17, 80, 20)
gameMapObj.addForbiddenTiles(1, 1, 9, 6)
gameMapObj.addBorderTiles()

# Orcs random over whole map
Monster().spawnRandomMonsters(entityList, gameMapObj, orc, 50)
Monster().spawnRandomMonsters(entityList, gameMapObj, troll, 20)
Monster().spawnRandomMonsters(entityList, gameMapObj, goblin, 10)

rad = 3         # Radius of light
rays = 360
steps = rad
gameOn = True
curHan.renderMode = True

curHan.renderMessages()

inventory = Inventory()
# potion = NormalPotion('Potion', 99, 'Heals 1/5 of max HP', 3, True, healPart=0.2)
# maxPotion = MaxPotion('Max Potion', 99, 'Heals full HP', 3, True, healPart=1)
# test1 = InvItem('test1', 99, 'Heals full HP', 99, True)
# test2 = InvItem('test2', 99, 'Heals full HP', 1, True)
# test3 = InvItem('test3', 99, 'Heals full HP', 69, True)
# inventory.addItem(potion, False)
# inventory.addItem(maxPotion, False)
# inventory.addItem(test1, False)
# inventory.addItem(test2, False)
# inventory.addItem(test3, False)

while gameOn:
    # curHan.screen.clear()
    # curHan.renderFrame(gameMap, exploredGameMap, entityList, itemList, player, rad, rays, steps)

    curHan.renderPlayerStats(player)

    curHan.renderInventory(inventory, player)

    curHan.renderDeviders(4)

    attackedMonster = Monster().returnAttackedMonster(entityList)

    if isinstance(attackedMonster, Monster):

        curHan.renderMessages(attackedMonster.attackedMsg\
            .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg),
                              isinstance(attackedMonster, Monster))

        if attackedMonster.hp <= 0:
            attackedMonster.spawnRandomItem(itemList, itemPresets, 5)
            entityList.pop((attackedMonster.x, attackedMonster.y))

    if fountain.msgFlag:
        curHan.renderMessages(fountain.npcMsgList[1] if player.healedHp == 0 else
                              fountain.npcMsgList[0].format(player.healedHp), True)
        fountain.msgFlag = False
        if fountain.healedTimes >= fountain.healTimesMax:
            fountain.respawnNpc(entityList, itemList, gameMapObj)

    if inventory.msgFlag:
        curHan.renderMessages(inventory.msg, inventory.msgFlag)
        inventory.msgFlag = False

    for entity in entityList.values():
        if isinstance(entity, NPC) and entity.msgFlag:
            curHan.renderMessages(entity.npcMsgList[entity.curMsgIndex], entity.msgFlag)
            entity.loopMsgs()
            entity.msgFlag = False
            break

    curHan.renderFrame(gameMapObj, entityList, itemList, player, rad, rays, steps)

    gameOn = curHan.playerInput(player, inventory, entityList, itemList, gameMapObj)

menu.gameOver(curHan.screen)


""" Curses End """
curHan.cursesEnd()

