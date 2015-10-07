import pygame as pg

from .. import prepare
from ..components import easing


class Star(pg.sprite.Sprite):
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['star']
        self.rect = self.image.get_rect(topleft=location)
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 2000
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change

    def update(self, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_elastic(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class StarsPanel(pg.sprite.Sprite):
    """
    It's very similar to lives_panel, only stars aren't there
    from the beginning, they will be added one by one later.
    They use some easing when they appear.
    """
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.value = 0
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 30)
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=(675, 480))
        self.stars = pg.sprite.Group()
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change

    def start(self):
        self.value = 0
        self.stars.empty()
        self.tweening = True
        self.tween_time = 0

    def get_image(self):
        image = pg.Surface((136, 56))
        image.fill(prepare.GUI_BG_COLOR)
        image.set_colorkey(prepare.GUI_BG_COLOR)
        rect = image.get_rect()
        pg.draw.rect(image, pg.Color('black'), rect, 3)
        return image

    def add_star(self):
        self.value += 1
        star = Star((self.rect.x + 12 + (self.value - 1) * 40,
                     self.rect.y + 12))
        self.stars.add(star)

    def update(self, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
        self.stars.update(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.stars.draw(surface)
