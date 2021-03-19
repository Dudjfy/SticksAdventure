from Entity import *

player = Entity(10, 10, '@', 'Player', 'white', True)
orc = Entity(15, 10, 'o', 'Orc', 'green', True)
sword = Entity(15, 15, '/', 'Sword', 'light_blue', False)
test = Entity()

entityList = []
entityList.append(player)
entityList.append(orc)
entityList.append(sword)
entityList.append(test)

entityBlockingCordsList = []
for entity in entityList:
    if entity.blocksMovement and entity != player:
        entityBlockingCordsList.append([entity.y, entity.x])

print(entityBlockingCordsList)

while True:
    # Represents render/draw
    for entity in entityList:
        print('X:{} Y:{} Char:{} Name:{} Color:{} Blocks Movement:{}'.format(
            entity.x, entity.y, entity.char, entity.name, entity.color, entity.blocksMovement))

    # Represents movement
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
