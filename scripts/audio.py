import pygame
import os

from .constants import *

class Audio:

    audio = {}
    musicChannel = None
    SFXChannel = None
    muted = True

    @classmethod
    def load(cls):
        cls.audio = cls.load_audio(os.path.join(PATH, "assets/audio/"))
        cls.musicChannel = pygame.mixer.Channel(0)
        cls.SFXChannel = pygame.mixer.Channel(1)
        cls.SFXChannel.set_volume(0.15)

    @classmethod
    def load_audio(cls, path):
        audio = {}
        for fileName in os.listdir(path):
            filePath = os.path.join(path, fileName)
            if os.path.isdir(filePath):
                audio[fileName] = cls.load_audio(filePath)
            else:
                audio[fileName[:-4]] = pygame.mixer.Sound(filePath)
        return audio

    @classmethod
    def play_sfx(cls, sfx):
        if not cls.muted:
            cls.SFXChannel.play(cls.audio["sfx"][sfx])
    
    @classmethod
    def play_music(cls, music):
        if not cls.muted:
            cls.musicChannel.play(cls.audio["music"][music])