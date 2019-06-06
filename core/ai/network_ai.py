"""
AI Inputs:
    5 sensors which each give a distance to a wall (between 0 and 100), or return 100 if there are no walls nearby

Possible AI Actions:
    0 - Do Nothing
    1 - Steer Left
    2 - Steer Right

"""
import numpy as np
from .neural_network import NeuralNetwork


class NetworkAI:
    def __init__(self, car_list):
        self.set_car_list(car_list)
        self.reset_scores()
        self.initialize_neural_networks()
        self.generation_num = 1

    def update_cars(self, delta_time):
        car_index = 0
        for car in self.cars:
            self.calculate_score(car, car_index)

            if car.has_crashed():
                car_index += 1
                continue

            self.stabilize_velocity(car, 200, delta_time)

            # output = self.get_output_from_neural_network(car)
            # # print(output)
            # self.perform_action(car, output, delta_time)


            self.perform_action(car, self.get_output_from_neural_network(car), delta_time)

            car_index += 1

    def calculate_score(self, car, car_index):
        if car.has_crashed():
            if self.have_applied_crash_deduction(car_index) is False:
                self.scores[car_index] -= 500
                self.crash_deductions.append(car_index)
        else:
            self.scores[car_index] += (np.sum(car.get_sensor_values()))

            if car.has_passed_checkpoint():
                self.scores[car_index] += (car.get_distance_to_checkpoint() * 20)
            else:
                self.scores[car_index] -= (car.get_distance_to_checkpoint() * 20)

            # if car.has_passed_checkpoint():
            #     self.scores[car_index] += (car.get_distance_to_checkpoint())
            # else:
            #     self.scores[car_index] -= (car.get_distance_to_checkpoint())

    def get_output_from_neural_network(self, car):
        nn = car.get_neural_network()
        if nn is None:
            return np.random.rand(1)

        sensor_vals = car.get_sensor_values()
        return nn.get_output(sensor_vals)

    def perform_action(self, car, output, delta_time):
        if output < 0.58:
            car.steer_left(delta_time)
        elif output < 0.66:
            car.no_steering()
        else:
            car.steer_right(delta_time)

    def perform_random_action(self, car, delta_time):
        action = np.random.rand(1)
        if action < 0.333:
            car.steer_left(delta_time)
        elif action < 0.666:
            car.no_steering()
        else:
            car.steer_right(delta_time)

    def create_new_generation(self):
        self.generation_num += 1
        self.mutate_neural_networks()
        self.reset_scores()

    def mutate_neural_networks(self):
        best_car = self.get_highest_score_car()
        best_nn = best_car.get_neural_network()
        best_nn_weights = best_nn.get_current_weights()

        saved_best_car = False
        for car in self.cars:
            if not saved_best_car:
                car.set_neural_network(best_nn)
                saved_best_car = True

            else:
                new_weights = []
                for val in best_nn_weights:
                    new_val = val * (1 + (self.get_random_sign() * np.random.uniform(0, 0.4)))
                    new_weights.append(new_val)

                car.set_neural_network(NeuralNetwork(new_weights))

                # DEBUG
                print("\nMUTATED NETWORK")
                print("Old Network Weights: " + str(best_nn_weights))
                print("New Network Weights: " + str(new_weights))

    def get_random_sign(self):
        rand = np.random.randn()
        if rand > 0:
            return 1
        else:
            return -1

    def initialize_neural_networks(self):
        for car in self.cars:
            weights = np.random.rand(5)
            nn = NeuralNetwork(weights)
            car.set_neural_network(nn)

    def should_perform_random_action(self):
        chance = np.random.rand(1)
        if chance <= 0.10:
            return True
        else:
            return False

    def stabilize_velocity(self, car, desired_velocity, delta_time):
        if car.velocity.x < desired_velocity:
            car.accelerate(delta_time)
        else:
            car.brake(delta_time)

    def reset_scores(self):
        self.scores = []
        for car in self.cars:
            self.scores.append(0)

        self.max_score_reached_this_generation = -10000
        self.crash_deductions = []

    def print_scores(self):
        for score in self.scores:
            print(score)

    def get_highest_score_car(self):
        self.max_score_reached_this_generation = max(self.scores)
        max_index = self.scores.index(self.max_score_reached_this_generation)
        return self.cars[max_index]

    def have_applied_crash_deduction(self, car_index):
        applied = car_index in self.crash_deductions
        return applied

    def all_cars_crashed(self):
        for car in self.cars:
            if car.has_crashed() is False:
                return False

        return True

    def set_car_list(self, car_list):
        self.cars = car_list


