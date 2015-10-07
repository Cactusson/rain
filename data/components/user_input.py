import pygame as pg

from .. import prepare
from ..components import data
from ..components import easing


class UserInput(pg.sprite.Sprite):
    """
    A box that shows player's input. Can change its BG color.
    No more than 5 characters.
    Player can add, remove numbers to the value, also clear the value.
    """
    def __init__(self, topleft=(576, 155), size=(203, 75)):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 55)
        self.text = ''
        self.usual_color = pg.Color('#D9DAD7')
        self.color_right = pg.Color('#80EF91')
        self.color_wrong = pg.Color('#CB3B3B')
        self.color = self.usual_color
        self.image = pg.Surface((size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=topleft)
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change
        self.color_delay = 500
        self.color_timer = 0.0

    def start(self):
        self.text = ''
        self.tweening = True
        self.tween_time = 0
        self.color = self.usual_color
        self.image.fill(self.color)

    def change_color(self, keyword, now):
        if keyword == 'right':
            self.color = self.color_right
        elif keyword == 'wrong':
            self.color = self.color_wrong
        self.image.fill(self.color)
        self.color_timer = now

    def get_input(self):
        if self.text:
            return self.text
        else:
            return None

    def empty(self):
        self.text = ''
        self.input_image = None
        self.input_rect = None

    def add(self, number):
        if len(self.text) < 5:
            self.text += number
            self.update_value()

    def remove(self):
        if self.text:
            self.text = self.text[:-1]
        self.update_value()

    def get_event_key(self, event_key):
        for index, keys in enumerate(data.keys):
            if event_key in keys:
                self.add(str(index))

    def update(self, now, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
            self.update_value()
        if self.color != self.usual_color:
            if now - self.color_timer > self.color_delay:
                self.color = self.usual_color
                self.image.fill(self.color)

    def update_value(self):
        self.input_image = self.font.render(self.text, True, pg.Color('black'))
        self.input_rect = self.input_image.get_rect(
            center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.text:
            surface.blit(self.input_image, self.input_rect)
