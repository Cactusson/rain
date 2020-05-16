import random
import pygame as pg

from .. import prepare, tools
from ..components.drop import Drop
from ..components.particle import Particle
from ..components.gui import GUI


class Game(tools._State):
    """
    The actual game happens here.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.next = 'HIGH_SCORE'
        self.drops = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.gui = GUI(self.numpad_action)
        self.drop_delay = 2500  # generate the first drop after 2.5 secs
        self.lose_delay = 2000  # wait 2 secs when lose, then quit to HS
        self.mid_level_delay = 30000  # add a star every 30 seconds
        self.min_drop_delay = 1.5
        self.max_drop_delay = 3.0

    def start(self):
        """
        This function is called every time the new game is started.
        Refreshes everything.
        """
        self.drops.empty()
        self.particles.empty()
        self.lose_timer = None
        self.mid_level_timer = self.current_time
        self.drop_timer = self.current_time
        self.lives = 3
        self.level = 0
        self.max_level = 3
        self.gui.start()

    def next_level(self):
        """
        Sets self.level to the next one.
        """
        self.level += 1
        self.gui.stars_panel.add_star()

    def lose_a_life(self):
        """
        Substracts a life from self.lives, checks if it was the last one
        and sets self.lose_timer to the current_time if yes.
        """
        self.lives -= 1
        for drop in self.drops:
            drop.back()
        self.gui.lives_panel.lose_a_life()
        self.drop_timer = self.current_time
        self.drop_delay = 2500
        if self.lives <= 0:
            self.lose_timer = self.current_time

    def generate_drop(self):
        """
        Checks if enough time passed since the last drop,
        if yes, then generate a new one.
        """
        if self.current_time > self.drop_timer + self.drop_delay:
            location = random.randint(60, 400), -100
            self.drops.add(Drop(location, self.level))
            self.drop_timer = self.current_time
            self.drop_delay = random.uniform(
                self.min_drop_delay, self.max_drop_delay) * 1000

    def create_particles(self, center, color):
        """
        When a drop is being destroyed, pops particles
        going in all directions.
        """
        for direction in ['topright', 'topleft', 'bottomright', 'bottomleft']:
            self.particles.add(Particle(center, direction, color))
            if random.randint(1, 2) == 1:
                self.particles.add(Particle(center, direction, color))

    def get_input(self):
        """
        Gets user's input and acts accordingly, popping some drops
        or just substracting score.
        I am sure I could've made this function better.
        """
        user_input = self.gui.user_input.get_input()
        if not user_input:
            return
        self.gui.user_input.empty()
        sun_popped = False
        score = 0
        for drop in self.drops:
            if drop.state == 'BACKING':
                score = 0
                self.gui.score.update_value(score)
                return
            if (user_input == drop.answer and (
                    drop.state is 'USUAL' or drop.state == 'TWEENING')):
                if drop.state == 'TWEENING':
                    score += 5
                else:
                    add_score = (600 - drop.rect.centery) // 100
                    if add_score == 0:
                        add_score = 1
                    score += add_score
                if drop.kind == 'sun':
                    sun_popped = True
                drop.state = 'DYING'
        if sun_popped:
            for drop in self.drops:
                if drop.state in ['USUAL', 'TWEENING']:
                    drop.state = 'DYING'
        if score:
            self.gui.user_input.change_color('right', self.current_time)
            self.gui.score.change_state('GROW', self.current_time)
        else:
            score = -3
            self.gui.user_input.change_color('wrong', self.current_time)
            self.gui.score.change_state('SHAKE_SINE')
        self.gui.score.update_value(score, self.current_time)

    def numpad_action(self, name):
        """
        This is called when user hits a button on numpad.
        Probably should've mixed it somehow with identical lines
        from self.get_event() ('Del' and 'Enter').
        """
        if name in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.gui.user_input.add(name)
        elif name == 'Del':
            self.gui.user_input.remove()
        elif name == 'Clear':
            self.gui.user_input.empty()
        elif name == 'Enter':
            if not self.gui.score.tweening:
                self.get_input()

    def startup(self, current_time, persistant):
        """
        The first thing to do is to set current_time because
        it is needed in update function.
        """
        self.current_time = current_time
        self.start()
        return tools._State.startup(self, current_time, persistant)

    def cleanup(self):
        """
        The only thing to send to the next state, is player's score.
        """
        self.done = False
        self.persist['recent_result'] = self.gui.score.value
        return self.persist

    def get_event(self, event):
        """
        ESC: leave to HS.
        ENTER: get input
        BACKSPACE: remove input
        Check if the player is clicking on one of numpad's buttons.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.done = True
            elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                if not self.gui.score.tweening:
                    self.get_input()
            elif event.key == pg.K_BACKSPACE:
                self.gui.user_input.remove()
            else:
                self.gui.user_input.get_event_key(event.key)
        elif event.type == pg.MOUSEBUTTONUP:
            for button in self.gui.numpad.buttons:
                button.click()

    def update(self, surface, keys, current_time, dt):
        """
        Check if it's time to move on to the next level.
        Check if player's losing and it's time to quit.
        Update everything.
        """
        self.current_time = current_time
        if self.level < self.max_level and (
            self.current_time - self.mid_level_timer > self.mid_level_delay
        ):
            self.mid_level_timer = self.current_time
            self.next_level()
        if (
            self.lose_timer
            and self.current_time - self.lose_timer > self.lose_delay
        ):
            self.done = True
        self.generate_drop()
        self.drops.update(dt, self)
        self.particles.update(self.current_time, dt)
        self.gui.update(current_time, dt)
        self.draw(surface)

    def draw(self, surface):
        """
        Draw everything.
        """
        surface.fill(prepare.BG_COLOR)
        for drop in self.drops:
            drop.draw(surface)
        for particle in self.particles:
            particle.draw(surface)
        self.gui.draw(surface)
