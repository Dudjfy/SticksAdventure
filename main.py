from Entity import *

player = Entity(10, 10, '@', 'Player', 'blue', True)

entities = []
entities.append(player)

for entity in entities:
    print('X:{}     Y:{}    Char:{}     Name:{}     Color:{}    Blocks Movement:{}'.format(
        entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))
