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

        self.xpReward = self.xpRewardBase + self.xpIncrease * self.lvl

    def returnAttackedMonster(self, entityList):
        for entity in entityList.values():
            if isinstance(entity, Monster) and entity.attacked:
                entity.attacked = False
                return entity
        else:
            return ''

    def spawnRandomMonsters(self, entityList, gameMap, entityBase, amountMax, randomSpawningAmount=False, playableWidthMin=1, playableWidthMax=80,
                   playableHeightMin=1, playableHeightMax=20):
        for i in range(amountMax if not randomSpawningAmount else random.randint(0, amountMax)):
            while True:
                entity = Monster(char=entityBase.char, name=entityBase.name, dark=entityBase.dark,
                                 light=entityBase.light, blocksMovement=entityBase.blocksMovement, hp=entityBase.hp,
                                 dmg=entityBase.dmg, lvl=entityBase.lvl, xpRewardBase=entityBase.xpRewardBase,
                                 attackedMsg=entityBase.attackedMsg, deathMsg=entityBase.deathMsg)
                entity.x = random.randint(playableWidthMin, playableWidthMax)
                entity.y = random.randint(playableHeightMin, playableHeightMax)
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


class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True,
                 order=7, hp=30, dmg=4, lvl=1, xp=0, xpConst=0.2, baseHp=10, baseDmg=2, maxHp=10, healedHp=0):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.xp = xp
        self.xpConst = xpConst
        self.maxHp = baseHp
        self.healedHp = healedHp

    def move(self, entityList, gameMap, dx, dy):
        cords = (self.x + dx, self.y + dy)
        if not (gameMap.get(cords)).blocksMovement:
            entity = entityList.get(cords)
            if isinstance(entity, Entity) and entityList.get(cords).blocksMovement:
                if isinstance(entity, Monster):
                    self.attack(entity)
                    if entity.hp <= 0:
                        entity.attackedMsg = entity.deathMsg
                        self.xp += entity.xpReward
                        self.calcLevel(entityList)
                        # entityList.pop(cords)
                elif isinstance(entity, NPC):
                    if entity.name == 'Health Fountain':
                        entity.msgFlag = True
                        self.heal()

            else:
                entityList.pop((self.x, self.y))
                self.x += dx
                self.y += dy
                entityList[(self.x, self.y)] = self

    def calcLevel(self, entityList):
        if int(self.xpConst * sqrt(self.xp)) != 0:
            oldLvl = self.lvl
            self.lvl = int(self.xpConst * sqrt(self.xp))
            if oldLvl != self.lvl:
                self.levelUp()
                Monster().entityListUpdate(entityList, self)

    def levelUp(self):
        self.maxHp = int(self.baseHp + (self.lvl - 1) * sqrt(self.xp) * self.xpConst)
        self.dmg = int(self.baseDmg + (self.lvl - 1) * sqrt(self.xp) * self.xpConst ** 2)
        self.heal()

    def heal(self, healPart=5):
        if self.hp + self.maxHp // healPart <= self.maxHp:
            self.hp += self.maxHp // healPart
            self.healedHp = self.maxHp // healPart
        else:
            self.healedHp = self.maxHp - self.hp
            self.hp = self.maxHp


class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=2):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)


class NPC(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True, order=3,
                 npcMsg='NPC', msgFlag=False, healAmount=3):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)
        self.healAmount = healAmount
        self.npcMsg = npcMsg
        self.msgFlag = msgFlag

    def respawnNpc(self, entityList, itemList, gameMap, playableWidthMin=1, playableWidthMax=80,
                   playableHeightMin=1, playableHeightMax=20):
        while True:
            x = random.randint(playableWidthMin, playableWidthMax)
            y = random.randint(playableHeightMin, playableHeightMax)
            cords = (x, y)
            if not gameMap.get(cords).blocksMovement:
                if entityList.get(cords) == None and itemList.get(cords) == None:
                    entityList.pop((self.x, self.y))
                    self.x = x
                    self.y = y
                    entityList[(self.x, self.y)] = self
                    break

class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=False, order=1):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order)