#!/usr/bin/python

import pygame as pg

import trader.ui as ui

from trader.screen.company_list import CompanyListScreen
from trader.screen.player_stock import PlayerStockScreen
from trader.screen.buy_stock import BuyStockScreen

from trader.model.company import Company, CompanyDB
from trader.model.player  import Player

class App:

    class Popup:
        def __init__(self, app):
            self.active = False
            self.app = app

        def show(self, t1, t2, callback):
            self.text1 = t1
            self.text2 = t2
            self.active = True
            self.callback = callback

        def keydown(self, key):
            if key == ui.key_escape:
                self.active = False
                if self.callback:
                    self.callback()

                self.app.repaint()

        def is_active(self):
            return self.active

        def paint(self):
            width1 = len(self.text1)
            height = 2
            if self.text2:
                height += 2
                width2 = len(self.text2)

            width = width1
            if self.text2 and width2 > width:
                width = width2

            width += 16

            ui.set_bg_color(ui.BLUE)
            ui.fill_box((100-width)/2, 16, width, height)

            ui.drawtext( (100-width1)/2, 17, self.text1)
            if(self.text2):
                ui.drawtext( (100-width2)/2, 19, self.text2)

            ui.draw_box((100-width)/2, 16, width, height)
            ui.set_bg_color(ui.BLACK)


    def _register_screen(self, obj):
        print("Registered screen '%s'" % obj.screen_name)
        self.screen_objects[obj.screen_name] = obj

    def __init__(self):
        pg.init()
        pg.font.init()

        self._popup = self.Popup(self)
        self.companies = CompanyDB()
        self.player = Player(self.companies)

        self.companies.register("C1", "Company 1", 100, 100)
        self.companies.register("C2", "Company 2", 100, 100)
        self.companies.register("C3", "Company 3", 100, 100)

        self.screen = pg.display.set_mode((800, 600))
        self.screen_objects = dict()

        self._register_screen(BuyStockScreen(self, self.player)) 

        self._register_screen(
            CompanyListScreen(
                self, 
                self.companies, 
                self.player))

        self._register_screen(
            PlayerStockScreen(
                self,
                self.player))

        self.set_screen("company_list")

    def repaint(self):
        self._repaint = True

    def popup_message(self, text1, text2=None, callback=None):
        self._popup.show(text1, text2, callback)
        self.repaint()

    def set_screen(self, name, old_screen=None): 
        if name == 'old':
            name = self.old_screen

        if name in self.screen_objects:
            self.current_screen = self.screen_objects[name]
            
        else:
            raise RuntimeError("screen not found '%s'"%name)

        self.old_screen = old_screen
        self.current_screen.activate()

    def run(self):
        print("starting")

        ui.init(self.screen)

        run_loop = True
        self.repaint()

        while run_loop:

            pg.time.wait(10) # don't cane the CPU

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run_loop = False

                if event.type == pg.KEYDOWN:
                    if self._popup.is_active():
                        self._popup.keydown(event.key)
                    else:
                        self.current_screen.keydown(event.key)
                    continue

            if(self._repaint):
                self.current_screen.paint()
                if self._popup.is_active():
                    self._popup.paint()

                pg.display.flip()
                self._repaint = False

if __name__ == '__main__': App().run()
