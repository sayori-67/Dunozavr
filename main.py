import pygame

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dunozavr")

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

FPS = 60

clock = pygame.time.Clock()

ground_y = height - 100

dino_sprites = [
    pygame.image.load("image/dino/Dino-left-up.png").convert_alpha(),
    pygame.image.load("image/dino/Dino-right-up.png").convert_alpha(),
    pygame.image.load("image/dino/Dino-stand.png").convert_alpha()

]

dino_rect = dino_sprites[0].get_rect()
dino_rect.x = 100

dino_y = ground_y
dino_vel_y = 0

graviti = 0.6
jump_strength = -15
dino_is_jumping = False

dino_animation_index = 0
dino_animation_timer = 0
DINO_ANIMATION_SPEED = 0.15

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

    if dino_is_jumping or dino_y < ground_y:
        dino_vel_y = jump_strength
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

    screen.fill(WHITE)

    screen.blit(current_dino_sprite, dino_rect)
    pygame.display.flip()

pygame.quit()
