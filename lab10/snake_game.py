import psycopg2
import pygame
import sys
import random


def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="snake_game",
        user="postgres",
        password="1234"
    )


def create_tables():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_user (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    current_level INT DEFAULT 1
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_score (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES game_user(id),
                    level INT NOT NULL,
                    score INT NOT NULL,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()


def get_or_create_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, current_level FROM game_user WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                print(f"Welcome back, {username}! Your current level: {user[1]}")
                return user[0], user[1]
            cur.execute("INSERT INTO game_user (username) VALUES (%s) RETURNING id", (username,))
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"New user created: {username}. Level = 1")
            return new_id, 1


def save_game_state(user_id, level, score):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s)",
                (user_id, level, score)
            )
            cur.execute(
                "UPDATE game_user SET current_level = %s WHERE id = %s",
                (level, user_id)
            )
        conn.commit()


pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with DB")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


LEVEL_SPEED = {1: 8, 2: 10, 3: 12, 4: 14, 5: 16}
LEVEL_WALLS = {
    1: [],
    2: [(200, 200, 200, 20)],
    3: [(100, 100, 400, 20), (100, 300, 400, 20)],
    4: [(50, 50, 500, 20), (50, 500, 500, 20)],
    5: [(50, 50, 500, 20), (50, 500, 500, 20), (250, 150, 100, 300)]
}

POINTS_PER_LEVEL = 5  

def game(level, user_id):
    snake = [(300, 300)]
    direction = (10, 0)
    score = 0
    paused = False
    walls = LEVEL_WALLS[level]
    font = pygame.font.SysFont(None, 36)

    
    def generate_food():
        while True:
            f = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
            if not any(wx <= f[0] <= wx+ww and wy <= f[1] <= wy+wh for wx, wy, ww, wh in walls):
                return f

    food = generate_food()

    while True:
        clock.tick(LEVEL_SPEED[level])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_state(user_id, level, score)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_game_state(user_id, level, score)
                        print(f"Game paused. Progress saved! Score: {score}")
                if not paused:
                    if event.key == pygame.K_UP and direction != (0, 10):
                        direction = (0, -10)
                    elif event.key == pygame.K_DOWN and direction != (0, -10):
                        direction = (0, 10)
                    elif event.key == pygame.K_LEFT and direction != (10, 0):
                        direction = (-10, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-10, 0):
                        direction = (10, 0)

        if paused:
            win.fill(WHITE)
            text = font.render("PAUSED - Press P to continue", True, RED)
            win.blit(text, (100, 280))
            pygame.display.update()
            continue

      
        x, y = snake[-1]
        new_head = (x + direction[0], y + direction[1])
        snake.append(new_head)

        
        if abs(new_head[0] - food[0]) < 10 and abs(new_head[1] - food[1]) < 10:
            score += 1
            food = generate_food()

            
            new_level = (score // POINTS_PER_LEVEL) + 1
            if new_level > level and new_level in LEVEL_SPEED:
                level = new_level
                walls = LEVEL_WALLS[level]
                print(f"Level up! Now level {level}")

        else:
            snake.pop(0)

        
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            print("Hit border! Saving...")
            save_game_state(user_id, level, score)
            pygame.quit()
            sys.exit()

       
        for wx, wy, ww, wh in walls:
            if wx <= new_head[0] <= wx + ww and wy <= new_head[1] <= wy + wh:
                print("Hit wall! Saving...")
                save_game_state(user_id, level, score)
                pygame.quit()
                sys.exit()

       
        win.fill(WHITE)
        for s in snake:
            pygame.draw.rect(win, GREEN, (*s, 10, 10))
        pygame.draw.rect(win, RED, (*food, 10, 10))
        for wx, wy, ww, wh in walls:
            pygame.draw.rect(win, BLACK, (wx, wy, ww, wh))

        
        score_text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
        win.blit(score_text, (10, 10))

        pygame.display.update()

if __name__ == "__main__":
    create_tables()
    username = input("Enter username: ")
    user_id, level = get_or_create_user(username)
    print(f"Starting Snake at level {level}!")
    game(level, user_id)
