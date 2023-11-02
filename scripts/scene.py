import sys
import pygame
from time import perf_counter
from random import randint, choice
from .data import *
from .assets import *
from .audio import *
from .camera import *
from .object import *
from .collectable import *
from .entity import *
from .particle import *
from .player import *
from .ship import *
from .stars import *
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
        self.friction = 0.5
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())
        self.camera = Camera(game)

        # ---- Objects ----
        self.objects = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.environment = Stars(self.camera)
        self.particles = list()
        self.player = pygame.sprite.GroupSingle()
        self.delayedEntities = list()
        Object.scene = self
        Collectable.scene = self
        Entity.scene = self
        PolarEntity.scene = self
        Particle1D.scene = self
        ProceduralParticle.scene = self

        self.fixedUpdate = False
        self.environmentUpdate = True
        self.objectsUpdate = True
        self.entitiesUpdate = True
        self.particlesUpdate = True
        self.playerUpdate = True
        self.UIUpdate = True

        # UI
        self.STATES = {"menu" : UIManager(),
                       "playing" : UIManager(),
                       "pause" : UIManager(),
                       "rules" : UIManager(),
                       "settings" : UIManager(),
                       "about" : UIManager(),
                       "inventory" : UIManager(),
                       "game over" : UIManager()}
        self.state = "playing"
        self.UIManager = self.STATES[self.state]
        self.UISetup()

        self.cooldownRate = 0
        self.spawningRate = 10

    def __call__(self):
        self.step()
    
    def start(self):
        Audio.play_music("main_theme")
        self.world_creation()

    def spawn_random_ennemy(self, ennemytype=None):
        ennemy_types = ["fighter", "frigate", "bomber", "imperial", "scout", "torpedo"]
        range_ = 1000
        ennemy_type = choice(ennemy_types)
        if ennemytype:
            ennemy_type = ennemytype
        Ship.instantiate(ennemy_type, self.player.sprite, (randint(-range_, range_), randint(-range_, range_)))

    def world_creation(self):
        self.player.add(Player())
        for _ in range(10):
            self.spawn_random_ennemy()
        self.camera.follow(self.player.sprite)
 
    def UISetup(self):
        self.UIManager.add(Image((100, self.game.RESOLUTION[1] - 20), Assets.ui["burst0"]))

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
        retryBut = Button((self.game.RESOLUTION[0] / 2, 450), (250, 100), Assets.fonts["rubik40"], "Retry", command=self.restart)
        quitBut = Button((self.game.RESOLUTION[0] / 2, 600), (250, 100), Assets.fonts["rubik40"], "Main Menu", command=lambda:self.change_state("menu"))
        self.UIManager.adds(resumeBut, retryBut, quitBut)

        self.change_state("game over")
        gameOverTitle = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik60"], "Game Over")
        resumeBut = Button((self.game.RESOLUTION[0] / 2, 300), (250, 100), Assets.fonts["rubik40"], "Retry", command=self.restart)
        self.UIManager.adds(gameOverTitle, resumeBut)

        self.change_state("menu")
        bgImg = Image((self.game.RESOLUTION[0] / 2, self.game.RESOLUTION[1] / 2), Assets.sprites[Data.config["main_background"]])
        title = Label((self.game.RESOLUTION[0] / 2, 150), Assets.fonts["rubik80"], "SPACE RACER", (52, 147, 224))
        playBut = Button((self.game.RESOLUTION[0] / 2, 300), (300, 80), Assets.fonts["rubik40"], "PLAY", command=lambda:self.change_state("playing"))
        rulesBut = Button((self.game.RESOLUTION[0] / 2, 400), (300, 80), Assets.fonts["rubik40"], "RULES", command=lambda:self.change_state("rules"))
        settingsBut = Button((self.game.RESOLUTION[0] / 2, 500), (300, 80), Assets.fonts["rubik40"], "SETTINGS", command=lambda:self.change_state("settings"))
        aboutBut = Button((self.game.RESOLUTION[0] / 2, 600), (300, 80), Assets.fonts["rubik40"], "ABOUT", command=lambda:self.change_state("about"))
        quitBut = Button((self.game.RESOLUTION[0] / 2, 700), (300, 80), Assets.fonts["rubik40"], "QUIT", command=self.game.close)
        self.UIManager.adds(bgImg, title, playBut, rulesBut, settingsBut, aboutBut, quitBut)

    def change_state(self, newState):
        self.state = newState
        self.UIManager = self.STATES[self.state]

    def update_player(self, player):
        player.update(self.deltaTime, self.mousePos)
        # burst_power = min(int(player.power / 50), 4)
        # UImage = self.UIManager.get(0)
        # UImage.image = Assets.ui[f"burst{burst_power}"]

        for entity in self.entities:
            if player.collide(entity):
                player.on_collision(entity)
                entity.on_collision(player)
        
        objList = self.objects.sprites().copy()
        for obj in objList:
            if obj.transform.collide(player.transform):
                self.objects.remove(obj)
                player.powerup(obj.powerup)

    def update_objects(self, objects):
        for obj in objects:
            obj.update(self.deltaTime)
    
    def entity_collisions(self, entities):
        entityList = entities.sprites().copy()

        for i in range(len(entityList)):
            for j in range(i + 1, len(entityList)):
                entity1 = entityList[i]
                entity2 = entityList[j]
                if entity1.collide(entity2):
                    entity1.on_collision(entity2)
                    entity2.on_collision(entity1)

    def update_entities(self, entities):
        delayedEntities = self.delayedEntities.copy()
        for entity in delayedEntities:
            delayedEntities[delayedEntities.index(entity)][0] -= self.deltaTime
            if entity[0] <= 0:
                self.entities.add(entity[1])
                self.delayedEntities.remove(entity)

        for entity in entities:
            entity.update(self.deltaTime)

        self.entity_collisions(self.entities)

    def update_particles(self, particles):
        for particle in particles:
            particle.update(self.deltaTime)
        
    def update_spawn(self):
        self.cooldownRate += self.deltaTime
        if self.cooldownRate >= self.spawningRate:
            self.spawn_random_ennemy()
            self.cooldownRate = 0
            self.spawningRate -= 0

    def step(self):
        self.ticks += 1
        self.clock.tick(self.FPS)
        currentTime = perf_counter()
        update_start_time = currentTime
        self.deltaTime = currentTime - self.lastFrame if not self.fixedUpdate else 1 / self.DEFAULT_FPS
        self.deltaTime = min(self.deltaTime, 0.1)
        self.lastFrame = currentTime
        self.fps = round(self.clock.get_fps())
        self.mousePos = pygame.Vector2(pygame.mouse.get_pos())

        if self.state == "playing":

            # self.update_spawn()
            if self.environmentUpdate: self.environment.update(self.deltaTime)
            if self.objectsUpdate: self.update_objects(self.objects)
            if self.entitiesUpdate: self.update_entities(self.entities)
            if self.particlesUpdate: self.update_particles(self.particles)
            if self.playerUpdate: self.update_player(self.player.sprite)

            self.camera.update(self.deltaTime)

        if self.UIUpdate: self.UIManager.update(self.mousePos)

        self.updateLatency = round((perf_counter() - update_start_time) * 1000, 1)
    
    def restart(self):
        self.player.sprite.respawn()
        self.environment.empty()
        self.entities.empty()
        self.particles.clear()

        self.world_creation()
        self.spawningRate = 10
        self.camera.follow(self.player.sprite)
        self.change_state("playing")