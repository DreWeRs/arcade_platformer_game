import arcade


class GameView(arcade.View):
    def __init__(self, level_name):
        super().__init__()

    def on_draw(self):
        self.clear()
