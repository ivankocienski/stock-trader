
# wrapper for boring SDL stuff

import pygame as pg

WHITE  = (255, 255, 255)
GREY   = (180, 180, 180)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (200, 255,   0)
BLUE   = (100, 100, 255)

screen = None
font   = None

color_bg = BLACK
color_fg = WHITE

key_up = pg.K_UP
key_escape = pg.K_ESCAPE
key_enter  = pg.K_RETURN
key_down = pg.K_DOWN
key_f1   = pg.K_F1
key_f2   = pg.K_F2
key_b    = pg.K_b
key_backspace = pg.K_BACKSPACE

key_0    = pg.K_0
key_1    = pg.K_1
key_2    = pg.K_2
key_3    = pg.K_3
key_4    = pg.K_4
key_5    = pg.K_5
key_6    = pg.K_6
key_7    = pg.K_7
key_8    = pg.K_8
key_9    = pg.K_9

def init(s):
    global screen
    global font
    screen = s

    font = pg.font.Font("data/vga.ttf", 16)

def cls():
    global screen 
    screen.fill((0,0,0))

def set_bg_color(c):
    global color_bg
    color_bg = c

def set_fg_color(c):
    global color_fg
    color_fg = c

def drawtext(x, y, msg):
    global screen
    global font
    global color_fg

    x *= 8
    y *= 16

    text_surface = font.render(msg, False, color_fg, color_bg) 
    screen.blit(text_surface, (x, y))





