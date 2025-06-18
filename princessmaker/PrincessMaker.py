import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("신해솔 공주만들기 대작전")
clock = pygame.time.Clock()

# 배경
intro_background = pygame.image.load("시작화면.png")
intro_background2 = pygame.image.load("찐시작화면.png")
play_background = pygame.image.load("게임진행화면.png")
bad_ending_background = pygame.image.load("배드엔딩.png")
happy_ending_background = pygame.image.load("해피엔딩배경.png")

# 공주
princess_x = 100
princess_y = 400
princess_width = 80
princess_height = 150
princess_bow = pygame.image.load("돌.png").convert_alpha()
jumping = False
jump_speed = 0
gravity = 1
SPEED = 7
life = 3

# 장애물
bird = pygame.image.load("새.png")
puddle = pygame.image.load("웅덩이.png")
TralaleroTralala = pygame.image.load("트랄라레로트랄랄라.png")
obstacles = []
obstacle_timer = 0

# 진행
progress = 0
progress_speed = 0.1
princess_run = [pygame.image.load("공주달려1.png").convert_alpha(),pygame.image.load("공주달려2.png").convert_alpha(),pygame.image.load("공주달려3.png").convert_alpha(),pygame.image.load("공주달려4.png").convert_alpha()]
run_frame = 0
frame_delay = 5
frame_count = 0
run_frame_sequence = [0, 1, 2, 3, 2, 1, 0]
run_frame_index = 0
cloud1 = pygame.image.load("구름1.png")
cloud = [[800, 70], [1200, 150], [1600, 30]]

# 메인 함수 : 시작화면
def game_intro():
    screen.blit(intro_background, (0, 0))
    pygame.display.update()
    pygame.time.delay(1000)
    screen.blit(intro_background2, (0, 0))
    pygame.display.update()

    # 시작화면에서 스페이스바 누르면 게임 시작
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game()  # 게임 실행

def bad_ending():
    screen.blit(bad_ending_background, (0, 0))
    pygame.display.update()

    pygame.mixer.music.stop()
    pygame.mixer.music.load("배드엔딩브금.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(1)

    # 배드엔딩 화면에서 스페이스 누르면 다시 시작화면
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_intro()

def happy_ending():
    screen.blit(happy_ending_background, (0, 0))
    ending_img1 = pygame.image.load("해피엔딩1.png").convert()
    ending_img2 = pygame.image.load("해피엔딩2.png").convert()
    ending_img3 = pygame.image.load("해피엔딩3.png").convert()
    ending_img4 = pygame.image.load("공주합격.png").convert()

    pygame.mixer.music.stop()
    pygame.mixer.music.load("해피엔딩브금.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(1)

    # 페이드인
    def fade_in_image(image, duration=60):
        alpha = 0
        fade_surface = image.copy()
        fade_surface.set_alpha(alpha)

        #그라데이션 엔딩
        for _ in range(duration):
            alpha += int(255 / duration)
            if alpha > 255:
                alpha = 255
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(60)

    # 순서대로 페이드인
    fade_in_image(ending_img1)
    pygame.time.delay(600)
    fade_in_image(ending_img2)
    pygame.time.delay(600)
    fade_in_image(ending_img3)
    pygame.time.delay(600)
    fade_in_image(ending_img4)
    pygame.time.delay(600)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 본 게임 진행
def game():
    global princess_x, princess_y, princess_width, princess_height, jumping, jump_speed, life, obstacles, obstacle_timer, cloud, progress, progress_speed, run_frame, frame_delay, run_frame_index, frame_count
    life = 3
    obstacles = []
    progress = 0
    running = True
    while running:
        clock.tick(60)
        screen.blit(play_background, (0, 0) )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 주인공 달리기 사진 반복
        frame_count += 1
        if frame_count >= frame_delay:
            run_frame_index = (run_frame_index + 1) % len(run_frame_sequence)
            frame_count = 0

        keys = pygame.key.get_pressed()
        # 기본, 숙이기, 점프 사진 상태
        if not jumping and not keys[pygame.K_DOWN]:
            current_frame = run_frame_sequence[run_frame_index]
            screen.blit(princess_run[current_frame], (princess_x, princess_y))
        elif keys[pygame.K_DOWN]:
            screen.blit(princess_bow, (princess_x, princess_y))
        else:
            screen.blit(princess_run[0], (princess_x, princess_y))

        # 점프
        if keys[pygame.K_SPACE] and not jumping:
            jumping = True
            jump_speed = -15
        if jumping:
            princess_y += jump_speed
            jump_speed += gravity
            if princess_y >= 400:
                princess_y = 400
                jumping = False

        # 숙이기
        if not jumping:
            if keys[pygame.K_DOWN]:
                princess_y = 470
                princess_height = 40
            else:
                princess_y = 400
                princess_height = 150

        # 진행도 바
        pygame.draw.rect(screen, (200, 200, 200), [250, 10, 400, 20])
        pygame.draw.rect(screen, (255, 100, 100), [250, 10, 4 * progress, 20])
        progress += progress_speed
        if progress >= 100:
            progress = 100
            happy_ending()

        # 장애물 생성
        obstacle_timer += 1
        if obstacle_timer > 50:
            obstacle_timer = 0
            kind = random.choice(["bird", "TralaleroTralala", "hole"])
            if kind == "bird":
                obstacles.append([900, 400, 50, 50, "bird"])
            elif kind == "TralaleroTralala":
                obstacles.append([900, 470, 30, 30, "TralaleroTralala"])
            elif kind == "hole":
                obstacles.append([900, 517, 60, 15, "hole"])
        for obs in obstacles:
            if obs[4] == "bird":
                screen.blit(bird, (obs[0], obs[1]))
            elif obs[4] == "TralaleroTralala":
                screen.blit(TralaleroTralala, (obs[0], obs[1]))
            elif obs[4] == "hole":
                screen.blit(puddle, (obs[0], obs[1]))
            obs[0] -= SPEED

        # 장애물 충돌 체크
        for obs in obstacles[:]:
            if (princess_x < obs[0] + obs[2] and princess_x + princess_width > obs[0] and princess_y < obs[1] + obs[3] and princess_y + princess_height > obs[1]):
                life -= 1
                obstacles.remove(obs)
                if life <= 0:
                    bad_ending()

        # 구름 이동
        for c in cloud:
            screen.blit(cloud1, (c[0], c[1]))
            c[0] -= 2
            if c[0] < -200:
                c[0] = 1000
                c[1] = random.randint(50, 200)

        # 남은 목숨 표시
        font = pygame.font.SysFont(None, 36)
        life_text = font.render(f"LIFE : {life}", True, (255, 0, 0))
        screen.blit(life_text, (10, 10))

        pygame.display.update()

game_intro()
