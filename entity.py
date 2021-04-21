# -*- coding: utf-8 -*-
import random
from math import sqrt

# Entity class for all the interactive units on game map
class Entity:
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=4):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.dark = dark
        self.light = light
        self.blocksMovement = blocksMovement
        self.order = order

    # Empty collision which can be used for all entities accordingly
    def collision(self, player, entityList):
        pass

# Creatures are entities who can move and attack, player is a creature as well
class Creature(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True,
                 order=5, hp=0, dmg=0, lvl=1, baseHp=10, baseDmg=2):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.hp = hp
        self.dmg = dmg
        self.lvl = lvl
        self.baseHp = baseHp
        self.baseDmg = baseDmg

    # Attack function for general creatures
    def attack(self, enemy):
        enemy.attacked = True
        enemy.attackedOnce = True
        self.hp -= enemy.dmg
        enemy.hp -= self.dmg

    # Move function for all creatures
    def move(self, entityList, gameMap, inventory, dx, dy):
            self.x += dx
            self.y += dy

# Monster Class
class Monster(Creature):
    # Initializes a lot of monster related variables
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=6,
                 hp=10, dmg=2, lvl=1, attacked=False, attackedMsg='Attacked', deathMsg='Died', baseHp=10,
                 baseDmg=2, xpReward=0, xpRewardBase=15, lvlGap=3, xpIncrease=15, attackedOnce=False):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.attacked = attacked
        self.attackedMsg = attackedMsg
        self.deathMsg = deathMsg
        self.xpRewardBase = xpRewardBase
        self.xpIncrease = xpIncrease
        self.lvlGap = lvlGap
        self.attackedOnce = attackedOnce
        self.hp = self.baseHp
        self.dmg = self.baseDmg

        # Calculates reward directly
        self.xpReward = self.xpRewardBase + self.xpIncrease * self.lvl

    # Changes collision
    def collision(self, player, entityList):
        player.attack(self)
        if self.hp <= 0:
            self.attackedMsg = self.deathMsg
            player.xp += self.xpReward
            player.calcLevel(entityList)

    # Spawns Random items on dead monsters
    def spawnRandomItem(self, itemList, itemPresets, itemClassTypes, amount):
        # Weights for right random distribution
        weights = [item.weight for item in itemPresets]
        # Uses random for chosing an item
        item = (random.choices(itemPresets, weights=weights, k=1))[0]
        itemClassType = itemClassTypes.get(item.name)

        # Returns sometimes, so that items don't spawn all the time
        if (item.name).lower() == 'empty':
            return

        # For potions (should be for all stackable types) randomizes amount as well
        elif isinstance(item.invItem, itemClassTypes.get('Potion')):
            amounts = [i for i in range(1, amount + 1)]
            item.invItem.amount = random.choices(amounts, weights=sorted(amounts, reverse=True), k=1)[0]

        # Creates new item
        newItem = Item(x=self.x, y=self.y, char=item.char, name=item.name, dark=item.dark, light=item.light,
                       blocksMovement=item.blocksMovement, order=item.order, picked=item.picked,
                       weight=item.weight, invItem=itemClassType(item.invItem.name, item.invItem.stackSize,
                        item.invItem.desc, item.invItem.amount, item.invItem.consumable,
                        item.invItem.equipped, item.invItem.used))

        # Assigned the variables respectively
        if isinstance(item.invItem, itemClassTypes.get('Potion')):
            newItem.invItem.healPart=item.invItem.healPart
        elif isinstance(item.invItem, itemClassTypes.get('Weapon')):
            newItem.invItem.dmg = item.invItem.dmg
        elif isinstance(item.invItem, itemClassTypes.get('Armor')):
            newItem.invItem.defence = item.invItem.defence

        # Adds items to itemList
        itemList[newItem.x, newItem.y] = newItem

    # Returns attacked monster
    def returnAttackedMonster(self, entityList):
        for entity in entityList.values():
            if isinstance(entity, Monster) and entity.attacked:
                entity.attacked = False
                return entity
        else:
            return ''

    # Spawns random monster
    def spawnRandomMonsters(self, entityList, itemList, gameMapObj, entityBase, amountMax, randomSpawningAmount=False,
                            playableWidthMin=1, playableWidthMax=80, playableHeightMin=1, playableHeightMax=20):
        # Loops by the amount of monsters to spawn, can be random amount
        for i in range(amountMax if not randomSpawningAmount else random.randint(0, amountMax)):
            while True:
                # creates new monster entity
                entity = Monster(char=entityBase.char, name=entityBase.name, dark=entityBase.dark,
                                 light=entityBase.light, blocksMovement=entityBase.blocksMovement,
                                 hp=entityBase.baseHp, dmg=entityBase.baseDmg, baseHp=entityBase.baseHp,
                                 baseDmg=entityBase.baseDmg, lvl=entityBase.lvl,
                                 xpRewardBase=entityBase.xpRewardBase,
                                 attackedMsg=entityBase.attackedMsg, deathMsg=entityBase.deathMsg)

                entity.x = random.randint(playableWidthMin, playableWidthMax)
                entity.y = random.randint(playableHeightMin, playableHeightMax)

                # Checks if possible to spawn, otherwise loops again until it can
                if not (entity.x, entity.y) in gameMapObj.forbiddenTiles:
                    if not (gameMapObj.gameMap.get((entity.x, entity.y))).blocksMovement:
                        if entityList.get((entity.x, entity.y)) == None and \
                                gameMapObj.gameMap.get((entity.x, entity.y)) != None and \
                                itemList.get((entity.x, entity.y)) == None:
                            entityList[(entity.x, entity.y)] = entity
                            break
    # Level-up and assignment of new values, proportional against player leveling
    def levelUp(self, player):
        if player.lvl - self.lvlGap > 0 and not self.attackedOnce:
            self.lvl = player.lvl - self.lvlGap
            self.xpReward = self.xpRewardBase + self.xpIncrease * self.lvl
            self.hp = int(self.baseHp + player.hp // 2)
            self.dmg = int(self.baseDmg + self.lvl - 1)

    # Updates entities when player levels up
    def entityListUpdate(self, entityList, player):
        for entity in entityList.values():
            if isinstance(entity, Monster):
                entity.levelUp(player)

# Boss class, a bit different from Monster
class Boss(Monster):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=6,
                 hp=120, dmg=20, attacked=False, attackedMsg='Attacked', deathMsg='Died', attackedOnce=False,
                 lvl=1, baseHp=120, baseDmg=20):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order, hp, dmg,
                         baseHp=baseHp, baseDmg=baseDmg)
        self.attacked = attacked
        self.attackedMsg = attackedMsg
        self.deathMsg = deathMsg
        self.attackedOnce = attackedOnce
        self.baseHp = baseHp
        self.baseDmg = baseDmg

    # Changes collision
    def collision(self, player, entityList):
        player.attack(self)
        if self.hp <= 0:
            self.attackedMsg = self.deathMsg

    # Returns attacked monster differently
    def returnAttackedMonster(self, entityList):
        for entity in entityList.values():
            if isinstance(entity, Boss) and entity.attacked:
                entity.attacked = False
                return entity
        else:
            return ''

    # Doesn't level up
    def levelUp(self, player):
        pass

    # Doesn't update entityList
    def entityListUpdate(self, entityList, player):
        pass

# Stationary class, can't move and attack
class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=2, key=False):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.key = key

# NPC class
class NPC(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=3,
                 npcMsgList=['NPC'], msgFlag=False, healAmount=3, healedTimes=0, healTimeMax=3, curMsgIndex=0):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.healAmount = healAmount
        self.npcMsgList = npcMsgList
        self.msgFlag = msgFlag
        self.healTimesMax = healTimeMax
        self.healedTimes = healedTimes
        self.curMsgIndex = curMsgIndex

    # NPC respawning
    def respawnNpc(self, entityList, itemList, gameMapObj, playableWidthMin=1, playableWidthMax=80,
                   playableHeightMin=1, playableHeightMax=20):
        # If it can heal variable is reset
        self.healedTimes = 0
        # Tries to find new place to respawn, when successful exits
        while True:
            x = random.randint(playableWidthMin, playableWidthMax)
            y = random.randint(playableHeightMin, playableHeightMax)
            cords = (x, y)
            if cords not in gameMapObj.forbiddenTiles:
                if not gameMapObj.gameMap.get(cords).blocksMovement:
                    if entityList.get(cords) == None and itemList.get(cords) == None:
                        entityList.pop((self.x, self.y))
                        self.x = x
                        self.y = y
                        entityList[(self.x, self.y)] = self
                        break

    # Looping of messages
    def loopMsgs(self):
        if self.curMsgIndex < len(self.npcMsgList) - 1:
            self.curMsgIndex += 1
        else:
            self.curMsgIndex = 0

# Wizard class, different collision
class Wizard(NPC):
    def collision(self, player, entityList):
        self.msgFlag = True

# Fountain class class, different collision, heals
class Fountain(NPC):
    def collision(self, player, entityList):
        self.healedTimes += 1
        self.msgFlag = True
        player.heal()

# Item class, for items that can lie on the ground
class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=False, order=1,
                 picked=False, weight=1, invItem=None):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.picked = picked
        self.weight = weight
        self.invItem = invItem

    # Spawns random item entity at random location, similar to random spawning in monster
    def spawnRandomItemEntity(self, entityList, itemList, gameMapObj, entityBase, invItemBase, amountMax=1,
                              randomSpawningAmount=False, playableWidthMin=1, playableWidthMax=80,
                              playableHeightMin=1, playableHeightMax=20):
        for i in range(amountMax if not randomSpawningAmount else random.randint(0, amountMax)):
            while True:
                entity = Item(char=entityBase.char, name=entityBase.name, dark=entityBase.dark,
                                 light=entityBase.light, blocksMovement=entityBase.blocksMovement,
                              invItem=invItemBase)

                entity.x = random.randint(playableWidthMin, playableWidthMax)
                entity.y = random.randint(playableHeightMin, playableHeightMax)
                if not (entity.x, entity.y) in gameMapObj.forbiddenTiles:
                    if not (gameMapObj.gameMap.get((entity.x, entity.y))).blocksMovement:
                        if entityList.get((entity.x, entity.y)) == None and \
                                gameMapObj.gameMap.get((entity.x, entity.y)) != None and \
                                itemList.get((entity.x, entity.y)) == None:
                            itemList[(entity.x, entity.y)] = entity
                            break
