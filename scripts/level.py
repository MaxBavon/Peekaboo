import pygame
import csv
import os

from .data import *
from .assets import *


class Level:

    def __init__(self):
        self.tilemap = []
        self.tileset = []
        
        self.parallalax_factor = 0.2
        self.background = None

        self.level = 0

        self.width = 0
        self.height = 0
        self.border = pygame.Rect(0, 0, 0, 0)

    def load_tilemap(self, lvl):
        path = f"data/level{lvl}/"
        self.tilemap = list(csv.reader(open(path + f"level{lvl}_Collisions.csv")))

    def load_tileset(self, lvl):
        self.tileset = Assets.tiles[Data.levels[f"level{lvl}"]["name"]]

    def load(self, lvl):
        self.level = lvl
        self.load_tilemap(lvl)
        self.load_tileset(lvl)

        self.width = len(self.tilemap[0])
        self.height = len(self.tilemap)
        self.border = pygame.Rect(0, 0, self.width * TILE_SIZE, self.height * TILE_SIZE)

    def collide(self, entity):
        collisions = []
        X, Y = int(entity.transform.centerx // TILE_SIZE), int(entity.transform.centery // TILE_SIZE)
        detection_range = 2
        for y in range(Y - detection_range, Y + detection_range + 1):
            for x in range(X - detection_range, X + detection_range + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    ID = int(self.tilemap[y][x])
                    if ID != -1:
                        tile = pygame.Rect((x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                        if entity.transform.colliderect(tile):
                            collisions.append(tile)
        return collisions

    def collide_rect(self, entity_rect):
        collisions = []
        X, Y = entity_rect.x // TILE_SIZE, entity_rect.y // TILE_SIZE
        detection_range = 2
        for y in range(Y - detection_range, Y + detection_range + 1):
            for x in range(X - detection_range, X + detection_range + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    ID = int(self.tilemap[y][x])
                    if ID != -1:
                        tile = pygame.Rect((x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                        if entity_rect.colliderect(tile):
                            collisions.append(tile)
        return collisions

    def update(self, deltaTime):
        pass

    def render(self, surface, offset, screen):
        topleft = screen.topleft
        X, Y = topleft[0] // TILE_SIZE, topleft[1] // TILE_SIZE

        for y in range(Y, Y + screen.height // TILE_SIZE + 2):
            for x in range(X, X + screen.width // TILE_SIZE + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    ID = int(self.tilemap[y][x])
                    if ID != -1:
                        tile_pos = pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)
                        surface.blit(self.tileset[ID], tile_pos - offset)

    def render_debug(self, surface, offset, screen):
        topleft = screen.topleft
        X, Y = topleft[0] // TILE_SIZE, topleft[1] // TILE_SIZE

        for y in range(Y, Y + screen.height // TILE_SIZE + 2):
            for x in range(X, X + screen.width // TILE_SIZE + 1):
                if (x >= 0 and x < self.width) and (y >= 0 and y < self.height):
                    ID = int(self.tilemap[y][x])
                    if ID != -1:
                        pygame.draw.rect(surface, (0,255,0), (x * TILE_SIZE - offset.x, y * TILE_SIZE - offset.y, TILE_SIZE, TILE_SIZE), 1)

        border = pygame.Rect(self.border.x - offset.x, self.border.y - offset.y, self.border.w, self.border.h)
        pygame.draw.rect(surface, (255,0,0), border, 2)