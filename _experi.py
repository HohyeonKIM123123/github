import pygame
import sys
import random
import time
import os
# 초기화
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm RPG")
clock = pygame.time.Clock()
FPS = 60
# 색상/폰트
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)
FONT = pygame.font.SysFont("malgungothic", 48)
SMALL_FONT = pygame.font.SysFont("malgungothic", 32)
BIG_FONT = pygame.font.SysFont("Arial", 72)
# 상대 경로를 통한 이미지 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_image(filename):
    return pygame.image.load(os.path.join(BASE_DIR, filename)).convert_alpha()
# 이미지 로드
background = load_image("origbig.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
hero_img_raw = load_image("hero.png")
hero_width, hero_height = hero_img_raw.get_size()
hero = pygame.transform.scale(hero_img_raw, (int(hero_width * 0.15), int(hero_height * 0.15)))
enemy_img_raw = load_image("monster.png")
enemy_width, enemy_height = enemy_img_raw.get_size()
enemy = pygame.transform.scale(enemy_img_raw, (int(enemy_width * 0.4), int(enemy_height * 0.4)))
arrow_shot_img = load_image("arrow1.png")
# 위치
hero_pos = (50, HEIGHT - hero.get_height() - 50)
enemy_pos = (WIDTH - enemy.get_width() - 50, HEIGHT - enemy.get_height() - 50)
# 방향키 문자열 매핑
KEY_MAP = {
    pygame.K_LEFT: "←",
    pygame.K_RIGHT: "→",
    pygame.K_UP: "↑",
    pygame.K_DOWN: "↓"
}
# 체력 바 그리기
def draw_hp_bar(hp):
    bar_x = WIDTH - 250
    bar_y = 30
    for i in range(2):
        color = GREEN if i < hp else GRAY
        pygame.draw.rect(screen, color, (bar_x + i * 40, bar_y, 30, 30))
# 텍스트 렌더링
def draw_text(text, font, color, surface, x, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    surface.blit(render, rect)
# 방향키 시퀀스 그리기
def draw_directions(direction_list, user_input, start_y):
    box_size = 50
    margin = 8
    max_per_row = 10
    for idx, key in enumerate(direction_list):
        row = idx // max_per_row
        col = idx % max_per_row
        total_width = (box_size + margin) * min(len(direction_list), max_per_row)
        start_x = WIDTH // 2 - total_width // 2
        x = start_x + col * (box_size + margin)
        y = start_y + row * (box_size + margin)
        rect = pygame.Rect(x, y, box_size, box_size)
        if direction_list is user_input:
            color = (0, 200, 0)
        else:
            if idx < len(user_input):
                if user_input[idx] == key:
                    color = (0, 200, 0)
                else:
                    color = (200, 0, 0)
            else:
                color = (100, 100, 100)
        pygame.draw.rect(screen, color, rect, border_radius=6)
        if key in KEY_MAP:
            key_text = KEY_MAP[key]
            text_surf = SMALL_FONT.render(key_text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
# 난이도 설정
def get_stage_settings(stage):
    input_length = 5 + max(0, stage - 1)
    time_limit = max(1.0, 10 - (stage - 1) * 0.3)
    if stage == 1:
        allowed_keys = [pygame.K_LEFT, pygame.K_RIGHT]
    elif stage == 2:
        allowed_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]
    else:
        allowed_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    return input_length, time_limit, allowed_keys
# 랜덤 시퀀스 생성
def generate_random_directions(length, allowed_keys):
    return [random.choice(allowed_keys) for _ in range(length)]
# 게임 시작 대기 화면
def wait_for_start():
    screen.blit(background, (0, 0))
    draw_text("게임을 시작하려면 Y를 누르세요", SMALL_FONT, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return
# 방향키 입력 미니게임
def direction_mini_game(stage):
    input_length, time_limit, allowed_keys = get_stage_settings(stage)
    target = generate_random_directions(input_length, allowed_keys)
    user_input = []
    start_time = pygame.time.get_ticks()
    input_completed = False
    result_show_start = None
    correct_count = 0
    timer_stopped = False
    while True:
        screen.blit(background, (0, 0))
        draw_text(f"방향키 입력 미니게임 (단계 {stage})", SMALL_FONT, (200, 200, 200), screen, WIDTH // 2, 60)
        current_time = pygame.time.get_ticks()
        if not timer_stopped:
            elapsed_time = (current_time - start_time) / 1000
            remaining_time = max(0, time_limit - elapsed_time)
        elif result_show_start is not None:
            remaining_time = max(0, time_limit - (result_show_start - start_time) / 1000)
        else:
            remaining_time = 0
        draw_text(f"남은 시간: {remaining_time:.1f} / {time_limit:.1f} 초", SMALL_FONT, (255, 100, 100), screen, WIDTH // 2, HEIGHT // 4 - 40)
        draw_text("입력할 방향:", SMALL_FONT, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        draw_directions(target, user_input, HEIGHT // 4 + 40)
        draw_text("입력한 방향:", SMALL_FONT, (200, 200, 200), screen, WIDTH // 2, HEIGHT // 2 + 80)
        draw_directions(user_input, user_input, HEIGHT // 2 + 110)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not input_completed:
                if event.key in allowed_keys and len(user_input) < len(target):
                    user_input.append(event.key)
                    if len(user_input) == len(target):
                        input_completed = True
                        timer_stopped = True
                        correct_count = sum(1 for i in range(len(target)) if user_input[i] == target[i])
                        result_show_start = pygame.time.get_ticks()
        if not input_completed and not timer_stopped and elapsed_time >= time_limit:
            input_completed = True
            timer_stopped = True
            correct_count = sum(1 for i in range(len(user_input)) if user_input[i] == target[i])
            result_show_start = pygame.time.get_ticks()
        if input_completed:
            color = (100, 255, 100) if correct_count == len(target) else (255, 200, 50)
            draw_text(f"정답 수: {correct_count}/{len(target)}", FONT, color, screen, WIDTH // 2, HEIGHT * 0.8)
            if result_show_start is not None and pygame.time.get_ticks() - result_show_start > 1200:
                return correct_count, len(target)
        pygame.display.flip()
        clock.tick(60)
# 메인 게임 루프
def main():
    stage = 1
    round_num = 1
    enemy_hp = 10
    max_hp = 10
    running = True
    while running:
        wait_for_start()
        while enemy_hp > 0:
            screen.blit(background, (0, 0))
            screen.blit(hero, hero_pos)
            screen.blit(enemy, enemy_pos)
            draw_text(f"Round {round_num}", SMALL_FONT, BLACK, screen, 1100, 40)
            draw_text(f"Level {stage}", SMALL_FONT, BLACK, screen, 1100, 90)
            draw_hp_bar(enemy_hp)
            pygame.display.flip()
            pygame.time.wait(800)
            correct, total = direction_mini_game(stage)
            if correct == total:
                result = "PERFECT!"
                damage = 2
            elif correct >= total * 0.8:
                result = "GOOD!"
                damage = 1
            elif correct >= total * 0.5:
                result = "BAD!"
                damage = 1
            else:
                result = "MISS!"
                damage = 0
            enemy_hp -= damage
            screen.blit(background, (0, 0))
            screen.blit(hero, hero_pos)
            screen.blit(enemy, enemy_pos)
            draw_text(result, BIG_FONT, RED if result == "PERFECT!" else (255, 200, 50), screen, WIDTH // 2, HEIGHT // 2)
            draw_hp_bar(max(0, enemy_hp))
            pygame.display.flip()
            pygame.time.wait(1200)
            round_num += 1
            if round_num % 3 == 0:
                stage += 1
        screen.blit(background, (0, 0))
        draw_text("YOU WIN!", BIG_FONT, RED, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("다시 하려면 Y, 종료는 N", FONT, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        stage = 1
                        round_num = 1
                        enemy_hp = max_hp
                        waiting = False
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
if __name__ == "__main__":
    main()