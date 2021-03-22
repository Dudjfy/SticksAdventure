# -*- coding: utf-8 -*-
class GameMap:
    def __init__(self):
        self.gameMap = {}
        self.wallChar = '#'
        self.floorCharDark = ' '
        self.floorCharLight = '.'

    def createGameMapFromFile(self):
        file = open('map.txt', 'r')

        for y, row in enumerate(file):
            for x, tile in enumerate(row):
                if tile == self.floorCharDark:
                    self.gameMap[(x, y)] = Tile(x, y, self.floorCharDark, self.floorCharLight, 'Floor', 2, 1, False)
                elif tile == self.wallChar:
                    self.gameMap[(x, y)] = (Tile(x, y, self.wallChar, self.wallChar, 'Wall', 2, 1, True))
        file.close()
        return self.gameMap

class Tile:
    def __init__(self, x=0, y=0, charDark='?', charLight='?', name='No Name', dark=1, light=2, blocksMovement=True):
        self.x = x
        self.y = y
        self.charDark = charDark
        self.charLight = charLight
        self.name = name
        self.dark = dark
        self.light = light
        self.blocksMovement = blocksMovement