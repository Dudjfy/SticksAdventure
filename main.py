from Entity import *

player = Entity(10, 10, '@', 'Player', 'white', True)
orc = Entity(15, 10, 'o', 'Orc', 'green', True)
sword = Entity(15, 15, '/', 'Sword', 'light_blue', False)
test = Entity()

entities = []
entities.append(player)
entities.append(orc)
entities.append(sword)
entities.append(test)

while True:
    for entity in entities:
        print('X:{}     Y:{}    Char:{}     Name:{}     Color:{}    Blocks Movement:{}'.format(
            entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))

    inp = input('>>> ').strip().lower()
    for letter in inp:
        if letter == 'w':
            player.y -= 1
        if letter == 's':
            player.y += 1
        if letter == 'a':
            player.x -= 1
        if letter == 'd':
            player.x += 1
