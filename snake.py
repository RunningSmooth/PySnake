import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        self.y_window = 640
        self.x_window = 480
        self.window = pygame.display.set_mode((self.y_window, self.x_window))
        pygame.display.set_caption('Pygame by RunningSmooth')

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

                self.draw_head()
                for i in range(len(self.x_snake)):
                    # if i == len(self.x_snake) - 1:
                    #     self.draw_tail(self.y_snake[i], self.x_snake[i])
                    # else:
                    pygame.draw.rect(self.window, (133, 168, 21), [self.y_snake[i], self.x_snake[i], self.block_size, self.block_size])
                self.draw_food()
                self.draw_head()

            elif self.mode == 2:
                if self.go_init:
                    self.window.fill((0, 0, 0))
                    final_score = self.font_style.render("Your Score: " + str(self.score), True, (255, 255, 255))
                    go_message = self.font_style.render("Game Over", True, (255, 0, 0))
                    continue_message = self.font_style.render("Press SPACE to continue", True, (255, 255, 255))
                    self.window.blit(final_score, [self.y_window * 0.35, self.x_window * 0.25])
                    self.window.blit(go_message, [self.y_window * 0.37, self.x_window * 0.5])
                    self.window.blit(continue_message, [self.y_window * 0.18, self.x_window * 0.75])
                    self.init_values()
                    self.go_init = False

            pygame.display.update()
            clock.tick(self.game_speed)

    def init_values(self):
        ''' Function sets the initial values for the game. '''
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
        ''' Function checks if the snakes head collides with itself or the arena borders. '''
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
        ''' Function checks if the snake ate the food and if needed places a new food. '''
        # checks if snake head is on food -> if yes then place new food and snake grows
        if self.x_head == self.x_food and self.y_head == self.y_food:
            set_food = True
            while set_food:
                # randomise food position
                self.y_food = random.randint(0,
                                             int((self.y_window - self.block_size) / self.block_size)) * self.block_size
                self.x_food = random.randint(0,
                                             int((self.x_window - self.block_size) / self.block_size)) * self.block_size
                valid = True
                # checks if the food is not placed on the snake
                if self.y_food != self.y_head and self.x_food != self.x_head:
                    for i in range(len(self.y_snake)):
                        if self.y_food == self.y_snake[i] and self.x_food == self.x_snake[i]:
                            valid = False
                            break
                else:
                    valid = False
                # checks if position was valid -> if true then food can stay, else position the food again.
                if valid:
                    set_food = False
            # every 3 points the game gets faster
            self.score += 1
            if self.score % 3 == 0:
                self.game_speed += 1
        # if the head of the snake is not on food, the last element in the snake array is deleted
        else:
            self.y_snake.__delitem__(len(self.y_snake) - 1)
            self.x_snake.__delitem__(len(self.x_snake) - 1)

    def event_handler(self):
        ''' Function checks for events, like keyboard input or button clicks. '''
        for event in pygame.event.get():
            # Button event
            if event.type == pygame.QUIT:
                self.active = False
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                # Snake go up.
                if event.key == pygame.K_w:
                    if self.x_change != self.block_size or len(self.x_snake) == 0:
                        self.x_change = -self.block_size
                        self.y_change = 0
                # Snake go down.
                elif event.key == pygame.K_s:
                    if self.x_change != -self.block_size or len(self.x_snake) == 0:
                        self.x_change = self.block_size
                        self.y_change = 0
                # Snake go left.
                elif event.key == pygame.K_a:
                    if self.y_change != self.block_size or len(self.x_snake) == 0:
                        self.x_change = 0
                        self.y_change = -self.block_size
                # Snake go right.
                elif event.key == pygame.K_d:
                    if self.y_change != -self.block_size or len(self.x_snake) == 0:
                        self.x_change = 0
                        self.y_change = self.block_size
                # Change mode
                elif event.key == pygame.K_SPACE:
                    # start game
                    if self.mode == 0:
                        self.mode += 1
                        self.x_change = 0
                        self.y_change = 0
                        self.go_init = True
                    # start main menu
                    elif self.mode == 2:
                        self.mode = 0

    def draw_food(self):
        ''' Function draws the food '''
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

    def draw_head(self):
        ''' Function draws the snakes head. '''
        # Left
        if self.y_change < 0:
            # Head
            self.window.fill((133, 168, 21), ((self.y_head, self.x_head + 6), (2, 8)))
            self.window.fill((133, 168, 21), ((self.y_head + 2, self.x_head + 4), (2, 12)))
            self.window.fill((133, 168, 21), ((self.y_head + 4, self.x_head + 2), (2, 16)))
            self.window.fill((133, 168, 21), ((self.y_head + 6, self.x_head), (14, 20)))
            # Eyes
            self.window.fill((0, 0, 0), ((self.y_head + 5, self.x_head + 5), (3, 3)))
            self.window.fill((0, 0, 0), ((self.y_head + 5, self.x_head + 12), (3, 3)))
        # Right
        elif self.y_change > 0:
            # Head
            self.window.fill((133, 168, 21), ((self.y_head + 18, self.x_head + 6), (2, 8)))
            self.window.fill((133, 168, 21), ((self.y_head + 16, self.x_head + 4), (2, 12)))
            self.window.fill((133, 168, 21), ((self.y_head + 14, self.x_head + 2), (2, 16)))
            self.window.fill((133, 168, 21), ((self.y_head, self.x_head), (14, 20)))
            # Eyes
            self.window.fill((0, 0, 0), ((self.y_head + 12, self.x_head + 5), (3, 3)))
            self.window.fill((0, 0, 0), ((self.y_head + 12, self.x_head + 12), (3, 3)))
        # Down
        elif self.x_change > 0:
            # Head
            self.window.fill((133, 168, 21), ((self.y_head + 6, self.x_head + 18), (8, 2)))
            self.window.fill((133, 168, 21), ((self.y_head + 4, self.x_head + 16), (12, 2)))
            self.window.fill((133, 168, 21), ((self.y_head + 2, self.x_head + 14), (16, 2)))
            self.window.fill((133, 168, 21), ((self.y_head, self.x_head), (20, 14)))
            # Eyes
            self.window.fill((0, 0, 0), ((self.y_head + 5, self.x_head + 12), (3, 3)))
            self.window.fill((0, 0, 0), ((self.y_head + 12, self.x_head + 12), (3, 3)))
        # Up
        elif self.x_change < 0:
            # Head
            self.window.fill((133, 168, 21), ((self.y_head + 6, self.x_head), (8, 2)))
            self.window.fill((133, 168, 21), ((self.y_head + 4, self.x_head + 2), (12, 2)))
            self.window.fill((133, 168, 21), ((self.y_head + 2, self.x_head + 4), (16, 2)))
            self.window.fill((133, 168, 21), ((self.y_head, self.x_head + 6), (20, 14)))
            # Eyes
            self.window.fill((0, 0, 0), ((self.y_head + 5, self.x_head + 5), (3, 3)))
            self.window.fill((0, 0, 0), ((self.y_head + 12, self.x_head + 5), (3, 3)))

    def draw_tail(self, pos_y, pos_x):
        ''' Function draws the snakes tail.
        Parameters:
            pos_x (int): horizontal position of the tail
            pos_y (int): vertical position of the tail
         '''
        # Left
        if self.y_change < 0:
            self.window.fill((133, 168, 21), ((pos_y, pos_x), (8, 20)))
            self.window.fill((133, 168, 21), ((pos_y + 8, pos_x + 2), (3, 16)))
            self.window.fill((133, 168, 21), ((pos_y + 11, pos_x + 4), (3, 12)))
            self.window.fill((133, 168, 21), ((pos_y + 14, pos_x + 6), (3, 8)))
            self.window.fill((133, 168, 21), ((pos_y + 17, pos_x + 8), (3, 4)))
        # Right
        elif self.y_change > 0:
            self.window.fill((133, 168, 21), ((pos_y + 12, pos_x), (8, 20)))
            self.window.fill((133, 168, 21), ((pos_y + 9, pos_x + 2), (3, 16)))
            self.window.fill((133, 168, 21), ((pos_y + 6, pos_x + 4), (3, 12)))
            self.window.fill((133, 168, 21), ((pos_y + 3, pos_x + 6), (3, 8)))
            self.window.fill((133, 168, 21), ((pos_y, pos_x + 8), (3, 4)))
        # Down
        elif self.x_change > 0:
            self.window.fill((133, 168, 21), ((pos_y, pos_x + 12), (20, 8)))
            self.window.fill((133, 168, 21), ((pos_y + 2, pos_x + 9), (16, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 4, pos_x + 6), (12, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 6, pos_x + 3), (8, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 8, pos_x), (4, 3)))
        # Up
        elif self.x_change < 0:
            self.window.fill((133, 168, 21), ((pos_y, pos_x), (20, 8)))
            self.window.fill((133, 168, 21), ((pos_y + 2, pos_x + 8), (16, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 4, pos_x + 11), (12, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 6, pos_x + 14), (8, 3)))
            self.window.fill((133, 168, 21), ((pos_y + 8, pos_x + 17), (4, 3)))

    def draw_arena(self):
        ''' Function draws the arena. '''
        rows = self.x_window / self.block_size
        columns = self.y_window / self.block_size
        # Drawing horizontal lines
        for i in range(int(rows)):
            self.window.fill((43, 43, 43), ((0, self.block_size * i - 1), (self.y_window, 2)))
        # Drawing vertical lines
        for i in range(int(columns)):
            self.window.fill((43, 43, 43), ((self.block_size * i - 1, 0), (2, self.x_window)))


if __name__ == '__main__':
    Snake = Game()
