import pygame as pg

from .. import prepare


class Label(pg.sprite.Sprite):
    """
    Just some text.
    """
    def __init__(self, font_name, font_size, text, color, center=None,
                 topleft=None, bg=None):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        self.color = color
        self.text = text
        self.image = self.font.render(self.text, True, self.color, bg)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            message = 'Center or topleft should be among the kwargs of Label'
            raise ValueError(message)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
