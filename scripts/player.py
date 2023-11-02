import pygame
from .entity import *
from .data import *
from .assets import *
from .audio import *
from .components import *
from .weapon import *
from .engine import *
from .particle import *
from .bullet import *
from math import atan2, degrees


class Player(PolarEntity):

    def __init__(self):
        data = Data.entities["player"]
        super().__init__("player")

        self.animator = Animator(Assets.sprites[data.animation], data.animSpeed)
        self.animator.play("idle")

        self.weapon = Weapon(data.weapon)
        self.engine = Engine(data.engine)
        self.power = 0
        self.powering = False
        self.shooted = False
        self.shooting = False
        self.lookingDir = pygame.Vector2(0, 0)

        self.create_sprite(0)
        self.health = data.health

    def create_sprite(self, deltaTime):
        self.sprite = self.engine.animator.animate(deltaTime)
        self.sprite.blit(self.weapon.animator.animate(deltaTime), self.weapon.offset)
        self.sprite.blit(self.animator.animate(deltaTime), (0, 0))

    def animate(self, deltaTime):
        self.engine.animator.play("powering") if self.powering else self.engine.animator.play("idle")
        self.weapon.animator.queue("shooting") if self.shooted else self.weapon.animator.queue("idle")
        self.create_sprite(deltaTime)
        self.image = pygame.transform.rotate(self.sprite, self.angle)
        self.transform.update(self.image)
    
    def inputs(self):
        keyboard = self.scene.game.keyboard
        self.powering = keyboard[self.scene.game.keys["power"]]

        mouse = self.scene.game.mouse
        self.shooting = mouse[self.scene.game.keys["shoot"]]

    def update(self, deltaTime, mousePos):
        if self.health <= 0:
            self.on_death()

        self.inputs()
        
        self.lookingDir = (self.scene.camera.screen_to_world_point(mousePos) -  self.transform.position).normalize()
        self.angle = int(degrees(atan2(self.lookingDir.x , self.lookingDir.y))) + 180

        if self.powering:
            self.velocity += self.lookingDir * self.engine.thrust

        if not self.powering and self.velocity.magnitude_squared() < 100:
            self.velocity.update(0, 0)
        else:
            self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), self.scene.friction * deltaTime)
        self.transform.position += self.velocity * deltaTime

        if self.shooting:
            self.shoot()

        self.power = self.velocity.magnitude() / self.engine.thrust
        ProceduralParticle.instantiate(self.engine.particle, self.transform.position, self.velocity, -self.lookingDir, thurst=self.powering)
        self.animate(deltaTime)
        
        self.shooted = False
        self.weapon.update(self, deltaTime)

    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)

        self.scene.game.renderer.render_text(str(self.health), (0, 0))

    def render_debug(self, surface, offset):
        super().render_debug(surface, offset)

        pos_txt = f"Pos : {self.transform.position}"
        vel_txt = f"Vel: {self.velocity}"
        angle_txt = f"Angle: {self.angle}"
        frame_txt = f"Frame: {self.animator.frame}"
        self.scene.game.renderer.render_text(pos_txt, (0, 0))
        self.scene.game.renderer.render_text(vel_txt, (0, 20))
        self.scene.game.renderer.render_text(angle_txt, (0, 40))
        self.scene.game.renderer.render_text(frame_txt, (0, 60))

    def shoot(self):
        if self.weapon.animator.anim == "idle":
            self.shooted = True
            self.weapon.shoot()
    
    def powerup(self, powerup):
        if "engine" in powerup:
            self.engine.change(powerup)
        if "weapon" in powerup:
            self.weapon.change(powerup)

    def on_collision(self, entity):
        if entity.type == "bullet" and "player" in entity.collisions:
            self.health -= entity.damage
        elif entity.type == "ennemy":
            self.health -= 1
    
    def on_death(self):
        self.scene.change_state("game over")
    
    def respawn(self):
        data = Data.entities["player"]

        self.transform.position.update(data.position)
        self.velocity.update(0, 0)
        self.angle = 0
        self.power = 0
        self.powering = False
        self.lookingDir = pygame.Vector2(0, 0)

        self.create_sprite(0)
        self.health = data.health