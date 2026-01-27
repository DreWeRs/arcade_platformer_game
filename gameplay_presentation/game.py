import arcade
from pyglet.graphics import Batch

from gameplay_presentation.game_logic import Logic

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
# Физика и движение
GRAVITY = 1  # Пикс/с^2
MOVE_SPEED = 6  # Пикс/с
JUMP_SPEED = 20  # Начальный импульс прыжка, пикс/с
LADDER_SPEED = 4
# Качество жизни прыжка
COYOTE_TIME = 0.08  # Сколько после схода с платформы можно ещё прыгнуть
JUMP_BUFFER = 0.12  # Если нажали прыжок чуть раньше приземления, мы его «запомним» (тоже лайфхак для улучшения качества
MAX_JUMPS = 1  # С двойным прыжком всё лучше, но не сегодня
SCREEN_TITLE = "Real Jump"


class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()

    def setup(self):
        self.player = arcade.Sprite(
            ":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png",
            scale=0.5)
        self.tile_map = arcade.load_tilemap(
            "assets/level1.tmx",
            scaling=0.5)  # Во встроенных ресурсах есть даже уровни!
        self.player.center_x = 100
        self.player.center_y = 100
        self.player.health_points = 3
        self.player_spritelist = arcade.SpriteList()
        self.player_spritelist.append(self.player)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.score = 0
        self.batch = Batch()
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
        self.logics = Logic(self.scene)
        """обьединяем спрайты с колизией в один список для передачи 
               ,как параметр wall в физ.движок"""
        self.collisions = arcade.SpriteList()
        for elem in self.scene['doors_red']:
            self.collisions.append(elem)

        for elem in self.scene['doors_yellow']:
            self.collisions.append(elem)

        for elem in self.scene['walls']:
            self.collisions.append(elem)

        # Физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            walls=self.collisions,
            ladders=self.scene['ladders']
        )

    def on_draw(self):
        self.clear()
        self.player_spritelist.draw()
        self.scene.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        """лестницы"""
        on_ladder = self.physics_engine.is_on_ladder()  # На лестнице?
        if on_ladder:
            # По лестнице вверх/вниз
            if self.up and not self.down:
                self.player.change_y = LADDER_SPEED
            elif self.down and not self.up:
                self.player.change_y = -LADDER_SPEED
            else:
                self.player.change_y = 0

        self.player.change_y -= GRAVITY
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move
        # Прыжок: can_jump() + койот + буфер
        grounded = self.physics_engine.can_jump(y_distance=6)  # Есть пол под ногами?
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += delta_time

        # Учтём «запомненный» пробел
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        # Можно прыгать, если стоим на земле или в пределах койот-времени
        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                # Просим движок прыгнуть: он корректно задаст начальную вертикальную скорость
                self.physics_engine.jump(JUMP_SPEED)
                self.jump_buffer_timer = 0

        # Обновляем физику — движок сам двинет игрока и платформы
        self.physics_engine.update()
        # вызываем логику объектов
        self.logics.keys_logic('keys_yellow', 'doors_yellow', self.player, self.collisions)
        self.logics.keys_logic('keys_red', 'doors_red', self.player, self.collisions)
        self.score = self.logics.coins_logic('coins', self.score, self.player)
        self.logics.trampoline_logic('trampolines', self.player, JUMP_SPEED * 2)

        self.text = arcade.Text(f'Score: {self.score}',
                                10, self.height - 30, arcade.color.WHITE,
                                24, batch=self.batch)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key == arcade.key.SPACE:
            self.jump_pressed = False
            # Вариативная высота прыжка: отпустили рано — подрежем скорость вверх
            if self.player.change_y > 0:
                self.player.change_y *= 0.45
