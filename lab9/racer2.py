import pygame
import random
import sys

pygame.init()

# ========== WINDOW ==========
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# ========== COLORS ==========
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)

# ========== PLAYER ==========
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(200, 500))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 20:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 20:
            self.rect.x += self.speed

# ========== ENEMY ==========
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill((0, 0, 200))
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -50))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(40, 360), -50)

# ========== COIN ==========
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 5])   # разные веса монет
        self.image = pygame.Surface((25, 25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(random.randint(40, 360), -20))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Sprites
player = Player()
enemy = Enemy()

player_group = pygame.sprite.Group(player)
enemy_group = pygame.sprite.Group(enemy)
coin_group = pygame.sprite.Group()

coins_collected = 0
next_speed_increase = 10   # каждые 10 "веса" ускорение Enemy

# GAME LOOP
COIN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_EVENT, 1500)  # монета появляется каждые 1.5 сек

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == COIN_EVENT:
            coin_group.add(Coin())

    screen.fill(GRAY)

    # === Update ===
    player_group.update()
    enemy_group.update()
    coin_group.update()

    # === Collision with enemy ===
    if pygame.sprite.spritecollide(player, enemy_group, False):
        print("GAME OVER!")
        sys.exit()

    # === Collision with coins ===
    collided_coins = pygame.sprite.spritecollide(player, coin_group, True)
    for coin in collided_coins:
        coins_collected += coin.weight

        # === Increase enemy speed ===
        if coins_collected >= next_speed_increase:
            enemy.speed += 1
            next_speed_increase += 10

    # === Draw ===
    player_group.draw(screen)
    enemy_group.draw(screen)
    coin_group.draw(screen)

    # === Show coin counter ===
    coin_text = font.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(coin_text, (280, 10))

    pygame.display.update()
    clock.tick(60)

