import os
import sys
import pygame as pg

from . import tools


SCREEN_SIZE = (800, 600)
ORIGINAL_CAPTION = 'Rain'

BG_COLOR = pg.Color('#BFE9DB')
GUI_BG_COLOR = pg.Color('#6AC1B8')
# FRAME_COLOR = pg.Color('#07588A')

pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

if getattr(sys, 'frozen', False):
    # The application is frozen
    fonts_path = os.path.join(os.path.dirname(sys.executable), 'fonts')
    graphics_path = os.path.join(os.path.dirname(sys.executable), 'graphics')
else:
    # The application is not frozen
    fonts_path = os.path.join('resources', 'fonts')
    graphics_path = os.path.join('resources', 'graphics')

FONTS = tools.load_all_fonts(fonts_path)
GFX = tools.load_all_gfx(graphics_path)
