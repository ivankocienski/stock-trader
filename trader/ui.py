
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
key_down = pg.K_DOWN
key_f1   = pg.K_F1
key_f2   = pg.K_F2

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





