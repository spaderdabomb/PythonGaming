import arcade
import os

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "Snake"

SNAKE_BLOCK_WIDTH = 15
SNAKE_BLOCK_HEIGHT = 15

MOVE_SPEED = 1


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.AMAZON)

        self.current_direction = 'up'
        self.center_x = SCREEN_WIDTH/2
        self.center_y = 0

        self.snake = None
        self.coin = None

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here

        pass

    def on_draw_test(self, delta):
        """
        Render the screen.
        """

        arcade.start_render()

        # Coin generation
        self.coin = arcade.draw_circle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 10, arcade.color.YELLOW_ROSE)


        # Movement
        self.snake = arcade.draw_rectangle_filled(self.center_x, self.center_y, SNAKE_BLOCK_WIDTH, SNAKE_BLOCK_HEIGHT,
                                 arcade.color.ALIZARIN_CRIMSON)

        if self.current_direction == 'up':
            self.center_x += 0
            self.center_y += MOVE_SPEED
        elif self.current_direction == 'down':
            self.center_x += 0
            self.center_y -= MOVE_SPEED
        elif self.current_direction == 'right':
            self.center_x += MOVE_SPEED
            self.center_y += 0
        elif self.current_direction == 'left':
            self.center_x -= MOVE_SPEED
            self.center_y += 0

        # Screen wrapping
        if (self.center_x > SCREEN_WIDTH) and (self.current_direction == 'right'):
            self.center_x -= SCREEN_WIDTH
        elif (self.center_y > SCREEN_HEIGHT) and (self.current_direction == 'up'):
            self.center_y -= SCREEN_HEIGHT
        elif (self.center_x < 0) and (self.current_direction == 'left'):
            self.center_x += SCREEN_WIDTH
        elif (self.center_y < 0) and (self.current_direction == 'down'):
            self.center_y += SCREEN_HEIGHT

        # Collision detection
        #bro = arcade.SpriteList.draw(0, 0, 10, 10)



    def detect_snake_collision(self):

        snake = self.center_x - SNAKE_BLOCK_WIDTH/2
        snake_x_right = self.center_x + SNAKE_BLOCK_WIDTH/2
        snake_y_top = self.center_y + SNAKE_BLOCK_HEIGHT/2
        snake_y_bottom = self.center_y - SNAKE_BLOCK_HEIGHT/2






    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.UP:
            self.current_direction = 'up'
        elif key == arcade.key.DOWN:
            self.current_direction = 'down'
        elif key == arcade.key.RIGHT:
            self.current_direction = 'right'
        elif key == arcade.key.LEFT:
            self.current_direction = 'left'


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


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.schedule(game.on_draw_test, 1/240)
    arcade.run()


if __name__ == "__main__":
    main()