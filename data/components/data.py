"""
Here are all the info that is used in the game.
Keys for user_input.
numpad_data for numpad, drop data and dividers for drops.
"""


import pygame as pg


keypad_keys = [
    pg.K_KP0, pg.K_KP1, pg.K_KP2, pg.K_KP3, pg.K_KP4,
    pg.K_KP5, pg.K_KP6, pg.K_KP7, pg.K_KP8, pg.K_KP9]

number_keys = [
    pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
    pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]

keys = [(keypad_key, number_key) for keypad_key, number_key
        in zip(keypad_keys, number_keys)]


numpad_data = [
    ('7', (576, 231), (50, 50)),
    ('8', (627, 231), (50, 50)),
    ('9', (678, 231), (50, 50)),
    ('4', (576, 282), (50, 50)),
    ('5', (627, 282), (50, 50)),
    ('6', (678, 282), (50, 50)),
    ('1', (576, 333), (50, 50)),
    ('2', (627, 333), (50, 50)),
    ('3', (678, 333), (50, 50)),
    ('0', (576, 384), (50, 50)),
    ('Del', (729, 231), (50, 101)),
    ('Enter', (729, 333), (50, 101)),
    ('Clear', (627, 384), (101, 50)),
]


drop_data = [
    {
        'signs': ['+', '-'],
        'add_bottom': 1,
        'add_top': 10,
    },
    {
        'signs': ['+', '-', '*', '/'],
        'add_bottom': 4,
        'add_top': 50,
        'multi_bottom': 2,
        'multi_first_top': 7,
        'multi_second_top': 4,
        'div_first_bottom': 4,
        'div_first_top': 20,
        'div_second_bottom': 2,
        'div_second_top': 4,
    },
    {
        'signs': ['+', '-', '*', '/'],
        'add_bottom': 20,
        'add_top': 200,
        'multi_bottom': 2,
        'multi_first_top': 20,
        'multi_second_top': 5,
        'div_first_bottom': 4,
        'div_first_top': 40,
        'div_second_bottom': 2,
        'div_second_top': 15,
    },
    {
        'signs': ['+', '-', '*', '/'],
        'add_bottom': 50,
        'add_top': 500,
        'multi_bottom': 2,
        'multi_first_top': 20,
        'multi_second_top': 20,
        'div_first_bottom': 4,
        'div_first_top': 100,
        'div_second_bottom': 2,
        'div_second_top': 40,
    }
    ]


def get_dividers(bottom, top):
    dividers = {}
    for number in range(bottom, top+1):
        for i in range(bottom+1, number):
            if number % i == 0:
                if number in dividers:
                    dividers[number].append(i)
                else:
                    dividers[number] = [i]
    return dividers


dividers = get_dividers(1, 40)
