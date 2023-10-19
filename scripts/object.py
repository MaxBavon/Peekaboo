import pygame
from .sprite import *


class Object(Sprite):

    __all__ = ["position", "image", "hitbox", "size"]
    scene = None

    def __init__(self, pos, img):
        super().__init__(pos, img)
        self.hitbox = img.get_rect(center=self.position)
        self.size = pygame.Vector2(img.get_size())
    
    def __str__(self):
        return f"Sprite <Pos ({self.position.x}, {self.position.y})>"
    
    @classmethod
    def instantiate(cls, pos, color):
        cls.scene.objects.add(cls(pos, color))

    def collide(self, other):
        return self.hitbox.colliderect(other.hitbox)

    def destroy(self):
        self.scene.particles.kill(self)
