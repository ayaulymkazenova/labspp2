import pygame, sys, random

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

DARK_BLUE = (10, 10, 40)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 50, 50)
PURPLE = (180, 50, 230)
LIGHT_YELLOW = (255, 255, 200)
DARK_RED = (100, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

snake = [(100, 100), (80, 100), (60, 100)]
snake_dir = "RIGHT"

foods = []
FOOD_LIFETIME = 5000
FOOD_SPAWN_DELAY = 2000

score = 0
level = 1
speed = 10

FOOD_COLORS = {
    1: GOLD,
    2: RED,
    3: PURPLE
}

def show_text():
    score_text = font.render(f"Score: {score}", True, LIGHT_YELLOW)
    level_text = font.render(f"Level: {level}", True, LIGHT_YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

def game_over():
    screen.fill(DARK_RED)
    over_text = font.render("Game Over!", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 10))
    pygame.display.flip()
    pygame.time.wait(1500)
    pygame.quit()
    sys.exit()

def random_food_position():
    while True:
        x = random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake and not any(f['pos'] == (x, y) for f in foods):
            return (x, y)

def spawn_food():
    weight = random.choices([1, 2, 3], weights=[70, 20, 10], k=1)[0]
    pos = random_food_position()
    spawn_time = pygame.time.get_ticks()
    foods.append({'pos': pos, 'weight': weight, 'spawn_time': spawn_time})

spawn_food()
last_food_spawn = pygame.time.get_ticks()

while True:
    current_time = pygame.time.get_ticks()

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

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        game_over()

    if new_head in snake:
        game_over()

    snake.insert(0, new_head)

    food_eaten = False
    for food in foods[:]:
        if new_head == food['pos']:
            score += food['weight']
            foods.remove(food)
            food_eaten = True
            if score // 4 + 1 > level:
                level = score // 4 + 1
                speed = 10 + (level - 1) * 2

    if not food_eaten:
        snake.pop()

    for food in foods[:]:
        if current_time - food['spawn_time'] > FOOD_LIFETIME:
            foods.remove(food)

    if not foods and current_time - last_food_spawn > FOOD_SPAWN_DELAY:
        spawn_food()
        last_food_spawn = current_time

    screen.fill(DARK_BLUE)

    for pos in snake:
        pygame.draw.rect(screen, CYAN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    for food in foods:
        color = FOOD_COLORS.get(food['weight'], GOLD)
        pygame.draw.rect(screen, color, pygame.Rect(food['pos'][0], food['pos'][1], CELL_SIZE, CELL_SIZE))

    show_text()
    pygame.display.update()
    clock.tick(speed)
