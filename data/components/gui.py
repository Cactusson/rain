import pygame as pg

from .. import prepare
from ..components import easing
from ..components.score import Score
from ..components.numpad import Numpad
from ..components.user_input import UserInput
from ..components.stars_panel import StarsPanel
from ..components.lives_panel import LivesPanel


class GUI(pg.sprite.Sprite):
    """
    This is a class that holds together all the elements of GUI:
    score, numpad, user_input, stars_panel and lives_panel.
    """
    def __init__(self, numpad_button_call):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((800-555+5, 600))
        self.image.fill(prepare.GUI_BG_COLOR)
        self.rect = self.image.get_rect(topleft=(555, 0))
        self.tweening = True
        self.tween_time = 0
        self.tween_duration = 1500
        self.tween_change = -300
        self.tween_begin = self.rect.x - self.tween_change
        self.score = Score()
        self.numpad = Numpad(numpad_button_call)
        self.user_input = UserInput()
        self.lives_panel = LivesPanel()
        self.stars_panel = StarsPanel()

    def start(self):
        """
        At the start of the new game, refresh everything.
        """
        self.score.start()
        self.stars_panel.start()
        self.numpad.start()
        self.user_input.start()
        self.lives_panel.start()
        self.tweening = True
        self.tween_time = 0

    def update(self, current_time, dt):
        if self.tweening:
            self.tween_time += dt * 1000
            self.rect.x = easing.ease_out_bounce(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.tweening = False
        self.score.update(current_time, dt)
        self.numpad.update(dt)
        self.user_input.update(current_time, dt)
        self.lives_panel.update(dt)
        self.stars_panel.update(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.score.draw(surface)
        self.numpad.draw(surface)
        self.user_input.draw(surface)
        self.lives_panel.draw(surface)
        self.stars_panel.draw(surface)
