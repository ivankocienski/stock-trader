
from trader import ui
from .base import BaseScreen
from .trade_stock import Trade

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

    def activate(self, data):
        super().activate(data)
        self.current_pos = 0
        self.symbol_index_top = 0
        self.player_symbols = self.player.owned_stock_symbols

    def keydown(self, key):
        super().keydown(key)

        if key == ui.key_up and self.current_pos > 0:
            self.current_pos -= 1
            self.app.repaint()

        if key == ui.key_down and self.current_pos < len(self.player_symbols)-1:
            self.current_pos += 1
            self.app.repaint()

        if key == ui.key_s:
            symbol = self.player_symbols[self.current_pos]
            trade = Trade(
                player  = self.player,
                company = self.company_db.lookup(symbol),
                mode    = 'sell')

            self.app.set_screen(
                    "trade_stock",
                    return_to="player_stock",
                    data=trade)

        # adjust top of view
        if self.current_pos < self.symbol_index_top:
            self.symbol_index_top = self.current_pos

        if self.current_pos > (self.symbol_index_top+32):
            self.symbol_index_top = self.current_pos-32

    def paint(self):
        ui.cls()

        ui.set_fg_color(ui.GREY)
        ui.set_bg_color(ui.BLACK)
        ui.drawtext(0, 0, "Player Stock")

        self.table.start_render()

        pos = 0

        while self.table.needs_rendering():
            if pos >= len(self.player_symbols) or pos >= 33:
                break

            sym  = self.player_symbols[pos+self.symbol_index_top]
            owns = self.player.retrieve(sym)

            company_data = (
                    owns.company.name,
                    sym,
                    str(owns.quantity),
                    str(owns.value()))
                    
            if pos == self.current_pos - self.symbol_index_top:
                ui.set_fg_color(ui.BLACK)
                ui.set_bg_color(ui.GREEN)
            else:
                ui.set_fg_color(ui.GREEN)
                ui.set_bg_color(ui.BLACK)

            self.table.render_next_row(company_data)

            pos += 1

