import pygame as pg

from .. import prepare


class Button(pg.sprite.Sprite):
    """
    Button is some text on a bg. If you click on it, call (function)
    will be called.
    """
    def __init__(self, pos, text, font_name, font_size, call):
        pg.sprite.Sprite.__init__(self)
        self.call = call
        self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        self.idle_image, self.hover_image = self.make_images(text)
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=pos)
        self.hover = False

    def make_images(self, text):
        """
        Button changes its image depending if the player is hovering it or not.
        """
        idle_color = pg.Color('black')
        hover_color = pg.Color('white')
        hover_fill = pg.Color('purple')
        idle_image = self.font.render(text, True, idle_color)
        hover_image = self.font.render(text, True, hover_color, hover_fill)
        return idle_image, hover_image

    def click(self):
        if self.hover:
            self.call()

    def update(self, mouse_pos):
        """
        Check if the button is hovered.
        """
        hover = self.rect.collidepoint(mouse_pos)
        if hover:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
        self.hover = hover

    def draw(self, surface):
        surface.blit(self.image, self.rect)
