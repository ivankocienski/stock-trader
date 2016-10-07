
from trader import ui
from .base  import BaseScreen
from .trade_stock import Trade

class CompanyListScreen(BaseScreen):

    screen_name = 'company_list'

    def __init__(self, app, company_list, player):
        super().__init__(app)
        self.company_list = company_list
        self.player = player
        self.table = ui.Table(0, 1, 100, 34)

        self.table.add_column("Name", 30)
        self.table.add_column("Symbol", 10)
        self.table.add_column("Volume", 10, True)
        self.table.add_column("Price", 10, True)
    
    def activate(self, data):
        super().activate(data)
        self.symbol_index = self.company_list.symbols()
        self.symbol_index_top = 0
        self.current_pos = 0

    def keydown(self, key):
        super().keydown(key)

        if key == ui.key_up and self.current_pos > 0:
            self.current_pos -= 1
            self.app.repaint()

        if key == ui.key_down and self.current_pos < len(self.symbol_index)-1:
            self.current_pos += 1
            self.app.repaint()

        if key == ui.key_b:
            symbol  = self.symbol_index[self.current_pos]
            trade = Trade(
                player  = self.player,
                company = self.company_list.lookup(symbol),
                mode    = 'buy')

            self.app.set_screen(
                    "trade_stock", 
                    return_to="company_list",
                    data = trade)

        # adjust top of view
        if self.current_pos < self.symbol_index_top:
            self.symbol_index_top = self.current_pos

        if self.current_pos > (self.symbol_index_top+32):
            self.symbol_index_top = self.current_pos-32
        
    def paint(self):

        ui.cls()
        self.table.start_render()

        pos = 0
        while self.table.needs_rendering():
            if pos >= len(self.symbol_index) or pos >= 33:
                break

            sym = self.symbol_index[pos + self.symbol_index_top]
            com = self.company_list.lookup(sym)

            company_data = (
                    com.name,
                    sym,
                    com.share_count,
                    com.share_value)
                    
            if pos == self.current_pos - self.symbol_index_top:
                ui.set_fg_color(ui.BLACK)
                ui.set_bg_color(ui.GREEN)
            else:
                ui.set_fg_color(ui.GREEN)
                ui.set_bg_color(ui.BLACK)

            self.table.render_next_row(company_data)

            pos += 1


        ui.set_fg_color(ui.GREY)
        ui.set_bg_color(ui.BLACK)

        ui.draw_hline(0, 35, 100)

        ui.drawtext(0, 36, "Funds=%i Value=%i Date=000"%(self.player.funds, self.player.total_value()))

