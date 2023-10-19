import pygame

__all__ = ["Sprite"]

class Sprite(pygame.sprite.Sprite):

    __all__ = ["position", "image"]
    scene = None

    def __init__(self, pos, img):
        super().__init__()
        self.position = pygame.Vector2(pos)
        self.image = img

    def __str__(self):
        return f"Sprite <Pos ({self.position.x}, {self.position.y})>"

    @classmethod
    def instantiate(cls, pos, img):
        cls.scene.sprites.add(cls(pos, img))

    def render(self, surface, offset, screen):
        if pygame.Rect(self.position, self.image.get_size()).colliderect(screen):
            surface.blit(self.image, self.position - offset)

    def destroy(self):
        self.scene.sprites.kill(self)