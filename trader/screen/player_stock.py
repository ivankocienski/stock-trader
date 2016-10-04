
from trader import ui
from .base import BaseScreen

class PlayerStockScreen(BaseScreen):

    screen_name = 'player_stock'

    def __init__(self, app, player, company_db):
        super().__init__(app)
        self.player = player
        self.company_db = company_db

        self.table = ui.Table(0, 1, 100, 34)

        self.table.add_column("Name", 30)
        self.table.add_column("Symbol", 10)
        self.table.add_column("Owned", 10, True)
        self.table.add_column("Value", 10, True)

    def keydown(self, key):
        super().keydown(key)

    def paint(self):
        ui.cls()

        self.table.start_render()

        pos = 0
        symbols = self.player.owned_stock_symbols() 

        while self.table.needs_rendering():
            if pos >= len(symbols):
                break
    
            sym  = symbols[pos]
            com  = self.company_db.lookup(sym)
            owns = self.player.owned_stock[sym]

            company_data = (
                    com.name,
                    sym,
                    str(owns),
                    str(owns * com.stock.value))
                    
            self.table.render_next_row(company_data)

            pos += 1



#        for symbol,quantity in self.player:
#            company = self.company_db.lookup(symbol)
#            #ui.drawtext(0, pos, symbol)
#            
#            text = "%10s %5d %5d"%(company.name, quantity, quantity*company.stock.value)
#            ui.drawtext(0, pos, text)
#
#            pos += 1

        ui.drawtext(0, 0, "Player Stock")
