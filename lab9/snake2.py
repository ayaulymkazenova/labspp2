import pygame
import random
import sys

pygame.init()

# ========== CONSTANTS ==========
WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake with Levels & Timed Food")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# ========== COLORS ==========
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (30, 144, 255)

# ========== SNAKE ==========
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"
speed = 8

# ========== GAME STATE ==========
score = 0
level = 1
next_level_score = 4   # каждые 4 очка — новый уровень

# ========== FOOD ==========
class Food:
    def __init__(self):
        self.position = self.generate_food_position()
        self.weight = random.choice([1, 2, 5])
        self.color = GOLD if self.weight == 5 else RED
        self.timer = random.choice([0, 2000, 3000])  # 0 = вечная еда

    def generate_food_position(self):
        while True:
            x = random.randint(0, (WIDTH // CELL) - 1) * CELL
            y = random.randint(0, (HEIGHT // CELL) - 1) * CELL
            if (x, y) not in snake:
                return (x, y)

food = Food()
FOOD_TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FOOD_TIMER_EVENT, 1000)

food_alive_time = 0

# ========== GAME LOOP ==========
while True:
    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == FOOD_TIMER_EVENT and food.timer > 0:
            food_alive_time += 1000
            if food_alive_time >= food.timer:
                food = Food()
                food_alive_time = 0

    # ---- INPUT ----
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != "DOWN":
        direction = "UP"
    if keys[pygame.K_DOWN] and direction != "UP":
        direction = "DOWN"
    if keys[pygame.K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    if keys[pygame.K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"

    # ---- MOVE SNAKE ----
    x, y = snake[0]
    if direction == "UP": y -= CELL
    if direction == "DOWN": y += CELL
    if direction == "LEFT": x -= CELL
    if direction == "RIGHT": x += CELL

    new_head = (x, y)

    # ---- WALL COLLISION ----
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        print("GAME OVER! Hit the wall.")
        sys.exit()

    # ---- SELF COLLISION ----
    if new_head in snake:
        print("GAME OVER! Hit itself.")
        sys.exit()

    snake.insert(0, new_head)

    # ---- FOOD COLLISION ----
    if new_head == food.position:
        score += food.weight

        if score >= next_level_score:
            level += 1
            speed += 2
            next_level_score += 4

        food = Food()
        food_alive_time = 0
    else:
        snake.pop()

    # ---- DRAW EVERYTHING ----
    screen.fill(BLACK)

    # Draw snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, food.color, (food.position[0], food.position[1], CELL, CELL))

    # Draw UI
    score_text = font.render(f"Score: {score}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))

    pygame.display.update()
    clock.tick(speed)
