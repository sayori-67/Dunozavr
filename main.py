import pygame
import random

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Google_dino")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

score = 0

FPS = 60
clock = pygame.time.Clock()

game_speed = 5

ground_y = height - 100

game_active = True


ground_image = pygame.image.load("image/ground/Ground.png").convert_alpha()

ground_rect = ground_image.get_rect()
ground_width = ground_rect.width

ground_x1 = 0
ground_x2 = ground_width

ground_blit_y = ground_y - ground_rect.height

dino_sprites = [
    pygame.image.load("image/dino/Dino-left-up.png").convert_alpha(),
    pygame.image.load("image/dino/Dino-right-up.png").convert_alpha(),
    pygame.image.load("image/dino/Dino-stand.png").convert_alpha()
]

dino_rect = dino_sprites[0].get_rect()
dino_rect.x = 100

dino_y = ground_y
dino_vel_y = 0

gravity = 0.6
jump_strength = -15

dino_is_jumping = False

dino_animation_index = 0
dino_animation_timer = 0
DINO_ANIMATION_SPEED = 0.15
dino_rect.bottom = int(dino_y)

cactus_list = []
obstacle_spawn_timer = 120
OBSTACLE_SPAWN_RATE_MIN = 90
OBSTACLE_SPAWN_RATE_MAX = 200

cactus_sprites = [
    pygame.image.load("image/cactus/Cactus-1.png").convert_alpha(),
    pygame.image.load("image/cactus/Cactus-2.png").convert_alpha(),
    pygame.image.load("image/cactus/Cactus-3.png").convert_alpha(),
    pygame.image.load("image/cactus/Cactus-4.png").convert_alpha(),
    pygame.image.load("image/cactus/Cactus-5.png").convert_alpha()
]

def spawn_cactus():
    cactus_img = random.choice(cactus_sprites)
    cactus_rect = cactus_img.get_rect()
    cactus_rect.x = width + random.randint(0, 100)
    cactus_rect.bottom = ground_y
    cactus_list.append({
        "img" : cactus_img,
        "rect" : cactus_rect
    })

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

ptero_list = []
PTERO_ANIMATION_SPEED = 0.1
PTERO_SPAWN_CHANCE = 0.3
PTERO_Y_POSITIONS = [ground_y - 80, ground_y - 120, ground_y -40]

try:
    ptero_sprites =  [pygame.image.load("image/ptero/Ptero1.png").convert_alpha(),
        pygame.image.load("image/ptero/Ptero2.png").convert_alpha()]
except pygame.error as e:
    print('error', e)
    ptero_sprites = []

def spawn_ptero():
    if not ptero_sprites:
        return
    ptero_rect = ptero_sprites[0].get_rect()
    ptero_rect.x = width + random.randint(100,200)
    ptero_rect.centery = random.choice(PTERO_Y_POSITIONS)

    ptero_list.append({
        "sprites":ptero_sprites,
        "rect":ptero_rect,
        "anim_index":0,
        "anim_timer":0
    })

def restart_game():
    """"функция перезапуска игры"""
    global score, game_active
    global dino_y, dino_vel_y, dino_is_jumping
    global dino_animation_index, dino_animation_timer
    global ground_x1, ground_x2, obstacle_spawn_timer

    score = 0
    game_active = True
    dino_y = ground_y
    dino_vel_y = 0
    dino_is_jumping = False
    dino_rect.bottom = int(dino_y)

    dino_animation_index =0
    dino_animation_timer = 0.0
    ground_x1 = 0
    ground_x2 = ground_width

    cactus_list.clear()
    ptero_list.clear()
    obstacle_spawn_timer = 120


running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_active:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not dino_is_jumping:
                    dino_vel_y = jump_strength
                    dino_is_jumping = True
            else:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
    if game_active:

        if dino_is_jumping or dino_y < ground_y:
            dino_vel_y += gravity
            dino_y += dino_vel_y

            if dino_y >= ground_y:
                dino_y = ground_y
                dino_vel_y = 0
                dino_is_jumping = False

        if dino_is_jumping:
            current_dino_sprite = dino_sprites[2]
        else:
            dino_animation_timer += DINO_ANIMATION_SPEED

            if dino_animation_timer >= 1:
                dino_animation_timer = 0
                dino_animation_index = (dino_animation_index + 1) % 2

            current_dino_sprite = dino_sprites[dino_animation_index]

        dino_rect.bottom = int(dino_y)

        ground_x1 -= game_speed
        ground_x2 -= game_speed

        if ground_x1 <= -ground_width:
            ground_x1 = ground_x2 + ground_width

        if ground_x2 <= -ground_width:
            ground_x2 = ground_x1 + ground_width
        obstacle_spawn_timer -= 1
        if obstacle_spawn_timer <= 0:
            if random.random() < PTERO_SPAWN_CHANCE and ptero_sprites:
                spawn_ptero()
            else:
                spawn_cactus()
            obstacle_spawn_timer = random.randint(OBSTACLE_SPAWN_RATE_MIN, OBSTACLE_SPAWN_RATE_MAX)

        for cactus in cactus_list[:]:
            cactus["rect"].x -= game_speed

            if dino_rect.colliderect(cactus["rect"]):
                game_active = False

            if cactus["rect"].right < 0:
                score += 1
                cactus_list.remove(cactus)

        for ptero in ptero_list[:]:
            ptero["rect"].x -= game_speed
            ptero["anim_timer"] += PTERO_ANIMATION_SPEED

            if ptero["anim_timer"] >= 1:
                ptero["anim_timer"] = 0
                ptero["anim_index"] = (ptero["anim_index"] + 1) % len(ptero_sprites)

            if ptero["rect"].right < 0:
                ptero_list.remove(ptero)
                score += 15

    screen.fill(WHITE)

    screen.blit(ground_image, (ground_x1, ground_blit_y))
    screen.blit(ground_image, (ground_x2, ground_blit_y))

    for cactus in cactus_list:
        screen.blit(cactus["img"], cactus["rect"])

    if ptero_sprites:
        for ptero in ptero_list:
            current_ptero_sprite = ptero_sprites[ptero["anim_index"]]
            screen.blit(current_ptero_sprite, ptero["rect"])

    if game_active:
        screen.blit(current_dino_sprite, dino_rect)
    else:
        screen.blit(dino_sprites[2], dino_rect)

        draw_text(
            screen,
            "game over",
            48,
            width / 2,
            height / 4,
            GRAY
        )

        draw_text(
            screen,
            f"очки: {score}",
            40,
            width / 2,
            height / 2,
            GRAY)

    if not game_active:
        draw_text(
            screen,
            "game over",
            48,
            width / 2,
            height / 2,
            GRAY
        )
        draw_text(
            screen,
            f"ваши очки: {score}",
            48,
            width / 2,
            height / 4,
            GRAY
        )
        draw_text(screen, "presss to r", 26, width / 2, height / 2 +50, GRAY)
        draw_text(screen, "presss to esc", 26, width / 2, height / 2 +90, GRAY)


    pygame.display.flip()

pygame.quit()