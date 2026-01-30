import math
import random

import arcade


class Particle(arcade.SpriteCircle):
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
        self.change_y += 0.2
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.alpha -= 3
        self.scale_x *= 0.98
        self.scale_y *= 0.98

        self.time_alive += dt

        if self.time_alive >= self.lifetime or self.alpha <= 0:
            self.remove_from_sprite_lists()
