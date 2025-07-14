import pygame
import sys
import random
import time

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm RPG")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

# 폰트
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 72)

# 이미지 로드 (사용자는 이 이름으로 저장해야 함)
background = pygame.image.load(r"C:\Users\ghgh2\OneDrive\바탕 화면\github\02_pyGame\Nature Landscapes Free Pixel Art\nature_2\origbig.png")
hero = pygame.image.load(r"C:\Users\ghgh2\OneDrive\바탕 화면\github\02_pyGame\화면 캡처 2025-07-14 141456.jpg")
enemy = pygame.image.load(r"C:\Users\ghgh2\OneDrive\바탕 화면\github\orc_attack_frames\frame_1.png")
arrow_imgs = {
    'up': pygame.image.load("assets/arrow_up.png"),
    'down': pygame.image.load("assets/arrow_down.png"),
    'left': pygame.image.load("assets/arrow_left.png"),
    'right': pygame.image.load("assets/arrow_right.png")
}
perfect_img = pygame.image.load("assets/perfect.png")
good_img = pygame.image.load("assets/good.png")
bad_img = pygame.image.load("assets/bad.png")
arrow_shot_img = pygame.image.load(r"C:\Users\ghgh2\OneDrive\바탕 화면\github\02_pyGame\Tiny RPG Character Asset Pack v1.03 -Free Soldier&Orc\Arrow(Projectile)\Arrow01(32x32).png")

# 위치
hero_pos = (50, HEIGHT - 250)
enemy_pos = (WIDTH - 250, HEIGHT - 300)
arrow_box_pos = (WIDTH // 2 - 200, 50)

# 게임 변수
clock = pygame.time.Clock()
FPS = 60
arrow_keys = ['left', 'right']
level = 1
round_num = 1
enemy_hp = 2
input_sequence = []
user_input = []
max_time = 10
arrow_result = None
show_arrow_result_time = 0

# 화살
arrow_shot_x = hero_pos[0] + 100
arrow_shot_y = hero_pos[1] + 50
arrow_shot_active = False
arrow_shot_speed = 20

# 시퀀스 생성 함수
def generate_sequence(level):
    length = 5 if level < 3 else 10
    keys = ['left', 'right'] if level < 3 else ['up', 'down', 'left', 'right']
    return [random.choice(keys) for _ in range(length)]

# 데미지 계산
def calculate_damage(seq, user_seq):
    correct = sum([1 for i, k in enumerate(user_seq) if i < len(seq) and k == seq[i]])
    if len(seq) == 0:
        return 0, 'miss'
    accuracy = correct / len(seq)
    if accuracy == 1.0:
        return 2, 'perfect'
    elif accuracy >= 0.8:
        return 1, 'good'
    elif accuracy >= 0.5:
        return 1, 'bad'
    else:
        return 0, 'miss'

# 텍스트 렌더링
def draw_text(text, pos, color=BLACK, size=36):
    f = pygame.font.SysFont("Arial", size)
    surface = f.render(text, True, color)
    screen.blit(surface, pos)

# 체력 바 그리기
def draw_hp_bar(hp):
    bar_x = WIDTH - 250
    bar_y = 30
    for i in range(2):
        color = GREEN if i < hp else GRAY
        pygame.draw.rect(screen, color, (bar_x + i * 40, bar_y, 30, 30))

# 게임 루프
running = True
input_sequence = generate_sequence(level)
start_time = time.time()

while running:
    screen.blit(background, (0, 0))
    screen.blit(hero, hero_pos)
    screen.blit(enemy, enemy_pos)

    # 라운드 & 레벨 표시
    draw_text(f"Round {round_num}", (1000, 20))
    draw_text(f"Level {level}", (1000, 60))

    # 체력 표시
    draw_hp_bar(enemy_hp)

    # 방향키 시퀀스 그리기
    for idx, key in enumerate(input_sequence):
        screen.blit(arrow_imgs[key], (arrow_box_pos[0] + idx * 50, arrow_box_pos[1]))

    # 입력 결과 표시
    if arrow_result and time.time() - show_arrow_result_time < 1.5:
        if arrow_result == 'perfect':
            screen.blit(perfect_img, (WIDTH // 2 - 100, HEIGHT // 2))
        elif arrow_result == 'good':
            screen.blit(good_img, (WIDTH // 2 - 100, HEIGHT // 2))
        elif arrow_result == 'bad':
            screen.blit(bad_img, (WIDTH // 2 - 100, HEIGHT // 2))

    # 화살 발사 애니메이션
    if arrow_shot_active:
        screen.blit(arrow_shot_img, (arrow_shot_x, arrow_shot_y))
        arrow_shot_x += arrow_shot_speed
        if arrow_shot_x > enemy_pos[0]:
            arrow_shot_active = False
            arrow_shot_x = hero_pos[0] + 100

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 방향키 입력
        if event.type == pygame.KEYDOWN and not arrow_shot_active:
            if len(user_input) < len(input_sequence):
                if event.key == pygame.K_LEFT:
                    user_input.append('left')
                elif event.key == pygame.K_RIGHT:
                    user_input.append('right')
                elif event.key == pygame.K_UP:
                    user_input.append('up')
                elif event.key == pygame.K_DOWN:
                    user_input.append('down')

    # 시간 초과 or 입력 완료
    if time.time() - start_time > max_time or len(user_input) == len(input_sequence):
        damage, result = calculate_damage(input_sequence, user_input)
        arrow_result = result
        show_arrow_result_time = time.time()
        enemy_hp -= damage
        input_sequence = generate_sequence(level)
        user_input = []
        start_time = time.time()
        arrow_shot_active = True
        round_num += 1
        if round_num % 3 == 0:
            level += 1
            max_time = max(5, max_time - 1)

    # 게임 승리/패배 처리
    if enemy_hp <= 0:
        draw_text("YOU WIN!", (WIDTH // 2 - 150, HEIGHT // 2 - 50), RED, 72)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()