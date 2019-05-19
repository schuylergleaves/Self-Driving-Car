from wall import Wall


class Map:
    def __init__(self):
        self.walls = []

    def create_wall(self, x, y):
        self.walls.append(Wall(x, y))

    def get_wall_list(self):
        return self.walls

    def has_collision_with(self, car):
        car_rect = car.get_rect()

        for wall in self.walls:
            if wall.get_rect().colliderect(car_rect):
                return True

        return False