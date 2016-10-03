
from trader import ui
from .base import BaseScreen

class PlayerStockScreen(BaseScreen):

    screen_name = 'player_stock'

    def __init__(self, app, player, company_db):
        super().__init__(app)
        self.player = player
        self.company_db = company_db

    def keydown(self, key):
        super().keydown(key)

    def paint(self):
        ui.cls()
        pos = 2
        for symbol,quantity in self.player:
            company = self.company_db.lookup(symbol)
            #ui.drawtext(0, pos, symbol)
            
            text = "%10s %5d %5d"%(company.name, quantity, quantity*company.stock.value)
            ui.drawtext(0, pos, text)

            pos += 1

        ui.drawtext(0, 0, "Player Stock")
