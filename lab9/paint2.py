import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing App")
clock = pygame.time.Clock()

radius = 10
color = (0, 0, 255)
mode = 'brush'
drawing = False
start_pos = None

def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(screen, color, (x, y), width)

def draw_equilateral_triangle(screen, start, end, color):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    h = (math.sqrt(3) / 2) * length
    x3 = (x1 + x2) / 2 + px * h
    y3 = (y1 + y2) / 2 + py * h
    pygame.draw.polygon(screen, color, [(x1, y1), (x2, y2), (x3, y3)], 2)

running = True
last_pos = None

while running:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                color = (255, 0, 0)
            elif event.key == pygame.K_g:
                color = (0, 255, 0)
            elif event.key == pygame.K_b:
                color = (0, 0, 255)
            elif event.key == pygame.K_1:
                mode = 'rect'
            elif event.key == pygame.K_2:
                mode = 'circle'
            elif event.key == pygame.K_3:
                mode = 'eraser'
            elif event.key == pygame.K_4:
                mode = 'square'
            elif event.key == pygame.K_5:
                mode = 'right_triangle'
            elif event.key == pygame.K_6:
                mode = 'equilateral'
            elif event.key == pygame.K_7:
                mode = 'rhombus'
            elif event.key == pygame.K_0:
                mode = 'brush'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
            elif event.button == 3:
                radius = max(1, radius - 1)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                end_pos = event.pos
                if mode == 'rect' and start_pos:
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(start_pos[0] - end_pos[0]),
                        abs(start_pos[1] - end_pos[1])
                    )
                    pygame.draw.rect(screen, color, rect, 2)

                elif mode == 'square' and start_pos:
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    size = min(abs(dx), abs(dy))
                    size_x = size if dx >= 0 else -size
                    size_y = size if dy >= 0 else -size
                    rect = pygame.Rect(
                        start_pos[0],
                        start_pos[1],
                        size_x,
                        size_y
                    )
                    pygame.draw.rect(screen, color, rect, 2)

                elif mode == 'circle' and start_pos:
                    dx = start_pos[0] - end_pos[0]
                    dy = start_pos[1] - end_pos[1]
                    radius_c = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius_c, 2)

                elif mode == 'right_triangle' and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    points = [(x1, y1), (x2, y1), (x1, y2)]
                    pygame.draw.polygon(screen, color, points, 2)

                elif mode == 'equilateral' and start_pos:
                    draw_equilateral_triangle(screen, start_pos, end_pos, color)

                elif mode == 'rhombus' and start_pos:
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [
                        (cx - dx, cy),
                        (cx, cy - dy),
                        (cx + dx, cy),
                        (cx, cy + dy)
                    ]
                    pygame.draw.polygon(screen, color, points, 2)

                drawing = False
                start_pos = None
                last_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == 'brush':
                if last_pos:
                    drawLineBetween(screen, last_pos, event.pos, radius, color)
                last_pos = event.pos
            elif mode == 'eraser':
                pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)

    pygame.display.set_caption(f"Mode: {mode} | Color: {color} | Radius: {radius}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
