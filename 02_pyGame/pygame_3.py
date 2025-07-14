import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("캐릭터 이동")

character = pygame.image.load("C:/Users/ghgh2/OneDrive/바탕 화면/github/02-pyGame/character.png")
# 캐릭터 사이즈를 작게 조절 (원본의 1/5 크기로)
character = pygame.transform.scale(character, (character.get_width() // 20, character.get_height() // 20))
x, y = 100, 100
speed = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    screen.fill((0, 0, 0))
    screen.blit(character, (x, y))
    pygame.display.update()