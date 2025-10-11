import pygame
from global_vars import (
    width, height, icon, FPS, clock, screen, hero1, hero2, BASIC_SLASH_ANIMATION, BASIC_SLASH_SIZE, ICON_WIDTH, ICON_HEIGHT, BASIC_ATK_POSX, BASIC_ATK_POSY, BASIC_ATK_POSX_END, BASIC_SLASH_SIZE_BIG,
    white, red, black, green, cyan2, gold, MAX_SPECIAL, BASIC_ATK_COOLDOWN, MAIN_VOLUME,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LITERAL_HEALTH_DEAD, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING, RUNNING_ANIMATION_SPEED,
    JUMP_DELAY, RUNNING_SPEED, TEXT_ANTI_ALIASING,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    attack_display
)
from sprite_loader import SpriteSheet, SpriteSheet_Flipped
# from attack import Attacks, Attack_Display
import random
#AS OF 4/23/25 (12:15 AM)
'''SPECIAL LASTS 16-17 SECONDS
 if you don't do anything :))'''
'''
fire wizard
ult 64 w/ + damage
3rd 24
2nd 57-62 full duration
1st skill up 16

special
1st 22 center
2nd 52 full duration
3rd 28.5
ult 68


wanderer magician
1st idk it depends 7.5 - 30
heal 28
3rd 26
ult 52  

special
1st idk man it depends but increase dmg
heal 35
3rd 32
ult 65


fire knight dmg
1st 9
2nd 20
3rd 35
4th 55

special
1st 7.5
2nd 36
3rd 28-38 final (38 total)
4th 60-70 (70 total)


wind hashashin
1st 8
2nd 20
3rd 27
4th 60

special
1st 10
2nd 27  
3rd 29-32
4th 70
'''

class Player(pygame.sprite.Sprite):
    def __init__(self, player_type):
        super().__init__()
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Unknown"
        self.enemy = None
        self.items = [] # contains 3 or less than 3 item classes. ex. 
                            # self.items = [Item("War Helmet", r"assets\item icons\in use\Icons_40.png", ["str", "str flat", "hp regen"], [0.05, 1, 0.04])]
        self.damage_reduce = 0
        self.special_increase = 0
        self.lifesteal = 0
        self.stunned = False
        self.str_mult = 5
        self.int_mult = 5
        self.agi_mult = 0.1

        # stat
        self.strength = 40
        self.intelligence = 40
        self.agility = 40

        # Base Stats
        self.max_health = 0
        self.max_mana = 0
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = 0

        self.max_special = MAX_SPECIAL
        self.special = 0
        self.special_active = False

        self.mana_regen = DEFAULT_MANA_REGENERATION
        self.health_regen = DEFAULT_HEALTH_REGENERATION

        self.basic_attack_cooldown = BASIC_ATK_COOLDOWN

        self.default_animation_speed = DEFAULT_ANIMATION_SPEED

        
        # self.last_health = self.health
        
        # self.bonus_type = "strength"
        # self.bonus_value = self.strength
        # # self.item_info_dict = {}   
        # self.item_info_dict.update(self.player_instance.bonus_type, self.player_instance.bonus_value)  



        # Player Position
        self.x = 0
        self.y = 0
        self.width = 0

        #dmg
        self.atk1_cooldown = 0
        self.atk2_cooldown = 0
        self.atk3_cooldown = 0
        self.sp_cooldown = 0

        #self.damage_list = []
        #FORMULA = DESIRED DMG / TOTAL FRAME EX. dmg=25/34 == 0.6944
        self.atk1_damage = (0, 0)
        self.atk2_damage = (0, 0) # 60 total if ur in the center + the multiplier = 64
        self.atk3_damage = (0, 0)# 25+something 
        self.sp_damage = (0, 0) # (47.6, 14) = 61.6


        self.dmg_mult = 0

        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * self.dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * self.dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * self.dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * self.dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * self.dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * self.dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * self.dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * self.dmg_mult)

        # Player Animation Source
        jump_ani = None
        run_ani = None
        idle_ani= None
        atk1_ani= None
        sp_ani= None
        death_ani= None

        # Player Skill Sounds Effects Source
        # self.atk1_sound = pygame.mixer.Sound(None)
        # self.atk2_sound = pygame.mixer.Sound(None)
        # self.atk3_sound = pygame.mixer.Sound(None)
        # self.sp_sound = pygame.mixer.Sound(None)
        # self.atk1_sound.set_volume(0.5)
        # self.atk2_sound.set_volume(0.1)
        # self.atk3_sound.set_volume(0.5)
        # self.sp_sound.set_volume(0.5)

        # Player Skill Animations Source
        atk1 = None
        atk2 = None
        atk3 = None
        sp = None

        # Player Skill Icons Source
        skill_1 = None
        skill_2 = None
        skill_3 = None
        skill_4 = None

        # Player Icon Rects
        self.skill_1_rect = skill_1
        self.skill_2_rect = skill_2
        self.skill_3_rect = skill_3
        self.skill_4_rect = skill_4

        # Player Attack Animations Load
        self.atk1 = atk1
        self.atk2 = atk2
        self.atk3 = atk3
        self.sp = sp

        # Player Animations Load
        self.player_basic = None
        self.player_basic_flipped = None

        self.player_jump = None
        self.player_jump_flipped = None
        self.player_idle = None
        self.player_idle_flipped = None
        self.player_run = None
        self.player_run_flipped = None
        self.player_atk1 = None
        self.player_atk1_flipped = None
        self.player_atk2 = None
        self.player_atk2_flipped = None
        self.player_atk3 = None
        self.player_atk3_flipped = None
        self.player_sp = None
        self.player_sp_flipped = None
        self.player_death = None
        self.player_death_flipped = None

        # Player Image and Rect
        self.image = None
        self.rect = None # (midbottom = (self.x_pos, self.y_pos)) if p2
        self.hitbox_rect = pygame.Rect(0, 0, 50, 50)
        
        # Player Animation States
        self.player_basic_index = 0
        self.player_basic_index_flipped = 0
        
        self.player_jump_index = 0
        self.player_jump_index_flipped = 0
        self.player_idle_index = 0
        self.player_idle_index_flipped = 0
        self.player_run_index = 0
        self.player_run_index_flipped = 0
        self.player_atk1_index = 0
        self.player_atk1_index_flipped = 0
        self.player_atk2_index = 0
        self.player_atk2_index_flipped = 0
        self.player_atk3_index = 0
        self.player_atk3_index_flipped = 0
        self.player_sp_index = 0
        self.player_sp_index_flipped = 0
        self.player_death_index = 0
        self.player_death_index_flipped = 0

        # Player Attacking States
        self.attacking1 = False
        self.attacking2 = False
        self.attacking3 = False
        self.sp_attacking = False
        self.basic_attacking = False

        self.basic_attacking = False

        # ...
        self.last_atk_time = 0

        # Player Position
        self.x_pos = X_POS_SPACING if self.player_type == 1 else DEFAULT_X_POS
        self.y_pos = DEFAULT_Y_POS

        # Gravity
        self.y_velocity = 0
        self.jumping = False

        # Mana Values
        self.mana_cost_list = []

        # Modify
        self.lowest_mana_cost = 0

        # Skills
        self.attacks = []

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   

        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   

        # Main Inheritance
        self.running = False
        self.jumping = False
        self.facing_right = True 
        self.speed = RUNNING_SPEED
        self.running_animation_speed = RUNNING_ANIMATION_SPEED
        
        # self.base_attack_animation_speed = 0 # base atk speed for every hero, modify each if you want to set base 
        self.basic_attack_animation_speed = DEFAULT_ANIMATION_SPEED # also set this one too

        self.mana_costs = []

        self.y_velocity = 0
        self.jumping = False


        #Attack-------------------------------------------------------------

        basic_slash = [r'assets\attacks\Basic Attack\1', BASIC_SLASH_ANIMATION, 1]
        self.basic_slash = self.load_img_frames_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE)
        self.basic_slash_flipped = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE)

        self.basic_slash_big = self.load_img_frames_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE_BIG)
        self.basic_slash_flipped_big = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE_BIG)


        basic_slash2 = [r'assets\attacks\Basic Attack\2', BASIC_SLASH_ANIMATION, 1]
        self.basic_slash2 = self.load_img_frames_tile_method(basic_slash2[0], basic_slash2[1], basic_slash2[2], BASIC_SLASH_SIZE_BIG)
        self.basic_slash2_flipped = self.load_img_frames_flipped_tile_method(basic_slash2[0], basic_slash2[1], basic_slash2[2], BASIC_SLASH_SIZE_BIG)

        # melee
        self.basic_icon = pygame.transform.scale(pygame.image.load(r'assets\icons\Blade_Dance_icon.webp').convert_alpha(), (ICON_WIDTH / 1.5, ICON_HEIGHT / 1.5))

        # ranged
        self.basic_icon2 = pygame.transform.scale(pygame.image.load(r'assets\icons\aghanims-scepter-from-dota-2-made-in-blender-v0-ew9qzvl10s2d1.webp').convert_alpha(), (ICON_WIDTH / 1.5, ICON_HEIGHT / 1.5))  

        self.basic_sound = pygame.mixer.Sound(r'assets\sound effects\jump.swing-whoosh-110410.mp3')
        self.basic_sound.set_volume(0.5 * MAIN_VOLUME)
        
        # modify in hero
        if self.player_type == 1:
            self.basic_icon_rect = self.basic_icon.get_rect(center=(BASIC_ATK_POSX, BASIC_ATK_POSY))
        if self.player_type == 2:
            self.basic_icon_rect = self.basic_icon.get_rect(center=(BASIC_ATK_POSX_END, BASIC_ATK_POSY))

        
        self.special_sound = pygame.mixer.Sound(r'assets\sound effects\heart-beat-137135.mp3')
        self.special_sound.set_volume(1 * MAIN_VOLUME)

        #Attack-------------------------------------------------------------
        self.last_health = self.health
        # self.just_spawned = True
        self.damage_numbers = []

        self.damage_font = pygame.font.Font('assets/font/slkscr.ttf', 30)  # preload font

    def display_damage(self, damage, interval=30, color=(255, 0, 0), size=None):
        if not hasattr(self, 'rect'):
            return  # Safety check
        # Don't show healing text if player is already at max health or at the start of the game
        if (color == (0, 255, 0) and self.health >= self.max_health) or not hasattr(self, "spawn_time") or pygame.time.get_ticks() - self.spawn_time < 50:
            return
        # Don't show healing text if player is already at max health
        # Color (0,255,0) is used for heal display elsewhere
        
        if color == cyan2 and self.mana >= self.max_mana:
            return
        if color == gold and self.special >= self.max_special:
            return
        # if self.health > self.max_health: # don't show hp dmg when  game starts
        #     return

        # Random offset so numbers don’t overlap each other
        offset_x = random.randint(-20, 20)
        
        # Offset Y based on damage (higher damage = higher text)
        if damage > 20:
            offset_y = random.randint(90,100)
        elif damage > 10:
            offset_y = random.randint(70, 80)
        elif damage > 5:
            offset_y = random.randint(50, 60)
        else:
            offset_y = random.randint(10, 20)

        x = self.hitbox_rect.centerx + offset_x
        y = self.hitbox_rect.top - offset_y

        # Font size 
        if size is None:
            if damage > 20:
                size = size or (30 + int(damage))  # Big damage just adds to base size
            elif damage > 5:
                size = size or int(20 + damage * 2)  # Medium scaling
            else:
                size = size or int(20 + damage * 3)  # Small damage gets boosted 

        font = pygame.font.Font('assets/font/slkscr.ttf', size)

        # Format floating numbers cleanly
        if isinstance(damage, float):
            display_text = f"{damage:.1f}".rstrip('0').rstrip('.')  # E.g., 0.33 or 1.2
        elif abs(damage) < 0.001:
            display_text = "0"
        else:
            display_text = str(damage)

        self.damage_numbers.append({
            'text': display_text,
            'x': x,
            'y': y,
            'alpha': 255,
            'interval': interval,
            'color': color,
            'font': font
        })

       

    def update_damage_numbers(self, screen):
         # if getattr(self, "just_spawned", False):
        #         self.last_health = self.health
        #         self.just_spawned = False
        #         return
        if not hasattr(self, "spawn_time"):
            self.spawn_time = pygame.time.get_ticks()

        
        for dmg in self.damage_numbers[:]:
            # # Skip rendering and remove healing text if health is already at max
            dmg['y'] -= 1  # Move the text upward
            fade_amount = int(255 / dmg['interval'])
            dmg['alpha'] = max(0, dmg['alpha'] - fade_amount)

            if dmg['alpha'] <= 0:
                self.damage_numbers.remove(dmg)
                continue

            surf = dmg['font'].render(str(dmg['text']), TEXT_ANTI_ALIASING, dmg['color'])
            surf.set_alpha(dmg['alpha'])
            screen.blit(surf, (dmg['x'] - surf.get_width() // 2, dmg['y']))


    def detect_and_display_damage(self, interval=30):
        # This function only for health, check other call for display_damage()
        # print(self.health, self.last_health, 'ahah')
        delta = self.health - self.last_health
        # print(delta)
        if delta < 0:
            self.display_damage(-delta, interval=interval)  # Normal damage (red)
        elif delta > 0.1:  # Only show healing if it's significant (not just natural regen)
            self.display_damage(delta, interval=interval, color=(0, 255, 0))  # Green heal
        self.last_health = self.health


            
    def update_hitbox(self):
        # Center the hitbox inside the player's main rect
        self.hitbox_rect.center = (self.rect.midbottom[0], self.rect.midbottom[1] - 30)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)  # Red outline for debugging

    def display_items(self):
        pass


    def apply_item_bonuses(self):
        # print(self.basic_attack_animation_speed)
        #misc
        
        for item in self.items: # self.items is a list of item classes
            for bonus_value, bonus_type in zip(item.bonus_value, item.bonus_type):
                if bonus_type == 'move speed':
                    self.speed += self.speed * bonus_value
                    self.running_animation_speed += 10 * bonus_value

                if bonus_type == 'attack speed': 
                    self.basic_attack_animation_speed -= 0.1 * bonus_value  # 100 attack speed = 1 animation speed
                    if self.basic_attack_animation_speed < 0.01:  # Prevent negative or zero speed
                        self.basic_attack_animation_speed = 0.01
                    self.basic_attack_cooldown -= 0.5 * bonus_value
                    if self.basic_attack_cooldown < 0.01:  # Prevent negative or zero speed
                        self.basic_attack_cooldown = 0.01     

                    self.attacks[4].cooldown = self.basic_attack_cooldown
                    self.attacks_special[4].cooldown = self.basic_attack_cooldown

                if bonus_type == 'mana reduce':
                    for i in range(0, 4):
                        self.attacks[i].mana_cost -= int(self.attacks[i].mana_cost * bonus_value)
                        self.attacks_special[i].mana_cost -= int(self.attacks_special[i].mana_cost * bonus_value)
                
                if bonus_type == 'cd reduce':
                    for i in range(0, 5):
                        self.attacks[i].cooldown -= int(self.attacks[i].cooldown * bonus_value)
                        self.attacks_special[i].cooldown -= int(self.attacks_special[i].cooldown * bonus_value)

                if bonus_type == "lifesteal":
                    self.lifesteal += bonus_value

                if bonus_type =='dmg reduce':
                    self.damage_reduce += bonus_value

                if bonus_type =='sp increase':
                    self.special_increase += bonus_value

                if bonus_type == 'spell dmg':
                    # Apply bonus spell damage to each skill
                    self.atk1_damage = (
                        self.atk1_damage[0] + (self.atk1_damage[0] * bonus_value),
                        self.atk1_damage[1] + (self.atk1_damage[1] * bonus_value)
                    )
                    self.atk2_damage = (
                        self.atk2_damage[0] + (self.atk2_damage[0] * bonus_value),
                        self.atk2_damage[1] + (self.atk2_damage[1] * bonus_value)
                    )
                    self.atk3_damage = (
                        self.atk3_damage[0] + (self.atk3_damage[0] * bonus_value),
                        self.atk3_damage[1] + (self.atk3_damage[1] * bonus_value)
                    )
                    self.sp_damage = (
                        self.sp_damage[0] + (self.sp_damage[0] * bonus_value),
                        self.sp_damage[1] + (self.sp_damage[1] * bonus_value)
                    )

                    if hasattr(self, 'atk2_damage_2nd'): # For wind hashahin, or any heroes that needs attribute
                        self.atk2_damage_2nd = (  #reused by water princess
                        self.atk2_damage_2nd[0] + (self.atk2_damage_2nd[0] * bonus_value),
                        self.atk2_damage_2nd[1] + (self.atk2_damage_2nd[1] * bonus_value)
                    )
                    if hasattr(self, 'sp_damage_2nd'):
                        self.sp_damage_2nd = (
                        self.sp_damage_2nd[0] + (self.sp_damage_2nd[0] * bonus_value),
                        self.sp_damage_2nd[1] + (self.sp_damage_2nd[1] * bonus_value)
                    )
                    if hasattr(self, 'real_sp_damage'):
                        self.real_sp_damage = self.real_sp_damage + (self.real_sp_damage * bonus_value)


                    #some of these from water princess, will reuse some variable
                    if hasattr(self, 'atk3_damage_2nd'):
                        self.atk3_damage_2nd = self.atk3_damage_2nd + (self.atk3_damage_2nd * bonus_value)
                    if hasattr(self, 'atk1_damage_2nd'):
                        self.atk1_damage_2nd = self.atk1_damage_2nd + (self.atk1_damage_2nd * bonus_value)
                    if hasattr(self, 'sp_damage_3rd'): # For water princess
                        self.sp_damage_3rd = (
                        self.sp_damage_3rd[0] + (self.sp_damage_3rd[0] * bonus_value),
                        self.sp_damage_3rd[1] + (self.sp_damage_3rd[1] * bonus_value)
                    )
                    if hasattr(self, 'sp_atk1_damage'):
                        self.sp_atk1_damage = self.sp_atk1_damage + (self.sp_atk1_damage * bonus_value)
                    if hasattr(self, 'sp_atk2_damage'):
                        self.sp_atk2_damage = self.sp_atk2_damage + (self.sp_atk2_damage * bonus_value)
                    if hasattr(self, 'sp_atk2_damage_2nd'): # For water princess
                        self.sp_atk2_damage_2nd = (
                        self.sp_atk2_damage_2nd[0] + (self.sp_atk2_damage_2nd[0] * bonus_value),
                        self.sp_atk2_damage_2nd[1] + (self.sp_atk2_damage_2nd[1] * bonus_value)
                    )
                    if hasattr(self, 'sp_atk2_damage_3rd'): # For water princess
                        self.sp_atk2_damage_3rd = (
                        self.sp_atk2_damage_3rd[0] + (self.sp_atk2_damage_3rd[0] * bonus_value),
                        self.sp_atk2_damage_3rd[1] + (self.sp_atk2_damage_3rd[1] * bonus_value)
                    )
                    if hasattr(self, 'sp_atk3_damage'): # For water princess
                        self.sp_atk3_damage = (
                        self.sp_atk3_damage[0] + (self.sp_atk3_damage[0] * bonus_value),
                        self.sp_atk3_damage[1] + (self.sp_atk3_damage[1] * bonus_value)
                    )
                    
                



                if bonus_type == 'str':
                    self.strength += self.strength * bonus_value
                    self.max_health = self.str_mult * self.strength
                if bonus_type == 'str flat':
                    self.strength += bonus_value
                    self.max_health = self.str_mult * self.strength
                if bonus_type == 'int':
                    self.intelligence += self.intelligence * bonus_value
                    self.max_mana = self.int_mult * self.intelligence
                if bonus_type == 'int flat':
                    self.intelligence += bonus_value
                    self.max_mana = self.int_mult * self.intelligence
                if bonus_type == 'agi':
                    self.agility += self.agility * bonus_value
                    self.basic_attack_damage = self.agi_mult * self.agility
                if bonus_type == 'agi flat':
                    self.agility += bonus_value
                    self.basic_attack_damage = self.agi_mult * self.agility

                if bonus_type == 'mana regen':
                    self.mana_regen += self.mana_regen * bonus_value
                if bonus_type == 'hp regen':
                    self.health_regen += self.health_regen * bonus_value
                
                # self.max_mana = self.intelligence * self.int_mult
                
                # self.mana = self.max_mana
                #print(self.strength, bonus_value, self.strength * bonus_value)
                #print(bonus_value, bonus_type, self.strength, self.strength * bonus_value, self.strength + bonus_value)

        for item in self.items:
            for bonus_value, bonus_type in zip(item.bonus_value, item.bonus_type):
                

                

                if bonus_type == 'hp':
                    self.max_health += self.max_health * bonus_value
                if bonus_type == 'hp flat':
                    self.max_health += bonus_value
                if bonus_type == 'mana':
                    self.max_mana += self.max_mana * bonus_value
                if bonus_type == 'mana flat':
                    self.max_mana += bonus_value
                if bonus_type == 'atk':
                    self.basic_attack_damage += self.basic_attack_damage * bonus_value
                if bonus_type == 'atk flat':
                    self.basic_attack_damage += bonus_value
                

        # print(self.basic_attack_damage)

        # self.max_health = self.strength * self.str_mult
        # self.health = self.max_health
        # self.max_mana = self.intelligence * self.int_mult
        # self.mana = self.max_mana
        # self.basic_attack_damage = self.agility * self.agi_mult

    # def apply_item_bonuses(self):
    #     for item in self.items:
    #         for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
    #             if bonus_type == "hp":  # Percentage-based health bonus
    #                 self.max_health += self.max_health * bonus_value
    #                 self.health = self.max_health  # Update current health to match max health
    #             elif bonus_type == "hp_flat":  # Flat health bonus
    #                 self.max_health += bonus_value
    #                 self.health = self.max_health
    #             elif bonus_type == "mana":  # Percentage-based mana bonus
    #                 self.max_mana += self.max_mana * bonus_value
    #                 self.mana = self.max_mana  # Update current mana to match max mana
    #             elif bonus_type == "mana_flat":  # Flat mana bonus
    #                 self.max_mana += bonus_value
    #                 self.mana = self.max_mana
    #             elif bonus_type == "atk":  # Percentage-based attack bonus
    #                 self.basic_attack_damage += self.basic_attack_damage * bonus_value
    #             elif bonus_type == "atk_flat":  # Flat attack bonus
    #                 self.basic_attack_damage += bonus_value

    # Documentation

        # # First, gather primary stat bonuses
        # str_bonus = 0
        # int_bonus = 0
        # agi_bonus = 0

        # # First pass: apply percentage and flat bonuses to primary stats
        # for item in self.items:
        #     for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
        #         if bonus_type == "str":
        #             str_bonus += self.strength * bonus_value
        #         elif bonus_type == "str_flat":
        #             str_bonus += bonus_value
        #         elif bonus_type == "int":
        #             int_bonus += self.intelligence * bonus_value
        #         elif bonus_type == "int_flat":
        #             int_bonus += bonus_value
        #         elif bonus_type == "agi":
        #             agi_bonus += self.agility * bonus_value
        #         elif bonus_type == "agi_flat":
        #             agi_bonus += bonus_value

        # # Apply stat bonuses
        # self.strength += str_bonus
        # self.intelligence += int_bonus
        # self.agility += agi_bonus

        # # Recalculate derived stats based on new primary stats
        # self.max_health = self.strength * self.str_mult
        # self.max_mana = self.intelligence * self.int_mult
        # self.basic_attack_damage = self.agility * self.agi_mult
        # self.health = self.max_health
        # self.mana = self.max_mana

        # # Second pass: apply derived stat bonuses
        # for item in self.items:
        #     for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
        #         if bonus_type == "hp":
        #             self.max_health += self.max_health * bonus_value
        #             self.health = self.max_health
        #         elif bonus_type == "hp_flat":
        #             self.max_health += bonus_value
        #             self.health = self.max_health
        #         elif bonus_type == "mana":
        #             self.max_mana += self.max_mana * bonus_value
        #             self.mana = self.max_mana
        #         elif bonus_type == "mana_flat":
        #             self.max_mana += bonus_value
        #             self.mana = self.max_mana
        #         elif bonus_type == "atk":
        #             self.basic_attack_damage += self.basic_attack_damage * bonus_value
        #         elif bonus_type == "atk_flat":
        #             self.basic_attack_damage += bonus_value

    '''
    Image Loading Function Reference
    Each function loads a sequence of .png images from a specified folder, applies optional scaling and rotation, and returns a list of Pygame surfaces (frames). Use the correct function depending on the numbering format and modifications like flipping or rotating.

    📁 1. Basic Numbering (1.png, 2.png, 3.png, etc.)
    load_img_frames(folder, count, starts_at_zero=False, size=1)
    Use for: Simple numbered files like Attack_1_1.png, Attack_1_2.png, ...

    Modifiers: 🔹Scale only

    load_img_frames_rotate(folder, count, starts_at_zero=False, size=1, rotate=0)
    Same as above but adds 🔄 rotation

    load_img_frames_flipped(folder, count, starts_at_zero=False, size=1)
    Same as load_img_frames, but applies a horizontal 🔁 flip

    load_img_frames_flipped_rotate(folder, count, starts_at_zero=False, size=1, rotate=0)
    Combination of flipping + rotation

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\characters\Fire wizard\slash pngs\Attack_1_"
    frames = load_img_frames(folder, 9)
    🔢 2. Padded Numbering (01.png, 02.png, 03.png, etc.)
    load_img_frames_numbering_method_simple(folder, count, starts_at_zero=False, size=1)
    Use for: Padded filenames like 00.png, 01.png, ...

    Path format: folder + '01.png'

    Windows/Mac compatible path format

    load_img_frames_numbering_method(folder, count, starts_at_zero=False, size=1)
    Same as above, but forces backslash \ in path (Windows-specific)

    Path format: folder\01.png

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\attacks\fire wizard\atk2\"
    frames = load_img_frames_numbering_method_simple(folder, 5)
    🧱 3. Tile Format (tile000.png, tile001.png, ...)
    load_img_frames_tile_method(folder, count, starts_at_zero=False, size=1)
    Use for: tile000.png, tile001.png, ...

    Applies scale and returns frames

    Stops if file is not found

    load_img_frames_flipped_tile_method(folder, count, starts_at_zero=False, size=1)
    Same as above, but applies a horizontal 🔁 flip

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\attacks\fire wizard\atk1\"
    frames = load_img_frames_tile_method(folder, 10)
    📝 Notes
    count is the number of frames you want to load.

    starts_at_zero=True will start from 0, otherwise starts from 1.

    size=1 means no scaling (1.5 means 150% size, 0.5 means half size).

    rotate=0 means no rotation (positive = clockwise, negative = counterclockwise).

    Use raw string (r"your\path") or double backslashes ("your\\path") to avoid issues on Windows.

    '''



    def load_img_frames(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        '''
        images = []
        for i in range(count):
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    def load_img_frames_rotate(self, folder, count, starts_at_zero=False, size=1, rotate=0):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same, add rotate
        images = []
        for i in range(count):
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images
    
    def load_img_frames_numbering_method_simple(self, folder, count, starts_at_zero=False, size=1, rotate=0, flip=False):
        '''
        assets\attacks\fire wizard\atk2\01.png
        assets\attacks\fire wizard\atk2\02.png
        '''
        images = []
        for i in range(count):
            frame_number = i + (0 if starts_at_zero else 1)
            # 01 02
            img_path = (fr'{folder}{str(frame_number).zfill(2)}.png')
            # print(img_path)
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), flip, False)
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images
    
    def load_img_frames_numbering_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk2\01.png
        ''' #same but force backslash
        images = []
        for i in range(count):
            frame_number = i + (0 if starts_at_zero else 1)
            # \01 \02
            img_path = (fr'{folder}\{str(frame_number).zfill(2)}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    
    def load_img_frames_flipped(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same but rotate flip
        images = []
        for i in range(count):
            # 1 2 3
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    def load_img_frames_flipped_rotate(self, folder, count, starts_at_zero=False, size=1, rotate=0):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same but rotate flip
        images = []
        for i in range(count):
            # 1 2 3
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images

    def load_img_frames_tile_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk1\tile000.png
        assets\attacks\fire wizard\atk1\tile001.png
        '''
        images = []
        for i in range(count):
            # Generate zero-padded file name (e.g., 0010)
            frame_number = i + (0 if starts_at_zero else 1)
            img_path = fr"{folder}\tile{frame_number:03d}.png"  # Zero-pad to 4 digits
            try:
                image = pygame.image.load(img_path).convert_alpha()
                image = pygame.transform.rotozoom(image, 0, size)
                images.append(image)
            except FileNotFoundError:
                print(f"File not found: {img_path}")
                break
        return images
    
    def load_img_frames_flipped_tile_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk1\tile000.png
        assets\attacks\fire wizard\atk1\tile001.png
        ''' # same but flip
        images = []
        for i in range(count):
            # Generate zero-padded file name (e.g., 0010)
            frame_number = i + (0 if starts_at_zero else 1)
            img_path = fr"{folder}\tile{frame_number:03d}.png"  # Zero-pad to 4 digits
            try:
                image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
                image = pygame.transform.rotozoom(image, 0, size)
                images.append(image)
            except FileNotFoundError:
                print(f"File not found: {img_path}")
                break
        return images
    
    def load_attack_class(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0, frame_duration=30):
        spritesheet = pygame.image.load(filepath).convert_alpha()
        spritesheet_width = spritesheet.get_width()
        spritesheet_height = spritesheet.get_height()
        # Debugging: Print the spritesheet dimensions and frame dimensions
        # print(f"Spritesheet size: {spritesheet_width}x{spritesheet_height}")
        calculated_frame_width = spritesheet_width // columns
        calculated_frame_height = spritesheet_height // rows
        # print(f"Calculated frame size: {calculated_frame_width}x{calculated_frame_height}")
        # Check if the provided frame dimensions match the calculated ones
        if frame_width != calculated_frame_width or frame_height != calculated_frame_height:
            # print(
            #     f"Warning: Provided frame dimensions ({frame_width}x{frame_height}) "
            #     f"do not match calculated dimensions ({calculated_frame_width}x{calculated_frame_height})."
            # )
            frame_width = calculated_frame_width
            frame_height = calculated_frame_height

        spritesheet = SpriteSheet(filepath, frame_width, frame_height, rows, columns, scale, rotation)
        frames = spritesheet.get_frames()
        return frames
    
    def animate(self, frames, index, loop=True, basic_atk=False):
        current_time = pygame.time.get_ticks()
        #print(f"{self.__class__.__name__} animation speed: {self.basic_attack_animation_speed}")
        frame_duration = self.default_animation_speed if not self.basic_attacking else self.basic_attack_animation_speed
        #print(f"Animation type: {'basic' if self.basic_attacking else 'default'}, Duration: {frame_duration}")
        if current_time - self.last_atk_time > frame_duration:
            self.last_atk_time = current_time
            self.image = frames[int(index)]
            index += 1
            #print(basic_atk)
            if index >= len(frames):
                if loop:
                    index = 0  # Restart the animation
                else:
                    index = len(frames) - 1  # Stay on the last frame
                    return index, False  # Animation finished
        return index, True  # Animation still active
    
    def jump_animation(self):
        if self.facing_right:
            self.player_jump_index, _ = self.animate(self.player_jump, self.player_jump_index, loop=False)
        else:
            self.player_jump_index_flipped, _ = self.animate(self.player_jump_flipped, self.player_jump_index_flipped, loop=False)
        
        self.last_atk_time -= DEFAULT_ANIMATION_SPEED_FOR_JUMPING  # Animation Speed Reduced

    def simple_idle_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_idle_index, _ = self.animate(self.player_idle, self.player_idle_index, loop=True)
        else:
            self.player_idle_index_flipped, _ = self.animate(self.player_idle_flipped, self.player_idle_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
        
    def run_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_run_index, _ = self.animate(self.player_run, self.player_run_index, loop=True)
        else:
            self.player_run_index_flipped, _ = self.animate(self.player_run_flipped, self.player_run_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
        
    def atk1_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk1_index, self.attacking1 = self.animate(self.player_atk1, self.player_atk1_index, loop=False)
        else:
            self.player_atk1_index_flipped, self.attacking1 = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def atk2_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk2_index, self.attacking2 = self.animate(self.player_atk2, self.player_atk2_index, loop=False)
        else:
            self.player_atk2_index_flipped, self.attacking2 = self.animate(self.player_atk2_flipped, self.player_atk2_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def atk3_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk3_index, self.attacking3 = self.animate(self.player_atk3, self.player_atk3_index, loop=False)
        else:
            self.player_atk3_index_flipped, self.attacking3 = self.animate(self.player_atk3_flipped, self.player_atk3_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def sp_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_sp_index, self.sp_attacking = self.animate(self.player_sp, self.player_sp_index, loop=False)
        else:
            self.player_sp_index_flipped, self.sp_attacking = self.animate(self.player_sp_flipped, self.player_sp_index_flipped, loop=False)

        self.last_atk_time -= animation_speed

    def basic_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_basic_index, self.basic_attacking = self.animate(self.player_basic, self.player_basic_index, loop=False, basic_atk=True)
        else:
            self.player_basic_index_flipped, self.basic_attacking = self.animate(self.player_basic_flipped, self.player_basic_index_flipped, loop=False, basic_atk=True)

        self.last_atk_time -= animation_speed

        
    def play_death_animation(self):
        if self.is_dead():
            if self.facing_right:
                # Play normal death animation for facing right
                if self.player_death_index < len(self.player_death):  # If animation is still ongoing
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_atk_time > 140:  # Adjust frame duration as needed
                        self.last_atk_time = current_time
                        self.image = self.player_death[self.player_death_index]
                        self.player_death_index += 1
                else:
                    # Display the last frame of the death animation
                    self.image = self.player_death[-1]
            else:
                # Play flipped death animation for facing left
                if self.player_death_index < len(self.player_death_flipped):  # If animation is still ongoing
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_atk_time > 140:  # Adjust frame duration as needed
                        self.last_atk_time = current_time
                        self.image = self.player_death_flipped[self.player_death_index]
                        self.player_death_index += 1
                else:
                    # Display the last frame of the flipped death animation
                    self.image = self.player_death_flipped[-1]
                    
    def player_status(self, health, mana, special):
        font = pygame.font.Font(r'assets\font\slkscr.ttf', 20)

        # Re-declaring the values
        self.health = health
        self.mana = mana
        self.special = special

        # Color Definitions
        dark_red = 'darkred'  # Dark Red
        crimson = 'crimson'  # Crimson Red
        dark_olive_green = 'chartreuse'  # Dark Olive Green
        dim_gray = 'gray20'  # Dim Gray for decor

        if self.player_type == 1:
            self.health_bar_p1 = pygame.Rect(101, 150, self.health, 20)
            self.health_bar_p1_after = pygame.Rect(101, 150, self.white_health_p1, 20)
            self.mana_bar_p1 = pygame.Rect(101, 150+50, self.mana, 20)
            self.mana_bar_p1_after = pygame.Rect(101, 150+50, self.white_mana_p1, 20)

            self.special_bar_p1 = pygame.Rect(101, 125, self.special, 10)

            # Recalculate mana decor width based on max mana
            self.hpdecor_end_p1 = self.max_health + 10
            self.manadecor_end_p1 = self.max_mana + 10  # Fixing mana decor width based on max mana

            self.hp_decor_p1 = pygame.Rect(96, 145, self.hpdecor_end_p1, 30)
            self.mana_decor_p1 = pygame.Rect(96, 145 + 50, self.manadecor_end_p1, 30)  # Fixed width for mana decor

            self.special_decor_p1 = pygame.Rect(96, 145 - 25, self.max_special + 10, 20)

            # White rects
            if self.health < self.white_health_p1:
                self.white_health_p1 -= WHITE_BAR_SPEED_HP
            if self.health > self.white_health_p1:
                self.white_health_p1 += WHITE_BAR_SPEED_HP
            if self.mana < self.white_mana_p1:
                self.white_mana_p1 -= WHITE_BAR_SPEED_MANA
            if self.mana > self.white_mana_p1:
                self.white_mana_p1 += WHITE_BAR_SPEED_MANA

            # Health limit
            if self.health > self.max_health:
                self.health = self.max_health
            # Mana limit
            if self.mana > self.max_mana:
                self.mana = self.max_mana

            if self.special > self.max_special:
                self.special = self.max_special
            
            if self.special < 0:
                self.special = 0

            # Health and Mana Text Color Change
            # Health color logic based on percentage
            if self.health < (self.max_health * 0.2):  # Below 20%
                health_color = crimson
                bar_color = crimson
                fill_color = white
            elif self.health < (self.max_health * 0.4):  # Below 40%
                health_color = (255,200,200)
                bar_color = dark_olive_green  # Slight mix of green and dark red
                fill_color = dark_red
            else:  # Above 40%
                health_color = white
                bar_color = green
                fill_color = red

            mana_color = red if self.mana < self.lowest_mana_cost else white

            if self.special == self.max_special:
                special_color = 'purple'
            elif self.special_active:
                special_color = 'blue'
            else:
                special_color = 'yellow'

            # Health and Mana Text
            self.health_display_text_p1 = font.render(f'[{int(self.health)}]', TEXT_ANTI_ALIASING, health_color)
            self.mana_display_text_p1 = font.render(f'[{int(self.mana)}]', TEXT_ANTI_ALIASING, mana_color)

            self.special_display_text_p1 = font.render(f'[{int(self.special)}]', TEXT_ANTI_ALIASING, special_color)

            # Blit Texts
            screen.blit(self.health_display_text_p1, (
                self.hp_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.hp_decor_p1.top + (self.hp_decor_p1.height // 2 - self.health_display_text_p1.get_height() // 2)
                ))

            screen.blit(self.mana_display_text_p1, (
                self.mana_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.mana_decor_p1.top + (self.mana_decor_p1.height // 2 - self.mana_display_text_p1.get_height() // 2)
                ))
            
            screen.blit(self.special_display_text_p1, (
                self.special_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.special_decor_p1.top + (self.special_decor_p1.height // 2 - self.health_display_text_p1.get_height() // 2)
                ))

            # Draw Rects
            pygame.draw.rect(screen, dim_gray, self.hp_decor_p1)  # Slightly brighter decor color
            pygame.draw.rect(screen, fill_color, self.health_bar_p1_after)  # Design when hp is low
            pygame.draw.rect(screen, bar_color, self.health_bar_p1)  # Design when hp is low   

            pygame.draw.rect(screen, dim_gray, self.mana_decor_p1)  # Decor
            pygame.draw.rect(screen, white, self.mana_bar_p1_after)  # Design when mana is low
            pygame.draw.rect(screen, cyan2, self.mana_bar_p1)  # Design when mana is low

            pygame.draw.rect(screen, dim_gray, self.special_decor_p1)
            pygame.draw.rect(screen, special_color, self.special_bar_p1)


        elif self.player_type == 2:
            # Start positions aligned to the right
            self.hpdecor_end_p2 = self.max_health + 10
            self.manadecor_end_p2 = self.max_mana + 10  # Fixing mana decor width based on max mana

            self.specialdecor_end_p2 = self.max_special + 10




            self.healthdecor_p2_starting = width - self.hpdecor_end_p2 - 96
            self.manadecor_p2_starting = width - self.manadecor_end_p2 - 96

            self.specialdecor_p2_starting = width - self.specialdecor_end_p2 - 96

            # Decorations
            self.hp_decor_p2 = pygame.Rect(self.healthdecor_p2_starting, 145, self.hpdecor_end_p2, 30)
            self.mana_decor_p2 = pygame.Rect(self.manadecor_p2_starting, 195, self.manadecor_end_p2, 30)  # Fixed width for mana decor

            self.special_decor_p2 = pygame.Rect(self.specialdecor_p2_starting, 145 - 25, self.specialdecor_end_p2, 20)

            # Adjust bar starting x-position to align inside the decor with a 5px padding
            bar_x_start = self.hp_decor_p2.left + 5
            hp_bar_max_width = self.hp_decor_p2.width - 10  # Width of the decor minus padding
            mana_bar_max_width = self.mana_decor_p2.width - 10

            special_bar_max_width = self.special_decor_p2.width - 10


            # Calculate dynamic bar widths based on percentage of current value
            self.health_bar_p2_width = int((self.health / self.max_health) * hp_bar_max_width)
            self.white_health_p2_width = int((self.white_health_p2 / self.max_health) * hp_bar_max_width)

            self.special_bar_p2_width = int((self.special / self.max_special) * special_bar_max_width)

            self.mana_bar_p2_width = int((self.mana / self.max_mana) * mana_bar_max_width)
            self.white_mana_p2_width = int((self.white_mana_p2 / self.max_mana) * mana_bar_max_width)

            # Health and Mana Rects (bars should start from right side and shrink towards left)
            self.health_bar_p2 = pygame.Rect(self.hp_decor_p2.right - self.health_bar_p2_width - 5, 150, self.health_bar_p2_width, 20)
            self.health_bar_p2_after = pygame.Rect(self.hp_decor_p2.right - self.white_health_p2_width - 5, 150, self.white_health_p2_width, 20)

            self.mana_bar_p2 = pygame.Rect(self.mana_decor_p2.right - self.mana_bar_p2_width - 5, 200, self.mana_bar_p2_width, 20)
            self.mana_bar_p2_after = pygame.Rect(self.mana_decor_p2.right - self.white_mana_p2_width - 5, 200, self.white_mana_p2_width, 20)


            self.special_bar_p2 = pygame.Rect(self.special_decor_p2.right - self.special_bar_p2_width - 5, 125, self.special_bar_p2_width, 10)

            

            # White rects update logic
            if self.health > self.white_health_p2:
                self.white_health_p2 += WHITE_BAR_SPEED_HP
            if self.health < self.white_health_p2:
                self.white_health_p2 -= WHITE_BAR_SPEED_HP
            if self.mana > self.white_mana_p2:
                self.white_mana_p2 += WHITE_BAR_SPEED_MANA
            if self.mana < self.white_mana_p2:
                self.white_mana_p2 -= WHITE_BAR_SPEED_MANA

            # # Limits
            # self.health = min(self.health, self.max_health)
            # self.mana = min(self.mana, self.max_mana)

            # self.special = min(self.special, self.max_special)

            # Health limit
            if self.health > self.max_health:
                self.health = self.max_health
            # Mana limit
            if self.mana > self.max_mana:
                self.mana = self.max_mana

            if self.special > self.max_special:
                self.special = self.max_special
            
            if self.special < 0:
                self.special = 0

            # Texts
            if self.health < (self.max_health * 0.2):  # Below 20%
                health_color_p2 = crimson
                bar_color_p2 = crimson
                fill_color_p2 = white
            elif self.health < (self.max_health * 0.4):  # Below 40%
                health_color_p2 = (255,200,200)
                bar_color_p2 = dark_olive_green  # Slight mix of green and dark red
                fill_color_p2 = dark_red
            else:  # Above 40%
                health_color_p2 = white
                bar_color_p2 = green
                fill_color_p2 = red

            mana_color_p2 = red if self.mana < self.lowest_mana_cost else white

            if self.special == self.max_special:
                special_color_p2 = 'purple'
            elif self.special_active:
                special_color_p2 = 'blue'
            else:
                special_color_p2 = 'yellow'

            self.health_display_text_p2 = font.render(f'[{int(self.health)}]', TEXT_ANTI_ALIASING, health_color_p2)
            self.mana_display_text_p2 = font.render(f'[{int(self.mana)}]', TEXT_ANTI_ALIASING, mana_color_p2)

            self.special_display_text_p2 = font.render(f'[{int(self.special)}]', TEXT_ANTI_ALIASING, special_color_p2)

            

            # Blit Texts
            screen.blit(self.health_display_text_p2, (
                self.hp_decor_p2.left - self.health_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.hp_decor_p2.top + (self.hp_decor_p2.height // 2 - self.health_display_text_p2.get_height() // 2)
            ))
            screen.blit(self.mana_display_text_p2, (
                self.mana_decor_p2.left - self.mana_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.mana_decor_p2.top + (self.mana_decor_p2.height // 2 - self.mana_display_text_p2.get_height() // 2)
            ))

            screen.blit(self.special_display_text_p2, (
                self.special_decor_p2.left - self.special_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.special_decor_p2.top + (self.special_decor_p2.height // 2 - self.health_display_text_p2.get_height() // 2)
            ))

            

            # Draw Rects
            pygame.draw.rect(screen, dim_gray, self.hp_decor_p2)
            pygame.draw.rect(screen, fill_color_p2, self.health_bar_p2_after)
            pygame.draw.rect(screen, bar_color_p2, self.health_bar_p2)

            pygame.draw.rect(screen, dim_gray, self.mana_decor_p2)
            pygame.draw.rect(screen, white, self.mana_bar_p2_after)
            pygame.draw.rect(screen, cyan2, self.mana_bar_p2)

            pygame.draw.rect(screen, dim_gray, self.special_decor_p2)
            pygame.draw.rect(screen, special_color_p2, self.special_bar_p2)

        # Variables are outside the class
        # Health and Mana Icon Draw
        # screen.blit(hp_icon, hp_icon_p1_rect)
        # screen.blit(hp_icon, hp_icon_p2_rect)
        # screen.blit(mana_icon, mana_icon_p1_rect)
        # screen.blit(mana_icon, mana_icon_p2_rect)

        if self.health <= 0:
            self.health = 0
            self.winner = 2 if self.player_type == 1 else 1

            return self.winner
    
    # Don't forget to have input method on the players since their attacks are specific :))
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey):
        pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')
                

            # if skill_1_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking1 = True
            # if skill_2_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking2 = True
            # if skill_3_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking3 = True
            # if skill_4_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.sp_attacking = True


    def is_skill_clicked(self, mouse_pos, mana):
        """
        Checks if a skill rect is clicked and if the player has enough mana.

        Args:
            mouse_pos (tuple): The current mouse position.
            mana (int): The player's current mana.

        Returns:
            int: The index of the clicked skill, or -1 if no skill is clicked or not enough mana.
        """
        for i, rect in enumerate(self.rects):
            if (rect.collidepoint(mouse_pos)):
                if mana >= self.mana_costs[i]:
                    return i
                else:
                    print("Not enough mana!")
                    return -1
        return -1

    def take_damage(self, damage):
        if self.is_dead():
            return
        if self.damage_reduce > 0:
            damage -= (damage * self.damage_reduce)
        self.health = max(0, self.health - damage)  # Ensure health doesn't go below 0
        # print(f"THIS PLAYER took {damage} damage. Current health: {self.health}")

        if self.health <= 0:
            self.die()  # Trigger the death process
            self.play_death_animation()  # Play death animation

    def take_mana(self, mana):
        self.mana = max(0, self.mana - mana)  # Ensure health doesn't go below 0
        # print(f"THIS PLAYER took {damage} damage. Current health: {self.health}")

    def is_dead(self):
        return hasattr(self, "health") and self.health <= LITERAL_HEALTH_DEAD
    
    def take_heal(self,heal):
        if self.is_dead():
            return
        self.health = max(0, self.health + heal)

    def take_special(self, amount):
        if self.is_dead():
            return
        if self.special_increase > 0:
            amount += (amount * self.special_increase)
        self.special = max(0, self.special + amount)

    def draw_distance(self, enemy): # self.enemy_distance = int(abs(self.player.x_pos - self.x_pos))
        font = pygame.font.Font(r'assets\font\slkscr.ttf', 20)
        enemy_distance = int(abs(self.x_pos - enemy.x_pos))
        enemy_distance_surf = font.render(str(enemy_distance), TEXT_ANTI_ALIASING, 'Red')
        screen.blit(enemy_distance_surf, (self.x_pos, self.y_pos - 120))
        line_rect = pygame.rect.Rect((self.x_pos if enemy.x_pos > self.x_pos else enemy.x_pos), self.y_pos - 60, enemy_distance, 2)
        pygame.draw.rect(screen, 'Red', line_rect)
    
    def stun(self, stunned, x_pos, y_pos, adjust_y_pos, jump_force=DEFAULT_JUMP_FORCE, gravity=DEFAULT_GRAVITY):
        if stunned:
            self.jumping = True
            self.y_pos = y_pos - adjust_y_pos
            self.x_pos = x_pos

            # I give up stunned stops attacking from magician, i will just not make it not attack while jumping
            # self.stunned = True
            # print(self.y_pos - DEFAULT_Y_POS)
            
            # if self.y_pos - DEFAULT_Y_POS <= 10:
            #     self.stunned = False



            # self.y_velocity = y_pos

            return True if stunned else False
            # self.jump_animation()
        

    
    def draw_hp(self):
        pass

    def die(self):
        if not self.is_dead():  # Check if the player is already dead
            self.health = 0  # Ensure the health is set to 0 when dying
            self.winner = 2 if self.player_type == 1 else 1  # Set the winner

    def move_to_screen(self): # drag the player when out of bounds
        # print('asd')
        if self.x_pos > width:
            self.x_pos -= 3
        if self.x_pos < 0:
            self.x_pos += 3
        
    def update(self):
        self.keys = pygame.key.get_pressed()
        self.input(
            (self.keys[pygame.K_z]) if self.player_type == 1 else (self.keys[pygame.K_u]), 
            (self.keys[pygame.K_x]) if self.player_type == 1 else (self.keys[pygame.K_i]), 
            (self.keys[pygame.K_c]) if self.player_type == 1 else (self.keys[pygame.K_o]), 
            (self.keys[pygame.K_v]) if self.player_type == 1 else (self.keys[pygame.K_p]),

            (self.keys[pygame.K_d]) if self.player_type == 1 else (self.keys[pygame.K_RIGHT]),
            (self.keys[pygame.K_a]) if self.player_type == 1 else (self.keys[pygame.K_LEFT]),
            (self.keys[pygame.K_w]) if self.player_type == 1 else (self.keys[pygame.K_UP])
            )
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation()
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation()
        else:
            self.simple_idle_animation()

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        # Update the hitbox position
        self.update_hitbox()
        self.draw_hitbox(screen)

        # Draw skill icons
        for attack in self.attacks:
            attack.draw_skill_icon(screen, self.mana)

        for mana in self.attacks:
            mana.draw_mana_cost(screen, self.mana)

        # Update the player status (health and mana bars)
        self.player_status(self.health, self.mana)

        # Update the health and mana bars
        if self.health != 0:
            self.mana += DEFAULT_MANA_REGENERATION
            self.health += DEFAULT_HEALTH_REGENERATION
        else:
            self.health = 0

        

        
        # self.draw_hitbox(screen)

        




        # PLAYER SPECIFIC UPDATES

        # SAMPLE APPLY ITEM CONSUMABLE:
        if self.keys[pygame.K_1]:  # Example: Use the first item
            if self.items:
                item = self.items.pop(0)  # Remove the used item
                if item.bonus_type == "hp":
                    self.health = min(self.max_health, self.health + item.bonus_value)
                elif item.bonus_type == "mana":
                    self.mana = min(self.max_mana, self.mana + item.bonus_value)
                elif item.bonus_type == "atk":
                    self.attack_power += item.bonus_value

        # DISPLAY ITEM ICONS

        for i, item in enumerate(self.items):
            screen.blit(item.image, (50 + i * 60, 250))  # Adjust position as needed


        self.die()

        

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)


