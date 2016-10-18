
from trader import ui
from .base  import BaseScreen

class CompanyInfoScreen(BaseScreen):

    screen_name = 'company_info'

    def __init__(self, app):
        super().__init__(app)
        self.company = None
    
    def activate(self, data):
        super().activate(data)
        self.company = data
        self.trading_periods = self.company.trading_periods()

    def keydown(self, key):
        super().keydown(key)
        
        if key == ui.key_escape:
            self.app.set_screen('return')

    def paint(self):

        ui.cls()

        max_value = self.trading_periods[0].val_high
        min_value = self.trading_periods[0].val_low

        for period in self.trading_periods[:80]:
            
            if period.val_low < min_value:
                min_value = period.val_low

            if period.val_high > max_value:
                max_value = period.val_high

        val_range = max_value - min_value
        graph = ui.Graph(min_value, val_range)
        width = 10
        xpos  = 799 - width

        for period in self.trading_periods[:80]:

            # body 
            color = (0, 255, 0)
            if period.val_open > period.val_close:
                color = (255, 0, 0)

            graph.fill_box(
                xpos,
                period.val_open,
                xpos+width,
                period.val_close,
                color)

            # stick
            x_pos = xpos + width / 2

            graph.draw_line(
                x_pos,
                period.val_high,
                x_pos,
                period.val_low)

            xpos -= width

            


        ui.drawtext(0, 0, "Company Information")
        ui.drawtext(0, 1, '"%s" %s'%(self.company.name, self.company.symbol))

