# -*- coding: utf-8 -*-
# Det övriga som inte har med tiles från gamemap att göra kommer härstamma från klassen entities
import random
from math import sqrt


class Entity:
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=4):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocksMovement = blocksMovement
        self.order = order

# Detta kommer vara det som kan gå runt och strida mot spelaren, samt själva spelaren
class Creature(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=5, hp=0, dmg=0, lvl=1, baseHp=10, baseDmg=2):
        super().__init__(x, y, char, name, color, blocksMovement, order)
        self.hp = hp
        self.dmg = dmg
        self.lvl = lvl
        self.baseHp = baseHp
        self.baseDmg = baseDmg

    def attack(self, enemy):
        enemy.attacked = True
        self.hp -= enemy.dmg
        enemy.hp -= self.dmg

    def move(self, entityList, gameMap, dx, dy):
            self.x += dx
            self.y += dy

class Monster(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=6, hp=10, dmg=2, lvl=1, attacked=False, attackedMsg='Attacked', baseHp=10, baseDmg=2):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.attacked = attacked
        self.attackedMsg = attackedMsg

    def returnAttackedMonster(self, entityList):
        for entity in entityList:
            if isinstance(entity, Monster) and entity.attacked:
                entity.attacked = False
                return entity

    def createRandomMonsters(self, entityList, entityBase, amountMax, randomSpawning=False):
        for i in range(amountMax if not randomSpawning else random.randint(0, amountMax)):
            entity = Monster(char=entityBase.char, name=entityBase.name, color=entityBase.color,
                             blocksMovement=entityBase.blocksMovement, hp=entityBase.hp, dmg=entityBase.dmg,
                             lvl=entityBase.lvl, attackedMsg=entityBase.attackedMsg)
            entity.x = random.randint(1, 80)
            entity.y = random.randint(1, 20)
            for oldEntity in entityList:
                if oldEntity.x == entity.x and oldEntity.y == entity.y:
                    break
            else:
                entityList.append(entity)

class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=7, hp=30, dmg=4, lvl=1, xp=0, xpConst=0.2, baseHp=10, baseDmg=2):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.xp = xp
        self.xpConst = xpConst

    def collisionDetectionMap(self, tileList, dx, dy):
        for tile in tileList:
            if tile.blocksMovement:
                if self.x + dx == tile.x and self.y + dy == tile.y:
                    return True
        return False

    def collisionDetectionEntityList(self, entityList, dx, dy):
        for entity in entityList:
            if entity.blocksMovement:
                if self.x + dx == entity.x and self.y + dy == entity.y:
                    if isinstance(entity, Monster):
                        self.attack(entity)
                        if entity.hp <= 0:
                            entityList.remove(entity)

                    return True
        return False

    def move(self, entityList, gameMap, dx, dy):
        if not self.collisionDetectionEntityList(entityList, dx, dy) and \
                not self.collisionDetectionMap(gameMap, dx, dy):
            self.x += dx
            self.y += dy

    def calcLevel(self):
        if int(self.xpConst * sqrt(self.xp)) != 0:
            oldLvl = self.lvl
            self.lvl = int(self.xpConst * sqrt(self.xp))
            if oldLvl != self.lvl:
                self.levelUp()

    def levelUp(self):
            self.hp = int(self.baseHp + (self.lvl - 1) * sqrt(self.xp) * self.xpConst)
            self.dmg = int(self.baseDmg + (self.lvl - 1) * sqrt(self.xp) * self.xpConst ** 2)

class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=2):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class NPC(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=3):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=False, order=1):
        super().__init__(x, y, char, name, color, blocksMovement, order)