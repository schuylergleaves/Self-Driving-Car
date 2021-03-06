import pygame
from .mode import Mode
from .state import State
from data import config
from core.car.car import Car
from core.map.map import Map
from core.ai.network_ai import NetworkAI
from pygame import Vector2


class Game:
    # ----- INITIALIZATION -----
    def __init__(self, mode):
        self.mode = mode
        self.init_game_state()
        self.init_game_window()
        self.init_game_objects()

    def init_game_state(self):
        self.state = State.BUILDING
        self.active = True

    def init_game_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
        self.text_font = pygame.font.SysFont("Courier", 30)
        self.clock = pygame.time.Clock()

    def init_game_objects(self):
        self.map = Map()
        self.cars = []
        self.selected_cars = []

        # user mode => one car
        if self.mode == Mode.USER:
            self.cars.append(Car(config.CAR_STARTING_X, config.CAR_STARTING_Y, config.CAR_SIZE, self.screen))

        # AI mode => population of cars
        elif self.mode == Mode.AI:
            for i in range(0, config.POPULATION_SIZE):
                self.cars.append(Car(config.CAR_STARTING_X, config.CAR_STARTING_Y, config.CAR_SIZE, self.screen))
            self.ai = NetworkAI(self.cars)



    # ----- MAIN GAME LOOP -----
    def run(self):
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.select_car_at_mouse_pos()

            self.update_internal_game_data()
            self.update_objects()
            self.handle_input()
            self.draw()

    def shutdown(self):
        self.active = False


    # ----- INTERNAL GAME STATE -----
    def update_internal_game_data(self):
        self.delta_time = self.get_time_since_last_frame()

    def get_time_since_last_frame(self):
        return self.clock.get_time() / 1000

    def set_state(self, state):
        self.state = state


    # ----- OBJECT MANIPULATION -----
    def update_objects(self):
        for car in self.cars:
            car.update(self.delta_time)

        self.handle_collisions()

    def handle_collisions(self):
        for car in self.cars:
            if self.map.has_collided_wall(car):
                car.crash()
            elif self.map.has_entered_finish_line(car):
                car.finish()

    def add_wall_at_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.map.add_wall(mouse_x, mouse_y)

    def add_finish_line_at_mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.map.add_finish_line(mouse_x, mouse_y)

    def reset_cars(self):
        for car in self.cars:
            car.set_position(Vector2(config.CAR_STARTING_X, config.CAR_STARTING_Y))
            car.reset_state()

    def reset_selected_cars(self):
        self.selected_cars = []

    def reset_map(self):
        self.map.reset()
        self.state = State.BUILDING

    def select_car_at_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == State.CAR_SELECTION:
            for car in self.cars:
                # if we find a car, then we select it and set state as driving to move on with next gen
                if car.get_rect().collidepoint(mouse_pos):
                    if car.selected:
                        self.selected_cars.remove(car)
                        car.selected = False
                    else:
                        self.selected_cars.append(car)
                        car.selected = True
                    return

    def crash_all_cars(self):
        for car in self.cars:
            car.crash()


    # ----- HANDLING INPUT -----
    def handle_input(self):
        # whether mode is AI or User, we must handle input for game state
        self.handle_user_input_for_game_state()

        if self.state == State.BUILDING:
            self.handle_user_input_for_map()

        if self.mode == Mode.USER:
            if self.state == State.DRIVING:
                self.handle_user_input_for_car()
        elif self.mode == Mode.AI:
            self.handle_ai_input_for_car()

    def handle_user_input_for_game_state(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_r]:
            self.reset_cars()
        elif pressed[pygame.K_p]:
            self.reset_map()
        elif pressed[pygame.K_RETURN]:
            if self.state == State.CAR_SELECTION and len(self.selected_cars) > 0:
                self.set_state(State.FINISHED_CAR_SELECTION)
            else:
                self.set_state(State.DRIVING)
        elif pressed[pygame.K_q]:
            self.crash_all_cars()

    def handle_user_input_for_map(self):
        # left click
        if pygame.mouse.get_pressed()[0]:
            self.add_wall_at_mouse_pos()

        # middle mouse btn
        if pygame.mouse.get_pressed()[1]:
            self.add_finish_line_at_mouse_pos()

    def handle_user_input_for_car(self):
        car = self.cars[0]

        if car.has_crashed():
            return

        pressed = pygame.key.get_pressed()
        dt = self.delta_time

        if pressed[pygame.K_w]:
            car.accelerate(dt)
        elif pressed[pygame.K_s]:
            car.decelerate(dt)
        else:
            car.no_acceleration()

        if pressed[pygame.K_d]:
            car.steer_right(dt)
        elif pressed[pygame.K_a]:
            car.steer_left(dt)
        else:
            car.no_steering()

        if pressed[pygame.K_SPACE]:
            car.brake(dt)

    def handle_ai_input_for_car(self):
        if self.state is State.DRIVING:
            self.ai.update_cars(self.delta_time)

            # if all cars crash, we must now select which car did best
            if self.ai.all_cars_have_crashed():
                self.set_state(State.CAR_SELECTION)

        # once we finish car selection, we are able to move onto
        if self.state is State.FINISHED_CAR_SELECTION:
            self.reset_cars()
            self.ai.create_new_generation(self.selected_cars)
            self.reset_selected_cars()
            self.set_state(State.DRIVING)


    # ----- DRAWING -----
    def draw(self):
        self.draw_background()
        self.draw_map()
        self.draw_car()
        # self.draw_sensors()
        self.draw_text()

        self.render_ui()
        self.limit_fps(config.FPS)

    def draw_text(self):
        if self.mode == Mode.USER:
            self.display_text("Car Velocity: %s" % self.cars[0].velocity, (5, 10))

            sensor_vals = self.cars[0].get_sensor_values()
            text_pos = 10
            for val in sensor_vals:
                self.display_text("Sensor: %s" % val, (980, text_pos))
                text_pos += 30

            if self.cars[0].has_crashed():
                self.display_text("Car has crashed!", (200, 200))

            if self.cars[0].has_finished():
                self.display_text("Car has finished!", (200, 200))

        self.display_text("Time Elapsed: %s" % str(pygame.time.get_ticks() / 1000), (400, 10))

        if self.state is State.BUILDING:
            self.display_text("State: BUILDING", (5, 40))
        elif self.state is State.DRIVING:
            self.display_text("State: DRIVING", (5, 40))
        elif self.state is State.CAR_SELECTION:
            self.display_text("State: CAR_SELECTION", (5, 40))
        elif self.state is State.FINISHED_CAR_SELECTION:
            self.display_text("State: FINISHED_CAR_SELECTION", (5, 40))

        self.display_text("NUM CARS SELECTED: %s" % len(self.selected_cars), (700, 70))

        if self.mode is Mode.AI:
            self.display_text("Generation: %s" % self.ai.generation_num, (5, 70))

    def draw_map(self):
        for wall in self.map.get_walls():
            pygame.draw.rect(self.screen, config.WALL_COLOR, wall.get_rect())

        for finish_line in self.map.get_finish_lines():
            pygame.draw.rect(self.screen, config.BLUE, finish_line.get_rect())

    def draw_car(self):
        for car in self.cars:
            self.screen.blit(car.get_image(), car.get_rect())

    def draw_background(self):
        self.screen.fill(config.GREY)

    def draw_sensors(self):
        for car in self.cars:
            for sensor in car.sensors:
                pygame.draw.line(self.screen, config.SENSOR_LINE_COLOR, car.position, (sensor.get_hit_point()))

    def display_text(self, text, position):
        text = self.text_font.render(text, True, config.BLACK)
        self.screen.blit(text, position)

    @staticmethod
    def render_ui():
        pygame.display.flip()

    def limit_fps(self, fps):
        self.clock.tick(fps)
