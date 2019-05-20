"""
AI Inputs:
    5 sensors which each give a distance to a wall (between 0 and 100), or return 100 if there are no walls nearby

Possible AI Actions:
    0 - Do Nothing
    1 - Steer Left
    2 - Steer Right

"""
import numpy as np


class NetworkAI:
    def __init__(self, car_list):
        self.cars = car_list
        self.generation_num = 0

    def update_cars(self, delta_time):
        for car in self.cars:
            # limits velocity to ~200
            if car.velocity.x < 200:
                car.accelerate(delta_time)
            else:
                car.brake(delta_time)

            rand = np.random.randint(0, 3)
            if rand == 0:
                car.no_steering()
            elif rand == 1:
                car.steer_left(delta_time)
            elif rand == 2:
                car.steer_right(delta_time)

    def create_new_generation(self):
        pass

    def all_cars_crashed(self):
        for car in self.cars:
            if car.has_crashed() is False:
                return False

        return True

    def set_new_car_list(self, car_list):
        self.cars = car_list


