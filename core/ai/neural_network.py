import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


class NeuralNetwork:
    def __init__(self, weights):
        self.weights = weights

    def get_output(self, input_data):
        normalized_input_data = np.divide(input_data, 200)

        initial_dot_val = np.dot(normalized_input_data, self.weights)

        output = sigmoid(initial_dot_val)

        # print("\n\nNEURAL NETWORK OUTPUT")
        # print("Input Data: " + str(normalized_input_data))
        # print("Weights 1: " + str(self.weights))
        # print("Initial Dot Val: " + str(initial_dot_val))
        # print("Output: " + str(output))

        return output

    def get_current_weights(self):
        return self.weights
