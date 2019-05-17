# ----------------------------------------------------------------
# Created referencing http://rmgi.blog/pygame-2d-car-tutorial.html
# @author Schuyler Gleaves - 5/16/2019
# ----------------------------------------------------------------
import pygame
from pygame.math import Vector2
from math import tan, radians, degrees


class Car:
    # constants - car properties
    MAX_ACCELERATION   = 5.0
    MAX_STEERING_ANGLE = 30
    CHASSIS_LENGTH     = 4

    # constants - physics properties
    ACCELERATION_MODIFIER   = 2.0
    STEERING_ANGLE_MODIFIER = 15
    BRAKE_MODIFIER          = 20

    def __init__(self, x, y, car_image):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0
        self.acceleration = 0
        self.steering_angle = 0
        self.car_image = car_image
        self.crashed = False

    def update(self, dt):
        if self.crashed:
            return

        self.velocity += Vector2(self.acceleration * dt, 0)

        # derivation for turning radius and angular velocity formula can be found in citation at top
        if self.steering_angle is not 0:
            turning_radius = self.CHASSIS_LENGTH / tan(radians(self.steering_angle))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def accelerate(self, dt):
        self.acceleration = min(self.acceleration + self.ACCELERATION_MODIFIER * dt, self.MAX_ACCELERATION)

    def decelerate(self, dt):
        self.acceleration = max(-self.MAX_ACCELERATION, self.acceleration - self.ACCELERATION_MODIFIER * dt)

    def no_acceleration(self):
        self.acceleration = 0

    def steer_right(self, dt):
        self.steering_angle = min(self.steering_angle - self.STEERING_ANGLE_MODIFIER * dt, self.MAX_STEERING_ANGLE)

    def steer_left(self, dt):
        self.steering_angle = max(-self.MAX_STEERING_ANGLE, self.steering_angle + self.STEERING_ANGLE_MODIFIER * dt)

    def no_steering(self):
        self.steering_angle = 0

    def brake(self, dt):
        self.velocity.x = max(0, self.velocity.x - self.BRAKE_MODIFIER * dt)

    def has_crashed(self):
        return self.crashed

    def crash(self):
        self.crashed = True
        self.acceleration = 0
        self.velocity = 0

    def get_rotated_image(self):
        return pygame.transform.rotate(self.car_image, self.angle)

    def get_rect(self):
        return self.get_rotated_image().get_rect()