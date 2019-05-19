

class NetworkAI:
    def __init__(self, car):
        self.car = None
        self.set_currently_active_car(car)
        self.generation = 0

    def set_currently_active_car(self, car):
        self.car = car

    def get_generation(self):
        return self.generation

    def increment_generation(self):
        self.generation += 1

    def update_car(self, dt):
        self.car.accelerate(dt)
