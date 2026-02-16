import math
import random

import arcade


class CoinParticle(arcade.SpriteCircle):
    def __init__(self, x, y):
        color = random.choice([
            (192, 192, 192, 255),
            (255, 200, 0, 255),
            (255, 255, 0, 255),
        ])
        size = random.randint(4, 8)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        self.alpha = 255
        self.lifetime = random.uniform(0.5, 1.0)
        self.time_alive = 0
        self.scale = 1.0

    def update(self, dt):
        self.change_y -= 0.2
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.alpha -= 3
        self.scale_x *= 0.98
        self.scale_y *= 0.98

        self.time_alive += dt

        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()


class TrampolineParticle(arcade.SpriteCircle):
    def __init__(self, x, y):
        color = random.choice([
            (66, 170, 255),
            (62, 95, 138),
            (154, 206, 235),
        ])
        size = random.randint(3, 5)
        super().__init__(size, color)
        self.center_x = x
        self.center_y = y

        base_speed = random.uniform(8, 11)
        horizontal_drift = random.uniform(-1.5, 1.5)

        self.change_x = horizontal_drift
        self.change_y = base_speed

        self.acceleration_x = random.uniform(-0.1, 0.1)
        self.acceleration_y = random.uniform(0.2, 0.3)

        self.alpha = 255
        self.lifetime = random.uniform(0.5, 1.0)
        self.time_alive = 0
        self.scale = 1.0

    def update(self, delta_time):
        self.time_alive += delta_time

        self.change_x += self.acceleration_x * delta_time
        self.change_y += self.acceleration_y * delta_time

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.alpha -= 3

        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()
