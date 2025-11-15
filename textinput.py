# demo.py
import pygame
from textclass import TextBox

pygame.init()

WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reusable TextBox Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Create the box
box_rect = pygame.Rect(50, 120, 400, 40)
textbox = TextBox(
    rect=box_rect,
    font=font,
    text_color=(0, 0, 0),
    bg_color=(255, 255, 255),
    active_color=(100, 150, 255),
    inactive_color=(180, 180, 180)
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        textbox.handle_event(event)

    textbox.update()

    screen.fill((240, 240, 240))
    textbox.draw(screen)

    # Optional: show instructions
    instr = font.render("Click box → type, Ctrl+C/V/Z, etc.", True, (80, 80, 80))
    screen.blit(instr, (50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()