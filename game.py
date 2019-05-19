import pygame
import config
from car import Car
from map import Map


class Game:
    def __init__(self):
        pygame.init()

        # setting up pygame window / properties
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        self.text_font = pygame.font.SysFont("Courier", 30)
        self.clock = pygame.time.Clock()
        self.active = True

        # creating game objects
        self.car = Car(config.CAR_STARTING_X, config.CAR_STARTING_Y, config.CAR_SIZE)
        self.map = Map()

    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()

            self.update_internal_game_data()
            self.car.update(self.delta_time)

            self.handle_input()
            self.handle_collisions()

            self.draw_game()

            self.limit_fps(config.FPS)

    def update_internal_game_data(self):
        self.delta_time = self.get_time_since_last_frame()

    def handle_input(self):
        self.handle_user_input_for_game_state()
        self.handle_user_input_for_map()
        self.handle_user_input_for_car()

    def handle_user_input_for_game_state(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_r]:
            self.reset_car()
        elif pressed[pygame.K_p]:
            self.reset_map()

    def handle_user_input_for_map(self):
        if pygame.mouse.get_pressed()[0]:
            self.add_wall_at_mouse_pos()

        if pygame.mouse.get_pressed()[1]:
            self.add_finish_at_mouse_pos()

    def handle_user_input_for_car(self):
        if self.car.has_crashed():
            return

        pressed = pygame.key.get_pressed()
        dt = self.delta_time

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

    def handle_collisions(self):
        if self.map.collided_wall(self.car):
            self.car.crash()
        elif self.map.entered_finish_line(self.car):
            self.car.finish()

    def draw_game(self):
        self.draw_background()
        self.draw_map()
        self.draw_car()

        self.display_text("Car Velocity: %s" % self.car.velocity, (5, 10))
        self.display_text("Car has crashed: %s" % self.car.has_crashed(), (5, 40))
        self.display_text("Car has finished: %s" % self.car.has_finished(), (5, 70))

        self.render_ui()

    def draw_map(self):
        for wall in self.map.get_walls():
            pygame.draw.rect(self.screen, config.WHITE, wall.get_rect())

        for finish_line in self.map.get_finish_lines():
            pygame.draw.rect(self.screen, config.BLUE, finish_line.get_rect())

    def draw_car(self):
        self.screen.blit(self.car.get_image(), self.car.get_rect())

    def draw_background(self):
        self.screen.fill(config.GREY)

    def add_wall_at_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.map.add_wall(mouse_x, mouse_y)

    def add_finish_at_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.map.add_finish_line(mouse_x, mouse_y)

    def reset_car(self):
        self.car = Car(config.CAR_STARTING_X, config.CAR_STARTING_Y, config.CAR_SIZE)

    def reset_map(self):
        self.map = Map()

    def display_text(self, text, position):
        text = self.text_font.render(text, True, config.WHITE)
        self.screen.blit(text, position)

    def get_time_since_last_frame(self):
        return self.clock.get_time() / 1000

    def render_ui(self):
        pygame.display.flip()

    def limit_fps(self, fps):
        self.clock.tick(fps)

    def shutdown(self):
        self.active = False
