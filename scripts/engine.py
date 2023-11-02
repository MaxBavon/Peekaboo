from .data import *
from .assets import *
from .components import *

__all__ = ["Engine"]

class Engine:

    __slots__ = ["name", "sprite", "animator", "thrust", "offset", "particle"]

    def __init__(self, engineType) -> None:
        data = Data.engines[engineType]
        self.name = engineType
        self.animator = Animator(Assets.sprites[data.animation], data.animSpeed)
        self.thrust = data.thrust * UNIT
        self.offset = data.offset
        self.particle = data.particle
        self.animator.play("idle")

    def change(self, engineType):
        data = Data.engines[engineType]
        self.name = engineType
        self.animator.switch_animations(Assets.sprites[data.animation], data.animSpeed)
        self.thrust = data.thrust * UNIT
        self.offset = data.offset
        self.particle = data.particle