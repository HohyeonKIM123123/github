import pygame
import os

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HAPPY")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(filename):
    return pygame.image.load(os.path.join(BASE_DIR, filename)).convert_alpha()

background = load_image("origbig.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock.tick(60)
