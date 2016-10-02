
from trader import ui
from .base import BaseScreen

class PlayerStockScreen(BaseScreen):

    screen_name = 'player_stock'

    def __init__(self, app, player):
        super().__init__(app)
        self.player = player

    def keydown(self, key):
        super().keydown(key)

    def paint(self):
        ui.cls()
        ui.drawtext(0, 0, "Player Stock")
