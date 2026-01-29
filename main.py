import arcade

from gameplay_presentation import const
from gameplay_presentation.window import MainWindow
from utilities.sounds_manager import SoundsManager


def setup_game(width, height, title):
    window = MainWindow(width, height, title)
    window.setup()

    sounds_manager = SoundsManager()
    window.sounds_manager = sounds_manager
    return window


def main():
    setup_game(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, "Platformer game")
    arcade.run()


if __name__ == "__main__":
    main()
