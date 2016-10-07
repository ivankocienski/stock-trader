
from trader import ui
from .base  import BaseScreen
from .trade_stock import Trade

class CompanyListScreen(BaseScreen):

    screen_name = 'company_list'

    def __init__(self, app, company_list, player):
        super().__init__(app)
        self.company_list = company_list
        self.current_pos = 0
        self.player = player
        self.table = ui.Table(0, 1, 100, 34)

        self.table.add_column("Name", 30)
        self.table.add_column("Symbol", 10)
        self.table.add_column("Volume", 10, True)
        self.table.add_column("Price", 10, True)

    def keydown(self, key):
        super().keydown(key)

        if key == ui.key_up and self.current_pos > 0:
            self.current_pos -= 1
            self.app.repaint()

        if key == ui.key_down and self.current_pos < self.company_list.count()-1:
            self.current_pos += 1
            self.app.repaint()

        if key == ui.key_b:
            symbol  = self.company_list.symbols()[self.current_pos]
            trade = Trade(
                player  = self.player,
                company = self.company_list.lookup(symbol),
                mode    = 'buy')

            self.app.set_screen(
                    "trade_stock", 
                    return_to="company_list",
                    data = trade)

    def paint(self):

        ui.cls()

        pos = 0

        self.table.start_render()

        symbols = self.company_list.symbols()

        while self.table.needs_rendering():
            if pos >= len(symbols):
                break

            com = self.company_list.lookup(symbols[pos])

            company_data = (
                    com.name,
                    com.symbol,
                    str(com.share_count),
                    str(com.share_value))
                    
            if pos == self.current_pos:
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

