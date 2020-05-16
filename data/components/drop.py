import random
import pygame as pg

from .. import prepare
from ..components.data import drop_data
from ..components.data import dividers
from ..components import easing


class Drop(pg.sprite.Sprite):
    def __init__(self, center, level):
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
        self.first_number, self.second_number, self.sign, self.answer = \
            self.get_nums(level)
        self.font = pg.font.Font(prepare.FONTS['Timeless'], 30)
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=self.center)
        self.speed = 100
        self.state = 'TWEENING'  # TWEENING, USUAL, DYING, BACKING
        self.tween_time = 0
        self.tween_duration = 500
        self.tween_begin = self.rect.y
        self.tween_change = 20 - self.tween_begin
        self.back_time = 0
        self.back_duration = 700

    def get_kind(self):
        """
        10% chance it's sun.
        """
        if random.randint(1, 10) == 1:
            return 'sun'
        else:
            return 'drop'

    def make_image(self):
        """
        All the different things in one image.
        """
        image = pg.Surface((self.radius*2, self.radius*2))
        image.fill(prepare.BG_COLOR)
        image.set_colorkey(prepare.BG_COLOR)
        rect = image.get_rect()
        pg.draw.circle(image, self.frame_color, rect.center, self.radius)
        pg.draw.circle(
            image, self.color, rect.center, self.radius - 4)
        rect = image.get_rect()
        rendered = self.render_text(rect.center)
        for (text, rect) in rendered:
            image.blit(text, rect)
        return image

    def render_text(self, center):
        """
        Two numbers and a sign with their positions relative to drop's center.
        """
        rendered = []

        first_number_image = self.font.render(
            self.first_number, True, pg.Color('black'))
        first_number_rect = first_number_image.get_rect(
            center=(center[0] + 20, center[1] - 20))
        rendered.append((first_number_image, first_number_rect))

        second_number_image = self.font.render(
            self.second_number, True, pg.Color('black'))
        second_number_rect = second_number_image.get_rect(
            center=(center[0] + 20, center[1] + 20))
        rendered.append((second_number_image, second_number_rect))

        if self.sign == '*':
            self.sign = '×'
        elif self.sign == '/':
            self.sign = '÷'
        sign_image = self.font.render(
            self.sign, True, pg.Color('black'))
        sign_rect = sign_image.get_rect(
            center=(center[0] - 20, center[1]))
        rendered.append((sign_image, sign_rect))

        return rendered

    def get_nums(self, level):
        """
        Returns two numbers, a sign and an answer to the expression.
        The method of getting the numbers depends on what sign is used.
        """
        data_dict = drop_data[level]
        signs = data_dict['signs']
        sign = random.choice(signs)
        if sign == '+':
            first_bottom = second_bottom = data_dict['add_bottom']
            first_top = second_top = data_dict['add_top']
            first_number = str(random.randint(first_bottom, first_top))
            second_number = str(random.randint(second_bottom, second_top))
        elif sign == '-':
            first_bottom = second_bottom = data_dict['add_bottom']
            first_top = data_dict['add_top']
            first_number = str(random.randint(first_bottom, first_top))
            second_top = int(first_number)
            second_number = str(random.randint(second_bottom, second_top))
        elif sign == '*':
            first_bottom = second_bottom = data_dict['multi_bottom']
            first_top = data_dict['multi_first_top']
            first_number = str(random.randint(first_bottom, first_top))
            second_top = data_dict['multi_second_top']
            second_number = str(random.randint(second_bottom, second_top))
        elif sign == '/':
            first_bottom = data_dict['div_first_bottom']
            first_top = data_dict['div_first_top']
            first_candidates = [num for num in dividers if
                                num >= first_bottom and num <= first_top]
            first_number = str(random.choice(first_candidates))
            second_bottom = data_dict['div_second_bottom']
            second_top = data_dict['div_second_top']
            second_candidates = [num for num in dividers[int(first_number)] if
                                 num >= second_bottom and num <= second_top]
            second_number = str(random.choice(second_candidates))
        expression = first_number + sign + second_number
        answer = int(eval(expression))
        return first_number, second_number, sign, str(answer)

    def back(self):
        """
        When a drop hits bottom of the screen, all the drops should
        get back to the top.
        """
        self.state = 'BACKING'
        self.back_begin = self.rect.y
        self.back_change = prepare.SCREEN_RECT.top - 120 - self.back_begin

    def dying(self, dt, game):
        """
        When a drop is dying, its radius will get smaller and in the end
        it will delete itself and create particles.
        """
        self.radius -= 500 * dt
        self.radius = int(self.radius)
        if self.radius < 10:
            game.create_particles(self.rect.center, self.frame_color)
            self.kill()
        else:
            self.image = self.make_image()
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, game):
        """
        Drop's behavior depends on its state at the moment.
        TWEENING when it has been just created.
        BACKING when it is going backwards.
        USUAL when it's just going downwards.
        DYING when it's done for.
        """
        if self.state == 'TWEENING':
            self.tween_time += dt * 1000
            self.rect.y = easing.ease_out_back(
                self.tween_time, self.tween_begin,
                self.tween_change, self.tween_duration)
            if self.tween_time > self.tween_duration:
                self.state = 'USUAL'
        elif self.state == 'BACKING':
            self.back_time += dt * 1000
            self.rect.y = easing.ease_in_expo(
                self.back_time, self.back_begin,
                self.back_change, self.back_duration)
            if self.back_time > self.back_duration:
                self.kill()
        elif self.state == 'USUAL':
            if self.rect.bottom >= prepare.SCREEN_RECT.bottom:
                game.lose_a_life()
            else:
                delta = self.speed * dt
                self.rect.centery += delta - 1 if self.rect.centery + delta < 0 else delta
        elif self.state == 'DYING':
            self.dying(dt, game)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
