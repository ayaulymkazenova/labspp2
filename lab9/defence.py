#Create a game where rectangles fall from the top of the screen at random x-positions
import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Triangles")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(200, 500))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Triangle(pygame.sprite.Sprite):
    def __init__(self, base_speed=4):
        super().__init__()
        self.weight = random.choice([1, 2, 3])
        side = 30
        height = int((3**0.5 / 2) * side)
        self.image = pygame.Surface((side, height), pygame.SRCALPHA)
        points = [
            (side // 2, 0),
            (0, height),
            (side, height)
        ]
        pygame.draw.polygon(self.image, YELLOW, points)
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH-30), -30))
        self.speed = base_speed + random.uniform(0, 1)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


player = Player()
player_group = pygame.sprite.Group(player)
triangle_group = pygame.sprite.Group()

triangles_collected = 0
base_speed = 4
next_speed_increase = 10

TRIANGLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TRIANGLE_EVENT, 1500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TRIANGLE_EVENT:
            new_triangle = Triangle(base_speed)
            triangle_group.add(new_triangle)

    screen.fill(GRAY)

    player_group.update()
    triangle_group.update()

    collided_triangles = pygame.sprite.spritecollide(player, triangle_group, True)
    for triangle in collided_triangles:
        triangles_collected += triangle.weight

    if triangles_collected >= next_speed_increase:
        base_speed += 0.5
        next_speed_increase += 10

    player_group.draw(screen)
    triangle_group.draw(screen)

    triangle_text = font.render(f"Score: {triangles_collected}", True, WHITE)
    screen.blit(triangle_text, (280, 10))

    speed_text = font.render(f"Speed: {base_speed:.1f}", True, WHITE)
    screen.blit(speed_text, (20, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()