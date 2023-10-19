from pygame.locals import *
import pygame.gfxdraw
import pygame

from .debugger import *
from .data import *
from .assets import *
from .renderer import *
from .scene import *


class Game:

    def __init__(self):
        self.debugger = Debugger()

        # _____ Application Configurations  ____
        pygame.init()
        pygame.mixer.init()

        self.debugger.prints_out(Data.load())

        Data.config["resolution"] = pygame.display.get_desktop_sizes()[0]
        self.RESOLUTION = Data.config["resolution"]
        self.fullscreen = Data.config["fullscreen"]
        self.vsync = Data.config["vsync"]
        fullscreen = pygame.FULLSCREEN if self.fullscreen else 0
        self.window = pygame.display.set_mode(self.RESOLUTION, fullscreen, vsync=self.vsync)

        self.loading()

        pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
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

        img = Assets.sprites["forest_bg_big"]
        Assets.sprites["forest_bg_big"] = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
        pygame.display.set_caption(Data.config["name"])
        pygame.display.set_icon(Assets.ui[Data.config["icon"]])

    def run(self):
        self.running = True
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
                if event.key == K_F3:
                    self.renderer.debugRender = not self.renderer.debugRender
                if event.key == K_F4:
                    self.scene.fixedUpdate = not self.scene.fixedUpdate
                if event.key == K_F5:
                    self.renderer.debugRenderUI = not self.renderer.debugRenderUI
                if event.key == K_F8:
                    self.scene.FPS = Data.config["fps"]
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.scene.UIManager.clicked()

    def close(self):
        self.running = False
        Data.save()
        self.debugger.close()
        pygame.quit()
        exit()