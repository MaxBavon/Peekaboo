from pygame.locals import *
import pygame.gfxdraw
import pygame

from .debugger import *
from .data import *
from .assets import *
from .audio import *
from .renderer import *
from .scene import *



class Game:

    def __init__(self):
        self.debugger = Debugger()

        # _____ Application Configurations  ____
        pygame.init()
        pygame.mixer.init()

        self.debugger.prints_out(Data.load())

        self.RESOLUTION = Data.config["resolution"]
        self.fullscreen = Data.config["fullscreen"]
        self.vsync = Data.config["vsync"]
        fullscreen = pygame.FULLSCREEN if self.fullscreen else 0
        if fullscreen:
            self.RESOLUTION = pygame.display.get_desktop_sizes()[0]
        self.window = pygame.display.set_mode(self.RESOLUTION, fullscreen, vsync=self.vsync)

        self.loading()

        pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        self.keys = {}
        for (func, name), (name2, key) in zip(Data.config["keys"].items(), Data.config["key_mapping"].items()):
            self.keys[func] = key
        Data.config["keys"]
        self.mouse = pygame.mouse.get_pressed()
        self.keyboard = pygame.key.get_pressed()
        self.events_ = pygame.event.get()

        self.scene = Scene(self)
        self.renderer = Renderer(self)

    def launch(self):
        self.run()
    
    def loading(self):
        loading_img = pygame.image.load("assets/ui/" + Data.config["loading"]).convert()
        loading_img = pygame.transform.scale(loading_img, self.RESOLUTION)
        self.window.blit(loading_img, (0, 0))
        pygame.display.update()
        Assets.load()

        img = Assets.sprites[Data.config["main_background"]]
        Assets.sprites[Data.config["main_background"]] = pygame.transform.scale(img, self.RESOLUTION)
        pygame.display.set_caption(Data.config["name"])
        pygame.display.set_icon(Assets.ui[Data.config["icon"]])

        Audio.load()

    def run(self):
        self.running = True
        self.scene.start()
        while self.running:
            self.events()
            self.scene()
            self.renderer()

    def events(self):
        self.mouse = pygame.mouse.get_pressed()
        self.keyboard = pygame.key.get_pressed()
        self.events_ = pygame.event.get()

        if self.keyboard[K_F6]: self.scene.FPS -= 1
        if self.keyboard[K_F7]: self.scene.FPS += 1
        # --- Touch Keys ---
        for event in self.events_:
            if event.type == QUIT:
               self.close()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.scene.state == "playing":
                        self.scene.change_state("pause")
                    elif self.scene.state == "pause":
                        self.scene.change_state("playing")
                    elif self.scene.state == "menu":
                        self.close()
                    else:
                        self.scene.change_state("menu")
                if event.key == K_F3: self.renderer.debugRender = not self.renderer.debugRender
                if event.key == K_F4: self.scene.fixedUpdate = not self.scene.fixedUpdate
                if event.key == K_F5: self.renderer.debugRenderUI = not self.renderer.debugRenderUI
                if event.key == K_F8: self.scene.FPS = Data.config["fps"]
                if event.key == K_1: self.scene.player.sprite.engine.change("base_engine")
                if event.key == K_2: self.scene.player.sprite.engine.change("burst_engine")
                if event.key == K_3: self.scene.player.sprite.engine.change("supercharged_engine")
                if event.key == K_4: self.scene.player.sprite.engine.change("big_engine")
                if event.key == K_5: self.scene.player.sprite.weapon.change("base_weapon")
                if event.key == K_6: self.scene.player.sprite.weapon.change("rocket_weapon")
                if event.key == K_7: self.scene.player.sprite.weapon.change("zapper_weapon")
                if event.key == K_8: self.scene.player.sprite.weapon.change("big_weapon")
                if event.key == K_0: self.scene.player.sprite.engine.change("boost_engine")
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.scene.UIManager.clicked()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.scene.state == "playing":
                        Audio.play_sfx("click")

    def close(self):
        self.running = False
        Data.save()
        self.debugger.close()
        pygame.quit()
        exit()