import arcade

from presentation.views.menu_view import MenuView


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        menu_view = MenuView()
        self.show_view(menu_view)
