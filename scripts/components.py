from typing import Any
import pygame

__all__ = ["Box", "Circle", "FRect", "Transform", "PolarTransform", "Animator1D", "Animator", "DataObject"]


class Box:

    __slots__ = ["x", "y", "w", "h"]

    def __init__(self, x, y, w, h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Circle:

    __slots__ = ["center"   , "radius"]

    def __init__(self, x, y, radius) -> None:
        self.center = pygame.Vector2(x, y)
        self.radius = radius


class FRect:

    __slots__ = ["x", "y", "width", "height"]

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, x):
        self.x = x

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, x):
        self.x = x - self.width

    @property
    def w(self):
        return self.width

    @w.setter
    def w(self, width):
        self.width = width

    @property
    def h(self):
        return self.height

    @h.setter
    def h(self, height):
        self.height = height

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, y):
        self.y = y

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, y):
        self.y = y - self.height

    @property
    def centerx(self):
        return self.x + self.width / 2

    @centerx.setter
    def centerx(self, x):
        self.x = x - self.width / 2

    @property
    def centery(self):
        return self.y + self.height / 2

    @centery.setter
    def centery(self, y):
        self.y = y - self.height / 2
    
    @property
    def center(self):
        return pygame.Vector2(self.x + self.width / 2, self.y + self.height / 2)

    @property
    def topleft(self):
        return pygame.Vector2(self.x, self.y)

    @property
    def size(self):
        return pygame.Vector2(self.width, self.height)

    @property
    def rect(self):
        return pygame.Rect(self.topleft, self.size)

    def colliderect(self, other):
        return (self.right > other.left and self.left < other.right) and (self.bottom > other.top and self.top < other.bottom)


class Transform:

    __slots__ = ["position", "imgSize", "boxCollider"]

    def __init__(self, pos, image, box):
        self.position = pygame.Vector2(pos)
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)
        self.boxCollider = Box(self.imgSize.x - box[0], self.imgSize.y - box[1], self.imgSize.x - box[2], self.imgSize.y - box[3])

    @property
    def left(self):
        return self.position.x - self.boxCollider.x

    @left.setter
    def left(self, x):
        self.position.x = x + self.boxCollider.x

    @property
    def right(self):
        return self.position.x + self.boxCollider.w

    @right.setter
    def right(self, x):
        self.position.x = x - self.boxCollider.w

    @property
    def top(self):
        return self.position.y - self.boxCollider.y

    @top.setter
    def top(self, y):
        self.position.y = y + self.boxCollider.y

    @property
    def bottom(self):
        return self.position.y + self.boxCollider.h

    @bottom.setter
    def bottom(self, y):
        self.position.y = y - self.boxCollider.h

    @property
    def centerx(self):
        return self.position.x

    @centerx.setter
    def centerx(self, x):
        self.position.x = x

    @property
    def centery(self):
        return self.position.y

    @centery.setter
    def centery(self, y):
        self.position.y = y

    @property
    def center(self):
        return self.position

    @property
    def topleft(self):
        return pygame.Vector2(self.left, self.top)

    @property
    def elements(self):
        return self.left, self.right, self.top, self.bottom

    @property
    def imgPosition(self):
        return pygame.Vector2(self.position.x - self.imgSize.x, self.position.y - self.imgSize.y)
        #return pygame.Vector2(self.left, self.top)

    @property
    def rect(self):
        return pygame.Rect(self.imgPosition, self.imgSize * 2)

    @property
    def hitbox(self):
        return pygame.Rect(self.left, self.top, self.boxCollider.x + self.boxCollider.w, self.boxCollider.y + self.boxCollider.h)

    def colliderect(self, other):
        return (self.right > other.left and self.left < other.right) and (self.bottom > other.top and self.top < other.bottom)

    def update(self, image):
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)
    
    def reset(self, image, box):
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)
        self.boxCollider = Box(self.imgSize.x - box[0], self.imgSize.y - box[1], self.imgSize.x - box[2], self.imgSize.y - box[3])


class PolarTransform:

    __slots__ = ["position", "radius", "imgSize"]

    def __init__(self, pos, hitRadius, image):
        self.position = pygame.Vector2(pos)
        self.radius = hitRadius
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, x):
        self.position.x = x

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, y):
        self.position.y = y

    @property
    def center(self):
        return self.position

    @property
    def elements(self):
        return self.position, self.radius

    @property
    def imgPosition(self):
        return pygame.Vector2(self.position.x - self.imgSize.x, self.position.y - self.imgSize.y)
    
    @property
    def rect(self):
        return pygame.Rect(self.imgPosition, self.imgSize * 2)

    @property
    def hitcircle(self):
        return Circle(self.position.x, self.position.y, self.radius)

    def collidepoint(self, point):
        return self.radius ** 2 <= (point.x - self.position.x) ** 2 + (point.y - self.position.y) ** 2

    def collide(self, other):
        return (self.position.x - other.position.x) ** 2 + (self.position.y - other.position.y) ** 2 <= (self.radius + other.radius) ** 2

    def update(self, image):
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)
    
    def reset(self, image, hitRadius):
        self.imgSize = pygame.Vector2(image.get_width()/2, image.get_height()/2)
        self.radius = hitRadius


class Animator1D:

    __slots__ = ["frame", "animation", "animLength", "animSpeed", "playing"]

    def __init__(self, animation, animSpeed):
        self.frame = 0
        self.animation = animation
        self.animLength = len(self.animation)
        self.animSpeed = animSpeed
        self.playing = False
    
    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def animate(self, deltaTime):
        if self.playing:
            self.frame += self.animSpeed * deltaTime
            self.frame %= self.animLength
            return self.animation[int(self.frame)].copy()
    
    def switch_animation(self, animation, animSpeed):
        self.animation = animation
        self.animLength = len(self.animation)
        self.playing = False
        self.frame = 0
        self.animSpeed = animSpeed
    
    def anim_end(self):
        return self.frame >= self.animLength - 1


class Animator:

    __slots__ = ["frame", "preAnim", "anim", "next_anim", "animations", "animLength", "animSpeed"]

    def __init__(self, animations, animSpeed):
        self.frame = 0
        self.preAnim = "None"
        self.anim = "None"
        self.next_anim = "None"
        self.animations = animations
        self.animLength = 0
        self.animSpeed = animSpeed
        self.play("idle")

    def animate(self, deltaTime):
        if self.next_anim != self.anim and self.anim_end():
            self.play(self.next_anim)
        self.frame += self.animSpeed * deltaTime
        self.frame %= self.animLength
        return self.animations[self.anim][int(self.frame)].copy()
    
    def play(self, anim):
        self.preAnim = self.anim
        self.anim = anim
        self.next_anim = anim
        if self.anim != self.preAnim:
            self.frame = 0
            self.animLength = len(self.animations[self.anim])

    def switch_animations(self, animations, animSpeed):
        self.animations = animations    
        self.preAnim = "None"
        self.anim = "None"
        self.next_anim = "None"
        self.animSpeed = animSpeed
        self.play("idle")

    def anim_end(self):
        return self.frame >= self.animLength - 1

    def queue(self, anim):
        self.next_anim = anim

class DataObject:

    def __init__(self, data) -> None:
        for key, val in data.items():
            self.__setattr__(key, val)

    def to_dict(self):
        return self.__dict__.copy()