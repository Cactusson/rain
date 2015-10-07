import random
import pickle
import pygame as pg

from .. import prepare, tools
from ..components.label import Label
from ..components.button import Button
from ..components.empty_drop import EmptyDrop


class HighScore(tools._State):
    """
    Screen with high score. Saves score and loads it using pickle.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=(
            prepare.SCREEN_RECT.centerx, 350))
        self.title = Label('Timeless', 90, 'HIGH SCORE', pg.Color('black'),
                           center=(self.rect.centerx, 75))
        self.button = Button((prepare.SCREEN_RECT.centerx, 500),
                             'BACK TO MENU', 'Timeless', 27, self.button_back)
        self.empty_drops = pg.sprite.Group()
        self.drop_delay = 1000
        self.drop_timer = 0
        self.recent_result_text = None
        try:
            results_file = open('results', 'rb')
            self.results = pickle.load(results_file)
            if len(self.results) != 5:
                self.results = [0, 0, 0, 0, 0]
        except:
            self.results = [0, 0, 0, 0, 0]

    def make_image(self):
        """
        Creates an image with a frame.
        """
        image = pg.Surface((600, 400)).convert()
        image.fill(pg.Color('black'))
        rect = image.get_rect()

        inner = pg.Surface((580, 380)).convert()
        inner.fill(prepare.BG_COLOR)
        inner_rect = inner.get_rect(center=(rect.centerx, 200))
        image.blit(inner, inner_rect)

        return image

    def create_table(self):
        """
        Creates a table, that is pg.sprite.Group with 5 sprites,
        on each of them is text like '1: 50'.
        If the results have been updated, it also updates the file
        with them.
        """
        highlighted = False
        if self.recent_result is not None:
            self.recent_result_text = Label(
                'Timeless', 20, 'Your score: {}'.format(self.recent_result),
                pg.Color('black'), center=(
                    self.rect.centerx, self.rect.top + 40))
            if self.recent_result >= self.results[-1]:
                self.results.append(self.recent_result)
                self.results.sort(reverse=True)
                self.results.pop()
            results_file = open('results', 'wb')
            pickle.dump(self.results, results_file)
        table = pg.sprite.Group()
        for i, num in enumerate(self.results):
            if num == self.recent_result and not highlighted:
                highlighted = True
                color = pg.Color('white')
                bg = pg.Color('orange')
            else:
                color = pg.Color('black')
                bg = None
            text = '{}. {}'.format(i + 1, num)
            topleft = (self.rect.centerx - 35, self.rect.top + 70 + 50 * i)
            line = Label('Timeless', 40, text, color, topleft=topleft, bg=bg)
            table.add(line)
        return table

    def button_back(self):
        """
        Function is called when user clicks on button 'BACK TO MENU'.
        """
        self.next = 'MENU'
        self.done = True

    def create_drop(self):
        """
        Creates a random empty drop every once in a while.
        """
        x = random.randint(60, 640)
        y = -50
        self.empty_drops.add(EmptyDrop((x, y)))

    def startup(self, current_time, persistant):
        """
        If coming from MENU, we should recreate its empty drops.
        If coming from GAME, update the results.
        """
        self.persist = persistant
        self.start_time = current_time
        if self.previous == 'MENU':
            self.empty_drops.add(self.persist['empty_drops'])
            if 'drop_timer' in self.persist:
                self.drop_timer = self.persist['drop_timer']
            else:
                self.drop_timer = current_time
            self.recent_result = None
        elif self.previous == 'GAME':
            if 'recent_result' in self.persist:
                self.recent_result = self.persist['recent_result']
            else:
                self.recent_result = None
        self.table = self.create_table()

    def cleanup(self):
        """
        Send information about empty drops.
        """
        self.done = False
        self.persist['empty_drops'] = self.empty_drops.sprites()
        self.persist['drop_timer'] = self.drop_timer
        self.empty_drops.empty()
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next = 'MENU'
                self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.button.click()

    def update(self, surface, keys, current_time, dt):
        if current_time - self.drop_timer > self.drop_delay:
            self.drop_timer = current_time
            self.create_drop()
        mouse_pos = pg.mouse.get_pos()
        self.button.update(mouse_pos)
        for drop in self.empty_drops:
            drop.update(dt)
        self.draw(surface)

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        self.empty_drops.draw(surface)
        self.title.draw(surface)
        surface.blit(self.image, self.rect)
        self.button.draw(surface)
        if self.recent_result is not None:
            self.recent_result_text.draw(surface)
        self.table.draw(surface)
