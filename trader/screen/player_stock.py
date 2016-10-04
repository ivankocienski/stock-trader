
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

    def activate(self):
        super().activate()
        self.current_pos = 0
        self.player_symbols = self.player.owned_stock_symbols() 

    def keydown(self, key):
        super().keydown(key)

        if key == ui.key_up and self.current_pos > 0:
            self.current_pos -= 1
            self.app.repaint()

        if key == ui.key_down and self.current_pos < len(self.player_symbols)-1:
            self.current_pos += 1
            self.app.repaint()

#        if key == ui.key_b:
#            symbol  = self.company_list.symbols()[self.current_pos]
#            company = self.company_list.lookup(symbol)
#            self.app.screen_objects['buy_stock'].company = company
#            self.app.set_screen("buy_stock", "company_list")

    def paint(self):
        ui.cls()

        ui.set_fg_color(ui.GREY)
        ui.set_bg_color(ui.BLACK)
        ui.drawtext(0, 0, "Player Stock")

        self.table.start_render()

        pos = 0

        while self.table.needs_rendering():
            if pos >= len(self.player_symbols):
                break
    
            sym  = self.player_symbols[pos]
            com  = self.company_db.lookup(sym)
            owns = self.player.owned_stock[sym]

            company_data = (
                    com.name,
                    sym,
                    str(owns),
                    str(owns * com.stock.value))
                    
            if pos == self.current_pos:
                ui.set_fg_color(ui.BLACK)
                ui.set_bg_color(ui.GREEN)
            else:
                ui.set_fg_color(ui.GREEN)
                ui.set_bg_color(ui.BLACK)

            self.table.render_next_row(company_data)

            pos += 1

