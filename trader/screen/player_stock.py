
from trader import ui
from .base import BaseScreen

class PlayerStockScreen(BaseScreen):
    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def keydown(self, key):
        super().keydown(key)

    def paint(self):
        ui.cls()
        pass
