import arcade
import random

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shapes!"

RECT_WIDTH = 50
RECT_HEIGHT = 50

NUMBER_OF_SHAPES = 200


class Shape:

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color
        self.shape_list = None

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle

    def draw(self):
        self.shape_list.center_x = 0
        self.shape_list.center_y = 0
        self.shape_list.angle = self.angle
        self.shape_list.draw()

class Ellipse(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_ellipse_filled(self.x, self.y,
                                             self.width, self.height,
                                             self.color, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)


class Rectangle(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_rectangle_filled(self.x, self.y,
                                               self.width, self.height,
                                               self.color, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []

        for i in range(NUMBER_OF_SHAPES):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            width = random.randrange(10, 30)
            height = random.randrange(10, 30)
            angle = random.randrange(0, 360)

            d_x = random.randrange(-3, 4)
            d_y = random.randrange(-3, 4)
            d_angle = random.randrange(-3, 4)

            red = random.randrange(256)
            green = random.randrange(256)
            blue = random.randrange(256)
            alpha = random.randrange(256)

            shape_type = random.randrange(2)

            if shape_type == 0:
                shape = Rectangle(x, y, width, height, angle, d_x, d_y,
                                  d_angle, (red, green, blue, alpha))
            else:
                shape = Ellipse(x, y, width, height, angle, d_x, d_y,
                                d_angle, (red, green, blue, alpha))
            self.shape_list.append(shape)

        self.myshape = Rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 200, 200, 10, 10, 10, 0, arcade.color.WHITE)

    def on_update(self, dt):
        """ Move everything """

        for shape in self.shape_list:
            shape.move()

        self.myshape.move()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        for shape in self.shape_list:
            shape.draw()

        # shape = arcade.create_rectangle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 200, 200, arcade.color.WHITE, 0)
        # shape.draw()

        self.myshape.draw()

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()