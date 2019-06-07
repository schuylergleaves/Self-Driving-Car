from core.map.entities.wall import Wall
from core.map.entities.finish_line import FinishLine


class Map:
    def __init__(self):
        self.walls = []
        self.finish_lines = []

    def add_wall(self, x, y):
        self.walls.append(Wall(x, y))

    def add_finish_line(self, x, y):
        self.finish_lines.append(FinishLine(x, y))

    def get_walls(self):
        return self.walls

    def get_finish_lines(self):
        return self.finish_lines

    def has_collided_wall(self, car):
        car_rect = car.get_collision_rect()

        for wall in self.walls:
            if wall.get_rect().colliderect(car_rect):
                return True

        return False

    def has_entered_finish_line(self, car):
        car_rect = car.get_collision_rect()

        for finish_line in self.finish_lines:
            if finish_line.get_rect().colliderect(car_rect):
                return True

        return False

    def reset(self):
        self.walls = []
        self.finish_lines = []