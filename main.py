from Entity import *

player = Entity(10, 10, '@', 'Player', 'white', True)
orc = Entity(15, 10, 'o', 'Orc', 'green', True)
sword = Entity(15, 15, '', 'Sword', 'light_blue', False)

entities = []
entities.append(player)
entities.append(orc)
entities.append(sword)

for entity in entities:
    print('X:{}     Y:{}    Char:{}     Name:{}     Color:{}    Blocks Movement:{}'.format(
        entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))
