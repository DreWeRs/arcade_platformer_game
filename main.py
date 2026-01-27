import arcade

from gameplay_presentation.window import MainWindow


def setup_game(width, height, title):
    main_window = MainWindow(width, height, title)
    main_window.setup()
    return main_window


def main():
    setup_game(900, 500, "Platformer game")
    arcade.run()


if __name__ == "__main__":
    main()
