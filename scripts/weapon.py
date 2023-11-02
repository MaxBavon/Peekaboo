from .data import *
from .assets import *
from .constants import *
from .components import *
from .bullet import *
import pygame

__all__ = ["Weapon"]

class Weapon:

    __slots__ = ["name", "damage", "bullet", "animator", "offset", "shootMode", "bullets"]

    def __init__(self, weapontype) -> None:
        data = Data.weapons[weapontype]
        self.name = weapontype
        self.damage = data.damage
        self.bullet = data.bullet
        self.offset = data.offset
        self.animator = Animator(Assets.sprites[data.animation], data.animSpeed)
        self.animator.play("idle")
        self.shootMode = data.shootMode
        self.bullets = []

    def change(self, weapontype):
        data = Data.weapons[weapontype]
        self.name = weapontype
        self.damage = data.damage
        self.animator.switch_animations(Assets.sprites[data.animation], data.animSpeed)
        self.bullet = data.bullet
        self.offset = data.offset
        self.shootMode = data.shootMode

    def shoot(self):
        for bullet in self.shootMode:
            self.bullets.append([bullet["delay"], bullet["offset"], bullet["velocity"]])

    def update(self, player, deltaTime):
        for bullet in self.bullets[:]:
            bullet[0] -= deltaTime
            if bullet[0] <= 0:
                delay, offset, velocity = bullet
                offset = pygame.Vector2(offset).rotate(-player.angle) * UNIT
                velocity = pygame.Vector2(velocity).rotate(-player.angle) * UNIT
                Bullet.instantiate(player.weapon.bullet, player.transform.position + offset, player.velocity, (player.lookingDir + velocity * deltaTime).normalize(), player.angle, delay=delay)
                self.bullets.remove(bullet)