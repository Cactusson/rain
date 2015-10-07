"""
All of the easing functions used in the game.
Got them from:
https://github.com/danro/jquery-easing/blob/master/jquery.easing.js
"""

import math


def ease_out_back(t, b, c, d, s=1.70158):
    t = t / d - 1
    return c * (t * t * ((s + 1) * t + s) + 1) + b


def ease_in_back(t, b, c, d, s=1.70158):
    t /= d
    return c * t * t * ((s + 1) * t - s) + b


def ease_in_expo(t, b, c, d):
    if t == 0:
        return b
    else:
        return c * math.pow(2, 10 * (t / d - 1)) + b


def ease_out_bounce(t, b, c, d):
    t /= d
    if (t < (1/2.75)):
        return c*(7.5625*t*t) + b
    elif (t < (2/2.75)):
        t -= (1.5/2.75)
        return c*(7.5625*(t)*t + .75) + b
    elif (t < (2.5/2.75)):
        t -= (2.25/2.75)
        return c*(7.5625*(t)*t + .9375) + b
    else:
        t -= (2.625/2.75)
        return c*(7.5625*(t)*t + .984375) + b


def ease_in_out_sine(t, b, c, d):
    return -c / 2 * (math.cos(math.pi * t / d) - 1) + b


def ease_out_elastic(t, b, c, d):
        s = 1.70158
        p = 0
        a = c
        if t == 0:
            return b
        t /= d
        if t == 1:
            return b+c
        if p == 0:
            p = d * .3
        if a < abs(c):
            a = c
            s = p/4
        else:
            s = p / (2 * math.pi) * math.asin(c / a)
        return a * math.pow(2, -10 * t) * math.sin((t * d - s) * (
            2 * math.pi) / p) + c + b
