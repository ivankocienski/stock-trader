
# wrapper for boring SDL stuff

import pygame as pg

# char size is 8x14

CHAR_WIDTH = 8
CHAR_HEIGHT = 14

WHITE  = (255, 255, 255)
GREY   = (180, 180, 180)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (200, 255,   0)
BLUE   = ( 50,  50, 255)

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
key_s    = pg.K_s
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
    y *= 14

    text_surface = font.render(msg, False, color_fg, color_bg) 
    screen.blit(text_surface, (x, y))

def fill_box(x, y, w, h):
    global screen
    global color_bg

    x = x *  8
    y = y * 14

    w = (w+1) * 8
    h = (h+1) * 14

    screen.fill(color_bg, (x, y, w, h))

def draw_hline(x, y, length):
    x *= 8
    length *= 8 
    y = y * 14 + 7

    global screen
    global color_fg

    pg.draw.line(screen, color_fg, (x, y), (x+length, y), 1)

def draw_vline(x, y, length):
    global screen
    global color_fg

    y *= 14
    length *= 14
    x = x * 8 + 4 

    pg.draw.line(screen, color_fg, (x, y), (x, y+length), 2)


def draw_box(x, y, w, h):
    global screen
    global color_fg

    x = x *  8 + 4 
    y = y * 14 + 7

    w *= 8
    h *= 14

    pg.draw.line(screen, color_fg, (x, y), (x, y+h), 2)
    pg.draw.line(screen, color_fg, (x+w, y), (x+w, y+h), 2)

    pg.draw.line(screen, color_fg, (x, y), (x+w, y), 1)
    pg.draw.line(screen, color_fg, (x, y+h), (x+w, y+h), 1)





class Table:
    """ renders a spreadsheet like table """

    def __init__(self, start_x, start_y, max_width, max_height):
        self.columns    = []
        self.start_x    = start_x
        self.start_y    = start_y
        self.max_width  = max_width
        self.max_height = max_height

    def add_column(self, name, width, right_align=False):
        self.columns.append((name, width, right_align))

    def start_render(self):
        formatter = '|'
        column_names = []
        for col in self.columns:
            formatter += ' '
            if col[2]: # right align?
                formatter += '%%%ds'%col[1] 
            else:
                formatter += '%%-%ds'%col[1] 

            formatter += ' |'
            
            column_names.append(col[0])
        
        self.formatter = formatter
        self.ypos = self.start_y
        drawtext(self.start_x, self.ypos, formatter%tuple(column_names))
        self.ypos += 1

    def needs_rendering(self):
        return self.ypos <= self.start_y+self.max_height

    def render_next_row(self, row_data, highlight=False):
        print_row = []
        pos = 0
        for data in row_data:
            column = self.columns[pos]
            print_row.append(str(data)[:column[1]])
            pos += 1

        drawtext(self.start_x, self.ypos, self.formatter%tuple(print_row))
        self.ypos += 1

class Graph:
    def __init__(self, min_y, val_range):
        self.min_y = min_y
        self.val_range = val_range

    def draw_line(self, x1, y1, x2, y2, color=(255, 255, 255)):
        global screen

        if self.val_range == 0:
            return 

        y_high = (y1 - self.min_y) / self.val_range 
        y_high = 600 - int(y_high * 600)

        y_low  = (y2 - self.min_y) / self.val_range 
        y_low  = 600 - int(y_low * 600)

        p1 = (x1, y_high)
        p2 = (x2, y_low)

        pg.draw.line(screen, color, p1, p2)

    def fill_box(self, x1, y1, x2, y2, color=(255, 255, 255)):
        global screen

        if self.val_range == 0:
            return 

        y1 = (y1 - self.min_y) / self.val_range
        y1 = 600 - int(y1 * 600)

        y2 = (y2 - self.min_y) / self.val_range
        y2 = 600 - int(y2 * 600)

        if y1 > y2:
            y1, y2 = y2, y1

        height = y2 - y1
        width  = x2 - x1

        rect = (x1, y1, width, height)
        screen.fill(color, rect)

