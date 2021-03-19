class Entity:
    def __init__(self, x=0, y=0, char='?', color=(255, 255, 255), name='No Name', blocksMovement=True,):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocksMovement = blocksMovement
