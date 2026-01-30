import arcade
from arcade.gui import UIManager, UIAnchorLayout, UILabel, UIFlatButton, UIBoxLayout

from gameplay_presentation.gui import menu_view
from utilities.get_date import get_date


class EndGameView(arcade.View):
    def __init__(self, score):
        super().__init__()
        arcade.set_background_color(arcade.color.CADMIUM_GREEN)
        self.window.default_camera.use()
        self.score = score

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=30)

        self.csv_manager = self.window.csv_manager

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        title_label = UILabel(
            text="Вы прошли уровень!",
            font_size=30,
            text_color=arcade.color.WHITE
        )
        score_label = UILabel(
            text=f'Ваш счёт: {self.score}',
            font_size=24,
            text_color=arcade.color.WHITE
        )
        return_button = UIFlatButton(
            text="Вернуться в меню",
            width=350,
            height=100,
            color=arcade.color.OUTER_SPACE,
        )

        return_button.on_click = self.return_to_menu

        self.box_layout.add(title_label)
        self.box_layout.add(score_label)
        self.box_layout.add(return_button)
        self.anchor_layout.add(title_label)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def return_to_menu(self, events):
        result = self.csv_manager.load_from_csv()
        result.append([self.score, get_date()])
        self.csv_manager.write_to_csv(result)
        self.window.show_view(menu_view.MenuView())
