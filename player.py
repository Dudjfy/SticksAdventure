from entity import *

# Jag valde att ha player entityn separat eftersom det är en stor klass med en massa
# komplicerade metoder. Dessutom vill jag ha inventory klassen i denna fil.
class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True,
                 order=7, hp=30, dmg=4, lvl=1, xp=0, xpConst=0.2, baseHp=10, baseDmg=2, maxHp=10, healedHp=0):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.xp = xp
        self.xpConst = xpConst
        self.maxHp = baseHp
        self.healedHp = healedHp

    def move(self, entityList, gameMap, dx, dy):
        coords = (self.x + dx, self.y + dy)
        if not (gameMap.get(coords)).blocksMovement:
            entity = entityList.get(coords)
            if isinstance(entity, Entity) and entityList.get(coords).blocksMovement:
                entity.collision(self, entityList)
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


class Inventory:
    def __init__(self, totalSize=10, visableSize=4, itemList=[], visableList=[], curItem=0):
        self.totalSize = totalSize
        self.visableSize = visableSize
        self.itemList = itemList
        self.visableList = visableList
        self.curItem = curItem

    def addItem(self, item):
        if len(self.itemList) < self.totalSize:
            self.itemList.append(item)
            if len(self.itemList) < self.visableSize:
                self.visableList.append(item)


class InvItem:
    def __init__(self, name='No Name', stackSize=1, desc='No Description', amount=1):
        self.name = name
        self.stackSize = stackSize
        self.desc = desc
        self.amount = amount