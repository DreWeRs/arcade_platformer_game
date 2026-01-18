import arcade


class GameView(arcade.View):
    def __init__(self, level_path):
        super().__init__()
        self.tile_map = arcade.load_tilemap(level_path)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # Когда будем писать логику то будем указывать спрайт листы через scene["Название слоя спрайтов"]

    def on_draw(self):
        self.clear()
