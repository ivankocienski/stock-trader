
from trader import ui
from .base import BaseScreen

class Trade:
    def __init__(self, **kwargs):
        self.player  = kwargs['player']
        self.company = kwargs['company']
        self.mode    = kwargs['mode']

class TradeStockScreen(BaseScreen):

    screen_name = 'trade_stock'

    def __init__(self, app):
        super().__init__(app);
    
    def activate(self, data):
        super().activate(data)
        self.trade = data
        self.quantity_string = ''
        self.confirm_trade = False 

    def keydown(self, key):
        if key == ui.key_escape:
            self.app.set_screen('return')

        if not self.confirm_trade:
            if key == ui.key_0:
                self.quantity_string += '0'
                self.app.repaint()
                
            elif key == ui.key_1:
                self.quantity_string += '1'
                self.app.repaint()

            elif key == ui.key_2:
                self.quantity_string += '2'
                self.app.repaint()

            elif key == ui.key_3:
                self.quantity_string += '3'
                self.app.repaint()

            elif key == ui.key_4:
                self.quantity_string += '4'
                self.app.repaint()

            elif key == ui.key_5:
                self.quantity_string += '5'
                self.app.repaint()

            elif key == ui.key_6:
                self.quantity_string += '6'
                self.app.repaint()

            elif key == ui.key_7:
                self.quantity_string += '7'
                self.app.repaint()

            elif key == ui.key_8:
                self.quantity_string += '8'
                self.app.repaint()

            elif key == ui.key_9:
                self.quantity_string += '9'
                self.app.repaint()

            elif key == ui.key_backspace and len(self.quantity_string) > 0:
                self.quantity_string = self.quantity_string[0:len(self.quantity_string)-1]
                self.app.repaint()

        if key == ui.key_down:
            self.confirm_trade = True
            self.app.repaint()

        elif key == ui.key_up:
            self.confirm_trade = False
            self.app.repaint()

        if key == ui.key_enter and self.confirm_trade:

            company = self.trade.company
            player  = self.trade.player

            if self.trade.mode == 'sell':
                if player.sell_stock(company, int(self.quantity_string)):
                    self.app.set_screen('return')
                else:
                    self.app.popup_message("Insufficient stock")
            
            elif self.trade.mode == 'buy':
                
                if player.buy_stock(company, int(self.quantity_string)):
                    self.app.set_screen('return')
                else:
                    self.app.popup_message("Insufficient funds")
                    

        


    def paint(self):
        ui.cls()
        ui.set_fg_color(ui.GREY)
        ui.set_bg_color(ui.BLACK)

        if self.trade.mode == 'sell':
            ui.drawtext(0, 0, "Sell stock")
        elif self.trade.mode == 'buy':
            ui.drawtext(0, 0, "Buy stock")
        else:
            raise RuntimeError('Trade mode "%s" not valid, must be either "buy" or "sell"'%self.trade.mode)


        ui.drawtext(2, 2, "Company '%s'" % self.trade.company.name) 
        ui.drawtext(2, 4, "Share price: %d" % self.trade.company.share_value) 

        if self.confirm_trade:
            ui.set_fg_color(ui.GREY)
        else:
            ui.set_fg_color(ui.WHITE)
        
        ui.drawtext(2, 6, "Quantity: %s"%self.quantity_string)

        if self.confirm_trade:
            if len(self.quantity_string) > 0 and int(self.quantity_string) > 0:
                ui.set_fg_color(ui.GREEN)
            else:
                ui.set_fg_color(ui.RED)

        else:
            ui.set_fg_color(ui.GREY)

            
        ui.drawtext(0, 8, "Confirm order")

    
