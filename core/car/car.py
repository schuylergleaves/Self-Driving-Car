# ----------------------------------------------------------------
# Created referencing http://rmgi.blog/pygame-2d-car-tutorial.html
# ----------------------------------------------------------------
import pygame
from pygame.math import Vector2
from math import tan, radians, degrees
from .state import State
import os


class Car:
    # constants - car properties
    MAX_ACCELERATION   = 80.0
    MAX_STEERING_ANGLE = 30
    MAX_VELOCITY       = 500
    CHASSIS_LENGTH     = 4

    # constants - physics modifiers
    ACCELERATION_MODIFIER   = 30.0
    STEERING_ANGLE_MODIFIER = 5
    BRAKE_MODIFIER          = 300
    COLLISION_OFFSET_VERT   = 0.8
    COLLISION_OFFSET_HORIZ  = 0.8

    # ----- INITIALIZATION -----
    def __init__(self, x, y, size):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.size = size
        self.angle = 0
        self.acceleration = 0
        self.steering_angle = 0
        self.state = State.RUNNING
        self.preload_image()

    def preload_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "../../assets/car.png")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.size)


    # ----- PHYSICS / ACTIONS -----
    def update(self, dt):
        if self.state is not State.RUNNING:
            self.velocity = 0
            self.acceleration = 0
            return

        # apply acceleration to velocity, limit to max
        self.velocity += Vector2(self.acceleration * dt, 0)
        if self.velocity.x > self.MAX_VELOCITY:
            self.velocity = Vector2(self.MAX_VELOCITY, 0)

        # derivation for turning radius and angular velocity formula can be found in citation at top
        if self.steering_angle is not 0:
            turning_radius = self.CHASSIS_LENGTH / tan(radians(self.steering_angle))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        # update position and car angle
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


    # ----- HANDLING STATE -----
    def has_crashed(self):
        return self.state == State.CRASHED

    def has_finished(self):
        return self.state == State.FINISHED

    def crash(self):
        self.state = State.CRASHED

    def finish(self):
        self.state = State.FINISHED


    # ----- GRAPHICS -----
    def get_image(self):
        # rotated to account for current angle of car
        return pygame.transform.rotate(self.image, self.angle)

    def get_rect(self):
        img_rect = self.get_image().get_rect()

        # we must adjust car pos so that we can have the rectangle align properly with middle of image
        adjusted_car_pos = self.position - Vector2(img_rect.width / 2, img_rect.height / 2)
        adjusted_rect = pygame.Rect(adjusted_car_pos.x, adjusted_car_pos.y, img_rect.width, img_rect.height)

        return adjusted_rect

    def get_collision_rect(self):
        """ returns a slightly smaller rectangle to account for image having whitespace"""
        rect = self.get_rect()
        collision_rect = pygame.Rect(rect.x, rect.y,
                                     rect.width * self.COLLISION_OFFSET_HORIZ,
                                     rect.height * self.COLLISION_OFFSET_VERT)
        return collision_rect