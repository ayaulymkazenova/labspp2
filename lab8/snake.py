import pygame, sys, random

# Initialize pygame
pygame.init()

# Game window
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# 🎨 Colors
DARK_BLUE = (10, 10, 40)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)
LIGHT_YELLOW = (255, 255, 200)
DARK_RED = (100, 0, 0)
WHITE = (255, 255, 255)

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Snake and food setup
snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = "RIGHT"

food_pos = (random.randrange(1, (WIDTH // CELL_SIZE)) * CELL_SIZE,
            random.randrange(1, (HEIGHT // CELL_SIZE)) * CELL_SIZE)
food_spawn = True

score = 0
level = 1
speed = 10  # base speed

def show_text():
    score_text = font.render(f"Score: {score}", True, LIGHT_YELLOW)
    level_text = font.render(f"Level: {level}", True, LIGHT_YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

def game_over():
    screen.fill(DARK_RED)
    over_text = font.render("Game Over! Press any key to exit.", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 10))
    pygame.display.flip()
    pygame.time.wait(1500)
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()

def random_food_position():
    """Generate random food position that doesn’t overlap with the snake."""
    while True:
        x = random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != "DOWN":
                snake_dir = "UP"
            elif event.key == pygame.K_DOWN and snake_dir != "UP":
                snake_dir = "DOWN"
            elif event.key == pygame.K_LEFT and snake_dir != "RIGHT":
                snake_dir = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_dir != "LEFT":
                snake_dir = "RIGHT"

    # Move snake
    head_x, head_y = snake[0]
    if snake_dir == "UP":
        head_y -= CELL_SIZE
    elif snake_dir == "DOWN":
        head_y += CELL_SIZE
    elif snake_dir == "LEFT":
        head_x -= CELL_SIZE
    elif snake_dir == "RIGHT":
        head_x += CELL_SIZE

    new_head = (head_x, head_y)

    # 🧱 Check for wall (border) collision
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    # 🐍 Check self-collision
    if new_head in snake:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # 🍎 Check if snake eats food
    if new_head == food_pos:
        score += 1
        food_spawn = False

        # Level up every 4 points
        if score % 4 == 0:
            level += 1
            speed += 2  # increase speed
    else:
        snake.pop()

    # 🍏 Spawn new food
    if not food_spawn:
        food_pos = random_food_position()
        food_spawn = True

    # Draw everything
    screen.fill(DARK_BLUE)
    for pos in snake:
        pygame.draw.rect(screen, CYAN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GOLD, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    # HUD
    show_text()

    pygame.display.update()
    clock.tick(speed)
