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
        self.clock = pygame.time.Clock()
        self.car = Car(config.CAR_STARTING_X, config.CAR_STARTING_Y)
        self.text_font = pygame.font.SysFont("Courier", 30)
        self.active = True
        self.dt = None

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()

            delta_time = self.get_time_since_last_frame()

            self.handle_user_input_for_car(delta_time)
            self.car.update(delta_time)

            self.draw_background()
            self.draw_car()
            self.display_text("Car Velocity: %s" % self.car.velocity, (5, 5))

            self.render_ui()
            self.limit_fps(config.FPS)

    def handle_user_input_for_car(self, dt):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            self.car.accelerate(dt)
        elif pressed[pygame.K_s]:
            self.car.decelerate(dt)
        else:
            self.car.no_acceleration()

        if pressed[pygame.K_d]:
            self.car.steer_right(dt)
        elif pressed[pygame.K_a]:
            self.car.steer_left(dt)
        else:
            self.car.no_steering()

        if pressed[pygame.K_SPACE]:
            self.car.brake(dt)

    def draw_car(self):
        rotated_img = pygame.transform.rotate(self.car_image, self.car.angle)
        rect = rotated_img.get_rect()

        # conversion from car pos to screen space
        car_pos = (self.car.position * config.PIXELS_PER_UNIT) - Vector2(rect.width / 2, rect.height / 2)
        self.screen.blit(rotated_img, (car_pos.x, car_pos.y))

    def draw_background(self):
        self.screen.fill(config.BLACK)

    def display_text(self, text, position):
        text = self.text_font.render(text, True, config.WHITE)
        self.screen.blit(text, (10, 10))

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