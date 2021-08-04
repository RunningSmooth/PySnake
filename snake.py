import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.y_window = 640
        self.x_window = 480
        self.window = pygame.display.set_mode((self.y_window, self.x_window))

        self.block_size = 20

        self.x_head = 100
        self.y_head = 100
        self.x_snake = []
        self.y_snake = []

        self.y_food = 180
        self.x_food = 200

        self.x_change = 0
        self.y_change = 0

        self.window.fill((0, 0, 0))

        self.font_style = pygame.font.SysFont(None, 50)
        self.active = True
        self.go_init = True
        self.score = 0

        self.game_speed = 10
        clock = pygame.time.Clock()
        self.mode = 0

        while self.active:
            self.event_handler()

            if self.mode == 0:
                self.window.fill((0, 0, 0))
                go_message = self.font_style.render("Press SPACE to start", True, (255, 255, 255))
                self.window.blit(go_message, [self.y_window * 0.22, self.x_window * 0.5])

            elif self.mode == 1:
                self.y_snake.insert(0, self.y_head)
                self.x_snake.insert(0, self.x_head)

                self.x_head += self.x_change
                self.y_head += self.y_change

                self.food_process()
                self.collision_check()

                self.window.fill((0, 0, 0))
                self.draw_arena()
                go_message = self.font_style.render(str(self.score), True, (255, 255, 0))
                self.window.blit(go_message, [self.x_window / 2, self.y_window / 2])

                pygame.draw.rect(self.window, (0, 255, 0), [self.y_head, self.x_head, self.block_size, self.block_size])
                for i in range(len(self.x_snake)):
                    pygame.draw.rect(self.window, (0, 0, 255), [self.y_snake[i], self.x_snake[i], self.block_size, self.block_size])
                self.draw_food()

            elif self.mode == 2:
                if self.go_init:
                    self.init_values()
                    self.window.fill((0, 0, 0))
                    final_score = self.font_style.render("Your Score: " + str(self.score), True, (255, 255, 255))
                    go_message = self.font_style.render("Game Over", True, (255, 0, 0))
                    continue_message = self.font_style.render("Press SPACE to continue", True, (255, 255, 255))
                    self.window.blit(final_score, [self.y_window * 0.35, self.x_window * 0.25])
                    self.window.blit(go_message, [self.y_window * 0.37, self.x_window * 0.5])
                    self.window.blit(continue_message, [self.y_window * 0.18, self.x_window * 0.75])
                    self.go_init = False

            pygame.display.update()
            clock.tick(self.game_speed)

    def init_values(self):
        self.x_head = 100
        self.y_head = 100
        self.x_snake = []
        self.y_snake = []
        self.x_change = 0
        self.y_change = 0
        self.y_food = 180
        self.x_food = 200
        self.score = 0
        self.game_speed = 10

    def collision_check(self):
        # checks if snake head lefts the field
        if self.x_head < 0 or self.x_head > self.x_window - self.block_size:
            self.mode = 2
        if self.y_head < 0 or self.y_head > self.y_window - self.block_size:
            self.mode = 2
        # checks if snake head is on snake body
        for i in range(len(self.x_snake)):
            if self.x_head == self.x_snake[i] and self.y_head == self.y_snake[i]:
                self.mode = 2

    def food_process(self):
        # checks if snake head is on food -> if yes then place new food and snake grows
        if self.x_head == self.x_food and self.y_head == self.y_food:
            set_food = True
            while set_food:
                self.y_food = random.randint(0,
                                             int((self.y_window - self.block_size) / self.block_size)) * self.block_size
                self.x_food = random.randint(0,
                                             int((self.x_window - self.block_size) / self.block_size)) * self.block_size
                # checks if food is placed on the snake -> if not then placement is valid, else roll position again
                valid = True
                if self.y_food != self.y_head and self.x_food != self.x_head:
                    for i in range(len(self.y_snake)):
                        if self.y_food == self.y_snake[i] and self.x_food == self.x_snake[i]:
                            valid = False
                            break
                else:
                    valid = False
                if valid:
                    set_food = False
            self.game_speed += 1
            self.score += 1
        else:
            self.y_snake.__delitem__(len(self.y_snake) - 1)
            self.x_snake.__delitem__(len(self.x_snake) - 1)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.x_change != self.block_size or len(self.x_snake) == 0:
                        self.x_change = -self.block_size
                        self.y_change = 0
                elif event.key == pygame.K_s:
                    if self.x_change != -self.block_size or len(self.x_snake) == 0:
                        self.x_change = self.block_size
                        self.y_change = 0
                elif event.key == pygame.K_a:
                    if self.y_change != self.block_size or len(self.x_snake) == 0:
                        self.x_change = 0
                        self.y_change = -self.block_size
                elif event.key == pygame.K_d:
                    if self.y_change != -self.block_size or len(self.x_snake) == 0:
                        self.x_change = 0
                        self.y_change = self.block_size
                elif event.key == pygame.K_SPACE:
                    if self.mode == 0:
                        self.mode += 1
                        self.x_change = 0
                        self.y_change = 0
                        self.go_init = True
                    elif self.mode == 2:
                        self.mode = 0

    def draw_food(self):
        # Cherry
        self.window.fill((255, 0, 0), ((self.y_food + 2, self.x_food + 11), (7, 7)))
        self.window.fill((255, 0, 0), ((self.y_food + 11, self.x_food + 11), (7, 7)))

        # Left Stalk
        self.window.fill((0, 255, 0), ((self.y_food + 4, self.x_food + 10), (3, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 5, self.x_food + 9), (1, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 6, self.x_food + 8), (1, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 7, self.x_food + 7), (1, 1)))
        # Right Stalk
        self.window.fill((0, 255, 0), ((self.y_food + 13, self.x_food + 10), (3, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 14, self.x_food + 9), (1, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 13, self.x_food + 8), (1, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 12, self.x_food + 7), (1, 1)))

        # Leaf
        self.window.fill((0, 255, 0), ((self.y_food + 8, self.x_food + 6), (4, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 9, self.x_food + 5), (2, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 9, self.x_food + 4), (1, 1)))
        self.window.fill((0, 255, 0), ((self.y_food + 8, self.x_food + 3), (1, 2)))
        self.window.fill((0, 255, 0), ((self.y_food + 5, self.x_food + 2), (4, 4)))
        self.window.fill((0, 255, 0), ((self.y_food + 4, self.x_food + 2), (1, 2)))
        self.window.fill((0, 255, 0), ((self.y_food + 3, self.x_food + 2), (1, 1)))

    def draw_arena(self):
        rows = self.x_window / self.block_size
        columns = self.y_window / self.block_size
        for i in range(int(rows)):
            self.window.fill((43, 43, 43), ((0, self.block_size * i - 1), (self.y_window, 2)))
        for i in range(int(columns)):
            self.window.fill((43, 43, 43), ((self.block_size * i - 1, 0), (2, self.x_window)))


if __name__ == '__main__':
    Snake = Game()
