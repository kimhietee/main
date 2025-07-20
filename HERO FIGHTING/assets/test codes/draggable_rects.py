import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 255, 128)

# Create two rectangles
free_rect = pygame.Rect(100, 100, 100, 100)
xonly_rect = pygame.Rect(300, 300, 100, 100)

# Dragging state
dragging_free = False
dragging_xonly = False
offset_x, offset_y = 0, 0

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if free_rect.collidepoint(event.pos):
                dragging_free = True
                mouse_x, mouse_y = event.pos
                offset_x = free_rect.x - mouse_x
                offset_y = free_rect.y - mouse_y

            elif xonly_rect.collidepoint(event.pos):
                dragging_xonly = True
                mouse_x = event.pos[0]
                offset_x = xonly_rect.x - mouse_x

        # Mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_free = False
            dragging_xonly = False

        # Mouse motion
        elif event.type == pygame.MOUSEMOTION:
            if dragging_free:
                mouse_x, mouse_y = event.pos
                free_rect.x = mouse_x + offset_x
                free_rect.y = mouse_y + offset_y
            elif dragging_xonly:
                mouse_x = event.pos[0]
                xonly_rect.x = mouse_x + offset_x

    # Draw rectangles
    pygame.draw.rect(screen, BLUE, free_rect)
    pygame.draw.rect(screen, GREEN, xonly_rect)

    pygame.display.flip()
    clock.tick(60)

# pygame.quit()