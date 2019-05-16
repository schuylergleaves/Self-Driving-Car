import pygame
import config
import os
from pygame.math import Vector2
from car import Car


class Game:
    def __init__(self):
        pygame.init()
        self.preload_images()

        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        self.clock  = pygame.time.Clock()
        self.car    = Car(5, 10)
        self.active = True

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()

            self.dt = self.get_time_since_last_frame()

            self.handle_user_input_for_car()
            self.car.update(self.dt)

            self.draw_background()
            self.draw_car()

            self.render_ui()
            self.limit_fps(config.FPS)

    def handle_user_input_for_car(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            self.car.accelerate(self.dt)
        elif pressed[pygame.K_s]:
            self.car.decelerate(self.dt)
        else:
            self.car.no_acceleration()

        if pressed[pygame.K_d]:
            self.car.steer_right(self.dt)
        elif pressed[pygame.K_a]:
            self.car.steer_left(self.dt)
        else:
            self.car.no_steering()

        if pressed[pygame.K_SPACE]:
            self.car.brake(self.dt)

    def draw_car(self):
        rotated = pygame.transform.rotate(self.car_image, self.car.angle)
        rect = rotated.get_rect()

        car_pos = (self.car.position * config.PIXELS_PER_UNIT) - Vector2(rect.width / 2, rect.height / 2)
        self.screen.blit(rotated, (car_pos.x, car_pos.y))

    def draw_background(self):
        self.screen.fill(config.BLACK)

    def preload_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "images/car.png")
        self.car_image = pygame.image.load(image_path)

    def get_time_since_last_frame(self):
        return self.clock.get_time() / 1000

    def render_ui(self):
        pygame.display.flip()

    def limit_fps(self, fps):
        self.clock.tick(fps)

    def shutdown(self):
        self.active = False