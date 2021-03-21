# -*- coding: utf-8 -*-
class GameMap:
    def __init__(self):
        self.gameMap = set()
        self.wallChar = '#'
        self.floorChar = ' '

    def createGameMapFromFile(self):
        file = open('map.txt', 'r')

        # print('test')
        for y, row in enumerate(file):
            for x, tile in enumerate(row):
                # print(tile, x, y, end='\t')
                if tile == self.floorChar:
                    self.gameMap.add(Tile(x, y, '.', 'Floor', 2, 1, False))
                elif tile == self.wallChar:
                    self.gameMap.add(Tile(x, y, self.wallChar, 'Wall', 2, 1, True))

class Tile:
    def __init__(self, x=0, y=0, char='?', name='No Name', dark=1, light=2, blocksMovement=True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.dark = dark
        self.light = light
        self.blocksMovement = blocksMovement