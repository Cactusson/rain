import random
import pygame as pg

from .. import prepare


class EmptyDrop(pg.sprite.Sprite):
    """
    An empty drop is just a circle-in-circle that appears in
    MENU and HS states, just goes downwards and kills itself when
    hits bottom of the screen (with its top).
    """
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.center = center
        self.kind = self.get_kind()
        if self.kind == 'sun':
            self.color = pg.Color('lightyellow')
            self.frame_color = pg.Color('yellow')
        elif self.kind == 'drop':
            self.color = pg.Color('lightblue')
            self.frame_color = pg.Color('blue')
        self.radius = 60
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 30)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=self.center)
        self.speed = 100

    def get_kind(self):
        """
        10% chance it's a sun.
        """
        if random.randint(1, 10) == 1:
            return 'sun'
        else:
            return 'drop'

    def make_image(self):
        surface = pg.Surface((self.radius*2, self.radius*2))
        surface.fill(prepare.BG_COLOR)
        surface.set_colorkey(prepare.BG_COLOR)
        rect = surface.get_rect()
        pg.draw.circle(surface, self.frame_color, rect.center, self.radius)
        pg.draw.circle(
            surface, self.color, rect.center, self.radius - 4)
        return surface

    def update(self, dt):
        if self.rect.top >= prepare.SCREEN_RECT.bottom:
            self.kill()
        else:
            delta = self.speed * dt
            self.rect.centery += delta - 1 if self.rect.centery + delta < 0 else delta

    def draw(self, surface):
        surface.blit(self.image, self.rect)
