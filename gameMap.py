# -*- coding: utf-8 -*-

# Game-map class
class GameMap:
    def __init__(self):
        self.gameMap = {}
        self.exploredGameMap = {}
        self.forbiddenTiles = []
        self.wallChar = '#'
        self.floorCharDark = ' '
        self.floorCharLight = '.'
        self.doorCharHorizontal = '-'
        self.doorCharVertical = '|'

    # Creates game-map from file
    def createGameMapFromFile(self):
        file = open('map.txt', 'r')

        for y, row in enumerate(file):
            for x, tile in enumerate(row):
                if tile == self.floorCharDark:
                    self.gameMap[(x, y)] = Floor(x, y)
                elif tile == self.wallChar:
                    self.gameMap[(x, y)] = Wall(x, y)
                elif tile == self.doorCharHorizontal:
                    self.gameMap[(x, y)] = HDoor(x, y)
                elif tile == self.doorCharVertical:
                    self.gameMap[(x, y)] = VDoor(x, y)
        file.close()

    # Adds border tiles to visible tiles dict
    def addBorderTiles(self):
        for tile in self.gameMap.values():
            if tile.x == 0 or tile.x == 81 or tile.y == 0 or tile.y == 21:
                self.exploredGameMap[(tile.x, tile.y)] = tile

    # Adds tiles to forbidden tiles dict
    def addForbiddenTiles(self, xMin, yMin, xMax, yMax):
        for x in range(xMin, xMax + 1):
            for y in range(yMin, yMax + 1):
                self.forbiddenTiles.append((x, y))

    # Replaces tiles with other tile types
    def replaceTile(self, x, y, tileType):
        self.gameMap.pop((x, y))
        tileTypes = {
            Floor().name: Floor,
            Wall().name: Wall,
            HDoor().name: HDoor,
            VDoor().name: VDoor
        }
        self.gameMap[(x, y)] = tileTypes[tileType](x, y)

# Tile class
class Tile:
    def __init__(self, x=0, y=0, charDark='?', charLight='?', name='No Name', dark=2, light=1, blocksMovement=True):
        self.x = x
        self.y = y
        self.charDark = charDark
        self.charLight = charLight
        self.name = name
        self.dark = dark
        self.light = light
        self.blocksMovement = blocksMovement

# Sets tile to a floor tile
class Floor(Tile):
    def __init__(self, x=0, y=0, charDark=GameMap().floorCharDark, charLight=GameMap().floorCharLight,
                 name='Floor', dark=2, light=1, blocksMovement=False):
        super().__init__(x, y, charDark, charLight, name, dark, light, blocksMovement)

# Sets tile to a wall tile
class Wall(Tile):
    def __init__(self, x=0, y=0, charDark=GameMap().wallChar, charLight=GameMap().wallChar,
                 name='Wall', dark=2, light=1, blocksMovement=True):
        super().__init__(x, y, charDark, charLight, name, dark, light, blocksMovement)

# General door tile class
class Door(Tile):
    pass

# Sets tile to a horizontal door tile
class HDoor(Door):
    def __init__(self, x=0, y=0, charDark=GameMap().doorCharHorizontal, charLight=GameMap().doorCharHorizontal,
                 name='Door', dark=2, light=1, blocksMovement=True):
        super().__init__(x, y, charDark, charLight, name, dark, light, blocksMovement)

# Sets tile to a vertical door tile
class VDoor(Door):
    def __init__(self, x=0, y=0, charDark=GameMap().doorCharVertical, charLight=GameMap().doorCharVertical,
                 name='Door', dark=2, light=1, blocksMovement=True):
        super().__init__(x, y, charDark, charLight, name, dark, light, blocksMovement)