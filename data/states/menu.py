import random
import pygame as pg

from .. import prepare, tools
from ..components.label import Label
from ..components.button import Button
from ..components.empty_drop import EmptyDrop


class Menu(tools._State):
    """
    A screen with three buttons: PLAY, HIGH SCORE and QUIT.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=(
            prepare.SCREEN_RECT.centerx, 400))
        self.title = Label('Timeless', 120, 'RAIN', pg.Color('black'),
                           center=(self.rect.centerx, 125))
        self.buttons = self.make_buttons()
        self.empty_drops = pg.sprite.Group()
        self.drop_delay = 1000
        self.drop_timer = 0

    def make_image(self):
        """
        Creates an image, nothing fancy.
        """
        image = pg.Surface((600, 300)).convert()
        image.fill(pg.Color('black'))
        rect = image.get_rect()

        inner = pg.Surface((580, 280)).convert()
        inner.fill(prepare.BG_COLOR)
        inner_rect = inner.get_rect(center=(rect.centerx, 150))
        image.blit(inner, inner_rect)

        return image

    def make_buttons(self):
        """
        There are three buttons in the menu, each has its own call function.
        (their names start with 'button_')
        """
        buttons = pg.sprite.Group()
        play = Button((prepare.SCREEN_RECT.centerx, 300),
                      'PLAY', 'Timeless', 30, self.button_play)
        high_score = Button((prepare.SCREEN_RECT.centerx, 400),
                            'HIGH SCORE', 'Timeless', 30, self.button_hs)
        quit = Button((prepare.SCREEN_RECT.centerx, 500),
                      'QUIT', 'Timeless', 30, self.button_quit)
        buttons.add(play, high_score, quit)
        return buttons

    def button_play(self):
        self.next = 'GAME'
        self.done = True

    def button_hs(self):
        self.next = 'HIGH_SCORE'
        self.done = True

    def button_quit(self):
        self.quit = True

    def create_drop(self):
        x = random.randint(60, 640)
        y = -50
        self.empty_drops.add(EmptyDrop((x, y)))

    def startup(self, current_time, persistant):
        """
        The same thing as in HIGH_SCORE state.
        """
        self.persist = persistant
        self.start_time = current_time
        self.drop_timer = current_time
        self.empty_drops.add(self.persist['empty_drops'])
        if 'drop_timer' in self.persist:
            self.drop_timer = self.persist['drop_timer']
        else:
            self.drop_timer = current_time

    def cleanup(self):
        """
        Also the same as in HS.
        """
        self.done = False
        if self.next == 'HIGH_SCORE':
            self.persist['empty_drops'] = self.empty_drops.sprites()
            self.persist['drop_timer'] = self.drop_timer
        self.empty_drops.empty()
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in self.buttons:
                button.click()

    def update(self, surface, keys, current_time, dt):
        if current_time - self.drop_timer > self.drop_delay:
            self.drop_timer = current_time
            self.create_drop()
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
        for drop in self.empty_drops:
            drop.update(dt)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        self.empty_drops.draw(surface)
        self.title.draw(surface)
        surface.blit(self.image, self.rect)
        self.buttons.draw(surface)
