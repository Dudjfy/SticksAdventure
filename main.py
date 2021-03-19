from Entity import *

player = Entity(10, 10, '@', 'Player', 'blue', True)
orc = Entity(15, 10, 'o', 'Orc', 'white', True)



entities = []
entities.append(player)
entities.append(orc)

for entity in entities:
    print('X:{}     Y:{}    Char:{}     Name:{}     Color:{}    Blocks Movement:{}'.format(
        entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))
