import time

from Entity import *
import curses

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
screen.nodelay(1)
curses.start_color()

curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

h, w = screen.getmaxyx()
text = 'Test'
x = w//2 - len(text)//2
y = h//2

screen.attron(curses.color_pair(1))
screen.addstr(y, x, text)
screen.attroff(curses.color_pair(1))

screen.refresh()
time.sleep(3)

curses.curs_set(0)
curses.echo()
curses.nocbreak()

curses.endwin()

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
