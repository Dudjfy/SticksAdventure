# -*- coding: utf-8 -*-
# Det övriga som inte har med tiles från gamemap att göra kommer härstamma från klassen entities
import random
from math import sqrt


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

    def collision(self, player, entityList):
        pass

# Detta kommer vara det som kan gå runt och strida mot spelaren, samt själva spelaren
class Creature(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True,
                 order=5, hp=0, dmg=0, lvl=1, baseHp=10, baseDmg=2):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.hp = hp
        self.dmg = dmg
        self.lvl = lvl
        self.baseHp = baseHp
        self.baseDmg = baseDmg

    def attack(self, enemy):
        enemy.attacked = True
        enemy.attackedOnce = True
        self.hp -= enemy.dmg
        enemy.hp -= self.dmg

    def move(self, entityList, gameMap, dx, dy):
            self.x += dx
            self.y += dy


class Monster(Creature):
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


        self.xpReward = self.xpRewardBase + self.xpIncrease * self.lvl

    def collision(self, player, entityList):
        player.attack(self)
        if self.hp <= 0:
            self.attackedMsg = self.deathMsg
            player.xp += self.xpReward
            player.calcLevel(entityList)

    def returnAttackedMonster(self, entityList):
        for entity in entityList.values():
            if isinstance(entity, Monster) and entity.attacked:
                entity.attacked = False
                return entity
        else:
            return ''

    def spawnRandomMonsters(self, entityList, gameMap, forbiddenTiles, entityBase, amountMax, randomSpawningAmount=False, playableWidthMin=1, playableWidthMax=80,
                   playableHeightMin=1, playableHeightMax=20):
        for i in range(amountMax if not randomSpawningAmount else random.randint(0, amountMax)):
            while True:
                entity = Monster(char=entityBase.char, name=entityBase.name, dark=entityBase.dark,
                                 light=entityBase.light, blocksMovement=entityBase.blocksMovement,
                                 hp=entityBase.baseHp, dmg=entityBase.baseDmg, baseHp=entityBase.baseHp,
                                 baseDmg=entityBase.baseDmg, lvl=entityBase.lvl,
                                 xpRewardBase=entityBase.xpRewardBase,
                                 attackedMsg=entityBase.attackedMsg, deathMsg=entityBase.deathMsg)

                entity.x = random.randint(playableWidthMin, playableWidthMax)
                entity.y = random.randint(playableHeightMin, playableHeightMax)
                if not (entity.x, entity.y) in forbiddenTiles:
                    if not (gameMap.get((entity.x, entity.y))).blocksMovement:
                        if entityList.get((entity.x, entity.y)) == None and gameMap.get((entity.x, entity.y)) != None:
                            entityList[(entity.x, entity.y)] = entity
                            break

    def levelUp(self, player):
        if player.lvl - self.lvlGap > 0 and not self.attackedOnce:
            self.lvl = player.lvl - self.lvlGap
            self.xpReward = self.xpRewardBase + self.xpIncrease * self.lvl
            self.hp = int(self.baseHp + player.hp // 2)
            self.dmg = int(self.baseDmg + self.lvl - 1)

    def entityListUpdate(self, entityList, player):
        for entity in entityList.values():
            if isinstance(entity, Monster):
                entity.levelUp(player)

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

    def collision(self, player, entityList):
        player.attack(self)
        if self.hp <= 0:
            self.attackedMsg = self.deathMsg

    def returnAttackedMonster(self, entityList):
        for entity in entityList.values():
            if isinstance(entity, Boss) and entity.attacked:
                entity.attacked = False
                return entity
        else:
            return ''

    def levelUp(self, player):
        pass

    def entityListUpdate(self, entityList, player):
        pass

class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=2, key=False):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.key = key


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

    def respawnNpc(self, entityList, itemList, gameMap, forbiddenTiles, playableWidthMin=1, playableWidthMax=80,
                   playableHeightMin=1, playableHeightMax=20):
        self.healedTimes = 0
        while True:
            x = random.randint(playableWidthMin, playableWidthMax)
            y = random.randint(playableHeightMin, playableHeightMax)
            cords = (x, y)
            if cords not in forbiddenTiles:
                if not gameMap.get(cords).blocksMovement:
                    if entityList.get(cords) == None and itemList.get(cords) == None:
                        entityList.pop((self.x, self.y))
                        self.x = x
                        self.y = y
                        entityList[(self.x, self.y)] = self
                        break

    def loopMsgs(self):
        if self.curMsgIndex < len(self.npcMsgList) - 1:
            self.curMsgIndex += 1
        else:
            self.curMsgIndex = 0

class Wizard(NPC):
    def collision(self, player, entityList):
        self.msgFlag = True

class Fountain(NPC):
    def collision(self, player, entityList):
        self.healedTimes += 1
        self.msgFlag = True
        player.heal()

class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=False, order=1):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)