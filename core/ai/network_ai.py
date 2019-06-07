"""
AI Inputs:
    5 sensors which each give a distance to a wall (between 0 and 100), or return 100 if there are no walls nearby

Possible AI Actions:
    0 - Do Nothing
    1 - Steer Left
    2 - Steer Right

"""
import numpy as np
import core.util.random as util
from .neural_network import NeuralNetwork


class NetworkAI:
    def __init__(self, car_list):
        self.cars = car_list
        self.initialize_neural_networks()
        self.generation_num = 1

    def update_cars(self, delta_time):
        for car in self.cars:
            if car.has_crashed():
                continue

            self.stabilize_velocity(car, 200, delta_time)
            self.perform_action(car, self.get_output_from_neural_network(car), delta_time)


    # ----- CAR ACTIONS -----
    def perform_action(self, car, output, delta_time):
        if output < 0.7:
            car.steer_left(delta_time)
        elif output < 0.8:
            car.no_steering()
        else:
            car.steer_right(delta_time)

    def stabilize_velocity(self, car, desired_velocity, delta_time):
        if car.velocity.x < desired_velocity:
            car.accelerate(delta_time)
        else:
            car.brake(delta_time)

    def all_cars_have_crashed(self):
        for car in self.cars:
            if car.has_crashed() is False:
                return False

        return True


    # ----- NEURAL NETWORK ACTIONS -----
    def initialize_neural_networks(self):
        for car in self.cars:
            weights = np.random.rand(5)
            nn = NeuralNetwork(weights)
            car.set_neural_network(nn)

    def get_output_from_neural_network(self, car):
        nn = car.get_neural_network()

        # if nn is None:
        #     return np.random.rand(1)

        sensor_vals = car.get_sensor_values()
        return nn.get_output(sensor_vals)

    def create_new_generation(self, parent_cars):
        self.generation_num += 1
        self.mutate_neural_networks(parent_cars)

    def mutate_neural_networks(self, parent_cars):
        debug_iterations = 0
        parent_index = 0
        for car in self.cars:
            # we must first copy all parents into new generation
            if parent_index != len(parent_cars):
                car.set_neural_network(parent_cars[parent_index].get_neural_network())
                debug_iterations += 1
                print("\nSET PARENT NETWORK #%s" % parent_index)
                parent_index += 1

            # once we reached end of parents, then we must begin mutating parents
            else:
                rand_parent_index = np.random.randint(0, len(parent_cars))
                parent_nn = parent_cars[rand_parent_index].get_neural_network()
                parent_nn_weights = parent_nn.get_current_weights()
                new_weights = []
                for val in parent_nn_weights:
                    new_val = val + (util.get_random_sign() * np.random.uniform(0.1, self.get_mutation_val()))
                    new_weights.append(new_val)

                car.set_neural_network(NeuralNetwork(new_weights))
                debug_iterations += 1


                # DEBUG
                print("\nMUTATED NETWORK OF PARENT #%s" % rand_parent_index)
                print("Old Network Weights: " + str(parent_nn_weights))
                print("New Network Weights: " + str(new_weights))

        print("NUM ITERATIONS: " + str(debug_iterations))

    def get_mutation_val(self):
        """
        As the number of generations we have experienced increases, we decrease the amount of randomness in our
        mutations. This means that as the AI (hopefully) improves over generations, we will keep reproducing
        those successful children.
        """
        if self.generation_num > 20:
            return 0.2
        elif self.generation_num > 10:
            return 0.3
        elif self.generation_num > 5:
            return 0.4
        else:
            return 0.5


