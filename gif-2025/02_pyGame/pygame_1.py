import pygame
import sys

# 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((640, 580))
pygame.display.set_caption("3조 RPG 게임")

# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))  # 흰색 배경
    pygame.display.update()  #계속 리프레쉬
