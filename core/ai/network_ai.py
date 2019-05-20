"""
Version 1 of Neural Network AI
This AI will utilize a neural network to attempt to maneuver along a racetrack.
It will only focus on turning the wheel, as I will have the velocity limited around 200

AI Inputs:
    5 sensors which each give a distance to a wall (between 0 and 100), or return 100 if there are no walls nearby

Possible AI Actions:
    0 - Do Nothing
    1 - Steer Left
    2 - Steer Right

"""
from.neural_network import NeuralNetwork


class NetworkAI:
    def __init__(self, car):
        self.neural_network = NeuralNetwork()
        self.car = None
        self.set_currently_active_car(car)
        self.generation = 0

    def update_car(self, dt):
        # limits velocity to ~200
        if self.car.velocity.x < 200:
            self.car.accelerate(dt)
        else:
            self.car.brake(dt)

        # retrieve all necessary input vals for neural network
        sensor_values   = self.car.get_sensor_values()
        car_has_crashed = self.car.has_crashed()

        action_index = self.neural_network.get_action(sensor_values, car_has_crashed)
        self.perform_action(action_index)

    def perform_action(self, action_index):
        if action_index == 0:
            self.car.no_steering()
        elif action_index == 1:
            self.car.steer_left()
        elif action_index == 2:
            self.car.steer_right()

    def set_currently_active_car(self, car):
        self.car = car

    def get_generation(self):
        return self.generation

    def increment_generation(self):
        self.generation += 1
