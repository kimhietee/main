import pygame
# Screen and Display
width = 1280
height = 720
# 1280 x 800 PERFECT FULL SCREEN (pls modify your display resolution :)
# width = 1920
# height = 1080
icon = pygame.image.load(r'assets\icons\miku.png')
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
# screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
# Colors
white = 'White'
red = 'Red'
black = 'Black'
green = 'Green'
cyan2 = 'Cyan2'
gold = 'Gold'
MAIN_VOLUME = 0.5
TEXT_ANTI_ALIASING = False
MAX_ITEM = 20
# MAX DEFAULT ITEM = 3


SINGLE_MODE_ACTIVE = False # constant
MUTE = False # constant
SHOW_HITBOX = False
DRAW_DISTANCE = False
SHOW_GRID = False

# Default Dimensions
DEFAULT_WIDTH = width
DEFAULT_HEIGHT = height

# Player Limit
ZERO_WIDTH = 0
TOTAL_WIDTH = width

# Game Settings
DISABLE_HEAL_REGEN = False

DEFAULT_HEALTH_REGENERATION = 0.02
DEFAULT_MANA_REGENERATION = 0.1
DEFAULT_BASIC_ATK_DMG_BONUS = 1.2

LOW_HP = 20
LITERAL_HEALTH_DEAD = 0
SPECIAL_MULTIPLIER = 1 # +dmg
# SPECIAL_MULTIPLIER = 2
MAX_SPECIAL = 200
SPECIAL_DURATION = 0.2

MANA_COST_INCREASE = 0.3

DISABLE_SPECIAL_REDUCE = False

# Character Settings
DEFAULT_CHAR_SIZE = 1.25
DEFAULT_CHAR_SIZE_2 = 1.9
DEFAULT_ANIMATION_SPEED = 120
DEFAULT_ANIMATION_SPEED_FOR_JUMPING = 2
JUMP_DELAY = 50
RUNNING_SPEED = 2.2

# Spacing and Positioning
X_POS_SPACING = 100
DEFAULT_X_POS = (int(width)) - 100

# This is the ground position
DEFAULT_Y_POS = ((int(height)) * 0.76) * 1.05 #145 left if height == 720 
'''
DEFAULT_Y_POS = (720 * 0.76) * 1.05
              = 547.2 * 1.05
              = 574.56

DEFAULT_Y_POS = 574

The screen size (gameplay screeen):
background_size = (width, int(height * 0.798))  # 0.798 = 574 / 720
'''

SPACING_X = int(width * 0.078)
START_OFFSET_X = int(width * 0.039)
SKILL_Y_OFFSET = int(height * 0.896)
ICON_WIDTH = int(width * 0.058)
ICON_HEIGHT = int(height * 0.104)

BASIC_ATK_POSX = int(width * 0.039)
BASIC_ATK_POSY = int(height * 0.896)

BASIC_ATK_POSX_END = width - (int(width * 0.039))


# Physics
DEFAULT_GRAVITY = 0.6
DEFAULT_JUMP_FORCE = -13
JUMP_LOGIC_EXECUTE_ANIMATION = 2

# Bar Settings
WHITE_BAR_SPEED_HP = 0.1
WHITE_BAR_SPEED_MANA = 1
TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT = 20

RUNNING_ANIMATION_SPEED = 6
# Player Selection
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_1_SELECTED_HERO = None
PLAYER_2_SELECTED_HERO = None
PLAYER_1_ICON = None
PLAYER_2_ICON = None

# Attack Display
attack_display = pygame.sprite.Group()

# Basic Attack
BASIC_SLASH_ANIMATION = 5
BASIC_SLASH_SIZE = 2
BASIC_SLASH_SIZE_BIG = 3
BASIC_ATK_COOLDOWN = 500
BASIC_FRAME_DURATION = 100

# BASIC_ATK_DAMAGE = 6.5/5 # slow atk
# BASIC_ATK_DAMAGE2 = 2.7/5 # medium 2 atks
# BASIC_ATK_DAMAGE3 = 1.2/5 #fast atk
# BASIC_ATK_DAMAGE4 = 3.2 # ranged

#this does not matter, pls ignore this
BASIC_ATK_DAMAGE = 6.5 # slow atk
BASIC_ATK_DAMAGE2 = 2.7 # medium 2 atks
BASIC_ATK_DAMAGE3 = 1.2 #fast atk
BASIC_ATK_DAMAGE4 = 3.2 # ranged

# Miscellaneous
MULT = 0.7
dmg_mult = 0.05



hero1 = None
hero2 = None

#hero icons
fire_wizard_icon = r'assets\hero profiles\fire wizard prof.png'
wanderer_magician_icon = r'assets\hero profiles\wanderer magician prof.png'
fire_knight_icon = r'assets\hero profiles\fire knight prof.png'
wind_hashashin_icon = r'assets\hero profiles\wind hasashin prof.jpg'

#buttons
play_button_img = r'assets\UI\buttons\BTN PLAY.png'
text_box_img = r'assets\UI\buttons\Button BG.png'
loading_button_img = r'assets\UI\buttons\Loading icon.png'
menu_button_img = r'assets\UI\more\BTN MENU.png' 

# button modifers

scale = 1
center_pos = (width / 2, height / 2)
# font_size = 100
font_size = int(height * 0.02)# = 14






# a = ['Learn', 'Quiz', 'Practice', 'Contribute'] 
# b = a 
# c = a[:] 

# b[0] = 'Code'
# c[1] = 'Mcq'

# count = 0
# for c in (a, b, c): 
# 	if c[0] == 'Code': 
# 		count += 1
# 	if c[1] == 'Mcq': 
# 		count += 10

# print (count) 
# print(c)
# li = range(100, 110) 
# for i in li:
#     print(i)

# a = [10, 20, 30, 40, 50] 
# b = [1, 2, 3, 4, 5] 
# subtracted = list()
# for a, b in zip(a, b):
#     item = a -b
#     subtracted.append(item)

# print(subtracted)


# li = [2, 3, 9] 
# li = [[x for x in[li]] for x in range(3)] 
# print (li) 


# a = [x for x in range(5)] 
# b = [x for x in range(7) if x in a and x%2==0] 
# print(b)

# a = []
# a.append([1, [2, 3], 4])
# a.extend([7, 8, 9])
# print(a[0][1][1] + a[2])



# a = 'kimhey'
# print(a[0:6:2])

# size = 30
# for i in range(size):
#     count = size - i
#     print(' ' * (count // 2), end='')
#     print('*' * (i+1))
# x = 1
# b = [1,2,3,4,5,6,7,8,9,10]
# print(x in b)