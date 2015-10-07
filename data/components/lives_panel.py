import pygame as pg

from .. import prepare
from ..components import easing


class Life(pg.sprite.Sprite):
    """
    A life is just a sprite sitting in the LivesPanel.
    """
    def __init__(self, location):
        pg.sprite.Sprite.__init__(self)
        self.image = prepare.GFX['heart']
        self.rect = self.image.get_rect(topleft=location)
        self.falling = False
        self.fall_time = 0
        self.fall_duration = 700
        self.fall_begin = self.rect.y
        self.fall_change = prepare.SCREEN_RECT.bottom - self.fall_begin

    def update(self, dt):
        if self.falling:
            self.fall_time += dt * 1000
            self.rect.y = easing.ease_in_back(
                self.fall_time, self.fall_begin,
                self.fall_change, self.fall_duration)
            if self.fall_time > self.fall_duration:
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class LivesPanel(pg.sprite.Sprite):
    """
    A panel with lines: just a rectangle.
    """
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.value = 3
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 30)
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=(675, 550))
        self.lives = pg.sprite.Group()
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change
        for i in range(self.value):
            life = Life((self.rect.x + 10 + i * 30, self.rect.y + 15))
            life.tween_begin = life.rect.x - self.tween_change
            self.lives.add(life)

    def start(self):
        self.value = 3
        self.lives.empty()
        for i in range(self.value):
            life = Life((self.rect.x + 12 + i * 40, self.rect.y + 12))
            life.tween_begin = life.rect.x - self.tween_change
            self.lives.add(life)
        self.tweening = True
        self.tween_time = 0

    def get_image(self):
        image = pg.Surface((136, 56))
        image.fill(prepare.GUI_BG_COLOR)
        image.set_colorkey(prepare.GUI_BG_COLOR)
        rect = image.get_rect()
        pg.draw.rect(image, pg.Color('black'), rect, 3)
        return image

    def lose_a_life(self):
        """
        When a life is lost, the nearest to the right should drop.
        """
        lives = self.lives.sprites()
        life_to_lose = lives[0]
        for life in lives:
            if life.rect.x > life_to_lose.rect.x:
                life_to_lose = life
        life_to_lose.falling = True

    def update(self, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            for life in self.lives:
                life.rect.x = easing.ease_out_bounce(
                    self.tween_time, life.tween_begin,
                    self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
        self.lives.update(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.lives.draw(surface)
