import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRICK_COLOR = (200, 0, 0)
BALL_COLOR = (0, 255, 255)
PADDLE_COLOR = (0, 100, 255)

# 공 설정
ball_radius = 10
ball_speed = [5, -5]
ball_pos = [WIDTH // 2, HEIGHT // 2]

# 패들 설정
paddle_width = 100
paddle_height = 15
paddle_speed = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 40, paddle_width, paddle_height)

# 벽돌 설정
brick_rows = 5
brick_cols = 10
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height + 60, brick_width - 2, brick_height - 2)
        bricks.append(brick)

# 점수
score = 0
font = pygame.font.SysFont("Arial", 30)

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 움직이기
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-paddle_speed, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(paddle_speed, 0)

    # 공 움직이기
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    ball = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)

    # 벽과 충돌
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # 패들과 충돌
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # 벽돌과 충돌
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        del bricks[hit_index]
        ball_speed[1] = -ball_speed[1]
        score += 1

    # 바닥에 떨어짐
    if ball.bottom >= HEIGHT:
        running = False  # 게임 종료

    # 그리기
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.circle(screen, BALL_COLOR, ball_pos, ball_radius)

    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

# 종료
pygame.quit()