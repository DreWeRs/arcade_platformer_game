import arcade

from gameplay_presentation.gui.end_game_view import EndGameView
from utilities.particle import Particle


class Logic:
    def __init__(self, scene, window):
        self.scene = scene
        self.window = window

    def keys_logic(self, keys, doors, player, collisions):
        """логика дверей и ключей"""
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{keys}'])) > 0:
            for elem in self.scene[f'{doors}']:
                collisions.remove(elem)
            self.scene[f'{doors}'].clear()
            self.scene[f'{keys}'].clear()

    def coins_logic(self, coins, score, player):
        check_coins = arcade.check_for_collision_with_list(player, self.scene[f'{coins}'])
        particles = []
        for coin in check_coins:
            self.scene[f'{coins}'].remove(coin)
            score += 1

            for i in range(30):
                particle = Particle(coin.center_x, coin.center_y)
                particles.append(particle)

        return score, particles

    def trampoline_logic(self, trampoline, player, speed):
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{trampoline}'])) > 0:
            player.change_y = speed


    def checkpoints_flag(self, flag, player, checkpoint_x, checkpoint_y):
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{flag}'])) > 0:
            checkpoint_x, checkpoint_y = self.scene['checkpoint'][0].position
        return checkpoint_x, checkpoint_y

    def hazard(self, hazards, player, checkpoint_x, checkpoint_y):
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{hazards}'])) > 0:
            self.window.sounds_manager.damage_sound.play()
            player.center_x = checkpoint_x
            player.center_y = checkpoint_y

    def level_finished(self, finish_flag, player, score):
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{finish_flag}'])):
            self.window.sounds_manager.level_complete_sound.play()
            self.window.show_view(EndGameView(score))
