
from trader import ui
from .base  import BaseScreen

class CompanyListScreen(BaseScreen):

    screen_name = 'company_list'

    def __init__(self, app, company_list, player):
        super().__init__(app)
        self.company_list = company_list
        self.current_pos = 0
        self.player = player

    def activate(self):
        super().activate()

        def popup_done():
            print("The popup has been hidden")

        self.app.popup_message("Hello, World", "You have done a bad bad bad thing here", popup_done)

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
            company = self.company_list.lookup(symbol)
            self.app.screen_objects['buy_stock'].company = company
            self.app.set_screen("buy_stock", "company_list")

    def paint(self):

        ui.cls()

        pos = 0
        for c in self.company_list:
            if pos == self.current_pos:
                ui.set_fg_color(ui.BLACK)
                ui.set_bg_color(ui.GREEN)
            else:
                ui.set_fg_color(ui.GREEN)
                ui.set_bg_color(ui.BLACK)

            ui.drawtext(0, pos, c.name)
            pos += 1


        ui.set_fg_color(ui.GREY)
        ui.set_bg_color(ui.BLACK)
        ui.draw_hline(0, 35, 50)
        ui.draw_vline(29, 10, 10)

        ui.draw_box(5, 5, 20, 10)
        ui.drawtext(6, 6, "Hello")
        ui.drawtext(24, 14, "Goodbye")

        ui.drawtext(0, 36, "Funds=%i Value=%i Date=000"%(self.player.funds, self.player.total_value()))

