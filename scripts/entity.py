import pygame
from abc import abstractmethod
from .components import *
from .data import *
from .assets import *

__all__ = ["Entity", "PolarEntity"]


class Entity(pygame.sprite.Sprite):

    scene = None

    __slots__ = ["image", "transform", "velocity", "collisions", "grounded"]

    def __init__(self, entityType):
        super().__init__()
        # Physics
        data = Data.entities[entityType]
        self.image = Assets.sprites[data["sprite"]]
        self.transform = Transform(data["position"], self.image, data["hitbox"])
        self.velocity = pygame.Vector2(0)

        self.collisions = {"left" : False, "right" : False, "top" : False, "bottom" : False}
        self.grounded = False

    @classmethod
    def instantiate(cls, pos, img):
        cls.scene.entities.add(cls(pos, img))

    def horizontal_collision(self, level):
        if self.transform.left < level.border.left: # Level Border
            self.transform.left = level.border.left
        if self.transform.right > level.border.right:
            self.transform.right = level.border.right 

        for tile in level.collide(self): # TileMap
            if self.velocity.x > 0:
                self.transform.right = tile.left
                self.collisions["right"] = True
            if self.velocity.x < 0:
                self.transform.left = tile.right
                self.collisions["left"] = True

    def vertical_collision(self, level):
        if self.transform.top < level.border.top: # Level Border
            self.transform.top = level.border.top
            self.velocity.y = 0
        if self.transform.bottom > level.border.bottom:
            self.transform.bottom = level.border.bottom
            self.velocity.y = 0

        for tile in level.collide(self): # TileMap
            if self.velocity.y > 0:
                self.transform.bottom = tile.top
                self.velocity.y = 0
                self.collisions["bottom"] = True
            elif self.velocity.y < 0:
                self.transform.top = tile.bottom
                self.velocity.y = 0
                self.collisions["top"] = True

    def update(self, deltaTime, gravityScale):
        self.collisions = {"left" : False, "right" : False, "top" : False, "bottom" : False}
        # X Axis
        self.transform.position.x += self.velocity.x * deltaTime
        self.horizontal_collision(self.scene.level)

        # Y Axis
        self.velocity.y += gravityScale * deltaTime
        self.transform.position.y += self.velocity.y * deltaTime
        self.vertical_collision(self.scene.level)

        self.grounded = self.velocity.y == 0

    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)
 
    def render_debug(self, surface, offset):
        # Rect
        rect = self.transform.rect
        rect.center -= offset
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)
        # Hitbox
        color = (0, 255, 0) if self.grounded else (255, 0, 0)
        hitbox = self.transform.hitbox
        hitbox.center -= offset
        pygame.draw.rect(surface, color, hitbox, 1)
        # Position
        pygame.draw.circle(surface, (255, 255, 255), self.transform.position - offset, 2)

    def collide(self, entity):
        return self.transform.collide(entity.transform)

    def destroy(self):
        self.on_death()
        self.scene.entities.kill(self)

    @abstractmethod
    def on_collision(self, entity):
        pass

    @abstractmethod
    def on_death(self):
        pass


class PolarEntity(pygame.sprite.Sprite):

    scene = None

    # __slots__ = ["image", "transform", "velocity", "collisions", "grounded"]

    def __init__(self, entityType, pos=None):
        super().__init__()
        # Physics
        data = Data.entities[entityType]
        self.image = Assets.sprites[data.sprite]
        self.sprite = self.image.copy()
        if pos:
            self.transform = PolarTransform(pos, data.hitRadius, self.image)
        else:
            self.transform = PolarTransform(data.position, data.hitRadius, self.image)
        self.velocity = pygame.Vector2(0)
        self.movingSpeed = data.movingSpeed
        self.angle = 0
        self.friction = 0.2

    @classmethod
    def instantiate(cls, *args, **kwargs):
        cls.scene.entities.add(cls(*args, **kwargs))

    def horizontal_collision(self, level):
        pass

    def vertical_collision(self, level):
        pass

    def update(self, deltaTime):
        self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), self.friction * deltaTime)
        # X Axis
        self.transform.position.x += self.velocity.x * deltaTime
        self.horizontal_collision(self.scene.level)
        # Y Axis
        self.transform.position.y += self.velocity.y * deltaTime
        self.vertical_collision(self.scene.level)
        
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.transform.update(self.image)

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

    def collide(self, entity):
        return self.transform.collide(entity.transform)

    def destroy(self):
        self.on_death()
        self.scene.entities.kill(self)

    @abstractmethod
    def on_collision(self, entity):
        pass

    @abstractmethod
    def on_death(self):
        pass