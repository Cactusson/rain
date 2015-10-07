import pygame as pg

from .. import prepare
from ..components import easing
from ..components.label import Label


class Score(pg.sprite.Sprite):
    """
    A box with a number that shows the score.
    Also showing a change in score (self.change).
    It can shake, grow and shrink back.
    """
    def __init__(self, topleft=(635, 40), size=(80, 40)):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 30)
        self.small_font = pg.font.Font(prepare.FONTS['Timeless'], 20)
        self.color = pg.Color('white')
        self.color_right = pg.Color('#80EF91')
        self.color_wrong = pg.Color('#CB3B3B')
        self.size = size
        self.image = pg.Surface((self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=topleft)
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change
        self.inflate_delay = 1000
        self.inflate_offset_plus = (150, 150)
        self.inflate_offset_minus = (-75, -75)
        self.inflate_max_width = 90
        self.shake_duration = 300
        self.shake_begin = self.rect.x
        self.shake_change = -20
        self.change_delay = 1000

    def start(self):
        self.value = 0
        self.update_value()
        self.state = 'USUAL'  # USUAL, GROW, SHRINK, SHAKE_SINE, SHAKE_ELASTIC
        self.tweening = True
        self.tween_time = 0
        self.inflate_timer = 0.0
        self.shake_time = 0
        self.change = None
        self.change_timer = 0.0

    def change_state(self, new_state, now=None):
        """
        When something happens and the panel should start shaking or
        growing/shrinking, first check if it's not already doing something
        like that.
        """
        if self.state == 'USUAL':
            self.state = new_state
            if now:
                self.inflate_timer = now

    def change_rect(self, offset, dt):
        """
        This is where growing/shrinking takes place.
        """
        center = self.rect.center
        self.rect.inflate_ip(offset[0] * dt, offset[1] * dt)
        self.rect.center = center
        self.image = pg.Surface(self.rect.size)
        self.image.fill(self.color)

    def make_change_image(self, value):
        """
        A change image is a circle with a number and + or - sign.
        It will change its transparency in update()
        """
        image = pg.Surface((50, 50)).convert()
        image.fill(prepare.GUI_BG_COLOR)
        rect = image.get_rect()
        if value >= 0:
            color = pg.Color('green')
            pre = '+'
        else:
            color = pg.Color('red')
            pre = '-'
        pg.draw.circle(image, color, rect.center, 25)
        text = Label('Timeless', 20, pre + str(value), pg.Color('black'),
                     center=rect.center)
        image.blit(text.image, text.rect)
        return image

    def update_value(self, difference=0, now=None):
        self.value += difference
        if self.value < 0:
            self.value = 0
        self.text = self.font.render(str(self.value), True, pg.Color('black'))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        if difference != 0:
            self.change = pg.sprite.Sprite()
            self.change.image = self.make_change_image(difference)
            self.change.rect = self.change.image.get_rect(
                center=(675, self.rect.centery + 55))
            self.change.alpha = 255
            self.change.image.set_alpha(self.change.alpha)
            self.change_timer = now

    def update(self, now, dt):
        """
        The behavior depends on its current state.
        Shaking uses easing functions and growing/shrinking
        uses self.change_rect()
        """
        if self.change:
            if now - self.change_timer > self.change_delay:
                self.change = None
            else:
                self.change.alpha -= 50 * dt
                self.change.image.set_alpha(self.change.alpha)
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
            self.update_value()
        if self.state == 'GROW':
            if self.rect.width > self.inflate_max_width:
                self.state = 'SHRINK'
            else:
                self.change_rect(self.inflate_offset_plus, dt)
        elif self.state == 'SHRINK':
            if self.rect.size <= self.size:
                self.state = 'USUAL'
            else:
                self.change_rect(self.inflate_offset_minus, dt)
        elif self.state == 'SHAKE_SINE':
            self.shake_time += dt * 1000
            self.rect.x = easing.ease_in_out_sine(
                self.shake_time, self.shake_begin,
                self.shake_change, self.shake_duration)
            if self.shake_time > self.shake_duration:
                self.shake_begin = self.rect.x
                self.shake_time = 0
                self.state = 'SHAKE_ELASTIC'
            self.update_value()
        elif self.state == 'SHAKE_ELASTIC':
            self.shake_time += dt * 1000
            self.rect.x = easing.ease_out_elastic(
                self.shake_time, self.shake_begin,
                -self.shake_change, self.shake_duration)
            if self.shake_time > self.shake_duration:
                self.shake_begin = self.rect.x
                self.shake_time = 0
                self.state = 'USUAL'
            self.update_value()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)
        if self.change:
            surface.blit(self.change.image, self.change.rect)
