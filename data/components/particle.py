import random
import pygame as pg

from .. import prepare


velocities = {'topright': ((350, 500), (-500, -350)),
              'bottomright': ((350, 500), (350, 500)),
              'topleft': ((-500, -350), (-500, -350)),
              'bottomleft': ((-500, -350), (350, 500))}


class Particle(pg.sprite.Sprite):
    """
    Just a particle that will go in a specific direction and disappear
    leaving the screen.
    """
    def __init__(self, center, direction, color):
        pg.sprite.Sprite.__init__(self)
        self.center = center
        self.color = color
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=self.center)
        velx = velocities[direction][0]
        vely = velocities[direction][1]
        self.dx = random.randint(velx[0], velx[1])
        self.dy = random.randint(vely[0], vely[1])

    def get_image(self):
        size = random.randint(5, 20)
        image = pg.Surface((size, size))
        image.fill(prepare.BG_COLOR)
        rect = image.get_rect()
        pg.draw.circle(image, self.color, rect.center, size // 2)
        return image

    def update(self, current_time, dt):
        if (self.rect.right < prepare.SCREEN_RECT.left or
                self.rect.left > prepare.SCREEN_RECT.right or
                self.rect.bottom < prepare.SCREEN_RECT.top or
                self.rect.top > prepare.SCREEN_RECT.bottom):
            self.kill()
        else:
            self.rect.x += self.dx * dt
            self.rect.y += self.dy * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)
