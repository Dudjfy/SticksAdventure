class Entity:
    def __init__(self, x=0, y=0, char='?', name='No Name', color='black', blocksMovement=True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocksMovement = blocksMovement

class Creature(Entity):
    def move(self, dx, dy):
        self.x += dx
        self.y += dy