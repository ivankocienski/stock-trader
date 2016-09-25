import pygame as pg

import trader.ui as ui

from trader.screen.company_list import CompanyListScreen
from trader.screen.player_stock import PlayerStockScreen
from trader.model.company import Company
from trader.model.player  import Player

class App:

    def __init__(self):
        pg.init()
        pg.font.init()

        self.player = Player()

        self.companies = []
        self.companies.append(Company("Company 1", "C1", 100, 100))
        self.companies.append(Company("Company 2", "C2", 100, 100))
        self.companies.append(Company("Company 3", "C3", 100, 100))

        self.screen = pg.display.set_mode((800, 600))

        self.company_list_screen = CompanyListScreen(
                self, 
                self.companies, 
                self.player)

        self.player_stock_screen = PlayerStockScreen(
                self,
                self.player)
        self.set_screen("company_list")

    def repaint(self):
        self._repaint = True

    def set_screen(self, screen): 
        if screen == 'company_list':
            self.current_screen = self.company_list_screen
        elif screen == 'player_stock':
            self.current_screen = self.player_stock_screen
        else:
            raise RuntimeError("screen not found '%s'"%screen)

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
