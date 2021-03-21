# Det övriga som inte har med tiles från gamemap att göra kommer härstamma från klassen entities
class Entity:
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=4):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocksMovement = blocksMovement
        self.order = order


    # def sortEntityListInOrder(self, lst):
    #     orderedLst = []
    #     for entity in lst:
    #         if isinstance(entity, Player):
    #             orderedLst.append(entity)
    #         elif isinstance(entity, Monster):
    #             orderedLst.insert(-2, entity)
    #         elif isinstance(entity, Item):
    #             orderedLst.insert(0, entity)
    #         else:
    #             orderedLst.insert(orderedLst.index(), entity)
    #
    #     return orderedLst


# Detta kommer vara det som kan gå runt och strida mot spelaren, samt själva spelaren
class Creature(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=5, hp=0, dmg=0):
        super().__init__(x, y, char, name, color, blocksMovement, order)
        self.hp = hp
        self.dmg = dmg


    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def collisionDetection(self, tileList, dx, dy):
        for tile in tileList:
            if tile.blocksMovement:
                if self.x + dx == tile.x and self.y + dy == tile.y:
                    return True
        return False

class Monster(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=6, hp=10, dmg=2):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg)

class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=7, hp=30, dmg=4):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg)

class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=2):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class NPC(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=3):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=False, order=1):
        super().__init__(x, y, char, name, color, blocksMovement, order)