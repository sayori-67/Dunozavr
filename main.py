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

FPS = 80
clock = pygame.time.Clock()

game_speed = 5

ground_y = height - 100

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


game_active = True
running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not dino_is_jumping:
                dino_vel_y = jump_strength
                dino_is_jumping = True

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
            spawn_cactus()
            obstacle_spawn_timer = random.randint(OBSTACLE_SPAWN_RATE_MIN, OBSTACLE_SPAWN_RATE_MAX)

        for cactus in cactus_list[:]:
            cactus["rect"].x -= game_speed

            if dino_rect.colliderect(cactus["rect"]):
                game_active = False

            if cactus["rect"].right < 0:
                score += 1
                cactus_list.remove(cactus)

    screen.fill(WHITE)

    screen.blit(ground_image, (ground_x1, ground_blit_y))
    screen.blit(ground_image, (ground_x2, ground_blit_y))

    for cactus in cactus_list:
        screen.blit(cactus["img"], cactus["rect"])

    if game_active:
        screen.blit(current_dino_sprite, dino_rect)
    else:
        screen.blit(dino_sprites[2], dino_rect)

        draw_text(
            screen,
            "game over",
            48,
            width/2,
            height/2,
            GRAY,

        )
        draw_text(
            screen,
            f"your score's: {score}",
            48,
            width / 2,
            height / 4,
            GRAY,
        )


    pygame.display.flip()

pygame.quit()
