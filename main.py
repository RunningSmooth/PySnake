import pygame
import random

if __name__ == '__main__':
    pygame.init()
    y_window = 640
    x_window = 480
    window = pygame.display.set_mode((y_window, x_window))

    block_size = 20
    x_head = 100
    y_head = 100
    x_snake = []
    y_snake = []
    x_change = 0
    y_change = 0

    y_food = 180
    x_food = 200

    window.fill((100, 100, 100))
    pygame.draw.rect(window, (0, 255, 0), [y_head, x_head, block_size, block_size])
    for i in range(len(x_snake)):
        pygame.draw.rect(window, (0, 0, 255), [y_snake[i], x_snake[i], block_size, block_size])
    active = True

    clock = pygame.time.Clock()

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_s:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_a:
                    x_change = 0
                    y_change = -block_size
                elif event.key == pygame.K_d:
                    x_change = 0
                    y_change = block_size

        y_snake.insert(0, y_head)
        x_snake.insert(0, x_head)

        x_head += x_change
        y_head += y_change

        # checks if snake head is on food -> if yes then place new food and snake grows
        if x_head == x_food and y_head == y_food:
            set_food = True
            while set_food:
                y_food = random.randint(0, int((y_window - block_size) / block_size)) * block_size
                x_food = random.randint(0, int((x_window - block_size) / block_size)) * block_size
                # checks if food is placed on the snake -> if not then placement is valid, else roll position again
                valid = True
                if y_food != y_head and x_food != x_head:
                    for i in range(len(y_snake)):
                        if y_food == y_snake[i] and x_food == x_snake[i]:
                            valid = False
                            break
                else:
                    valid = False
                if valid:
                    set_food = False
        else:
            y_snake.__delitem__(len(y_snake) - 1)
            x_snake.__delitem__(len(x_snake) - 1)

        # checks if snake head lefts the field
        if x_head < 0 or x_head > x_window - block_size:
            active = False
        if y_head < 0 or y_head > y_window - block_size:
            active = False
        # checks if snake head is on snake body
        for i in range(len(x_snake)):
            if x_head == x_snake[i] and y_head == y_snake[i]:
                active = False

        window.fill((100, 100, 100))
        pygame.draw.rect(window, (0, 255, 0), [y_head, x_head, block_size, block_size])
        for i in range(len(x_snake)):
            pygame.draw.rect(window, (0, 0, 255), [y_snake[i], x_snake[i], block_size, block_size])
        pygame.draw.rect(window, (255, 0, 0), [y_food, x_food, block_size, block_size])

        pygame.display.update()
        clock.tick(15)
