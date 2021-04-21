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
    
    Spelet är tänkt att vara svårt, på samma sätt som spel den är baserad på denna tid. 
    Därför är det få instruktioner i själva spelet, användaren ska frsöka lista ut allting själv
    (även spelets kontroller). Dock har jag gjort en wizard npc som förklarar lite saker i två första rum, 
    så om man intaractar och pratar med honom (gå in i honom med WASD som när man attackerar monster) så
    berättar han lite hur spelet ska gå till.
    
    Controlls:
    WASD = Gå runt
    E = Ta upp saker från golvet (saker har blå färg)
    Q = Droppa en sak från inventory (man måste sedan antigen bekräfta med Y eller förneka med N)
    F = Använda en sak i inventory (den som är tillfälligt vald, symboliseras med en stjärna '*' som har en omvänd färg
    pallett)
    I/C = Visar information om valda saken
    arrow UP = För att blädra upp i inventory
    arrow DOWN = För att blädra ner i inventory
    
    ESC = Avslutar programmet, viktigt då man kör i konsolen
    
    Cheats:
    0 = Wallhacks, se hela mappen
    - (till höger om 0 på engelsk tangentbord) = +10 xp
    = (till höger om - på engelsk tangentbord) = +1/5 av Max hp

"""
# Creating objects of handler class and menu class, menu barely used though
curHan = CursesHandler()
menu = Menu()

# Sets up curses settings
curHan.cursesSetup()

# Creates entities objects for tutorial purposes
player = Player(78, 19, '@', 'Player', 2, 5, True, baseHp=30, baseDmg=4)
orc = Monster(68, 18, 'o', 'Orc', 2, 3, True, baseHp=10, baseDmg=2,
              attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=15)
troll = Monster(69, 18, 'T', 'Troll', 2, 3, True, baseHp=20, baseDmg=1,
                attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=40)
goblin = Monster(70, 18, 'G', 'Goblin', 2, 3, True, baseHp=4, baseDmg=6,
                 attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='{0} died', xpRewardBase=50)
boss = Boss(5, 2, 'B', 'Boss', 2, 9, True, hp=120, dmg=20,
            attackedMsg='{0} - HP:{1:>3} DMG:{2:>3}', deathMsg='Boss died. You won, Stick!')
fountain = Fountain(61, 19, '*', 'Health Fountain', 2, 6, True, healAmount=3, healedTimes=0, healTimeMax=3,
               npcMsgList=['Healed player {0} HP', 'Player already at max HP!'])

# Instead of adding teleporting functionality and different messages just two wizards are created in different rooms
introWizard = Wizard(80, 19, 'W', 'Wizard', 2, 7, True,
             npcMsgList=[('Welcome To The Dungeon, Stick!', ()), ('Let your adventure begin with WASD', (30, 31, 32, 33)),
                         ('to move, interact or attack others!', ()), ("To access the Boss room you'll need", ()),
                         ('to find a key hidden in the Dungeon', ()),
                         ('You may leave when the Boss falls!', ()), ('Good luck on your adventure, Stick!', ())])
pickUpWizard = Wizard(60, 17, 'W', 'Wizard', 2, 7, True,
             npcMsgList=[('Oh hey again Stick! Already here?', ()),
                         ('When you kill a monster, it may', ()), ('drop an item on the floor', ()),
                         ('To pick up an item, press E', (26,)), ('To cycle through your inventory use', ()),
                         ('UP and DOWN arrows', (0, 1, 7, 8, 9, 10)), ('To use items in inventory, press F', (33,)),
                         ("For current item info press I/C", (28, 30)),
                         ('In the Dungeon you may also find', ()), ('a Health Fountain, but every third', ()),
                         ('time you use it (WASD), it moves', (17, 18, 19, 20)), ('to another location in the Dungeon!', ())])

# Initializes entityList
entityList = {}

# Adds entities to entityList, a dict of cords corresponding to entities
entityList[(player.x, player.y)] = player
entityList[(orc.x, orc.y)] = orc
entityList[(troll.x, troll.y)] = troll
entityList[(goblin.x, goblin.y)] = goblin
entityList[(fountain.x, fountain.y)] = fountain
entityList[(introWizard.x, introWizard.y)] = introWizard
entityList[(pickUpWizard.x, pickUpWizard.y)] = pickUpWizard
entityList[(boss.x, boss.y)] = boss

# Creating items, different types and stats, most were and can be used for testing, most not used now though
key = Item(57, 17, '<', 'Key', 2, 4, False, invItem=Key('Key', 1, 'Key, opens locked doors', 1, False), weight=1)

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

# Initializes entityList
itemList = {}

# Possibility to add items to itemList directly

# itemList[(key.x, key.y)] = key
# itemList[(dagger.x, dagger.y)] = dagger
# itemList[(sword.x, sword.y)] = sword
# itemList[(leatherArmor.x, leatherArmor.y)] = leatherArmor
# itemList[(ironArmor.x, ironArmor.y)] = ironArmor
# itemList[(normalPotion.x, normalPotion.y)] = normalPotion
# itemList[(maxPotion.x, maxPotion.y)] = maxPotion

# List of item presets
itemPresets = []

# Adds items to presets
itemPresets.append(dagger)
itemPresets.append(sword)
itemPresets.append(leatherArmor)
itemPresets.append(ironArmor)
itemPresets.append(normalPotion)
itemPresets.append(maxPotion)
itemPresets.append(falseItem)

# Dict of item classes, to have one way dependency
itemClassTypes = {}

# Adds classes
itemClassTypes['Dagger'] = Dagger
itemClassTypes['Sword'] = Sword
itemClassTypes['Leather Armor'] = LeatherArmor
itemClassTypes['Iron Armor'] = IronArmor
itemClassTypes['Normal Potion'] = NormalPotion
itemClassTypes['Max Potion'] = MaxPotion
itemClassTypes['Potion'] = Potion
itemClassTypes['Weapon'] = Weapon
itemClassTypes['Armor'] = Armor

# Creates gameMap object from GameMap class
gameMapObj = GameMap()
# Creates map from file
gameMapObj.createGameMapFromFile()
# Adds forbidden tiles for spawning
gameMapObj.addForbiddenTiles(57, 17, 80, 20)
gameMapObj.addForbiddenTiles(1, 1, 9, 6)
# Adds border tiles to explored tiles so that the user can see the borders of the whole map
gameMapObj.addBorderTiles()

# Spawns monsters randomly over whole map, uses previously created entities as base for new monsters
Monster().spawnRandomMonsters(entityList, itemList, gameMapObj, orc, 50)
Monster().spawnRandomMonsters(entityList, itemList, gameMapObj, troll, 20)
Monster().spawnRandomMonsters(entityList, itemList, gameMapObj, goblin, 10)

# Variables for rendering and ray-tracing

# Radius of light
rad = 3
# Amount of rays
rays = 360
# Amount of steps per ray
steps = rad

# Game-loop variable
gameOn = True

# Render-mode, can be changed with cheats
curHan.renderMode = True

# Renders current intro messages
curHan.renderMessages()

# Creates an object of Inventory class
inventory = Inventory()

# Test items for inventory initialization

# potion = NormalPotion('Potion', 99, 'Heals 1/5 of max HP', 3, True, healPart=0.2)
# maxPotion = MaxPotion('Max Potion', 99, 'Heals full HP', 3, True, healPart=1)
# test1 = InvItem('test1', 99, 'Heals full HP', 99, True)
# test2 = InvItem('test2', 99, 'Heals full HP', 1, True)
# test3 = InvItem('test3', 99, 'Heals full HP', 69, True)

# Test items adding to inventory

# inventory.addItem(potion, False)
# inventory.addItem(maxPotion, False)
# inventory.addItem(test1, False)
# inventory.addItem(test2, False)
# inventory.addItem(test3, False)

# Spawns a random item for the tutorial
Monster(59, 19).spawnRandomItem(itemList, itemPresets[:len(itemPresets) - 1], itemClassTypes, 5)

# Spawns the key for the boss room somewhere in the dungeon
Item().spawnRandomItemEntity(entityList, itemList, gameMapObj, key, key.invItem)

# Initializes game-loop
while gameOn:
    # Renders player stats, the left column bellow GameMap
    curHan.renderPlayerStats(player)

    # Renders inventory
    curHan.renderInventory(inventory, player)

    # Renders dividers between columns
    curHan.renderDividers(4)

    # Gets the attacked monster if any
    attackedMonster = Monster().returnAttackedMonster(entityList)

    # Checks for attacked monster
    if isinstance(attackedMonster, Monster):
        # Renders monster's message
        curHan.renderMessages(attackedMonster.attackedMsg\
            .format(attackedMonster.name, attackedMonster.hp, attackedMonster.dmg),
                              isinstance(attackedMonster, Monster))
        # If the monster hp is 0 or less, the monster dies and is removed
        if attackedMonster.hp <= 0:
            attackedMonster.spawnRandomItem(itemList, itemPresets, itemClassTypes, 5)
            entityList.pop((attackedMonster.x, attackedMonster.y))

    # Checks for health fountain flag
    if fountain.msgFlag:
        # Renders message
        curHan.renderMessages(fountain.npcMsgList[1] if player.healedHp == 0 else
                              fountain.npcMsgList[0].format(player.healedHp), True)
        # Resets flag
        fountain.msgFlag = False

        # Respawns health fountain if used max amount of times
        if fountain.healedTimes >= fountain.healTimesMax:
            fountain.respawnNpc(entityList, itemList, gameMapObj)

    # Checks for inventory flag
    if inventory.msgFlag:
        # Renders message, resets flag
        curHan.renderMessages(inventory.msg, inventory.msgFlag)
        inventory.msgFlag = False

    # Checks for Entity flags
    for entity in entityList.values():
        if isinstance(entity, NPC) and entity.msgFlag:
            # Wizard, a NPC's flag
            if isinstance(entity, Wizard):
                # Renders message the Wizard way, with highlights
                curHan.renderMessages(entity.npcMsgList[entity.curMsgIndex][0], entity.msgFlag,
                                      entity.npcMsgList[entity.curMsgIndex][1])
            else:
                # Renders the common way
                curHan.renderMessages(entity.npcMsgList[entity.curMsgIndex], entity.msgFlag)

            # Loops messages, resests flag and exists loop
            entity.loopMsgs()
            entity.msgFlag = False
            break

    # Finally renders the frame
    curHan.renderFrame(gameMapObj, entityList, itemList, player, rad, rays, steps)

    # Both input and check if the game is exited or over
    gameOn = curHan.playerInput(player, inventory, entityList, itemList, gameMapObj)

# Shows Game Over screen
menu.gameOver(curHan.screen)

# Ends curses, returns to normal console settings
curHan.cursesEnd()

