import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

from gameplay_presentation.gui import menu_view


class ResultsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.ORANGE

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout(row_count=2)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        csv_manager = self.window.csv_manager
        self.results = csv_manager.load_from_csv()

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        header_label = UILabel(
            text=f'Счет | Дата',
            text_color=arcade.color.BLACK,
            font_size=24
        )
        self.box_layout.add(header_label)

        for row in self.results:
            label = UILabel(
                text=f'{row[0]} | {row[1]}',
                text_color=arcade.color.BLACK,
                font_size=24
            )
            self.box_layout.add(label)

        return_button = UIFlatButton(
            text="Вернуться в меню",
            width=350,
            height=100,
            color=arcade.color.OUTER_SPACE,
        )
        return_button.on_click = self.return_to_menu
        self.box_layout.add(return_button)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def return_to_menu(self, events):
        self.window.show_view(menu_view.MenuView())
