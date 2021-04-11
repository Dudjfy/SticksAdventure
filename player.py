from entity import *

# Jag valde att ha player entityn separat eftersom det är en stor klass med en massa
# komplicerade metoder. Dessutom vill jag ha inventory klassen i denna fil.
class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=2, light=1, blocksMovement=True,
                 order=7, hp=30, dmg=4, lvl=1, xp=0, xpConst=0.2, baseHp=10, baseDmg=2, maxHp=10, healedHp=0,
                 defence=0, sword=None, armor=None):
        super().__init__(x, y, char, name, dark, light, blocksMovement, order, hp, dmg, lvl, baseHp, baseDmg)
        self.xp = xp
        self.xpConst = xpConst
        self.maxHp = baseHp
        self.healedHp = healedHp
        self.sword = sword
        self.armor = armor
        self.defence = defence
        # self.msgFlag = msgFlag
        # self.msg = msg

    def attack(self, enemy):
        enemy.attacked = True
        enemy.attackedOnce = True
        self.hp -= enemy.dmg - (0 if self.armor == None else self.defence)
        enemy.hp -= self.dmg + (0 if self.sword == None else self.sword.dmg)

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

    def heal(self, healPart=0.2):
        if self.hp + int(self.maxHp * healPart) < self.maxHp:
            self.hp += int(self.maxHp * healPart)
            self.healedHp = int(self.maxHp * healPart)
        else:
            self.healedHp = self.maxHp - self.hp
            self.hp = self.maxHp

    def equip(self, eqPiece):
        if isinstance(eqPiece, Sword):
            if self.sword == None:
                self.sword = eqPiece
                return True
            else:
                self.sword = None
                return False

        elif isinstance(eqPiece, Armor):
            if self.armor == None:
                self.armor = eqPiece
                self.defence = eqPiece.defence
                return True
            else:
                self.armor = None
                self.defence = 0
                return False

class Inventory:
    def __init__(self, totalSize=10, visibleSize=4, itemList=[], startPos=0, curVisibleIdx=0, msgFlag=False,
                 msg='No Msg'):
        self.totalSize = totalSize
        self.visibleSize = visibleSize
        self.itemList = itemList
        self.startPos = startPos
        self.curVisibleIdx = curVisibleIdx
        self.msgFlag = msgFlag
        self.msg = msg

    def createItem(self, item):
        return InvItem(item.name, item.stackSize, item.desc, item.amount)

    def addItem(self, newItem, showMsg=True):
        ''' NEED TO FIX FOR ADDING ITEMS TO EXISTING ITEMS AMOUNT '''
        if len(self.itemList) < self.totalSize:
            if len(self.itemList) == 0:
                self.startPos = 0
                self.curVisibleIdx = 0
            for item in self.itemList:
                if item.name == newItem.name:
                    if item.amount == item.stackSize:
                        continue
                    elif item.amount + newItem.amount > item.stackSize:
                        newItem.amount = item.amount + newItem.amount - item.stackSize
                        item.amount = item.stackSize
                        if len(self.itemList) + 1 <= self.totalSize:
                            if showMsg:
                                self.msg = 'Picked up: {} - Amount: {}'.format(newItem.name, newItem.amount)
                                self.msgFlag = True
                            self.itemList.append(newItem)
                    else:
                        item.amount += newItem.amount
                    break
            else:
                if showMsg:
                    self.msg = 'Picked up: {}'.format(newItem.name)
                    self.msgFlag = True
                self.itemList.append(newItem)

    def nextItem(self, nextItem):
        if len(self.itemList) > 0:
            if nextItem == -1:
                if self.curVisibleIdx == 0:
                    if self.startPos > 0:
                        self.startPos -= 1
                else:
                    self.curVisibleIdx -= 1

            elif nextItem == 1:
                if self.curVisibleIdx == self.visibleSize - 1:
                    if self.startPos < len(self.itemList) - self.visibleSize:
                        self.startPos += 1
                elif self.curVisibleIdx < len(self.itemList) - 1:
                    self.curVisibleIdx += 1

    def useItem(self, player):
        if len(self.itemList) > 0:
            curItem = self.itemList[self.startPos + self.curVisibleIdx]
            if curItem.consumable:
                if curItem.amount > 0:
                    ''' NEED TO IMPLEMENT KEY USAGE '''
                    self.msg = 'Used {}'.format(curItem.name)
                    self.msgFlag = True

                    curItem.use(player)
                    curItem.amount -= 1
                    if curItem.amount == 0:
                        self.itemList.pop(self.startPos + self.curVisibleIdx)
                        if len(self.itemList) > 0:
                            if self.startPos == 0:
                                if self.curVisibleIdx > len(self.itemList) - 1:
                                    self.curVisibleIdx -= 1
                            elif self.startPos + self.visibleSize > len(self.itemList):
                                self.startPos -= 1
            else:
                if isinstance(curItem, Key):
                    self.msg = "Can't use key this way, find a door"
                else:
                    self.msg = '{} {}'.format('Equipped' if curItem.use(player) else 'Unequipped', curItem.name)
                self.msgFlag = True


class InvItem:
    def __init__(self, name='No Name', stackSize=1, desc='No Description', amount=1, consumable=False,
                 equipped=False, used=False):
        self.name = name
        self.stackSize = stackSize
        self.desc = desc
        self.amount = amount
        self.consumable = consumable
        self.equipped = equipped
        self.used = used

    def use(self, player):
        pass


''' Potions '''
class Potion(InvItem):
    def __init__(self, name='No Name', stackSize=1, desc='No Description', amount=1, consumable=False,
                 equipped=False, used=False, msg='No Msg', healPart=1):
        super().__init__(name, stackSize, desc, amount, consumable, equipped, used)
        self.healPart = healPart

    def use(self, player):
        player.heal(self.healPart)


class NormalPotion(Potion):
    pass


class MaxPotion(Potion):
    pass

''' Weapons '''
class Weapon(InvItem):
    def __init__(self, name='No Name', stackSize=1, desc='No Description', amount=1, consumable=False,
                 equipped=False, used=False, msg='No Msg', dmg=0):
        super().__init__(name, stackSize, desc, amount, consumable, equipped, used)
        self.dmg = dmg

    def use(self, player):
        return player.equip(self)


class Dagger(Weapon):
    pass


class Sword(Weapon):
    pass

''' Armour '''
class Armor(InvItem):
    def __init__(self, name='No Name', stackSize=1, desc='No Description', amount=1, consumable=False,
                 equipped=False, used=False, msg='No Msg', defence=0):
        super().__init__(name, stackSize, desc, amount, consumable, equipped, used)
        self.defence = defence

    def use(self, player):
        return player.equip(self)


class LeatherArmor(Armor):
    pass


class IronArmor(Armor):
    pass

''' Key '''
class Key(InvItem):
    pass

