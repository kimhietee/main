import pygame
import heroes as main
import gameloop


def controls():
    command_img = main.pygame.transform.scale(
        pygame.image.load(r'assets\command image.png').convert(), (main.width/2, main.height))
    control_img = main.pygame.transform.scale(
        pygame.image.load(r'assets\control image.png').convert(), (main.width/2, main.height))
    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                gameloop.menu()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameloop.menu_button.is_clicked(event.pos):
                    gameloop.menu() 
                    return
                
        
        main.screen.blit(command_img, (0, 0))
        main.screen.blit(control_img, (main.width/2, 0))
        gameloop.menu_button.draw(main.screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)