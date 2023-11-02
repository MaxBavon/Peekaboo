import pygame
from .entity import *
from .data import *
from .assets import *
from .audio import *
from .components import *
from .particle import *


class Bullet(PolarEntity):
    
    def __init__(self, bulletType, pos, vel, direction, angle):
        data = Data.bullets[bulletType]
        super().__init__(bulletType, pos)
        self.velocity = vel + direction * data.speed * UNIT
        self.lifeSpan = data.lifeSpan
        self.damage = data.damage

        self.animator = Animator1D(Assets.sprites[data.animation], data.animSpeed)

        rotatedAnim = self.animator.animation.copy()
        for i in range(self.animator.animLength):
            rotatedAnim[i] = pygame.transform.rotate(rotatedAnim[i], angle)
        self.animator.switch_animation(rotatedAnim, data.animSpeed)
        self.animator.play()
        self.image = self.animator.animate(0)
        self.transform.update(self.image)

        self.bulletHit = data.bulletHit
        self.resistance = data.resistance
        self.shield = self.resistance
        self.collisions = data.collisions

    def update(self, deltaTime):
        self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), self.scene.friction * deltaTime)
        self.transform.position += self.velocity * deltaTime
        
        if self.velocity.magnitude_squared() < self.lifeSpan ** 2:
            self.destroy()

        self.image = self.animator.animate(deltaTime)
    
    def on_collision(self, entity):
        if entity.type in self.collisions:
            self.destroy()
        elif (entity.type == "bullet" and entity.collisions != self.collisions):
            self.shield -= entity.resistance
            if self.shield <= 0:
                self.destroy()

    def on_death(self):
        Particle1D.instantiate(self.bulletHit, self.transform.position - pygame.Vector2(self.sprite.get_size()) / 2)
        Audio.play_sfx("little_explosion")