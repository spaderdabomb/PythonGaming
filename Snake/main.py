import arcade
import os
import collections
import time
import numpy as np
import random

from ArcadeCustom.CustomClasses import Rectangle, Circle
from ArcadeCustom.CustomMethods import collision_detection_rects

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "Snake"

SNAKE_BLOCK_WIDTH = 16
SNAKE_BLOCK_HEIGHT = 16
SNAKE_BLOCK_ANGLE = 0

COIN_BLOCK_WIDTH = 16
COIN_BLOCK_HEIGHT = 16
COIN_BLOCK_ANGLE = 0

MOVE_SPEED = 8
FPS = 60
FRAMES_PER_SQUARE = SNAKE_BLOCK_HEIGHT / MOVE_SPEED


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.AMAZON)

        self.shape_list = None

        self.setupbool = False
        self.frames_since_direction_change = 0
        self.frames_since_previous_tail_change = 0
        self.ready_for_direction_change = False
        self.fps = FPSCounter()

        self.coin = None
        self.coins_collected = 0
        self.scoretext_str = None
        self.scoretext = None

        self.snaketail_arr = []
        self.current_direction_arr = []
        self.snaketail_pos_arr = []
        self.shape_list = []

        self.tempy = 0

    def setup(self):
        """ Set up the game and initialize the variables. """
        snake = Rectangle(SCREEN_WIDTH/2, 0, SNAKE_BLOCK_WIDTH, SNAKE_BLOCK_HEIGHT,
                          arcade.color.ALIZARIN_CRIMSON)
        self.snaketail_arr.append(snake)
        self.coin = Rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, COIN_BLOCK_WIDTH, COIN_BLOCK_HEIGHT,
                              arcade.color.YELLOW_ROSE)
        print(self.coin.x)
        self.current_direction_arr.append('up')

    def on_update(self, dt):
        """ Move everything """

        # for shape in self.snaketail_arr:
        #     shape.move(0, 1, 0)

        for i in reversed(range(self.coins_collected + 1)):
            if i == 0:
                if self.current_direction_arr[i] == 'up':
                    self.snaketail_arr[i].x += 0
                    self.snaketail_arr[i].y += MOVE_SPEED
                elif self.current_direction_arr[i] == 'down':
                    self.snaketail_arr[i].x += 0
                    self.snaketail_arr[i].y -= MOVE_SPEED
                elif self.current_direction_arr[i] == 'right':
                    self.snaketail_arr[i].x += MOVE_SPEED
                    self.snaketail_arr[i].y += 0
                elif self.current_direction_arr[i] == 'left':
                    self.snaketail_arr[i].x -= MOVE_SPEED
                    self.snaketail_arr[i].y += 0
            else:
                self.snaketail_arr[i].x = self.snaketail_arr[i - 1].x
                self.snaketail_arr[i].y = self.snaketail_arr[i - 1].y

            # Screen wrapping
            if (self.snaketail_arr[i].x > SCREEN_WIDTH) and (self.current_direction_arr[i] == 'right'):
                self.snaketail_arr[i].x -= SCREEN_WIDTH
            elif (self.snaketail_arr[i].y > SCREEN_HEIGHT) and (self.current_direction_arr[i] == 'up'):
                self.snaketail_arr[i].y -= SCREEN_HEIGHT
            elif (self.snaketail_arr[i].x < 0) and (self.current_direction_arr[i] == 'left'):
                self.snaketail_arr[i].x += SCREEN_WIDTH
            elif (self.snaketail_arr[i].y < 0) and (self.current_direction_arr[i] == 'down'):
                self.snaketail_arr[i].y += SCREEN_HEIGHT

        self.detect_snake_collision()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        # Update shapes
        self.coin.draw()
        for shape in self.snaketail_arr:
            shape.draw()

        # Update game logic
        self.scoretext_str = 'Score: ' + str(self.coins_collected)
        self.scoretext = arcade.draw_text(self.scoretext_str, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 30,
                                          arcade.color.WHITE,
                                          align="left", anchor_x="right", bold=True, font_size=16)

        # FPS tracker
        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 80, arcade.color.BLACK, 16)
        self.fps.tick()

    def detect_snake_collision(self):

        collision_detected = collision_detection_rects(self.snaketail_arr[0], self.coin)
        if collision_detected:
            temp_snaketail = Rectangle(self.snaketail_arr[self.coins_collected - 1].x,
                                       self.snaketail_arr[self.coins_collected - 1].y,
                                       SNAKE_BLOCK_WIDTH, SNAKE_BLOCK_HEIGHT,
                                       arcade.color.ALIZARIN_CRIMSON)

            self.snaketail_arr.append(temp_snaketail)
            self.current_direction_arr.append(self.current_direction_arr[self.coins_collected])
            self.coins_collected += 1
            self.create_new_coin()

    def create_new_coin(self):
        rand_x = np.random.randint(0, int(SCREEN_WIDTH / 2))
        rand_y = np.random.randint(0, int(SCREEN_HEIGHT / 2))

        self.coin = Rectangle(rand_x, rand_y, COIN_BLOCK_WIDTH, COIN_BLOCK_HEIGHT,
                              arcade.color.YELLOW_ROSE)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """

        if key == arcade.key.UP or arcade.key.DOWN or arcade.key.RIGHT or arcade.key.LEFT:
            self.frames_since_direction_change = 0

        if (key == arcade.key.UP) and (self.current_direction_arr[0] is not 'down'):
            self.current_direction_arr[0] = 'up'
        elif key == arcade.key.DOWN:
            self.current_direction_arr[0] = 'down'
        elif key == arcade.key.RIGHT:
            self.current_direction_arr[0] = 'right'
        elif key == arcade.key.LEFT:
            self.current_direction_arr[0] = 'left'

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
