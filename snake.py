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

        self.window.fill((100, 100, 100))

        self.font_style = pygame.font.SysFont(None, 50)
        active = True

        game_speed = 10
        clock = pygame.time.Clock()
        mode = 0

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.x_change = -self.block_size
                        self.y_change = 0
                    elif event.key == pygame.K_s:
                        self.x_change = self.block_size
                        self.y_change = 0
                    elif event.key == pygame.K_a:
                        self.x_change = 0
                        self.y_change = -self.block_size
                    elif event.key == pygame.K_d:
                        self.x_change = 0
                        self.y_change = self.block_size
                    elif event.key == pygame.K_SPACE:
                        if mode == 0:
                            mode += 1
                            self.x_change = 0
                            self.y_change = 0
                        elif mode == 2:
                            mode = 0

            if mode == 0:
                self.window.fill((100, 100, 100))
                go_message = self.font_style.render("Press SPACE to start", True, (255, 255, 0))
                self.window.blit(go_message, [self.x_window / 2, self.y_window / 2])

            elif mode == 1:
                self.y_snake.insert(0, self.y_head)
                self.x_snake.insert(0, self.x_head)

                self.x_head += self.x_change
                self.y_head += self.y_change

                # checks if snake head is on food -> if yes then place new food and snake grows
                if self.x_head == self.x_food and self.y_head == self.y_food:
                    set_food = True
                    while set_food:
                        self.y_food = random.randint(0, int((self.y_window - self.block_size) / self.block_size)) * self.block_size
                        self.x_food = random.randint(0, int((self.x_window - self.block_size) / self.block_size)) * self.block_size
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
                    game_speed += 1
                else:
                    self.y_snake.__delitem__(len(self.y_snake) - 1)
                    self.x_snake.__delitem__(len(self.x_snake) - 1)

                # checks if snake head lefts the field
                if self.x_head < 0 or self.x_head > self.x_window - self.block_size:
                    mode = 2
                if self.y_head < 0 or self.y_head > self.y_window - self.block_size:
                    mode = 2
                # checks if snake head is on snake body
                for i in range(len(self.x_snake)):
                    if self.x_head == self.x_snake[i] and self.y_head == self.y_snake[i]:
                        mode = 2

                self.window.fill((100, 100, 100))

                pygame.draw.rect(self.window, (0, 255, 0), [self.y_head, self.x_head, self.block_size, self.block_size])
                for i in range(len(self.x_snake)):
                    pygame.draw.rect(self.window, (0, 0, 255), [self.y_snake[i], self.x_snake[i], self.block_size, self.block_size])
                pygame.draw.rect(self.window, (255, 0, 0), [self.y_food, self.x_food, self.block_size, self.block_size])

            elif mode == 2:
                self.init_values()
                game_speed = 10
                self.window.fill((100, 100, 100))
                go_message = self.font_style.render("Game Over", True, (255, 0, 0))
                self.window.blit(go_message, [self.x_window / 2, self.y_window / 2])

            pygame.display.update()
            clock.tick(game_speed)

    def init_values(self):
        self.x_head = 100
        self.y_head = 100
        self.x_snake = []
        self.y_snake = []

        self.y_food = 180
        self.x_food = 200

        self.x_change = 0
        self.y_change = 0

    def run(self):
        pass


if __name__ == '__main__':
    Snake = Game()


#
# pygame.draw.rect(window, (0, 255, 0), [y_head, x_head, block_size, block_size])
# for i in range(len(x_snake)):
#     pygame.draw.rect(window, (0, 0, 255), [y_snake[i], x_snake[i], block_size, block_size])
#
# game_over = False





