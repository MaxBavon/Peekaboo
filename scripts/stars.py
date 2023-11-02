import pygame
from random import randint
from .assets import *

__all__ = ["Stars"]

class Stars:

    __slots__ = ["camera", "capacity", "galaxy_cap", "stars", "galaxys", "timer", "rate"]

    def __init__(self, cam):
        self.camera = cam
        self.capacity = 50
        self.galaxy_cap = 250
        self.stars = []
        self.galaxys = []
        self.timer = 0
        self.rate = 0

    def generate(self):
        posX = randint(self.camera.rect.left, self.camera.rect.right)
        posY = randint(self.camera.rect.top, self.camera.rect.bottom)
        surf = Assets.sprites[f"star{randint(1, 4)}"].copy()
        surf.set_alpha(randint(50, 200))
        self.stars.append((pygame.Vector2(posX, posY), surf))
    
    def generate_galaxy(self):
        posX = randint(self.camera.rect.left, self.camera.rect.right)
        posY = randint(self.camera.rect.top, self.camera.rect.bottom)
        color = [randint(50, 255)] * 3
        self.galaxys.append((pygame.Vector2(posX, posY), color))

    def update(self, deltaTime):
        self.timer += deltaTime
        if self.timer >= self.rate:
            if len(self.stars) < self.capacity:
                self.generate()
                self.timer = 0
            if len(self.galaxys) < self.galaxy_cap:
                self.generate_galaxy()
                self.timer = 0

        for star in self.stars.copy():
            if not self.camera.rect.collidepoint(star[0]):
                self.stars.remove(star)
        
        for galaxy in self.galaxys:
            if not self.camera.rect.collidepoint(galaxy[0]):
                self.galaxys.remove(galaxy)

    def render(self, surface, offset):
        for star in self.stars:
            surface.blit(star[1], star[0] - offset)
        for galaxy in self.galaxys:
            pygame.gfxdraw.pixel(surface, int(galaxy[0].x - offset.x), int(galaxy[0].y - offset.y), galaxy[1])

    def empty(self):
        self.stars.clear()
        self.galaxys.clear()