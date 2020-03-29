import arcade
import math
import numpy as np

from ArcadeCustom.CustomClasses import Rectangle, Circle


def collision_detection_rects(object1: Rectangle, object2: Rectangle):
    # Collision detection between two drawn objects using rectangular bounding boxes

    collision_detected = False
    if ((object1.x <= (object2.x + object2.width)) and ((object1.x + object1.width) >= object2.x) and
            (object1.y <= (object2.y + object2.height)) and ((object1.y + object1.height) >= object2.y)):
        collision_detected = True

    return collision_detected

def collision_detection_circles(object1: Circle, object2: Circle):
    # Collision detection between two circular objects

    collision_detected = False
    dx = object1.x - object2.x
    dy = object1.y - object2.y
    distance = np.sqrt(dx**2 + dy**2)
    if (distance <= (object1.radius + object2.radius)):
        collision_detected = True

    return collision_detected
