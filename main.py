import pygame
import random

# Инициализация Pygame
pygame.init()

# Основные параметры
WIDTH, HEIGHT = 400, 600  # Размер окна
FPS = 60  # Частота кадров
LIVES = 3  # Количество жизней

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Загрузка и масштабирование изображений
background_image = pygame.image.load("фон 1.png")
original_width, original_height = background_image.get_size()

# Масштабирование фона пропорционально по ширине окна
scale_factor = WIDTH / original_width
new_width = WIDTH
new_height = int(original_height * scale_factor)
background_image = pygame.transform.scale(background_image, (new_width, new_height))
background_rect = background_image.get_rect()

# Уменьшение персонажа
character_image = pygame.image.load("утенок.png")
CHARACTER_WIDTH, CHARACTER_HEIGHT = 1654 // 8, 2339 // 8
character_image = pygame.transform.scale(character_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

# Увеличение препятствий
obstacle_image = pygame.image.load("бревно.png")
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = int(278 * 1.5), int(278 * 1.5)
obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Game")

# Функция для отображения текста
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = character_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.top = 50
        self.is_jumping = False
        self.speed_y = 0
        self.lives = LIVES
        self.invincible = False
        self.invincible_start = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.speed_y = -10  # Скорость прыжка

        if self.is_jumping:
            self.speed_y += 0.5  # Гравитация
            self.rect.y += self.speed_y

            if self.rect.top >= 50:
                self.rect.top = 50
                self.is_jumping = False

        if self.invincible:
            current_time = pygame.time.get_ticks()
            if (current_time - self.invincible_start) < 1500:  # 1.5 секунды
                if current_time % 300 < 150:
                    self.image.set_alpha(0)
                else:
                    self.image.set_alpha(255)
            else:
                self.invincible = False
                self.image.set_alpha(255)

    def collide(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_start = pygame.time.get_ticks()

# Класс для препятствий
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, WIDTH - OBSTACLE_WIDTH))
        self.rect.y = random.randint(HEIGHT, HEIGHT + 200)
        self.speed = 1

    def update(self):
        self.rect.y -= self.speed  # Движение снизу вверх
        if self.rect.bottom < 0:
            self.rect.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
            self.rect.y = random.randint(HEIGHT, HEIGHT + 200)

# Основной цикл игры
def main():
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Character()
    all_sprites.add(player)

    for _ in range(5):  # Уменьшено количество препятствий для увеличения промежутков
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    running = True
    background_y = 0
    background_speed = 1

    start_time = pygame.time.get_ticks()
    waiting = True

    while running and waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False

        screen.fill(BLACK)
        draw_text(screen, "Game starting in 3 seconds...", 36, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 3000:
            waiting = False

    game_over = False
    fade_out = False
    player_exit = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        background_y -= background_speed
        if background_y <= -background_rect.height:
            background_y = 0

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits and not player.is_jumping and not player.invincible:
            player.collide()
            if player.lives <= 0:
                game_over = True

        if not game_over and background_y <= -new_height + HEIGHT:
            fade_out = True

        if game_over or fade_out:
            if fade_out:
                player_exit = True
            else:
                screen.fill(BLACK)
                draw_text(screen, "Game Over", 36, WIDTH // 2, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000)
            running = False

        screen.blit(background_image, (0, background_y))
        screen.blit(background_image, (0, background_y + background_rect.height))
        all_sprites.draw(screen)
        draw_text(screen, f"Lives: {player.lives}", 24, WIDTH // 2, 10)

        pygame.display.flip()

    if player_exit:
        while player.rect.top < HEIGHT:
            player.rect.y += 2
            screen.blit(background_image, (0, background_y))
            screen.blit(background_image, (0, background_y + background_rect.height))
            all_sprites.draw(screen)
            draw_text(screen, f"Lives: {player.lives}", 24, WIDTH // 2, 10)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
