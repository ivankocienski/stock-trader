
from trader import ui

class BaseScreen:
    screen_name = 'none'

    def __init__(self, app):
        self.app = app
        
    def keydown(self, key):
        if key == ui.key_f1:
            self.app.set_screen("company_list")

        elif key == ui.key_f2:
            self.app.set_screen("player_stock")

    def activate(self, data):
        print("activating '%s'"%self.__class__.__name__)
        self.app.repaint()

    def paint(self):
        pass


