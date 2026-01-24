import arcade


class Logic:
    def __init__(self, scene):
        self.scene = scene

    def keys_logic(self, keys, doors, player, collisions):
        """логика дверей и ключей"""
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{keys}'])) > 0:
            for elem in self.scene[f'{doors}']:
                collisions.remove(elem)
            self.scene[f'{doors}'].clear()
            self.scene[f'{keys}'].clear()

    def coins_logic(self, coins, score, player):
        check_coins = arcade.check_for_collision_with_list(player, self.scene[f'{coins}'])
        for coin in check_coins:
            self.scene[f'{coins}'].remove(coin)
            score += 1
        return score

    def trampoline_logic(self, trampoline, player, speed):
        if len(arcade.check_for_collision_with_list(player, self.scene[f'{trampoline}'])) > 0:
            player.change_y = speed
