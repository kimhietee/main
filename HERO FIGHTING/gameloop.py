import pygame

import random
from global_vars import (IMMEDIATE_RUN,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img, SPECIAL_DURATION, DISABLE_SPECIAL_REDUCE,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LOW_HP, LITERAL_HEALTH_DEAD,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    attack_display, MULT, dmg_mult, loading_screen_bg
)
from global_vars import SHOW_HITBOX

import global_vars


from button import ImageButton, ImageInfo
import heroes as main



# from Animate_BG import BackgroundHandler

import Animate_BG

import key






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

winner = 'hero2'
paused = False

# Add a global variable to track the pause state
is_paused = False
xaxa = pygame.time.Clock()

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

            text_surface = font.render(pos_text, global_vars.TEXT_ANTI_ALIASING, (150, 150, 255))
            screen.blit(text_surface, (x - 5, y + 2))


        
# def map_selection():

#     font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
#     default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

#     while True:
#         keys = pygame.key.get_pressed()
#         mouse_pos = pygame.mouse.get_pos()
#         mouse_press = pygame.mouse.get_pressed()
#         key_press = pygame.key.get_pressed()

#         main.screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()   

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_button.is_clicked(event.pos):
#                     # fade(background, menu)
#                     menu()
#                     return
#             if keys[pygame.K_RETURN]:
#                 menu()
#                 return

        # main.screen.blit(background, (0, 0))
        # Animate_BG.waterfall_night_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
        # create_title('Map Selection', font, default_size, height * 0.1)
        # menu_button.draw(screen, mouse_pos)

        # pygame.display.update()
        # xaxa.tick(main.FPS)
def run_background(bg):
    bg.display(screen)
import time
def game(bg=None):
    global winner, paused, is_paused
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
    cube_sound.set_volume(0.8 * global_vars.MAIN_VOLUME) 

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

    final_elapsed_time = None
    paused_start_time = None
    total_paused_duration = 0

    #testing purposes
    #testing
    main.hero1.x_pos += 250
    main.hero2.x_pos -= 150

    

    # Import keybinds as data from json
    






    while True:
        # print(main.hero1.mana)
            
        
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        # Handle pause timing correctly by accumulating paused durations.
        if not paused:
            # If we have a paused_start_time it means we just resumed; accumulate the paused duration
            if paused_start_time is not None:
                total_paused_duration += (current_time - paused_start_time)
                paused_start_time = None

            # Update global_vars so other modules (like heroes) can read paused totals
            global_vars.PAUSED = False
            global_vars.PAUSED_TOTAL_DURATION = total_paused_duration
            global_vars.PAUSED_START = None

            if winner is None:
                # Elapsed time excludes total paused duration
                elapsed_time = (current_time - start_time - total_paused_duration) // 1000
            else:
                # Freeze final elapsed time when a winner is determined
                if final_elapsed_time is None:
                    final_elapsed_time = (current_time - start_time - total_paused_duration) // 1000
                elapsed_time = final_elapsed_time
        else:
            # When entering paused state, record when pause started (only once)
            if paused_start_time is None:
                paused_start_time = current_time
                global_vars.PAUSED = True
                global_vars.PAUSED_START = paused_start_time
        
        # if not paused:
        #     main.screen.fill((0, 0, 0))
        # print(global_vars.MAIN_VOLUME)

        for event in main.pygame.event.get():
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()

            if event.type == pygame.USEREVENT + 1 and not game_music_started:
                pygame.mixer.music.load(GAME_MUSIC_1)
                pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME * 0.5)  # Apply mute logic
                pygame.mixer.music.play(1, fade_ms=1500)
                game_music_started = True
                print("Started game music 1")

            elif event.type == pygame.USEREVENT and game_music_started and not second_track_played:
                pygame.mixer.music.load(GAME_MUSIC_2)
                pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME * 0.5)  # Apply mute logic
                pygame.mixer.music.play(loops=-1, fade_ms=1500)
                second_track_played = True
                print("Started game music 2")

            # if keys[pygame.K_ESCAPE]:
            #     menu()
            #     return

            if keys[pygame.K_ESCAPE]:
                paused = True
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if menu_button.is_clicked(event.pos):
            #         menu()
            #         return    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    paused = True 
                
            # Toggle pause state when the pause key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                is_paused = not is_paused

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

        
        if not paused:
            # Background
            # Animate_BG.waterfall_bg.display(screen)
            # Animate_BG.lava_bg.display(screen)
            # Animate_BG.dark_forest_bg.display(screen)
            
            run_background(main.map_selected)

            # main.screen.blit(background, (0, -(720*1.05 - 720)))

            draw_grid(screen) if global_vars.SHOW_GRID else None

            # print(main.hero1.health, main.hero1.max_health)
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


            timer_text = timer_font.render(f"[{elapsed_time}]", global_vars.TEXT_ANTI_ALIASING, main.white)

            main.screen.blit(timer_text, (main.width / 2.3, 30))  # Display timer at the top-left corner
            
            menu_button.draw(main.screen, mouse_pos)
            
            #drawing the hp and mana icon
            main.draw_hp_mana_icons()

            #drawing the damage display

            

            # Update and draw Fire Wizard
            main.hero1_group.draw(main.screen)
            main.hero1_group.update()
            

            # Update and draw Wanderer Magician
            # main.hero3_group.draw(main.screen)
            # main.hero3_group.update()
            # if not main.hero2.is_dead():
            
            main.hero2_group.draw(main.screen)
            main.hero2_group.update()

            # Update anddddddddddddd draw attacks
            attack_display.update()
            attack_display.draw(main.screen)
            if global_vars.SINGLE_MODE_ACTIVE:
                if global_vars.HERO1_BOT:
                    main.hero1.bot_logic()  # Add bot logic for 
                main.hero2.bot_logic()
                if hasattr(main, 'hero3') and main.hero3 is not None:
                    main.hero3.bot_logic()


            if main.hero1.is_dead():
                winner = 'hero2'
            elif main.hero2.is_dead():
                # In single player mode, check if all enemies are dead
                if global_vars.SINGLE_MODE_ACTIVE and hasattr(main, 'hero3') and main.hero3 is not None:
                    if main.hero3.is_dead():
                        winner = 'hero1'
                    else:
                        winner = None
                else:
                    winner = 'hero1'
            elif global_vars.SINGLE_MODE_ACTIVE and hasattr(main, 'hero3') and main.hero3 is not None:
                # In single player mode with 2 enemies, player wins only if both enemies are dead
                if main.hero2.is_dead() and main.hero3.is_dead():
                    winner = 'hero1'
                else:
                    winner = None
            else:
                winner = None
                

            # For displaying mana and special bonus (already on player class)
            # main.hero1.update_damage_numbers(main.screen)
            # main.hero2.update_damage_numbers(main.screen)
            # main.hero3.update_damage_numbers(main.screen)

            # main.hero2.health = 1 if not main.hero2.is_dead() else 0
            battle_end(mouse_pos, mouse_press)
            pause(mouse_pos, mouse_press)
            # print(FPS)
        else:
            pause(mouse_pos, mouse_press)


        

        


        #draw distance
        # main.hero2.draw_distance(main.hero1_group)
        # hero1.draw_hitbox(screen)
                
        main.pygame.display.update()
        main.clock.tick(main.FPS)
        # xaxa.tick(10000)

            
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
                # Only add health and show text if it increases (not already at max)
                # prev = hero1.health
                # Don't display since it will display 2 times
                hero1.health = min(hero1.max_health, hero1.health + bonus_amount)
                # actual = hero1.health - prev
                # if actual > 0:
                #     hero1.display_damage(actual, interval=30, color=(0, 255, 0))
            elif bonus_type == 'mana':
                prev = hero1.mana
                hero1.mana = min(hero1.max_mana, hero1.mana + bonus_amount)
                actual = hero1.mana - prev
                if actual > 0:
                    # blue text for mana pickups
                    hero1.display_damage(actual, interval=30, color=cyan2, size=50)

            elif bonus_type == 'special':
                prev = hero1.special
                hero1.special = min(hero1.max_special, hero1.special + bonus_amount)
                actual = hero1.special - prev
                if actual > 0:
                    # blue-ish text for special pickups
                    hero1.display_damage(actual, interval=30, color=gold, size=50)
                
            cube_x = random.randint(20, int(main.width - 20))
            cube_fall = random.randint(-2000, -500)
            print(f"Cube collected by Player 1: {bonus_type} +{bonus_amount}")
        elif cube_hitbox.colliderect(hero2.hitbox_rect):
            sound.play()
            if bonus_type == 'health':
                # prev = hero2.health
                # Don't display since it will display 2 times
                hero2.health = min(hero2.max_health, hero2.health + bonus_amount)
                # actual = hero2.health - prev
                # if actual > 0:
                #     hero2.display_damage(actual, interval=30, color=(0, 255, 0))
                
            elif bonus_type == 'mana':
                prev = hero2.mana
                hero2.mana = min(hero2.max_mana, hero2.mana + bonus_amount)
                actual = hero2.mana - prev
                if actual > 0:
                    hero2.display_damage(actual, interval=30, color=cyan2, size=50)

            elif bonus_type == 'special':
                prev = hero2.special
                hero2.special = min(hero2.max_special, hero2.special + bonus_amount)
                actual = hero2.special - prev
                if actual > 0:
                    hero2.display_damage(actual, interval=30, color=gold, size=50)

            cube_x = random.randint(20, int(main.width - 20))
            cube_fall =random.randint(-2000, -500)
            print(f"Cube collected by Player 2: {bonus_type} +{bonus_amount}")
    else:
        cube_x = random.randint(20, int(main.width - 20))
        cube_fall = -150

    return cube_fall, cube_x

menu_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2-(width*0.075), height*0.475),
    scale=0.8,
    text='menu',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
rematch_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.475),
    scale=0.8,
    text='rematch',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

resume_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.475),
    scale=0.8,
    text='resume',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

restart_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.575),
    scale=0.8,
    text='restart',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

in_game_settings_button = ImageButton(
    image_path=text_box_img,
    pos=(width/2-(width*0.075), height*0.575),
    scale=scale*0.8,
    text='Settings',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
def battle_end(mouse_pos, mouse_press, font=pygame.font.Font(fr'assets\font\slkscr.ttf', 100), default_size = ((width * DEFAULT_HEIGHT) / (height * DEFAULT_WIDTH)),):
    global paused
    if winner is not None:
        if winner == 'hero1':
            create_title('PLAYER 1 WINS!!!', font, default_size - 0.55, height * 0.40)
        elif winner == 'hero2':
            create_title('PLAYER 2 WINS!!!', font, default_size - 0.55, height * 0.40)
    
        menu_game.draw(screen, mouse_pos)
        rematch_game.draw(screen, mouse_pos)
        if mouse_press[0] and menu_game.is_clicked(mouse_pos):
            paused = False
            menu()
            return

        if mouse_press[0] and rematch_game.is_clicked(mouse_pos):
            paused = False
            reset_all()
            fade(loading_screen_bg, game)
            return

def pause(mouse_pos, mouse_press, font=pygame.font.Font(fr'assets\font\slkscr.ttf', 100), default_size = ((width * DEFAULT_HEIGHT) / (height * DEFAULT_WIDTH)),):
    global paused
    if paused:
        create_title('PAUSED', font, default_size - 0.55, height * 0.40)
    
        menu_game.draw(screen, mouse_pos)
        resume_game.draw(screen, mouse_pos)
        restart_game.draw(screen, mouse_pos)
        in_game_settings_button.draw(screen, mouse_pos)
        if mouse_press[0] and menu_game.is_clicked(mouse_pos):
            paused = False
            menu()
            

        if mouse_press[0] and resume_game.is_clicked(mouse_pos):
            paused = False

        if mouse_press[0] and restart_game.is_clicked(mouse_pos):
            paused = False
            reset_all()
            fade(loading_screen_bg, game)
            

        if mouse_press[0] and in_game_settings_button.is_clicked(mouse_pos):
            settings(in_game=True)


            

pygame.mixer.music.set_volume(0.8 * global_vars.MAIN_VOLUME)
def menu():
    
    pygame.mixer.music.fadeout(1000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(MENU_MUSIC)
    # Set volume based on mute state
    if global_vars.MUTE:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(global_vars.MAIN_VOLUME)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1, fade_ms=1500)  # Loop indefinitely
    print('playing music')

    # background = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\backgrounds\9.png').convert(), (main.width, main.height))

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
                pass
                # main.player_selection()
                # return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.is_clicked(event.pos):
                    global_vars.SINGLE_MODE_ACTIVE = True
                    main.player_selection()
                    return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if multiplayer_button.is_clicked(event.pos):
                    global_vars.SINGLE_MODE_ACTIVE = False
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
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_button.is_clicked(event.pos):
                    settings()
                    return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if campaign_button.is_clicked(event.pos):
                    campaign()
                    return

            if keys[pygame.K_SPACE]:
                main.player_selection()
                return
            
            if keys[pygame.K_r]:
                main.player_selection()
                return
            
            if keys[pygame.K_e]:
                controls()
                return
        # main.screen.blit(background, (0, 0))
        
        Animate_BG.waterfall_day_bg.display(screen, speed=50)
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

        

        # print(global_vars.MAIN_VOLUME)
        pygame.display.update()
        main.clock.tick(main.FPS)

def campaign():
    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # mouse_press = pygame.mouse.get_pressed()
        # key_press = pygame.key.get_pressed()

        main.screen.fill((50, 50, 50))
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
        menu_button.draw(screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)




keybinds = ImageButton(
    image_path=text_box_img,
    pos=(width/2, height*0.9),
    scale=0.8,
    text='Set Keys',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
def controls():
    # command_img = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\command image.png').convert(), (main.width/2, main.height))
    # control_img = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\control image.png').convert(), (main.width/2, main.height))

    skill_1_btn = RectButton(width*0.1, height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Skill 1")
    skill_2_btn = RectButton(width*0.1, height*0.3, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Skill 2")
    skill_3_btn = RectButton(width*0.1, height*0.4, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Skill 3")
    skill_4_btn = RectButton(width*0.1, height*0.5, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Skill 4")
    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()
        clicked = False
        
        main.screen.fill((0, 0, 0))
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
                if keybinds.is_clicked(mouse_pos):
                    print('cliked kbidns') 

            detect = not any([x for x in key.detect_key_skill.values()])
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if skill_1_btn.is_clicked(event.pos) and detect:
                    key.detect_key_skill['read_skill_1'] = skill_1_btn.toggle(key.detect_key_skill['read_skill_1'])
                    clicked = True
                if skill_2_btn.is_clicked(event.pos) and detect:
                    key.detect_key_skill['read_skill_2'] = skill_1_btn.toggle(key.detect_key_skill['read_skill_2'])
                    clicked = True
                if skill_3_btn.is_clicked(event.pos) and detect:
                    key.detect_key_skill['read_skill_3'] = skill_1_btn.toggle(key.detect_key_skill['read_skill_3'])
                    clicked = True
                if skill_4_btn.is_clicked(event.pos) and detect:
                    key.detect_key_skill['read_skill_4'] = skill_1_btn.toggle(key.detect_key_skill['read_skill_4'])
                    clicked = True
                
        # print(type(keys))
            
            
            if not detect:
                # print(event.type)
                # print(keys[pygame.K_a])
            
                # for index, pressed in enumerate(keys):
                #     print(keys[pygame.K_a])
                #     if pressed and index > 90:
                #         key_name = pygame.key.name(index).upper()
                #         print(f"Selected: {key_name}")
               


                for i in key.status:
                    if keys[i] == True:
                        print(f"selected {pygame.key.name(i)}")
                        
                        # break  # Remove to detect multiple
                    
                
                # for i in keys:
                #     if i in key.status:
                        
                    # for x,i in enumerate(keys):
                    #     if i == True:
                    #         print(x)
                        for i in key.detect_key_skill:
                                print(f"falsing {i}")
                                key.detect_key_skill[i] = False


        #------------------------
        keybinds.draw(screen, mouse_pos)

        #functoinability
        skill_1_btn.update(mouse_pos, key.detect_key_skill['read_skill_1'])
        skill_2_btn.update(mouse_pos, key.detect_key_skill['read_skill_2'])
        skill_3_btn.update(mouse_pos, key.detect_key_skill['read_skill_3'])
        skill_4_btn.update(mouse_pos, key.detect_key_skill['read_skill_4'])

        #draw
        skill_1_btn.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_2_btn.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_3_btn.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_4_btn.draw(screen, global_vars.TEXT_ANTI_ALIASING)







                
        
        # main.screen.blit(command_img, (0, 0))
        # main.screen.blit(control_img, (main.width/2, 0))
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
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    previous = ImageButton(
    image_path=text_box_img,
    pos=(main.width-80, 60),
    scale=0.75,
    text='previous',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.02),  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    
    inffo = ImageButton(
    image_path=text_box_img,
    pos=(main.width-150, main.height/1.5),
    scale=0.75,
    text='burn damage = 5 for fire knight',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.015),  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    
    switch = False
    
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
        # dev option
        if IMMEDIATE_RUN:
            main.player_selection()
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
        # Animate_BG.trees_bg.display(screen, speed=50)
        create_title('Fighting Kimhie', font, default_size, main.height * 0.2, color='Grey3')
        play_button.draw(main.screen, mouse_pos)

        

        pygame.display.update()
        main.clock.tick(main.FPS)

def reset_all():
    global fade_alpha, fading, fade_start_time
    global_vars.PAUSED = False
    global_vars.PAUSED_TOTAL_DURATION = 0
    global_vars.PAUSED_START = None
    # reset hero states
    heroes_to_reset = [main.hero1, main.hero2]
    if hasattr(main, 'hero3') and main.hero3 is not None:
        heroes_to_reset.append(main.hero3)
    for hero in heroes_to_reset:
        hero.freeze_sources = set()
        hero.root_sources = set()
        hero.frozen = False
        hero.rooted = False
        hero.stunned = False
        hero.slowed = False
        hero.freeze_source = None
        hero.root_source = None
        if hasattr(hero, 'atk_hasted'):
            # print('ahah')
            default_atk_speed_with_bonus = hero.get_atk_speed()
            hero.atk_hasted = False # removes the buff for forest ranger if possible
            hero.basic_attack_animation_speed = default_atk_speed_with_bonus
        if hasattr(hero, 'invisible'):
            hero.invisible = False
            hero.casting_invisible = False
            hero.invisible_duration = 0
        hero.y_velocity = 0
        hero.x_velocity = 0
        hero.running = False
        hero.attacking1 = hero.attacking2 = hero.attacking3 = hero.sp_attacking = False
        hero.basic_attacking = hero.sp_attacking = False
        hero.special_active = False
        hero.animation_done = False

    # reset cd
    for attack in main.hero1.attacks:
        attack.reduce_cd(True)
    for attack in main.hero2.attacks:
        attack.reduce_cd(True)
    if hasattr(main, 'hero3') and main.hero3 is not None:
        for attack in main.hero3.attacks:
            attack.reduce_cd(True)

    for attack in main.hero1.attacks_special:
        attack.reduce_cd(True)
    for attack in main.hero2.attacks_special :
        attack.reduce_cd(True)
    if hasattr(main, 'hero3') and main.hero3 is not None:
        for attack in main.hero3.attacks_special:
            attack.reduce_cd(True)

    #reset health
    main.hero1.health = main.hero1.max_health
    main.hero2.health = main.hero2.max_health
    main.hero1.mana = main.hero1.max_mana
    main.hero2.mana = main.hero2.max_mana
    main.hero1.special = 0
    main.hero2.special = 0
    if hasattr(main, 'hero3') and main.hero3 is not None:
        main.hero3.health = main.hero3.max_health
        main.hero3.mana = main.hero3.max_mana
        main.hero3.special = 0
        main.hero3.white_health_p2 = main.hero3.max_health
        main.hero3.white_mana_p2 = main.hero3.max_mana
        main.hero3.damage_numbers.clear()

    main.hero1.white_health_p1 = main.hero1.max_health
    main.hero2.white_health_p2 = main.hero2.max_health
    main.hero1.white_mana_p1 = main.hero1.max_mana
    main.hero2.white_mana_p2 = main.hero2.max_mana

    main.hero1.damage_numbers.clear()
    main.hero2.damage_numbers.clear()

    # reset pos
    main.hero1.x_pos = global_vars.X_POS_SPACING if main.hero1.player_type == 1 else global_vars.DEFAULT_X_POS
    main.hero1.y_pos = global_vars.DEFAULT_Y_POS
    main.hero2.x_pos = global_vars.X_POS_SPACING if main.hero2.player_type == 1 else global_vars.DEFAULT_X_POS
    main.hero2.y_pos = global_vars.DEFAULT_Y_POS
    if hasattr(main, 'hero3') and main.hero3 is not None:
        from global_vars import DEFAULT_X_POS, DEFAULT_Y_POS
        main.hero3.x_pos = DEFAULT_X_POS - 50  # Offset hero3 slightly to the left of hero2
        main.hero3.y_pos = DEFAULT_Y_POS

    # fade_overlay = pygame.Surface((width, height))
    # fade_overlay.fill((0, 0, 0))
    # fade_alpha = 0
    # fading = True
    # fade_start_time = pygame.time.get_ticks()

    attack_display.empty()
    # Reset paused tracking so timers/cooldowns start fresh
    

volume_limit = {'min':100, 'max':300}
current_volume = (global_vars.MAIN_VOLUME*100) + volume_limit['min']
volume_button_rect = pygame.Rect(current_volume, center_pos[1]-2, 13, 25)

# NOTE: The mute button does not use this function
from button import RectButton

def settings(in_game=False):
    global paused
    
    font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH)) / 1.5
    # global_vars.SMOOTH_BG = not global_vars.SMOOTH_BG

    
    # current_volume = global_vars.MAIN_VOLUME*100
    setting_font = pygame.font.Font(fr'assets\font\slkscr.ttf', int(height * 0.025))
    
    # true
    
    
    volume_clicked = False
    mute_hovered = False

    # Move volume bar to the right
    volume_bar_x = 100
    volume_bar_y = center_pos[1]
    volume_bar_decor_rect = pygame.Rect(volume_bar_x-5, volume_bar_y-5, (volume_limit['max']-volume_limit['min']+20), 30)
    volume_button_rect.x = volume_bar_x + (global_vars.MAIN_VOLUME * 200)  # 200 is the range
    volume_button_rect.y = volume_bar_y - 2

    # Mute button decor
    mute_rect = pygame.Rect(volume_bar_x-65, volume_bar_y-10, 40, 40)
    mute_clicked = global_vars.MUTE

    anti_alias_button = RectButton(width*0.1, height-height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Text Anti-Aliasing")
    smooth_bg_button = RectButton(width*0.3, height-height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Smooth Background")
    show_distance_button = RectButton(width*0.5, height-height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Distance")
    show_hitbox_button = RectButton(width*0.7, height-height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Hitbox")
    show_grid_button = RectButton(width*0.9, height-height*0.2, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Grid (don't)")

    show_health_bar = RectButton(width*0.5, center_pos[1], r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Health Bar")
    show_mana_bar = RectButton(width*0.7, center_pos[1], r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Mana Bar")
    show_special_bar = RectButton(width*0.9, center_pos[1], r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Special Bar")
    

    # text anti-alias


    while True:
        # print(global_vars.SMOOTH_BG)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        mute_hovered = mute_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

            if keys[pygame.K_ESCAPE]:
                if not in_game:
                    menu()
                return
            
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    if not in_game:
                        menu()
                    return
                if mute_rect.collidepoint(event.pos):
                    mute_clicked = not mute_clicked
                    global_vars.MUTE = mute_clicked
                    pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME)
                        
                if volume_button_rect.collidepoint(event.pos):
                    volume_clicked = True

                if anti_alias_button.is_clicked(event.pos):
                    global_vars.TEXT_ANTI_ALIASING = anti_alias_button.toggle(global_vars.TEXT_ANTI_ALIASING)
                
                if smooth_bg_button.is_clicked(event.pos):
                    global_vars.SMOOTH_BG = smooth_bg_button.toggle(global_vars.SMOOTH_BG)
                
                if show_distance_button.is_clicked(event.pos):
                    global_vars.DRAW_DISTANCE = show_distance_button.toggle(global_vars.DRAW_DISTANCE)

                if show_hitbox_button.is_clicked(event.pos):
                    global_vars.SHOW_HITBOX = show_hitbox_button.toggle(global_vars.SHOW_HITBOX)

                if show_grid_button.is_clicked(event.pos):
                    global_vars.SHOW_GRID = show_grid_button.toggle(global_vars.SHOW_GRID)

                if show_health_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_HEALTH_BAR = show_health_bar.toggle(global_vars.SHOW_MINI_HEALTH_BAR)

                if show_mana_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_MANA_BAR = show_mana_bar.toggle(global_vars.SHOW_MINI_MANA_BAR)

                if show_special_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_SPECIAL_BAR = show_special_bar.toggle(global_vars.SHOW_MINI_SPECIAL_BAR)
                
                

            
            elif event.type == pygame.MOUSEBUTTONUP:
                volume_clicked = False
        # print(global_vars.MAIN_VOLUME)
        # Volume bar logic
        volume_bar_rect = pygame.Rect(volume_bar_x, volume_bar_y, volume_button_rect.x-volume_bar_x, 20)

        if volume_clicked and not mute_clicked:
            volume_button_rect.x = mouse_pos[0]
        if volume_button_rect.x >= volume_bar_x + (volume_limit['max']-volume_limit['min']):
            volume_button_rect.x = volume_bar_x + (volume_limit['max']-volume_limit['min'])
        elif volume_button_rect.x <= volume_bar_x:
            volume_button_rect.x = volume_bar_x

        # Calculate volume
        global_vars.MAIN_VOLUME = ((volume_button_rect.x - volume_bar_x) / (volume_limit['max'] - volume_limit['min']))
        pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME)  # Apply mute logic


        Animate_BG.waterfall_rainy_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_rainy_bg.display(screen, speed=50)
        create_title('Settings', font, default_size, main.height * 0.2, color='Grey3')
        


        # Draw mute button decor
        mute_color = (0, 75, 0) if mute_hovered else (30, 30, 30)
        if mute_clicked:
            mute_color = (0, 150, 0)
        if mute_clicked and mute_hovered:
            mute_color = (0, 200, 0)
        
        # Draw mute button
        pygame.draw.rect(screen, mute_color, mute_rect)

        # Button functionality
        anti_alias_button.update(mouse_pos, global_vars.TEXT_ANTI_ALIASING)
        smooth_bg_button.update(mouse_pos, global_vars.SMOOTH_BG)
        show_distance_button.update(mouse_pos, global_vars.DRAW_DISTANCE)
        show_hitbox_button.update(mouse_pos, global_vars.SHOW_HITBOX)
        show_grid_button.update(mouse_pos, global_vars.SHOW_GRID)
        show_mana_bar.update(mouse_pos, global_vars.SHOW_MINI_MANA_BAR)
        show_special_bar.update(mouse_pos, global_vars.SHOW_MINI_SPECIAL_BAR)
        show_health_bar.update(mouse_pos, global_vars.SHOW_MINI_HEALTH_BAR)
        # Drawing buttons
        anti_alias_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        smooth_bg_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_distance_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_hitbox_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_grid_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_mana_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_special_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_health_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        # Draw mute text
        # mute_text = setting_font.render('Mute' if random.random() > 0.5 else "fsa", global_vars.TEXT_ANTI_ALIASING, white)
        mute_text = setting_font.render('Mute', global_vars.TEXT_ANTI_ALIASING, white)
        mute_text_rect = mute_text.get_rect(center=(mute_rect.centerx, mute_rect.centery-mute_rect.height))
        screen.blit(mute_text, mute_text_rect)

        # Draw volume bar decor
        pygame.draw.rect(screen, black, volume_bar_decor_rect)
        pygame.draw.rect(screen, white if not mute_clicked else black, volume_bar_rect)
        pygame.draw.rect(screen, 'Red' if not mute_clicked else black, volume_button_rect)

        # Draw volume number background and text
        vol_num_rect = pygame.Rect(volume_bar_x + (volume_limit['max']-volume_limit['min']) + 30, volume_bar_y-5, 60, 30)
        pygame.draw.rect(screen, black, vol_num_rect)
        vol_num = int(global_vars.MAIN_VOLUME * 100) if not mute_clicked else 0
        vol_num_font = pygame.font.Font(fr'assets\font\slkscr.ttf', int(height * 0.025))
        vol_num_text = vol_num_font.render(f'{vol_num}%', global_vars.TEXT_ANTI_ALIASING, white)
        vol_num_text_rect = vol_num_text.get_rect(center=vol_num_rect.center)
        screen.blit(vol_num_text, vol_num_text_rect)

        menu_button.draw(screen, mouse_pos)
        # print(global_vars.MUTE)

        pygame.display.update()
        main.clock.tick(main.FPS)







# Image Paths

# fade()
loading = ImageButton(
    image_path=loading_button_img,
    pos=center_pos,
    scale=0.8,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# Menu button to return to menu()
menu_button = ImageButton(
    image_path=menu_button_img,
    pos=(40, 10),
    scale=0.75,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# main_menu()
play_button = ImageButton(
    image_path=play_button_img,
    pos=center_pos,
    scale=scale,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
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
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
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
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
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
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

multiplayer_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]),
    scale=scale,
    text='Multiplayer',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

info_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 100, height - 100),
    scale=scale*0.8,
    text='Game Info',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

control_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 100, height - 50),
    scale=scale*0.8,
    text='Controls',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

settings_button = ImageButton(
    image_path=text_box_img,
    pos=(100, height - 50),
    scale=scale*0.8,
    text='Settings',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)



def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0):
    title = pygame.transform.rotozoom(font.render(f'{text}', global_vars.TEXT_ANTI_ALIASING, color), angle, scale)
    title_rect = title.get_rect(center = (width / 2, y_offset))
    screen.blit(title, title_rect)








if __name__ == '__main__':
    main_menu()


