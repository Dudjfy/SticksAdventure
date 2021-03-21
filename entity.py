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

# Detta kommer vara det som kan gå runt och strida mot spelaren, samt själva spelaren
class Creature(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=5, hp=0, dmg=0, lvl=1):
        super().__init__(x, y, char, name, color, blocksMovement, order)
        self.hp = hp
        self.dmg = dmg
        self.lvl = lvl

    def attack(self, enemy):
        self.hp -= enemy.dmg
        enemy.hp -= self.dmg
        if enemy.hp <= 0:
            pass
        if self.hp <= 0:
            pass

        # return enemy

    def move(self, entityList, gameMap, dx, dy):
            self.x += dx
            self.y += dy

class Monster(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=6, hp=10, dmg=2, lvl=1):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg, lvl)

class Player(Creature):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True,
                 order=7, hp=30, dmg=4, lvl=1, xp=0):
        super().__init__(x, y, char, name, color, blocksMovement, order, hp, dmg, lvl)
        self.xp = xp

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

class Stationary(Entity):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=2):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class NPC(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=True, order=3):
        super().__init__(x, y, char, name, color, blocksMovement, order)

class Item(Stationary):
    def __init__(self, x=0, y=0, char='?', name='No Name', color=1, blocksMovement=False, order=1):
        super().__init__(x, y, char, name, color, blocksMovement, order)