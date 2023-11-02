import pygame
from .components import *

__all__ = ["Object"]

class Object(pygame.sprite.Sprite):

    __all__ = ["image", "transform"]
    scene = None

    def __init__(self, pos, hitRadius, image):
        super().__init__()
        self.image = image
        self.transform = PolarTransform(pos, hitRadius, image)

    @classmethod
    def instantiate(cls, *args, **kargs):
        cls.scene.objects.add(cls(*args, **kargs))

    def collide(self, other):
        return self.transform.collide(other.transform)

    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)

    def render_debug(self, surface, offset):
        # Rect
        rect = self.transform.rect
        rect.center -= offset
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)
        # Hitbox
        color = (255, 0, 0)
        hitcircle = self.transform.hitcircle
        hitcircle.center -= offset
        pygame.draw.circle(surface, color, hitcircle.center, hitcircle.radius, 1)
        # Position
        pygame.draw.circle(surface, (255, 255, 255), self.transform.position - offset, 2)

    def destroy(self):
        self.scene.objects.remove(self)
