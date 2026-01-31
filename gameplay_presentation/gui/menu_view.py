from functools import partial

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UIFlatButton, UILabel

from gameplay_presentation.game import Level
from gameplay_presentation.gui.results_view import ResultsView


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ORANGE

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        title_label = UILabel(
            text="Platformer game",
            font_size=18,
            text_color=arcade.color.BLACK
        )
        level_button1 = UIFlatButton(
            text="Уровень 1",
            width=350,
            height=100,
            color=arcade.color.BRICK_RED
        )
        level_button1.on_click = partial(self.switch_view, button=1)

        level_button2 = UIFlatButton(
            text="Уровень 2",
            width=350,
            height=100,
            color=arcade.color.BRICK_RED
        )
        level_button2.on_click = partial(self.switch_view, button=2)

        results_button = UIFlatButton(
            text="История результатов",
            width=350,
            height=100,
            color=arcade.color.BRICK_RED
        )
        results_button.on_click = partial(self.switch_view, button=4)

        self.box_layout.add(title_label)
        self.box_layout.add(level_button1)
        self.box_layout.add(level_button2)
        self.box_layout.add(results_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def switch_view(self, events, button):
        if button == 1:
            self.game_view = Level(map_path='assets/level1.tmx')
            self.window.show_view(self.game_view)
        elif button == 2:
            self.game_view = Level(map_path='assets/level2.tmx')
            self.window.show_view(self.game_view)
        elif button == 4:
            results_view = ResultsView()
            self.window.show_view(results_view)
