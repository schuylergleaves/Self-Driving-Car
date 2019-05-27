from core.map.entities.wall import Wall
from core.map.entities.finish_line import FinishLine
from core.map.entities.check_point import CheckPoint


class Map:
    def __init__(self):
        self.walls = []
        self.finish_lines = []
        self.check_points = []

    def add_wall(self, x, y):
        self.walls.append(Wall(x, y))

    def add_finish_line(self, x, y):
        self.finish_lines.append(FinishLine(x, y))

    def add_check_point(self, x, y):
        self.check_points = []
        self.check_points.append(CheckPoint(x, y))

    def get_walls(self):
        return self.walls

    def get_finish_lines(self):
        return self.finish_lines

    def get_check_points(self):
        return self.check_points

    def collided_wall(self, car):
        car_rect = car.get_collision_rect()

        for wall in self.walls:
            if wall.get_rect().colliderect(car_rect):
                return True

        return False

    def entered_finish_line(self, car):
        car_rect = car.get_collision_rect()

        for finish_line in self.finish_lines:
            if finish_line.get_rect().colliderect(car_rect):
                return True

        return False
