import arcade

from gameplay_presentation.menu_view import MenuView


class MainWindow(arcade.Window):
    """Класс основного окна чтобы потом удобно оперировать образами (view)"""
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        menu_view = MenuView()
        self.show_view(menu_view)
