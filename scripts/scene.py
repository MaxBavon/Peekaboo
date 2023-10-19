import pygame
from time import perf_counter
from random import randint
from .data import *
from .assets import *
from .camera import *
from .level import *
from .sprite import *
from .object import *
from .entity import *
from .particle import *
from .player import *
from .ship import *
from .ui import *


__all__ = ["Scene"]


class Scene:

    def __init__(self, game) -> None:
        self.game = game
        self.clock = pygame.time.Clock()
        self.FPS = Data.config["fps"]
        self.DEFAULT_FPS = Data.config["fps"]
        self.fps = 0
        self.ticks = 0
        self.lastFrame = perf_counter()
        self.deltaTime = 0.00
        self.friction = 0.2
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())
        self.camera = Camera(game)

        # ---- Objects ----
        self.level = Level()
        self.sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.particles = list()
        self.player = pygame.sprite.GroupSingle()
        Sprite.scene = self
        Object.scene = self
        Entity.scene = self
        PolarEntity.scene = self
        Particle.scene = self

        self.fixedUpdate = False
        self.spritesUpdate = True
        self.objectsUpdate = True
        self.entitiesUpdate = True
        self.particlesUpdate = True
        self.playerUpdate = True
        self.UIUpdate = True

        self.world_creation()
        self.camera.follow(self.player.sprite)

        # UI
        self.STATES = {"menu" : UIManager(),
                       "playing" : UIManager(),
                       "pause" : UIManager(),
                       "rules" : UIManager(),
                       "settings" : UIManager(),
                       "about" : UIManager(),
                       "inventory" : UIManager()}
        self.state = "playing"
        self.UIManager = self.STATES[self.state]
        self.UISetup()

    def __call__(self):
        self.step()

    def world_creation(self):
        self.level.load(1)
        self.player.add(Player())
        for i in range(100):
            Ship.instantiate("fighter", self.player.sprite, (i*100, 200))

    def UISetup(self):
        self.change_state("settings")
        soundOffBut = ButtonImg((self.game.RESOLUTION[0] / 2, 300), Assets.ui["volume_off"])
        soundOnBut = ButtonImg((self.game.RESOLUTION[0] / 2, 450), Assets.ui["volume_on"])
        settingsTitle = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik60"], "Settings")
        self.UIManager.adds(soundOffBut, soundOnBut, settingsTitle)

        self.change_state("rules")
        rulesTitle = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik60"], "Rules")
        self.UIManager.adds(rulesTitle)

        self.change_state("about")
        aboutTitle = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik60"], "About")
        self.UIManager.adds(aboutTitle)

        self.change_state("pause")
        resumeBut = Button((self.game.RESOLUTION[0] / 2, 300), (250, 100), Assets.fonts["rubik40"], "Resume", command=lambda:self.change_state("playing"))
        retryBut = Button((self.game.RESOLUTION[0] / 2, 450), (250, 100), Assets.fonts["rubik40"], "Retry")
        quitBut = Button((self.game.RESOLUTION[0] / 2, 600), (250, 100), Assets.fonts["rubik40"], "Main Menu", command=lambda:self.change_state("menu"))
        self.UIManager.adds(resumeBut, retryBut, quitBut)

        self.change_state("menu")
        bgImg = Image((self.game.RESOLUTION[0] / 2, self.game.RESOLUTION[1] / 2), Assets.sprites["forest_bg_big"])
        title = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik80"], "SPACE RACER")
        playBut = Button((self.game.RESOLUTION[0] / 2, 300), (300, 80), Assets.fonts["rubik40"], "PLAY", command=lambda:self.change_state("playing"))
        rulesBut = Button((self.game.RESOLUTION[0] / 2, 400), (300, 80), Assets.fonts["rubik40"], "RULES", command=lambda:self.change_state("rules"))
        settingsBut = Button((self.game.RESOLUTION[0] / 2, 500), (300, 80), Assets.fonts["rubik40"], "SETTINGS", command=lambda:self.change_state("settings"))
        aboutBut = Button((self.game.RESOLUTION[0] / 2, 600), (300, 80), Assets.fonts["rubik40"], "ABOUT", command=lambda:self.change_state("about"))
        quitBut = Button((self.game.RESOLUTION[0] / 2, 700), (300, 80), Assets.fonts["rubik40"], "QUIT", command=self.game.close)
        self.UIManager.adds(bgImg, title, playBut, rulesBut, settingsBut, aboutBut, quitBut)

    def change_state(self, newState):
        self.state = newState
        self.UIManager = self.STATES[self.state]

    def instantiate_particle(self, pos):
        col = randint(128, 255), randint(128, 255), randint(128, 255)
        self.particles.append(Particle(pos, col))

    def update_sprites(self, sprites):
        for sprite in sprites:
            sprite.update(self.deltaTime)

    def update_objects(self, objects):
        for obj in objects:
            obj.update(self.deltaTime)

    def update_entities(self, entities):
        for entity in entities:
            entity.update(self.deltaTime)

    def update_particles(self, particles):
        for particle in particles:
            particle.update(self.deltaTime)

    def step(self):
        self.ticks += 1
        self.clock.tick(self.FPS)
        currentTime = perf_counter()
        update_start_time = currentTime
        self.deltaTime = currentTime - self.lastFrame if not self.fixedUpdate else 1 / self.DEFAULT_FPS
        self.lastFrame = currentTime
        self.fps = round(self.clock.get_fps())
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        if self.state == "playing":
            if self.playerUpdate: self.player.sprite.update(self.deltaTime, self.mousePos)
            if self.spritesUpdate: self.update_sprites(self.sprites)
            if self.objectsUpdate: self.update_objects(self.objects)
            if self.entitiesUpdate: self.update_entities(self.entities)
            if self.particlesUpdate: self.update_particles(self.particles)
            self.camera.update(self.deltaTime)

        if self.UIUpdate: self.UIManager.update(self.mousePos)

        self.updateLatency = round((perf_counter() - update_start_time) * 1000, 1)
    
    def kill_particle(self, particle):
        self.particles.remove(particle)
