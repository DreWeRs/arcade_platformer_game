import arcade

from gameplay_presentation import const
from gameplay_presentation.window import MainWindow
from utilities.csv_manager import CSVManager
from utilities.sounds_manager import SoundsManager


def setup_game(width, height, title):
    window = MainWindow(width, height, title)
    window.setup()

    sounds_manager = SoundsManager()
    csv_manager = CSVManager(file_path='results_list.csv')

    window.sounds_manager = sounds_manager
    window.csv_manager = csv_manager
    return window


def main():
    setup_game(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, "Platformer game")
    arcade.run()


if __name__ == "__main__":
    main()
