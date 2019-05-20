import numpy as np


class NeuralNetwork:
    NUM_ACTIONS = 3

    def __init__(self):
        np.random.seed(1)

    def get_action(self, sensor_values, car_has_crashed):
        self.confidence_vals = []


    def reward(self, sensor_values, car_has_crashed):
        reward_val = np.sum(sensor_values)
        if car_has_crashed:
            reward_val -= 5000

        return reward_val


