import pygame
import random
from global_vars import (
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img, SPECIAL_DURATION, DISABLE_SPECIAL_REDUCE,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size, MAIN_VOLUME, SHOW_GRID,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LOW_HP, LITERAL_HEALTH_DEAD,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    attack_display, MULT, dmg_mult
)
from global_vars import SHOW_HITBOX


from button import ImageButton, ImageInfo
import heroes as main



from Animate_BG import BackgroundHandler, bg_paths

import Animate_BG

animated_bg = BackgroundHandler(bg_paths)




# from heroes import player_selection, p1_select, p2_select, hero1_group, hero2_group
# from heroes import Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin
# from player_selector import PlayerSelector
# # from global_vars import (
#     width, height, icon, FPS, clock, screen, hero1, hero2,
#     white, red, black, green, cyan2, gold,
#     DEFAULT_WIDTH, DEFAULT_HEIGHT,
#     DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
#     LOW_HP, LITERAL_HEALTH_DEAD,
#     DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
#     JUMP_DELAY, RUNNING_SPEED,
#     X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
#     ICON_WIDTH, ICON_HEIGHT,
#     DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
#     WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
#     PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
#     attack_display, MULT, dmg_mult
# )



# from heroes import Fire_Wizard, Wanderer_Magicianoo

# The hero selection logic need to be at the main file :))d


# # Declaration of the eobject sprites (Single instance)
# fire_wizard = main.Fire_Wizard(PLAYER_2)
# wanderer_magician = main.Wanderer_Magician(PLAYER_1)

# # Group of objects sprites (Multiple instances)
# fire_wizard_group = main.pygame.sprite.Group()
# fire_wizard_group.add(fire_wizard)

# wanderer_magician_group = main.pygame.sprite.Group()
# wanderer_magician_group.add(wanderer_magician)
    
#basic attack
#ultimate regen
#increase mana every attack
#hook       

pygame.font.init()

MENU_MUSIC = r'assets\audios\price-of-freedom-33106.mp3'
GAME_MUSIC_1 = r'assets\audios\intense-battle-scene-115478.mp3'
GAME_MUSIC_2 = r'assets\audios\z-battle-227609.mp3'

MENU_FADE_DURATION = 1000  # in milliseconds
GAME_FADE_IN = 1500




def fade(background, action):
    # background = pygame.transform.scale(
    #     pygame.image.load(r'assets\backgrounds\12.png').convert(), (width, height))

    fade_overlay = pygame.Surface((width, height))
    fade_overlay.fill((0, 0, 0))
    fade_alpha = 0
    fading = True
    fade_start_time = pygame.time.get_ticks()

    while True:
        for event in main.pygame.event.get():
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()

        if fading:
            screen.blit(background, (0, 0))
            loading.draw(screen, pygame.mouse.get_pos())
            current_time = pygame.time.get_ticks()
            # pygame.time.get_ticks()
            fade_elapsed = current_time - fade_start_time
            fade_alpha = min(255, int((fade_elapsed / MENU_FADE_DURATION) * 255))
            fade_overlay.set_alpha(fade_alpha)
            screen.blit(fade_overlay, (0, 0))
            if fade_alpha >= 255:
                fading = False
                action()
                return
            
        pygame.display.update()
        main.clock.tick(main.FPS)

# def counter(itemlist): # this one is a dud
#     count = 0
#     for item in itemlist:
#         if item.is_selected():
#             count += 1
#     # print(count)
#     return count

def item_list(itemlist): # at least it works, not reusable tho
    value_list = []
    for i, item in enumerate(itemlist):
        if item.is_selected():
            value_list.append(item)
    return value_list


def draw_grid(screen, width=1280, height=720, grid_size=35, color=(100, 100, 100)):
    cell_width = width // grid_size
    cell_height = height // grid_size

    font = pygame.font.Font(None, 20)

    for i in range(grid_size + 1):
        # Vertical lines
        x = i * cell_width
        # pygame.draw.line(screen, color, (x, 0), (x, height), 1)

        # Horizontal lines
        y = i * cell_height
        pygame.draw.line(screen, color, (0, y), (width, y), 1)

    for row in range(grid_size):
        for col in range(grid_size):
            x = (col + 1) * cell_width
            y = row * cell_height

            # Reverse Y: higher numbers at the top
            reversed_y = height - y
            # pos_text = f"{x}, {reversed_y}"
            pos_text = f"{reversed_y}"

            text_surface = font.render(pos_text, True, (150, 150, 255))
            screen.blit(text_surface, (x - 5, y + 2))



        
        

def game(bg=None):
    game_music_started = False
    second_track_played = False
    print('stopping music')
    # bg_list = [
    #     r'assets\backgrounds\1.png',
    #     r'assets\backgrounds\2.png',
    #     r'assets\backgrounds\3.png',
    #     r'assets\backgrounds\4.jpg',
    #     r'assets\backgrounds\13.jpg',
    #     r'assets\backgrounds\14.png',
    #     r'assets\backgrounds\15.png',
    #     r'assets\backgrounds\16.png',
    #     r'assets\backgrounds\17.png'
    # ]
    # print(f'hahahahaa [{random.randint(0, len(bg_list)-1)}')
    # background = main.pygame.transform.scale(
    #     pygame.image.load(bg_list[random.randint(0, len(bg_list)-1)]).convert(), (main.width, main.DEFAULT_Y_POS + (720*1.1 - 720)))
    # ground = main.pygame.transform.scale(
    #     main.pygame.image.load(r'assets\backgrounds\10.jpg').convert(), (main.width, main.height))
    ground = pygame.Rect(0, main.DEFAULT_Y_POS, 2121, 1111)
    
    start_time = pygame.time.get_ticks()
    timer_font = pygame.font.Font(r'assets\font\slkscr.ttf', 50)  # Timer font

    cube_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
    cube_sound.set_volume(0.8 * MAIN_VOLUME) 

    cubes = [
        {'fall': -500, 'x': random.randint(20, int(main.width - 20)), 'color': 'Green', 'image': pygame.image.load(r'assets\icons\hp bonus.png').convert_alpha(), 'bonus_type': 'health', 'bonus_amount': 10, 'sound': cube_sound},
        {'fall': -300, 'x': random.randint(20, int(main.width - 20)), 'color': 'Blue', 'image': pygame.image.load(r'assets\icons\mana bonus.png').convert_alpha(), 'bonus_type': 'mana', 'bonus_amount': 30, 'sound': cube_sound},
        {'fall': -700, 'x': random.randint(20, int(main.width - 20)), 'color': 'Yellow', 'image': pygame.image.load(r'assets\icons\special bonus.png').convert_alpha(), 'bonus_type': 'special', 'bonus_amount': 15, 'sound': cube_sound},
    ]
    
    
    if game_music_started and not second_track_played:
        if not pygame.mixer.music.get_busy():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))
            
    FREEZE_SPECIAL = False
    freeze_toggled = True
    while True:
        
        
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Convert to seconds

        main.screen.fill((100, 100, 100))


        for event in main.pygame.event.get():
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()

            if random.randint(1, 2) == 1:
                if event.type == pygame.USEREVENT + 1 and not game_music_started:
                    pygame.mixer.music.load(GAME_MUSIC_1)
                    pygame.mixer.music.set_volume(0.5 * MAIN_VOLUME)
                    pygame.mixer.music.play(-1, fade_ms=1500)
                    game_music_started = True
                    print("Started game music 1")
            elif random.randint(1, 2) == 2:
                if event.type == pygame.USEREVENT and game_music_started and not second_track_played:
                    # Game music 1 finidddddddddddddshed — play second
                    pygame.mixer.music.load(GAME_MUSIC_2)
                    pygame.mixer.music.set_volume(0.5 * MAIN_VOLUME)
                    pygame.mixer.music.play(loops=-1, fade_ms=1500)  # Loop the second game track if you want
                    second_track_played = True
                    print("Started game music 2")

            if keys[pygame.K_ESCAPE]:
                menu()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    menu()
                    return    
                
            

            if keys[main.pygame.K_6]:
                print('ehj') 
                main.hero1.health += 20
                main.hero2.health += 20 
                main.hero1.mana += 20
                main.hero2.mana += 20
                if hasattr(main.bot, 'mana'):
                    main.bot.mana += 20
                if hasattr(main.bot, 'health'):
                    main.bot.health += 20

            # if keys[main.pygame.K_SPACE]: # reset
            #     main.hero1.health += 500
            #     main.hero2.health += 500
            #     main.hero1.mana += 500
            #     main.hero2.mana += 500
            #     main.hero1.special -= 500
            #     main.hero2.special -= 500

            if keys[main.pygame.K_1] and not keys[main.pygame.K_LALT]: # reset
                main.hero1.special += 500
                main.hero2.special += 500

            # if keys[main.pygame.K_2] and not keys[main.pygame.K_LALT] and not FREEZE_SPECIAL: # freeze
            #     FREEZE_SPECIAL = True
            #     # freeze_toggled = False
            #     if event.type == pygame.USEREVENT:
            #         print('freeze special toggled')
                

            # if keys[main.pygame.K_2] and keys[main.pygame.K_LALT]: # unfreeze (alt)
            #     FREEZE_SPECIAL = False
            #     # freeze_toggled = True
            #     if event.type == pygame.USEREVENT:
            #         print('unfreeze special toggled')

            if keys[main.pygame.K_3] and not keys[main.pygame.K_LALT]: # special to 1
                main.hero1.special = 0.01
                main.hero2.special = 0.01
                

            if keys[main.pygame.K_4] and not keys[main.pygame.K_LALT]: # disable special
                main.DISABLE_SPECIAL_REDUCE = False
            elif keys[main.pygame.K_4] and keys[main.pygame.K_LALT]: # special on (alt)
                main.DISABLE_SPECIAL_REDUCE = True

            if keys[main.pygame.K_2] and not keys[main.pygame.K_LALT]:
                main.DISABLE_SPECIAL_REDUCE = True
                main.hero1.special = 0.01
                main.hero2.special = 0.01

            if keys[main.pygame.K_5] and not keys[main.pygame.K_LALT]: # disable hp regen
                main.DISABLE_HEAL_REGEN = True
            if keys[main.pygame.K_5] and keys[main.pygame.K_LALT]: # hp regen (alt)
                main.DISABLE_HEAL_REGEN = False
            '''add another flag which also disables random unstuck direction, but in this case, it is the core flag, which is specific for the hero, not just on a skill, eg fire wizard escapes random direction, while also other hero escapes depends on where the player is. (this is for the skill, if the hero has escape, and that skill has specific flag(assuming that skill forcefully move the bot, or an escape skill, then it also behaves the same)'''

            # if FREEZE_SPECIAL: 
            #     main.hero1.special_active = True
            #     main.hero2.special_active = True
            #     main.hero1.special += 0.001
            #     main.hero2.special += 0.001
            # elsed:
            #     pass

        # print(FREEZE_SPECIAL)
                
# -------------------------------------------------------------------------------------

        # Background
        # Animate_BG.waterfall_bg.display(screen)
        # Animate_BG.lava_bg.display(screen)
        Animate_BG.dark_forest_bg.display(screen)

        # main.screen.blit(background, (0, -(720*1.05 - 720)))

        draw_grid(screen) if SHOW_GRID else None

        # draws animated cloud background (lag)
        # animated_bg.update()
        # animated_bg.draw(screen)
        
        # main.screen.blit(ground, (0,main.DEFAULT_Y_POS))

        # Ground
        pygame.draw.rect(main.screen, main.black, ground)


        for icons in main.p1_select:
            if icons.is_selected():
                icons.draw_icon(size=(75, 75))
        
        for icons in main.p2_select:
            if icons.is_selected():
                icons.draw_icon(size=(main.width - 75, 75))

        for i, item in enumerate(item_list(main.p1_items)):
            item.draw_icon(item_pos=(150+(50*i), 100), hero_icon=False)
        for i, item in enumerate(item_list(main.p2_items)):
            item.draw_icon(item_pos=(main.width-(150+(50*i)), 100), hero_icon=False)
    
        for cube in cubes:
            cube['fall'], cube['x'] = handle_cube(
                pygame.Rect(cube['x'], cube['fall'], 25, 25),
                cube['fall'],
                cube['x'],
                cube['color'],
                cube['image'],
                main.hero1,
                main.hero2,
                cube['bonus_type'],
                cube['bonus_amount'],
                cube['sound']
            )

        timer_text = timer_font.render(f"[{elapsed_time}]", True, main.white)
        main.screen.blit(timer_text, (main.width / 2.3, 30))  # Display timer at the top-left corner
        
        menu_button.draw(main.screen, mouse_pos)
        
        #drawing the hp and mana icon
        main.draw_hp_mana_icons()

        #drawing the damage display

        # Update anddddddddddddd draw attacks
        attack_display.update()
        attack_display.draw(main.screen)

        # Update and draw Fire Wizard
        main.hero1_group.update()
        main.hero1_group.draw(main.screen)

        # Update and draw Wanderer Magician
        # if not main.hero2.is_dead():
        main.hero2_group.update()
        main.hero2_group.draw(main.screen)
        if main.SINGLE_MODE_ACTIVE:
            main.hero2.bot_logic()

        


        #draw distance
        # main.hero2.draw_distance(main.hero1_group)
        # hero1.draw_hitbox(screen)
                
        main.pygame.display.update()
        main.clock.tick(main.FPS)
            
def handle_cube(cube, cube_fall, cube_x, cube_color, cube_image, hero1, hero2, bonus_type, bonus_amount, sound):
    """
    Handles the logic for a single cube.

    Args:
        cube: The `pygame.Rect` object representing the cube.
        cube_fall: The current y-position of the cube.
        cube_x: The current x-position of the cube.
        cube_color: The color of the cube (for debugging purposes).
        cube_image: The image to render for the cube.
        hero1: The first hero object.
        hero2: The second hero object.
        bonus_type: The type of bonus ('health', 'mana', 'special').
        bonus_amount: The amount of the bonus to apply.

    Returns:
        Updated cube_fall and cube_x values.
    """
    if cube_fall < main.DEFAULT_Y_POS - 20:
        cube_fall += 1
        cube = pygame.Rect(cube_x, cube_fall, 25, 25)
        cube_hitbox = pygame.rect.Rect(cube.x, cube.y, cube.width * (cube.width * .07), cube.height * (cube.height * .07))

        # Scale the im        git pull origin masterage to match the cube's size
        scaled_image = pygame.transform.scale(cube_image, (cube.width * (cube.width * .07), cube.height * (cube.height * .07)))
        main.screen.blit(scaled_image, cube)
        if SHOW_HITBOX:
            pygame.draw.rect(main.screen, 'Red', cube_hitbox, 1)


        # Collision detection
        if cube_hitbox.colliderect(hero1.hitbox_rect):
            sound.play()
            if bonus_type == 'health':
                hero1.health += bonus_amount
            elif bonus_type == 'mana':
                hero1.mana += bonus_amount
            elif bonus_type == 'special':
                hero1.special += bonus_amount
            cube_x = random.randint(20, int(main.width - 20))
            cube_fall = random.randint(-2000, -500)
            print(f"Cube collected by Player 1: {bonus_type} +{bonus_amount}")
        elif cube_hitbox.colliderect(hero2.hitbox_rect):
            sound.play()
            if bonus_type == 'health':
                hero2.health += bonus_amount
            elif bonus_type == 'mana':
                hero2.mana += bonus_amount
            elif bonus_type == 'special':
                hero2.special += bonus_amount
            cube_x = random.randint(20, int(main.width - 20))
            cube_fall = cube_fall = random.randint(-2000, -500)
            print(f"Cube collected by Player 2: {bonus_type} +{bonus_amount}")
    else:
        cube_x = random.randint(20, int(main.width - 20))
        cube_fall = -150

    return cube_fall, cube_x

def menu():
    pygame.mixer.music.fadeout(1000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(MENU_MUSIC)
    pygame.mixer.music.set_volume(0.8 * MAIN_VOLUME)

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1, fade_ms=1500)  # Loop indefinitely
    print('playing music')

    background = main.pygame.transform.scale(
        pygame.image.load(r'assets\backgrounds\9.png').convert(), (main.width, main.height))

    font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((100, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   


            
                pass
                # main.player_selection()
                # return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.is_clicked(event.pos):
                    main.SINGLE_MODE_ACTIVE = True
                    main.player_selection()
                    return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if multiplayer_button.is_clicked(event.pos):
                    main.SINGLE_MODE_ACTIVE = False
                    main.player_selection()
                    return
             
            if event.type == pygame.MOUSEBUTTONDOWN:
                if info_button.is_clicked(event.pos):
                    info()
                    return
                    # return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if control_button.is_clicked(event.pos):
                    controls()
                    return
                    # return
                
            if keys[pygame.K_SPACE]:
                main.player_selection()
                return
            
            if keys[pygame.K_r]:
                main.player_selection()
                return
            
            if keys[pygame.K_e]:
                controls()
                return
        main.screen.blit(background, (0, 0))
        create_title('Maine Menu', font, default_size, main.height * 0.2)
        single_button.draw(main.screen, mouse_pos)
        multiplayer_button.draw(main.screen, mouse_pos)

        info_button.draw(main.screen,mouse_pos)
        control_button.draw(main.screen,mouse_pos)

        settings_button.draw(main.screen,mouse_pos)




        if campaign_button.is_hovered(mouse_pos):
            coming_soon_button.draw(main.screen, mouse_pos)
        else:
            campaign_button.draw(main.screen, mouse_pos)

 
        pygame.display.update()
        main.clock.tick(main.FPS)

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

        main.screen.fill((100, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                menu()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    menu() 
                    return
                
        
        main.screen.blit(command_img, (0, 0))
        main.screen.blit(control_img, (main.width/2, 0))
        menu_button.draw(screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)

def info():
    hero_detail = main.pygame.transform.scale(
        pygame.image.load(r'assets\hero info detail.png').convert(), (main.width, main.height))
    hero_info = main.pygame.transform.scale(
        pygame.image.load(r'assets\hero info dmg.png').convert(), (main.width, main.height))

    next = ImageButton(
    image_path=text_box_img,
    pos=(main.width-80, 20),
    scale=0.75,
    text='Next',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.02),  # dynamic size ~29 at 720p
    text_color='white'
)
    previous = ImageButton(
    image_path=text_box_img,
    pos=(main.width-80, 60),
    scale=0.75,
    text='previous',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.02),  # dynamic size ~29 at 720p
    text_color='white'
)
    
    inffo = ImageButton(
    image_path=text_box_img,
    pos=(main.width-150, main.height/1.5),
    scale=0.75,
    text='burn damage = 5 for fire knight',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.015),  # dynamic size ~29 at 720p
    text_color='white'
)
    
    switch = False
    
    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((100, 100, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                menu()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    menu() 
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next.is_clicked(event.pos) and not switch:
                    switch = True
                    
                if previous.is_clicked(event.pos) and switch:
                    switch = False
                    
                
        if switch:
            main.screen.blit(hero_detail, (0, 0))
        else:
            main.screen.blit(hero_info, (0, 0))

        menu_button.draw(screen, mouse_pos)
        next.draw(screen, mouse_pos)
        previous.draw(screen, mouse_pos)
        inffo.draw(screen, mouse_pos) if switch else None

        pygame.display.update()
        main.clock.tick(main.FPS)


def main_menu():
    

    # background = main.pygame.transform.scale(
        # pygame.image.load(r'assets\backgrounds\8.png').convert(), (main.width, main.height))

    font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    # fade(background, menu)
                    menu()
                    return
            if keys[pygame.K_RETURN]:
                menu()
                return

        # main.screen.blit(background, (0, 0))
        Animate_BG.dragon_bg.display(screen, speed=50)
        create_title('Fighting Kimhie', font, default_size, main.height * 0.2, color='Grey3')
        play_button.draw(main.screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)

def reset_all():
    global fade_alpha, fading, fade_start_time
    for attack in main.hero1.attacks:
        attack.reduce_cd(True)
    for attack in main.hero2.attacks:
        attack.reduce_cd(True)

    main.hero1.health += main.hero1.max_health
    main.hero2.health += main.hero2.max_health
    main.hero1.mana += main.hero1.max_mana
    main.hero2.mana += main.hero2.max_mana

    # fade_overlay = pygame.Surface((width, height))
    # fade_overlay.fill((0, 0, 0))
    # fade_alpha = 0
    # fading = True
    # fade_start_time = pygame.time.get_ticks()

    attack_display.empty()












# Image Paths

# fade()
loading = ImageButton(
    image_path=loading_button_img,
    pos=center_pos,
    scale=0.8,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white'
)

# Menu button to return to menu()
menu_button = ImageButton(
    image_path=menu_button_img,
    pos=(40, 10),
    scale=0.75,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white'
)

# main_menu()
play_button = ImageButton(
    image_path=play_button_img,
    pos=center_pos,
    scale=scale,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white'
)

# menu()
campaign_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]-100),
    scale=scale,
    text='Campaign',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    hover_move=0
)
#_____ for campaign
coming_soon_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]-100),
    scale=scale*0.95,
    text='Coming Soon',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    hover_move=0,
    alpha=(0.75, 1)
)


single_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]-50),
    scale=scale,
    text='Single Player',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white'
)

multiplayer_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]),
    scale=scale,
    text='Multiplayer',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white'
)

info_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 100, height - 100),
    scale=scale*0.8,
    text='Game Info',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white'
)

control_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 100, height - 50),
    scale=scale*0.8,
    text='Controls',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white'
)

settings_button = ImageButton(
    image_path=text_box_img,
    pos=(100, height - 50),
    scale=scale*0.8,
    text='Settings',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white'
)







def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0):
    title = pygame.transform.rotozoom(font.render(f'{text}', False, color), angle, scale)
    title_rect = title.get_rect(center = (width / 2, y_offset))
    screen.blit(title, title_rect)








if __name__ == '__main__':
    main_menu()
        