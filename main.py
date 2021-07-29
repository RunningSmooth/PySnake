import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((640, 480))
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
