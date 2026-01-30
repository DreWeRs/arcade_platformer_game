import arcade


class SoundsManager:
    """вынесено из presentation для того чтобы не забивать папку, в utilites то что имеет минимум зависимостей"""
    def __init__(self):
        self.level_complete_sound = arcade.load_sound('assets/sounds/level-complete-sound.wav')
        self.damage_sound = arcade.load_sound('assets/sounds/damage-sound.wav')
