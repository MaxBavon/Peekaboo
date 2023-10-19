import pygame
from .sprite import *
from random import randint, uniform

class Particle:

    __all__ = ["position", "image"]
    scene = None

    def __init__(self, pos, color):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(randint(-250, 250), randint(-300, 500))
        self.color = color
        self.bounciness = uniform(0.5, 0.9)
        self.lifeSpan = randint(2, 10)

    def __str__(self):
        return f"Sprite <Pos ({self.position.x}, {self.position.y})>"

    @classmethod
    def instantiate(cls, pos, color):
        cls.scene.particles.append(cls(pos, color))

    def update(self, deltaTime):
        self.lifeSpan -= deltaTime
        
        # X Axis
        self.position.x += self.velocity.x * deltaTime

        if self.position.x < 0:
            self.position.x = 0
            self.velocity.x *= -self.bounciness
        if self.position.x > self.scene.game.RESOLUTION[0]:
            self.position.x = self.scene.game.RESOLUTION[0]
            self.velocity.x *= -self.bounciness
        
        # Y Axis
        self.velocity.y += 981 * deltaTime
        self.position.y += self.velocity.y * deltaTime
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -self.bounciness
        if self.position.y > self.scene.game.RESOLUTION[1]:
            self.position.y = self.scene.game.RESOLUTION[1]
            self.velocity.y *= -self.bounciness
        
        if self.lifeSpan <= 0:
            self.destroy()

    def render(self, surface, offset, screen):
        if screen.collidepoint(self.position):
            pygame.gfxdraw.pixel(surface, int(self.position.x - offset.x), int(self.position.y - offset.y), self.color)

    def destroy(self):
        self.scene.particles.remove(self)