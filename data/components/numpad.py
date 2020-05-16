import pygame as pg

from .. import prepare
from ..components import easing
from ..components.data import numpad_data


class NumpadButton(pg.sprite.Sprite):
    """
    A button with a number or text like 'Enter'.
    """
    def __init__(self, name, location, size, call):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.size = size
        self.call = call
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 20)
        self.idle_image, self.hover_image = self.make_images(self.name)
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=location)
        self.hover = False
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change

    def start(self):
        self.tweening = True
        self.tween_time = 0
        self.hover = False

    def make_images(self, text):
        idle_image = pg.Surface(self.size).convert()
        idle_image.fill(pg.Color('white'))
        idle_text = self.font.render(text, True, pg.Color('black'))
        rect = idle_image.get_rect()
        idle_text_rect = idle_text.get_rect(center=rect.center)
        idle_image.blit(idle_text, idle_text_rect)

        hover_image = pg.Surface(self.size).convert()
        hover_image.fill(pg.Color('#D69830'))
        hover_text = self.font.render(text, True, pg.Color('black'))
        rect = hover_image.get_rect()
        hover_text_rect = hover_text.get_rect(center=rect.center)
        hover_image.blit(hover_text, hover_text_rect)

        return idle_image, hover_image

    def click(self):
        if self.hover:
            self.call(self.name)

    def update(self, mouse_pos, dt):
        hover = self.rect.collidepoint(mouse_pos)
        self.image = self.hover_image if hover else self.idle_image
        self.hover = hover

        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Numpad(pg.sprite.Sprite):
    """
    A box with buttons with numbers and stuff.
    """
    def __init__(self, call):
        pg.sprite.Sprite.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(topleft=(572, 151))
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change
        self.buttons = pg.sprite.Group()
        for (name, location, size) in numpad_data:
            self.buttons.add(NumpadButton(name, location, size, call))

    def start(self):
        self.tweening = True
        self.tween_time = 0
        for button in self.buttons:
            button.start()

    def make_image(self):
        image = pg.Surface((211, 287)).convert()
        image.fill(pg.Color('blue'))
        image_rect = image.get_rect()
        inner_image = pg.Surface((205, 281)).convert()
        inner_image.fill(pg.Color('black'))
        inner_image_rect = inner_image.get_rect(center=image_rect.center)
        image.blit(inner_image, inner_image_rect)
        return image

    def update(self, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos, dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for button in self.buttons:
            button.draw(surface)
