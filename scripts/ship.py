import pygame
from .entity import *
from .data import *
from .assets import *
from .components import *
from math import atan2, degrees


class Ship(PolarEntity):

    def __init__(self, shipType, target, pos=None):
        data = Data.entities[shipType]
        self.shipType = shipType
        self.target = target
        print("Type : ", self.shipType)
        super().__init__(shipType, pos)

        self.animator = Animator(Assets.sprites[data.animation], 10)
        self.animator.play("shooting")

        self.engineAnimator = Animator(Assets.sprites[data.burst], 10)
        self.engineAnimator.play("idle")
        self.powering = False

        self.create_sprite(0)

    def create_sprite(self, deltaTime):
        self.sprite = self.engineAnimator.animate(deltaTime)
        self.sprite.blit(self.animator.animate(deltaTime), (0, 0))

    def animate(self, deltaTime):
        self.create_sprite(deltaTime)
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.transform.update(self.image)

    def physics_update(self, deltaTime):
        self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), self.friction * deltaTime)
        # X Axis
        self.transform.position.x += self.velocity.x * deltaTime
        self.horizontal_collision(self.scene.level)
        # Y Axis
        self.transform.position.y += self.velocity.y * deltaTime
        self.vertical_collision(self.scene.level)

    def update(self, deltaTime):
        movingDir = self.target.transform.position - self.transform.position
        self.velocity =  movingDir.normalize() * self.movingSpeed

        lookingDir = (self.transform.position + self.velocity - self.transform.position)
        self.angle = int(degrees(atan2(lookingDir.x , lookingDir.y))) + 180
        
        self.physics_update(deltaTime)
        self.animate(deltaTime)
    
    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)