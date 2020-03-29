import arcade

class Circle():
    def __init__(self, x: float, y: float, radius: float, color: arcade.color):

        # Attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

class Rectangle():
    def __init__(self, x: float, y: float, width: float, height: float, color: arcade.color):

        # Attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.snake = arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)