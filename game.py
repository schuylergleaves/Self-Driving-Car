import pygame
import config
import os
from pygame.math import Vector2
from car import Car
from map import Map


class Game:
    def __init__(self):
        pygame.init()
        self.preload_images()

        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        self.text_font = pygame.font.SysFont("Courier", 30)
        self.clock = pygame.time.Clock()

        self.car = Car(config.CAR_STARTING_X, config.CAR_STARTING_Y, self.car_image)
        self.map = Map()
        self.active = True
        self.dt = None

    def run(self):
        while self.active:
            # handling special events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()

            # initial polling for data
            delta_time = self.get_time_since_last_frame()

            # handle all user input
            self.handle_user_input_for_map()
            self.handle_user_input_for_car(delta_time)

            # updates to any objects
            self.car.update(delta_time)
            self.handle_car_collisions()

            # drawing
            self.draw_background()
            self.draw_map()
            self.draw_car()
            self.display_text("Car Velocity: %s" % self.car.velocity, (5, 10))
            self.display_text("Car has crashed: %s" % self.car.has_crashed(), (5, 40))

            # rendering
            self.render_ui()
            self.limit_fps(config.FPS)

    def handle_car_collisions(self):
        if self.map.has_collision_with(self.car):
            self.car.crash()

    def handle_user_input_for_map(self):
        if pygame.mouse.get_pressed()[0]:
            self.add_wall_at_mouse_pos()

    def handle_user_input_for_car(self, dt):
        if self.car.has_crashed():
            return

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

    def draw_map(self):
        for wall in self.map.get_wall_list():
            pygame.draw.rect(self.screen, config.WHITE, wall.get_rect())

    def draw_car(self):
        # rotated_img = pygame.transform.rotate(self.car_image, self.car.angle)
        rotated_img = self.car.get_rotated_image()
        rect = rotated_img.get_rect()

        # conversion from car pos to screen space
        car_pos = (self.car.position * config.PIXELS_PER_UNIT) - Vector2(rect.width / 2, rect.height / 2)
        self.screen.blit(rotated_img, (car_pos.x, car_pos.y))

    def draw_background(self):
        self.screen.fill(config.BLACK)

    def add_wall_at_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.map.create_wall(mouse_x, mouse_y)

    def display_text(self, text, position):
        text = self.text_font.render(text, True, config.WHITE)
        self.screen.blit(text, position)

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