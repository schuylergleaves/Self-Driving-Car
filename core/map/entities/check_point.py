import pygame


class CheckPoint:
    SIZE = 25

    def __init__(self, x, y):
        # subtract SIZE / 2 so that the x & y coords passed in represents the middle of the FinishLine object
        self.x = x - self.SIZE / 2
        self.y = y - self.SIZE / 2

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.SIZE, self.SIZE)
