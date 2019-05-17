from wall import Wall
import pygame
import config
from pygame.math import Vector2


class Map:
    def __init__(self):
        self.walls = []

    def create_wall(self, x, y):
        self.walls.append(Wall(x, y))
    def get_wall_list(self):
        return self.walls

    def has_collision_with(self, car):
        # converts car pos to screen space, then adds front offset to determine if the front of the car collides
        # with a given object
        rect = car.get_rect()
        car_pos = (car.position * config.PIXELS_PER_UNIT) - Vector2(rect.width / 2, rect.height / 2)

        for wall in self.walls:
            if wall.get_rect().collidepoint(car_pos):
                return True

        return False
