#!/usr/bin/python

import pygame as pg

import trader.ui as ui

from trader.screen.company_list import CompanyListScreen
from trader.screen.player_stock import PlayerStockScreen
from trader.screen.buy_stock import BuyStockScreen

from trader.model.company import Company, CompanyDB
from trader.model.player  import Player

class App:

    def _register_screen(self, obj):
        print("Registered screen '%s'" % obj.screen_name)
        self.screen_objects[obj.screen_name] = obj

    def __init__(self):
        pg.init()
        pg.font.init()

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
                    self.current_screen.keydown(event.key)
                    continue

            if(self._repaint):
                self.current_screen.paint()

                pg.display.flip()
                self._repaint = False

if __name__ == '__main__': App().run()
