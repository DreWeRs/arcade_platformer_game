import arcade

from presentation.game import Game


def setup_game(width, height, title):
    game = Game(width, height, title)
    game.setup()
    return game


def main():
    setup_game(900, 500, "Platformer game")
    arcade.run()


if __name__ == "__main__":
    main()
