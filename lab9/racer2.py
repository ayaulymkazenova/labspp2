#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initializing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
LAST_COIN_MILESTONE = 0
COIN_THRESHOLD = 5  # Increase speed every 5 coins

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load and scale background
background_original = pygame.image.load("AnimatedStreet.png")
background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Helper function to load and scale images
def load_and_scale_image(filename, width, height):
    try:
        original_image = pygame.image.load(filename)
        return pygame.transform.scale(original_image, (width, height))
    except pygame.error:
        # Fallback: create a simple colored circle if image missing
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 215, 0), (width//2, height//2), min(width, height)//2)
        return surface

#Create display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Racer")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = load_and_scale_image("Player.png", 40, 80)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = load_and_scale_image("Enemy.png", 40, 80)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# 🪙 Coin class with weight
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 1, 1, 2, 3])  # 1 is common, 2/3 are rare
        # Try to load different coin images based on weight (optional)
        image_map = {1: "Coin.png", 2: "Coin2.png", 3: "Coin3.png"}
        img_file = image_map.get(self.weight, "Coin.png")
        try:
            self.image = load_and_scale_image(img_file, 30, 30)
        except:
            self.image = load_and_scale_image("Coin.png", 30, 30)
        self.rect = self.image.get_rect()
        self.reset_position()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)
        # Optional: re-randomize weight on reset
        self.weight = random.choice([1, 1, 1, 2, 3])

# Create sprites
P1 = Player()
E1 = Enemy()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
# Start with one coin
C1 = Coin()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Custom events
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Optional: spawn additional coins over time (comment out if not needed)
# SPAWN_COIN = pygame.USEREVENT + 2
# pygame.time.set_timer(SPAWN_COIN, 3000)  # every 3 seconds

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Optional: background speed increase

        # Optional coin spawner (uncomment if using SPAWN_COIN)
        # if event.type == SPAWN_COIN:
        #     new_coin = Coin()
        #     coins.add(new_coin)
        #     all_sprites.add(new_coin)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Display score and coin count
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    coins_text = font_small.render(f"Coins: {COIN_SCORE}", True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))

    # Move and draw all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # 🪙 Coin collection
    collected = pygame.sprite.spritecollide(P1, coins, True)
    if collected:
        try:
            pygame.mixer.Sound('coin.wav').play()
        except:
            pass
        for coin in collected:
            COIN_SCORE += coin.weight
            # Respawn a new coin immediately
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

        # 🚀 Increase enemy speed every COIN_THRESHOLD coins
        current_milestone = COIN_SCORE // COIN_THRESHOLD
        if current_milestone > LAST_COIN_MILESTONE:
            LAST_COIN_MILESTONE = current_milestone
            SPEED += 1  # Increase game speed

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        try:
            pygame.mixer.Sound('crash.mp3').play()
        except:
            pass
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)