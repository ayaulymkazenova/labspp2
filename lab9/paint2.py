import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint (fixed)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# Canvas — где всё сохраняется
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Палитра и настройки
palette = [
    (0, 0, 0), (255, 255, 255),
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (128, 0, 128)
]
palette_rects = [pygame.Rect(10 + i * 36, 10, 32, 32) for i in range(len(palette))]

current_color = (0, 0, 0)
brush_size = 6
tool = "brush"  # brush, eraser, rectangle, circle, square, right_triangle, equilateral_triangle, rhombus

drawing = False
start_pos = None
last_pos = None

# Вспомогательная функция: рисует непрерывную линию (brush/eraser) на заданной поверхности
def draw_line_between(surface, start, end, size, color):
    # Bresenham-like stepper using distance
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = max(int(math.hypot(dx, dy)), 1)
    for i in range(dist + 1):
        x = int(start[0] + dx * i / dist)
        y = int(start[1] + dy * i / dist)
        pygame.draw.circle(surface, color, (x, y), size)

# Фигуры (рисуют на surface)
def draw_rectangle(surface, a, b, color, width=2):
    rect = pygame.Rect(min(a[0], b[0]), min(a[1], b[1]), abs(a[0]-b[0]), abs(a[1]-b[1]))
    pygame.draw.rect(surface, color, rect, width)

def draw_circle(surface, a, b, color, width=2):
    radius = int(math.hypot(b[0]-a[0], b[1]-a[1]))
    pygame.draw.circle(surface, color, a, radius, width)

def draw_square(surface, a, b, color, width=2):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    side = min(abs(dx), abs(dy))
    sx = a[0] + (0 if dx >= 0 else -side)
    sy = a[1] + (0 if dy >= 0 else -side)
    rect = pygame.Rect(sx, sy, side, side)
    pygame.draw.rect(surface, color, rect, width)

def draw_right_triangle(surface, a, b, color, width=2):
    # points: a, (a.x, b.y), b
    p1 = a
    p2 = (a[0], b[1])
    p3 = b
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

def draw_equilateral_triangle(surface, a, b, color, width=2):
    # side length determined by horizontal distance (or distance)
    side = int(math.hypot(b[0]-a[0], b[1]-a[1]))
    if side == 0:
        return
    height = int((math.sqrt(3)/2) * side)
    # decide orientation from vertical position of b relative to a
    if b[1] <= a[1]:
        # point upwards
        p1 = a
        p2 = (a[0] + side, a[1])
        p3 = (a[0] + side//2, a[1] - height)
    else:
        # point downwards
        p1 = a
        p2 = (a[0] + side, a[1])
        p3 = (a[0] + side//2, a[1] + height)
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)

def draw_rhombus(surface, a, b, color, width=2):
    cx = (a[0] + b[0]) // 2
    cy = (a[1] + b[1]) // 2
    points = [
        (cx, a[1]),   # top
        (b[0], cy),   # right
        (cx, b[1]),   # bottom
        (a[0], cy)    # left
    ]
    pygame.draw.polygon(surface, color, points, width)

# Отображение текущего инструмента (текст)
def draw_ui():
    # фон панели
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 60))
    # палитра
    for i, col in enumerate(palette):
        pygame.draw.rect(screen, col, palette_rects[i])
        pygame.draw.rect(screen, (0,0,0), palette_rects[i], 1)
    # подсказки инструментов
    ui_text = f"Tool: {tool} | Brush size: {brush_size} | Color: {current_color}"
    txt = font.render(ui_text, True, (10, 10, 10))
    screen.blit(txt, (10, 48))
    help_txt = "1:brush 2:eraser 3:rect 4:circle 5:square 6:right tri 7:equilateral 8:rhombus  +/- size"
    h = font.render(help_txt, True, (10,10,10))
    screen.blit(h, (350, 40))

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # выбор цвета из палитры
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка
                # проверяем клик по палитре
                clicked_palette = False
                for i, rect in enumerate(palette_rects):
                    if rect.collidepoint(event.pos):
                        current_color = palette[i]
                        clicked_palette = True
                        break
                if clicked_palette:
                    continue

                drawing = True
                start_pos = event.pos
                last_pos = event.pos

                # если кисть или ластик — сразу нарисовать точку
                if tool == "brush":
                    draw_line_between(canvas, start_pos, start_pos, brush_size, current_color)
                elif tool == "eraser":
                    draw_line_between(canvas, start_pos, start_pos, brush_size+6, (255,255,255))

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                # При отпускании — если фигура, рисуем её на canvas
                if tool == "rectangle":
                    draw_rectangle(canvas, start_pos, end_pos, current_color, width=2)
                elif tool == "circle":
                    draw_circle(canvas, start_pos, end_pos, current_color, width=2)
                elif tool == "square":
                    draw_square(canvas, start_pos, end_pos, current_color, width=2)
                elif tool == "right_triangle":
                    draw_right_triangle(canvas, start_pos, end_pos, current_color, width=2)
                elif tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, start_pos, end_pos, current_color, width=2)
                elif tool == "rhombus":
                    draw_rhombus(canvas, start_pos, end_pos, current_color, width=2)
                # для кисти/ластика ничего — они уже на canvas
            drawing = False
            start_pos = None
            last_pos = None

        if event.type == pygame.MOUSEMOTION and drawing:
            pos = event.pos
            if tool == "brush":
                draw_line_between(canvas, last_pos, pos, brush_size, current_color)
                last_pos = pos
            elif tool == "eraser":
                draw_line_between(canvas, last_pos, pos, brush_size+6, (255,255,255))
                last_pos = pos
            else:
                # для фигур — мы не рисуем на canvas до отпускания, просто обновляем превью (handled later)
                pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: tool = "brush"
            elif event.key == pygame.K_2: tool = "eraser"
            elif event.key == pygame.K_3: tool = "rectangle"
            elif event.key == pygame.K_4: tool = "circle"
            elif event.key == pygame.K_5: tool = "square"
            elif event.key == pygame.K_6: tool = "right_triangle"
            elif event.key == pygame.K_7: tool = "equilateral_triangle"
            elif event.key == pygame.K_8: tool = "rhombus"
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(80, brush_size + 1)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_c:
                # очистить canvas
                canvas.fill((255,255,255))

    # Отрисовка: сначала canvas (постоянный), затем UI и preview
    screen.fill((200,200,200))
    screen.blit(canvas, (0,0))
    draw_ui()

    # preview при рисовании фигур (не для кисти/ластика)
    if drawing and start_pos and tool not in ("brush", "eraser"):
        preview = canvas.copy()
        cur = pygame.mouse.get_pos()
        if tool == "rectangle":
            draw_rectangle(preview, start_pos, cur, current_color, width=2)
        elif tool == "circle":
            draw_circle(preview, start_pos, cur, current_color, width=2)
        elif tool == "square":
            draw_square(preview, start_pos, cur, current_color, width=2)
        elif tool == "right_triangle":
            draw_right_triangle(preview, start_pos, cur, current_color, width=2)
        elif tool == "equilateral_triangle":
            draw_equilateral_triangle(preview, start_pos, cur, current_color, width=2)
        elif tool == "rhombus":
            draw_rhombus(preview, start_pos, cur, current_color, width=2)
        screen.blit(preview, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
