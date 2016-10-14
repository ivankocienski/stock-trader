
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

    def keydown(self, key):
        super().keydown(key)
        
        if key == ui.key_escape:
            self.app.set_screen('return')

    def paint(self):

        ui.cls()

        ui.drawtext(0, 0, "Company Information")
        ui.drawtext(0, 1, '"%s" %s'%(self.company.name, self.company.symbol))

