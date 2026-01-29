import arcade
from arcade.camera import Camera2D
from pyglet.graphics import Batch

from gameplay_presentation import const
from gameplay_presentation.game_logic import Logic

SCREEN_TITLE = "Real Jump"


class Level(arcade.View):
    def __init__(self, map_path):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.map_path = map_path
        self.setup()

    def setup(self):
        self.player = arcade.Sprite(
            ":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png",
            scale=0.5)
        self.tile_map = arcade.load_tilemap(
            self.map_path,
            scaling=0.5)
        self.player.center_x = 100
        self.player.center_y = 100
        self.checkpoint_x = self.player.center_x
        self.checkpoint_y = self.player.center_y
        self.spawn_point = (self.checkpoint_x, self.checkpoint_y)
        self.player_spritelist = arcade.SpriteList()
        self.player_spritelist.append(self.player)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.score = 0
        self.batch = Batch()
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = const.MAX_JUMPS
        self.logics = Logic(self.scene, self.window)
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()
        """обьединяем спрайты с колизией в один список для передачи 
               ,как параметр wall в физ.движок"""
        self.collisions = arcade.SpriteList()

        for elem in self.scene['doors_red']:
            self.collisions.append(elem)

        for elem in self.scene['doors_yellow']:
            self.collisions.append(elem)

        for elem in self.scene['doors_blue']:
            self.collisions.append(elem)

        for elem in self.scene['walls']:
            self.collisions.append(elem)

        # Физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=const.GRAVITY,
            walls=self.collisions,
            ladders=self.scene['ladders']
        )

    def on_draw(self):
        self.clear()
        self.world_camera.use()  # Активируем камеру для игрового мира
        self.batch.draw()
        self.player_spritelist.draw()
        self.scene.draw()
        self.player_spritelist.draw()

    def on_update(self, delta_time):

        """лестницы"""
        on_ladder = self.physics_engine.is_on_ladder()  # На лестнице?
        if on_ladder:
            # По лестнице вверх/вниз
            if self.up and not self.down:
                self.player.change_y = const.LADDER_SPEED
            elif self.down and not self.up:
                self.player.change_y = -const.LADDER_SPEED
            else:
                self.player.change_y = 0

        self.player.change_y -= const.GRAVITY
        move = 0
        if self.left and not self.right:
            move = -const.MOVE_SPEED
        elif self.right and not self.left:
            move = const.MOVE_SPEED
        self.player.change_x = move
        # Прыжок: can_jump() + койот + буфер
        grounded = self.physics_engine.can_jump(y_distance=6)  # Есть пол под ногами?
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = const.MAX_JUMPS
        else:
            self.time_since_ground += delta_time

        # Учтём «запомненный» пробел
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        # Можно прыгать, если стоим на земле или в пределах койот-времени
        if want_jump:
            can_coyote = (self.time_since_ground <= const.COYOTE_TIME)
            if grounded or can_coyote:
                # Просим движок прыгнуть: он корректно задаст начальную вертикальную скорость
                self.physics_engine.jump(const.JUMP_SPEED)
                self.jump_buffer_timer = 0

        # Обновляем физику — движок сам двинет игрока и платформы
        self.physics_engine.update()

        # вызываем логику объектов
        self.checkpoint_x, self.checkpoint_y = self.logics.checkpoints_flag('checkpoint', self.player,
                                                                            self.checkpoint_x, self.checkpoint_y)
        self.logics.hazard('hazards', self.player, self.checkpoint_x, self.checkpoint_y)
        self.logics.keys_logic('keys_blue', 'doors_blue', self.player, self.collisions)
        self.logics.keys_logic('keys_yellow', 'doors_yellow', self.player, self.collisions)
        self.logics.keys_logic('keys_red', 'doors_red', self.player, self.collisions)
        self.score = self.logics.coins_logic('coins', self.score, self.player)
        self.logics.trampoline_logic('trampolines', self.player, const.JUMP_SPEED * 2)
        self.logics.level_finished('finish_flag', self.player, self.score)
        self.text = arcade.Text(f'Score: {self.score}',
                                10, self.height - 30, arcade.color.WHITE,
                                24, batch=self.batch)
        position = (
            self.player.center_x + const.SCREEN_WIDTH // 12,
            self.player.center_y + 150
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            const.CAMERA_LERP,  # Плавность следования камеры
        )
        self.scene.get_sprite_list("walls_back_base").color = (128, 128, 128)

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
            self.jump_buffer_timer = const.JUMP_BUFFER

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
