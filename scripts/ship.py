import pygame
from .entity import *
from .data import *
from .assets import *
from .audio import *
from .components import *
from .collectable import *
from .bullet import *
from math import atan2, degrees
from random import randint, choice


class Ship(PolarEntity):

    __slots__ = ["target", "type", "image", "transform", "velocity", "speed", "angle", "animator", "trail", "powering",
                 "health", "alive", "fireRate", "cooldown", "bullet", "movingDir", "distance_to_target", "trackingDist", "shootingDist", "loot"]

    def __init__(self, shipType, target, pos=None):
        data = Data.entities[shipType]
        self.target = target

        super().__init__(shipType, pos)

        self.animator = Animator(Assets.sprites[data.animation], 10)
        self.animator.play("powering")
        self.trail = data.trail

        self.powering = False

        self.health = data.health
        self.alive = True

        self.fireRate = data.fireRate
        self.cooldown = 0
        self.bullet = data.bullet

        self.movingDir = pygame.Vector2(0, 0)
        self.distance_to_target = 0
        self.trackingDist = data.trackingDist * UNIT
        self.shootingDist = data.shootingDist * UNIT
        self.loot = data.loot

    def update(self, deltaTime):
        self.alive = self.health > 0
        if self.alive:
            self.movingDir = (self.target.transform.position - self.transform.position)
            self.distance_to_target = self.movingDir.magnitude()
            self.movingDir = self.movingDir.normalize() if self.movingDir else pygame.Vector2(0, 0)

            if self.distance_to_target > self.trackingDist:
                self.velocity += self.movingDir * self.speed
            self.angle = int(degrees(atan2(self.movingDir.x , self.movingDir.y))) + 180

            self.cooldown += deltaTime

            if self.distance_to_target < self.shootingDist:
                if self.cooldown >= self.fireRate:
                    self.shoot()
        else:
            if self.animator.anim != "destroyed":
                self.animator.play("destroyed")
                Audio.play_sfx("explosion")
                self.transform.radius = 0
            else:
                if self.animator.anim_end():
                    self.destroy()

        self.sprite = self.animator.animate(deltaTime)
        super().update(deltaTime)

    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)

    def on_collision(self, entity):
        if entity.type == "bullet" and "ennemy" in entity.collisions:
            self.health -= entity.damage
        elif entity.type == "ennemy":
            self.ellastic_collision(entity)
        elif entity.type == "player":
           self.health = 0

    def shoot(self):
        self.cooldown = 0
        Bullet.instantiate(self.bullet, self.transform.position, self.velocity, self.movingDir, self.angle)
    
    def on_death(self):
        chance = randint(1, self.loot)
        if chance == 1:
            collectable_list = list(Data.objects.keys())
            collectable = choice(collectable_list)
            Collectable.instantiate(collectable, self.transform.position)
