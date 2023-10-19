import pygame

__all__ = ["Camera", "SmoothCamera"]

class Camera:

    __slots__ = ["game", "target", "position", "offset", "screenCenter", "rect"]

    def __init__(self, game):
        self.game = game
        self.target = pygame.Vector2(0)
        self.position = pygame.Vector2(0)
        self.offset = pygame.Vector2(0)
        self.screenCenter = pygame.Vector2(game.RESOLUTION[0]/2, game.RESOLUTION[1]/2)
        self.rect = pygame.Rect(self.position, (game.RESOLUTION[0], game.RESOLUTION[1]))

    def screen_to_world_point(self, point):
        return point + self.offset

    def world_to_screen_point(self, point):
        return point - self.offset

    def follow(self, entity):
        self.target = entity.transform
        self.position = self.target.position

    def update(self, deltaTime):
        self.position = self.target.position
        self.rect.center = self.position
        self.offset = self.position - self.screenCenter
        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)

    def render_debug(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.screenCenter, 0)


class SmoothCamera(Camera):

    __slots__ = ["game", "target", "position", "offset", "screenCenter", "rect", "smoothSpeed"]

    def __init__(self, game):
        super().__init__(game)
        self.smoothSpeed = 5#2.5
    
    def update(self, deltaTime):
        lerp = self.smoothSpeed * deltaTime
        if lerp <= 1:
            self.position = self.position.lerp(self.target.position, self.smoothSpeed * deltaTime)
        else:
            self.position = self.target.position

        self.rect.center = self.position
        self.offset = self.position - self.screenCenter
        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)