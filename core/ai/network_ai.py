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
        self.set_new_car_list(car_list)
        self.generation_num = 0
        self.create_new_generation()

    def update_cars(self, delta_time):
        car_index = 0
        for car in self.cars:
            if car.has_crashed():
                if self.have_applied_crash_deduction(car_index) is False:
                    self.scores[car_index] -= 500
                    self.applied_crash_deduction.append(car_index)
                car_index += 1
                continue

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

            self.scores[car_index] += (np.sum(car.get_sensor_values()) / 10000)

            car.update(delta_time)

            car_index += 1


    def debug_print_all_scores(self):
        for score in self.scores:
            print(score)

    def have_applied_crash_deduction(self, car_index):
        return car_index in self.applied_crash_deduction

    def create_new_generation(self):
        self.generation_num += 1
        self.scores = []
        for car in self.cars:
            self.scores.append(0)
        self.applied_crash_deduction = []

    def all_cars_crashed(self):
        for car in self.cars:
            if car.has_crashed() is False:
                return False

        return True

    def set_new_car_list(self, car_list):
        self.cars = car_list


