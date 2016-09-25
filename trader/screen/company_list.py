
from trader import ui
from .base  import BaseScreen

class CompanyListScreen(BaseScreen):

    def __init__(self, app, company_list, player):
        super().__init__(app)
        self.company_list = company_list
        self.current_pos = 0
        self.player = player

    def keydown(self, key):
        super().keydown(key)

        if key == ui.key_up and self.current_pos > 0:
            self.current_pos -= 1
            self.app.repaint()

        if key == ui.key_down and self.current_pos < len(self.company_list)-1:
            self.current_pos += 1
            self.app.repaint()

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
        ui.drawtext(0, 36, "Funds=%i Date=000"%self.player.funds)

