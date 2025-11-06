import pygame

pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drawing App")
clock = pygame.time.Clock()

# Начальные параметры
radius = 10
color = (0, 0, 255)  # Синий по умолчанию
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
                if mode == 'rect' and start_pos:
                    rect = pygame.Rect(min(start_pos[0], event.pos[0]),
                                       min(start_pos[1], event.pos[1]),
                                       abs(start_pos[0] - event.pos[0]),
                                       abs(start_pos[1] - event.pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)
                elif mode == 'circle' and start_pos:
                    dx = start_pos[0] - event.pos[0]
                    dy = start_pos[1] - event.pos[1]
                    radius_c = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius_c, 2)
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

    # Отображение текущего режима
    pygame.display.set_caption(f"Mode: {mode} | Color: {color} | Radius: {radius}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
