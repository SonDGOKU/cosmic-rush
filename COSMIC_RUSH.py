

import pygame
import random

pygame.init()
pygame.mixer.init()

# Window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Rush")

# Images
BG = pygame.transform.scale(
    pygame.image.load("bg.jpeg"),
    (WIDTH, HEIGHT)
)

PLAYER_IMG = pygame.transform.scale(
    pygame.image.load("player.png"),
    (70, 70)
)

ENEMY_IMG = pygame.transform.scale(
    pygame.image.load("enemy.png"),
    (60, 60)
)

DEBRIS_IMG = pygame.transform.scale(
    pygame.image.load("debris.png"),
    (25, 25)
)

# Sounds
LASER_SOUND = pygame.mixer.Sound("laser.wav")
HIT_SOUND = pygame.mixer.Sound("hit.wav")

# Fonts
FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 60)

# Player
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_vel = 7

# Bullets
bullets = []
bullet_vel = 10

# Enemies
enemies = []
enemy_vel = 2
enemy_spawn_delay = 60

# Space Debris
debris_list = []

for i in range(10):
    debris = {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "speed": random.randint(1, 2)
    }

    debris_list.append(debris)

# Score
score = 0

clock = pygame.time.Clock()


def draw_space_debris():
    for debris in debris_list:

        WIN.blit(
            DEBRIS_IMG,
            (debris["x"], debris["y"])
        )

        debris["y"] += debris["speed"]

        # Reset debris
        if debris["y"] > HEIGHT:
            debris["y"] = -50
            debris["x"] = random.randint(0, WIDTH)


def draw_window():
    WIN.blit(BG, (0, 0))

    # Draw debris
    draw_space_debris()

    # Draw player
    WIN.blit(PLAYER_IMG, (player_x, player_y))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)

    # Draw enemies
    for enemy in enemies:
        WIN.blit(ENEMY_IMG, (enemy.x, enemy.y))

    # Score
    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (10, 10))

    pygame.display.update()


def menu():
    while True:
        WIN.blit(BG, (0, 0))

        draw_space_debris()

        title = BIG_FONT.render("COSMIC RUSH", 1, (0, 255, 255))
        start = FONT.render("Press SPACE to Start", 1, "white")

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 300))
        WIN.blit(start, (WIDTH//2 - start.get_width()//2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def game_over():
    WIN.blit(BG, (0, 0))

    draw_space_debris()

    over_text = BIG_FONT.render("GAME OVER", 1, "red")
    score_text = FONT.render(f"Final Score: {score}", 1, "white")

    WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, 300))
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 400))

    pygame.display.update()

    pygame.time.delay(4000)


def main():
    global player_x, score

    menu()

    run = True
    frame = 0

    while run:
        clock.tick(60)
        frame += 1

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Shoot bullet
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(
                        player_x + 30,
                        player_y,
                        5,
                        20
                    )

                    bullets.append(bullet)
                    LASER_SOUND.play()

        # Movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_vel

        if keys[pygame.K_RIGHT] and player_x < WIDTH - 70:
            player_x += player_vel

        # Bullet movement
        for bullet in bullets[:]:
            bullet.y -= bullet_vel

            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if frame % enemy_spawn_delay == 0:
            enemy_x = random.randint(0, WIDTH - 60)

            enemy = pygame.Rect(
                enemy_x,
                -60,
                60,
                60
            )

            enemies.append(enemy)

        # Enemy movement
        player_rect = pygame.Rect(player_x, player_y, 70, 70)

        for enemy in enemies[:]:
            enemy.y += enemy_vel

            # Collision with player
            if enemy.colliderect(player_rect):
                HIT_SOUND.play()
                game_over()
                run = False

            # Remove enemy if off screen
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

            # Bullet collision
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):

                    if enemy in enemies:
                        enemies.remove(enemy)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    HIT_SOUND.play()
                    score += 1
                    break

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()