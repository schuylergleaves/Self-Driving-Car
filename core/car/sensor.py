from math import cos, sin, radians
from data import config


class Sensor:
    MAX_RANGE = 999

    def __init__(self, position, angle, screen):
        self.position = position
        self.angle = angle
        self.screen = screen

    def get_distance_to_wall(self):
        try:
            distance_traveled = 0
            while distance_traveled < self.MAX_RANGE:
                x = int(self.position.x + cos(radians(self.angle)) * distance_traveled)
                y = int(self.position.y + sin(radians(self.angle)) * distance_traveled)
                pixel_color = tuple(self.screen.get_at((x, y)))

                if pixel_color == config.WALL_COLOR:
                    return distance_traveled
                else:
                    distance_traveled += 1
        except IndexError:
            # if we happen to go out of screen bounds, that means there is no wall
            return self.MAX_RANGE

        return self.MAX_RANGE

    def get_hit_point(self):
        distance_traveled = self.get_distance_to_wall()
        x = int(self.position.x + cos(radians(self.angle)) * distance_traveled)
        y = int(self.position.y + sin(radians(self.angle)) * distance_traveled)
        return x, y
