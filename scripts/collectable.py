from .data import *
from .assets import *
from .object import *
from .components import *

__all__ = ["Collectable"]

class Collectable(Object):

    __slots__ = ["image", "transform", "animator"]
    alls = []

    def __init__(self, collectableType, pos):
        data = Data.objects[collectableType]
        animation = Assets.sprites[data["animation"]]
        super().__init__(pos, data["hitRadius"], animation[0])
        self.animator = Animator1D(Assets.sprites[data["animation"]], data["animSpeed"])
        self.animator.play()
        self.powerup = data["powerup"]
        self.lifespan = 20

    def update(self, deltaTime):
        self.image = self.animator.animate(deltaTime)
        self.lifespan -= deltaTime
        if self.lifespan <= 0:
            self.destroy()