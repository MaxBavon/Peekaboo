import pygame
from .data import *
from .assets import *
from .components import *
from random import randint


class ProceduralParticle:

    __slots__ = ["position", "velocity", "friction", "lifeSpan", "growthRate", "alpha", "fadeRate", "radius", "color"]
    scene = None

    def __init__(self, particleType, pos, vel, direction, thurst):
        data = Data.particles[particleType]
        self.position = pygame.Vector2(pos) + direction * data["offset"] * UNIT

        if thurst:
            self.velocity = vel + direction * data["speed"] * UNIT
            self.radius = randint(data["radius"][0], data["radius"][1]) * UNIT
        else:
            self.velocity = vel + direction * data["idleSpeed"] * UNIT
            self.radius = randint(data["idleRadius"][0], data["idleRadius"][1]) * UNIT
        
        self.friction = data["friction"]
        self.lifeSpan = data["lifeSpan"]
        self.growthRate = data["growthRate"]
        self.fadeRate = data["fadeRate"]
        self.alpha = 255
        self.color = self.generate_color(data["colors"][0], data["colors"][1])

    @classmethod
    def instantiate(cls, *args, **kwargs):
        cls.scene.particles.append(cls(*args, **kwargs))

    def generate_color(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = randint(min(r1, r2), max(r1, r2))
        g = randint(min(g1, g2), max(g1, g2))
        b = randint(min(b1, b2), max(b1, b2))
        return [r, g, b]

    def update(self, deltaTime):
        self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), self.friction * deltaTime)
        self.position += self.velocity * deltaTime
        self.lifeSpan -= deltaTime
        self.radius += self.growthRate * deltaTime
        if self.growthRate < 0: self.radius = max(self.radius, 0)
        self.color[0] += self.fadeRate * deltaTime
        self.color[1] += self.fadeRate * deltaTime
        self.color[2] += self.fadeRate * deltaTime
        self.color[0] = min(max(self.color[0], 0), 255)
        self.color[1] = min(max(self.color[1], 0), 255)
        self.color[2] = min(max(self.color[2], 0), 255)

        if self.lifeSpan <= 0:
            self.destroy()
        
    def glow_circle(self, rad):
        color = [int(self.color[0]), int(self.color[1]), int(self.color[2])]

        surf = pygame.Surface((rad * 2, rad * 2))
        try:
            pygame.draw.circle(surf, color, (rad, rad), rad)
        except ValueError:
            print(color)
        surf.set_colorkey((0, 0, 0))
        return surf

    def render(self, surface, offset, screen):
        if screen.collidepoint(self.position):
            rad = int(self.radius) + int(self.radius * 0.4)
            surf = self.glow_circle(rad)
            rad2 = int(self.radius)
            surf2 = self.glow_circle(rad2)

            surface.blit(surf, self.position - offset - pygame.Vector2(rad, rad), special_flags=pygame.BLEND_RGB_MAX)
            surface.blit(surf2, self.position - offset - pygame.Vector2(rad2, rad2), special_flags=pygame.BLEND_RGB_MAX)

    def destroy(self):
        self.scene.particles.remove(self)


class Particle1D:

    __slots__ = ["position", "image", "imgSize", "animator", "glowColor", "alpha"]
    scene = None
    renderer = None

    def __init__(self, particleType, pos) -> None:
        data = Data.particles[particleType]
        self.position = pygame.Vector2(pos)

        self.animator = Animator1D(Assets.sprites[data["animation"]], data["animSpeed"])
        self.animator.play()
        self.image = self.animator.animate(0)
        self.imgSize = pygame.Vector2(self.image.get_width() / 2, self.image.get_height() / 2)
        self.glowColor = data["glowColor"]
        self.alpha = data["glowColor"][3]

    @classmethod
    def instantiate(cls, *args, **kwargs):
        cls.scene.particles.append(cls(*args, **kwargs))

    def update(self, deltaTime):
        if self.animator.anim_end():
            self.destroy()

        self.image = self.animator.animate(deltaTime)
        self.alpha = self.glowColor[-1] - int(self.animator.frame * (self.glowColor[-1] / self.animator.animLength))

    def render(self, surface, offset, screen):
        if screen.collidepoint(self.position):
            self.renderer.render_glow(self.position - offset - self.imgSize, self.imgSize.x, self.glowColor[:-1] + [self.alpha])
            surface.blit(self.image, self.position - offset - self.imgSize)

    def destroy(self):
        self.scene.particles.remove(self)