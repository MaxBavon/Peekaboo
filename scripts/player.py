import pygame
from .entity import *
from .data import *
from .assets import *
from .components import *
from math import atan2, degrees


class Player(PolarEntity):

    def __init__(self):
        data = Data.entities["player"]
        super().__init__("player")

        self.animator = Animator(Assets.sprites[data.animation], 10)
        self.animator.play("idle")

        self.engineSprite = Assets.sprites[data.engine]
        self.burstAnimator = Animator(Assets.sprites[data.burst], 10)
        self.burstAnimator.play("powering")
        self.powering = False

        self.weaponAnimator = Animator(Assets.sprites[data.weapon], 10)
        self.weaponAnimator.play("idle")

        self.create_sprite(0)

    def create_sprite(self, deltaTime):
        self.sprite = self.burstAnimator.animate(deltaTime)
        self.sprite.blit(self.engineSprite, (0, 0))
        self.sprite.blit(self.weaponAnimator.animate(deltaTime), (0, 0))
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

    def update(self, deltaTime, mousePos):
        keys = self.scene.game.keyboard

        lookingDir = self.scene.camera.screen_to_world_point(mousePos) -  self.transform.position
        lookingDir = lookingDir.normalize()

        self.powering = False
        if keys[pygame.K_SPACE]:
            self.velocity += lookingDir * self.movingSpeed
            self.powering = True

        self.angle = int(degrees(atan2(lookingDir.x , lookingDir.y))) + 180

        self.physics_update(deltaTime)
        self.animate(deltaTime)
    
    def render(self, surface, offset, screen):
        if self.transform.rect.colliderect(screen):
            surface.blit(self.image, self.transform.imgPosition - offset)

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