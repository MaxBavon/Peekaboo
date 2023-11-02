import pygame
from time import perf_counter
from .data import *
from .assets import *
from .object import *
from .particle import *

__all__ = ["Renderer"]

class Renderer:

    def __init__(self, game) -> None:
        self.game = game
        self.scene = game.scene
        self.screen = game.window
        self.camera = self.scene.camera
        self.background = Data.config["background"]

        self.environmentRender = True
        self.playerRender = True
        self.objectsRender = True
        self.entitiesRender = True
        self.particlesRender = True
        self.UIRender = True
        self.debugRender = False
        self.debugRenderUI = True

        Particle1D.renderer = self

        self.renderLatency = 0.00
    def __call__(self):
        self.render_all()

    def render_text(self, text, pos, color=(255, 255, 255), font="rubik20"):
        current_font = Assets.fonts[font]
        surf = current_font.render(text, 1, color)
        self.screen.blit(surf, pos)

    def render_text_debug(self, text, y, color=(255, 255, 255), font="rubik20"):
        current_font = Assets.fonts[font]
        surf = current_font.render(text, 1, color)
        self.screen.blit(surf, (self.game.RESOLUTION[0] - current_font.size(text)[0], y))

    def render_glow(self, pos, radius, color=(255,255,255,100)):
        surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        surf.set_alpha(color[3])
        pygame.draw.circle(surf, color, (radius, radius), radius)
        self.screen.blit(surf, pos)

    def render_all(self):
        render_start_time = perf_counter()
        self.screen.fill(self.background)

        if self.scene.state == "playing" or self.scene.state == "pause":
            if self.environmentRender: self.render_environment(self.scene.environment)
            if self.particlesRender: self.render_particles(self.scene.particles)
            if self.objectsRender: self.render_objects(self.scene.objects)
            if self.entitiesRender: self.render_entities(self.scene.entities)
            if self.playerRender: self.render_player(self.scene.player.sprite)

        if self.UIRender: self.render_ui(self.scene.UIManager)
        if self.debugRenderUI: self.render_debug(self.scene)
        if self.scene.fixedUpdate:
            debugSurf = pygame.Surface(self.game.RESOLUTION)
            debugSurf.fill((255, 0, 0))
            debugSurf.set_alpha(25)
            self.screen.blit(debugSurf, (0, 0))

        pygame.display.update()
        self.renderLatency = round((perf_counter() - render_start_time) * 1000, 1)

    def render_environment(self, stars):
        stars.render(self.screen, self.camera.offset)

    def render_objects(self, objects):
        for obj in objects:
            obj.render(self.screen, self.camera.offset, self.camera.rect)
            if self.debugRender:
                obj.render_debug(self.screen, self.camera.offset)

    def render_entities(self, entities):
        for entity in entities:
            entity.render(self.screen, self.camera.offset, self.camera.rect)
            if self.debugRender:
                entity.render_debug(self.screen, self.camera.offset)

    def render_particles(self, particles):
        for particle in particles:
            particle.render(self.screen, self.camera.offset, self.camera.rect)

    def render_player(self, player):
        player.render(self.screen, self.camera.offset, self.camera.rect)
        if self.debugRender:
            player.render_debug(self.screen, self.camera.offset)

    def render_ui(self, UIManager):
        UIManager.render(self.screen)

    def render_debug(self, scene):
        fps_txt = f"FPS : {scene.fps} / MaxFPS : {scene.FPS}"
        dt_txt = f"DeltaTime : {round(scene.deltaTime, 3)}"
        if scene.fixedUpdate:
            color = (0, 255, 0)
            fixed_txt = f"Fixed : True"
        else:
            color = (255, 0, 0)
            fixed_txt = f"Fixed : False"
        update_lat_txt = f"Update : {scene.updateLatency}ms"
        render_lat_txt = f"Render : {self.renderLatency}ms"

        objects_txt = f"O : {len(scene.objects)}"
        entities_txt = f"E : {len(scene.entities)}"
        particles_txt = f"P : {len(scene.particles)}"
        camera_txt = f"Cam : {self.camera.offset}"

        self.render_text_debug(fps_txt, 0)
        self.render_text_debug(dt_txt, 20)
        self.render_text_debug(fixed_txt, 40, color)
        self.render_text_debug(update_lat_txt, 60, color=(255, 100, 100))
        self.render_text_debug(render_lat_txt, 80, color=(100, 100, 255))
        self.render_text_debug(objects_txt, 100)
        self.render_text_debug(entities_txt, 120)
        self.render_text_debug(particles_txt, 140)
        self.render_text_debug(camera_txt, 160)