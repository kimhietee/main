import pygame
import random
from global_vars import (
    width, height, icon, FPS, clock, screen, hero1, hero2,
    white, red, black, green, cyan2, gold,
    DEFAULT_WIDTH, DEFAULT_HEIGHT,
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

from player import Player
from attack import Attack_Display, Attacks
from sprite_loader import load_attack, load_attack_flipped
from player_selector import PlayerSelector
# from gameloop import hero1, hero2



# Animation Counts
FIRE_WIZARD_JUMP_COUNT = 6
FIRE_WIZARD_RUN_COUNT = 8 
FIRE_WIZARD_IDLE_COUNT = 7
FIRE_WIZARD_ATK1_COUNT = 8
FIRE_WIZARD_SP_COUNT = 14
FIRE_WIZARD_DEATH_COUNT = 6

FIRE_WIZARD_ATK1 = 12 - 2 # reduce frame
FIRE_WIZARD_ATK2 = 53
FIRE_WIZARD_ATK3 = 34
FIRE_WIZARD_SP = 28
# ---------------------
# print((FIRE_WIZARD_ATK2 * 0.01) * 4 * 5)
FIRE_WIZARD_ATK1_MANA_COST = 60
FIRE_WIZARD_ATK2_MANA_COST = 80
FIRE_WIZARD_ATK3_MANA_COST = 110
FIRE_WIZARD_SP_MANA_COST = 180

FIRE_WIZARD_ATK1_SIZE = 3
FIRE_WIZARD_ATK2_SIZE = 0.3
FIRE_WIZARD_ATK3_SIZE = 0.3
FIRE_WIZARD_SP_SIZE = 1.3

FIRE_WIZARD_ATK1_COOLDOWN = 10000
FIRE_WIZARD_ATK2_COOLDOWN = 5000 + 13000
FIRE_WIZARD_ATK3_COOLDOWN = 25000
FIRE_WIZARD_SP_COOLDOWN = 40000

FIRE_WIZARD_ATK1_DAMAGE = 16
FIRE_WIZARD_ATK2_DAMAGE = 0.03 # 20 total if ur in the center
FIRE_WIZARD_ATK3_DAMAGE = 0.125# 21 
FIRE_WIZARD_SP_DAMAGE = 0.375 # 52
print(FIRE_WIZARD_ATK3_DAMAGE)
dmg_mult = 0.05
FIRE_WIZARD_ATK1_DAMAGE = FIRE_WIZARD_ATK1_DAMAGE + (FIRE_WIZARD_ATK1_DAMAGE * dmg_mult)
FIRE_WIZARD_ATK2_DAMAGE = FIRE_WIZARD_ATK2_DAMAGE + (FIRE_WIZARD_ATK2_DAMAGE * dmg_mult)
FIRE_WIZARD_ATK3_DAMAGE = FIRE_WIZARD_ATK3_DAMAGE + (FIRE_WIZARD_ATK3_DAMAGE * dmg_mult)
FIRE_WIZARD_SP_DAMAGE = FIRE_WIZARD_SP_DAMAGE + (FIRE_WIZARD_SP_DAMAGE * dmg_mult)

class Fire_Wizard(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type # 1 for player 1, 2 for player 2

        # Base Stats
        self.max_health = 200
        self.max_mana = 200
        self.health = self.max_health
        self.mana = self.max_mana

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        # Player Animation Source
        jump_ani = [r'HERO FIGHTING\assets\characters\Fire wizard\jump pngs\Jump_', FIRE_WIZARD_JUMP_COUNT, 1]
        run_ani = [r'HERO FIGHTING\assets\characters\Fire wizard\run pngs\Run_', FIRE_WIZARD_RUN_COUNT, 1]
        idle_ani= [r'HERO FIGHTING\assets\characters\Fire wizard\idle pngs\image_0-', FIRE_WIZARD_IDLE_COUNT, 1]
        atk1_ani= [r'HERO FIGHTING\assets\characters\Fire wizard\fireball pngs\image_0-', FIRE_WIZARD_ATK1_COUNT, 1]
        sp_ani= [r'HERO FIGHTING\assets\characters\Fire wizard\flame jet pngs\image_0-', FIRE_WIZARD_SP_COUNT, 1]
        death_ani= [r'HERO FIGHTING\assets\characters\Fire wizard\dead\tile00', FIRE_WIZARD_DEATH_COUNT, 1]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire_wizard\fire-sound-efftect-21991.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3')
        self.sp_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire_wizard\052168_huge-explosion-85199.mp3')
        self.atk1_sound.set_volume(0.5)
        self.atk2_sound.set_volume(0.1)
        self.atk3_sound.set_volume(0.5)
        self.sp_sound.set_volume(0.5)

        # Player Skill Animations Source
        atk1 = [r'HERO FIGHTING\assets\attacks\fire wizard\atk1', FIRE_WIZARD_ATK1, 1]
        atk2 = [r'HERO FIGHTING\assets\attacks\fire wizard\atk2', FIRE_WIZARD_ATK2, 1]
        atk3 = [r'HERO FIGHTING\assets\attacks\fire wizard\atk3\png_', FIRE_WIZARD_ATK3, 1]
        sp = [r'HERO FIGHTING\assets\attacks\fire wizard\sp atk', FIRE_WIZARD_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'PYTHON WITH KIM  NEW!\skill_icons\FireballIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire_wizard\GlyphOfFireIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire_wizard\RodOfPower29Icon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire_wizard\MeteorIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = self.load_img_frames_tile_method(atk1[0], atk1[1], atk1[2], FIRE_WIZARD_ATK1_SIZE)
        self.atk1_flipped = self.load_img_frames_flipped_tile_method(atk1[0], atk1[1], atk1[2], FIRE_WIZARD_ATK1_SIZE)
        self.atk2 = self.load_img_frames_numbering_method(atk2[0], atk2[1], atk2[2], FIRE_WIZARD_ATK2_SIZE)
        self.atk3 = self.load_img_frames_numbering_method_simple(atk3[0], atk3[1], atk3[2], FIRE_WIZARD_ATK3_SIZE)
        self.sp = self.load_img_frames_numbering_method(sp[0], sp[1], sp[2], FIRE_WIZARD_SP_SIZE)

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)  
        self.player_atk2 = self.player_atk1
        self.player_atk2_flipped = self.player_atk1_flipped
        self.player_atk3 = self.player_atk1
        self.player_atk3_flipped = self.player_atk1_flipped
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            FIRE_WIZARD_ATK1_MANA_COST,
            FIRE_WIZARD_ATK2_MANA_COST,
            FIRE_WIZARD_ATK3_MANA_COST,
            FIRE_WIZARD_SP_MANA_COST
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=FIRE_WIZARD_ATK1_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=FIRE_WIZARD_ATK2_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=FIRE_WIZARD_ATK3_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=FIRE_WIZARD_SP_COOLDOWN,
                mana=self.mana
            )
        ]

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not self.is_dead():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += self.speed
                    if self.x_pos > width+50 - (self.rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = width+50 - (self.rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= self.speed
                    if self.x_pos < (0-50 + (self.rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (0-50 + (self.rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = DEFAULT_JUMP_FORCE  
                    self.last_atk_time = current_time  # Update the last jump time

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity

        # Stop at the ground level
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False 
        if self.y_pos > DEFAULT_Y_POS - JUMP_LOGIC_EXECUTE_ANIMATION:
            self.player_jump_index = 0
            self.player_jump_index_flipped = 0
            
            
        if not self.jumping and not self.is_dead():
            if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= FIRE_WIZARD_ATK1_MANA_COST and self.attacks[0].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx - 20 if self.facing_right else self.rect.centerx + 20,
                        y=self.rect.centery + 30,
                        frames=self.atk1 if self.facing_right else self.atk1_flipped,
                        frame_duration=100,
                        repeat_animation=1,
                        speed=3.5 if self.facing_right else -3.5,
                        dmg=FIRE_WIZARD_ATK1_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_WIZARD_ATK1_MANA_COST
                    self.attacks[0].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    self.atk1_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 1 used')


            elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= FIRE_WIZARD_ATK2_MANA_COST and self.attacks[1].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                        attack = Attack_Display(
                            x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk2,
                            frame_duration=50,
                            repeat_animation=4,
                            speed=5 if self.facing_right else -5,
                            dmg=FIRE_WIZARD_ATK2_DAMAGE,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=False) # Replace with the target
                        attack_display.add(attack)
                    self.mana -= FIRE_WIZARD_ATK2_MANA_COST
                    self.attacks[1].last_used_time = current_time
                    self.running = False
                    self.attacking2 = True
                    self.player_atk2_index = 0
                    self.player_atk2_index_flipped = 0
                    self.atk2_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 2 used')

            elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking:
                if self.mana >= FIRE_WIZARD_ATK3_MANA_COST and self.attacks[2].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                        y=self.rect.centery + 30,
                        frames=self.atk3,
                        frame_duration=60,
                        repeat_animation=3,
                        speed=0.5 if self.facing_right else -0.5,
                        dmg=FIRE_WIZARD_ATK3_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False,
                        continuous_dmg=False) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_WIZARD_ATK3_MANA_COST
                    self.attacks[2].last_used_time = current_time
                    self.running = False
                    self.attacking3 = True
                    self.player_atk3_index = 0
                    self.player_atk3_index_flipped = 0
                    self.atk3_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 3 used')
            elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3:
                if self.mana >= FIRE_WIZARD_SP_MANA_COST and self.attacks[3].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                        y=self.rect.centery - 100,
                        frames=self.sp,
                        frame_duration=80,
                        repeat_animation=1,
                        speed=5 if self.facing_right else -5,
                        dmg=FIRE_WIZARD_SP_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_WIZARD_SP_MANA_COST
                    self.attacks[3].last_used_time = current_time
                    self.running = False
                    self.sp_attacking = True
                    self.player_sp_index = 0
                    self.player_sp_index_flipped = 0
                    self.sp_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')
            
        
    
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
            if not DISABLE_HEAL_REGEN:
                self.health += DEFAULT_HEALTH_REGENERATION
        else:
            self.health = 0

        

        
MULT = 0.7

WANDERER_MAGICIAN_JUMP_COUNT = 6
WANDERER_MAGICIAN_RUN_COUNT = 8
WANDERER_MAGICIAN_IDLE_COUNT = 8
WANDERER_MAGICIAN_ATK1_COUNT = 7
WANDERER_MAGICIAN_ATK3_COUNT = 9
WANDERER_MAGICIAN_SP_COUNT = 16
WANDERER_MAGICIAN_DEATH_COUNT = 4

WANDERER_MAGICIAN_ATK1 = 4
WANDERER_MAGICIAN_ATK2 = 40
WANDERER_MAGICIAN_ATK3 = 10
WANDERER_MAGICIAN_SP = 3
# ---------------------
WANDERER_MAGICIAN_ATK1_MANA_COST = 70
WANDERER_MAGICIAN_ATK2_MANA_COST = 125
WANDERER_MAGICIAN_ATK3_MANA_COST = 125
WANDERER_MAGICIAN_SP_MANA_COST = 180

WANDERER_MAGICIAN_ATK1_SIZE = 2
WANDERER_MAGICIAN_ATK2_SIZE = 1
WANDERER_MAGICIAN_ATK3_SIZE = 1.5
WANDERER_MAGICIAN_SP_SIZE = 1.3

WANDERER_MAGICIAN_ATK1_COOLDOWN = 11000
WANDERER_MAGICIAN_ATK2_COOLDOWN = 10000 + 9000
WANDERER_MAGICIAN_ATK3_COOLDOWN = 25000
WANDERER_MAGICIAN_SP_COOLDOWN = 42000

WANDERER_MAGICIAN_ATK1_DAMAGE = 0 # dmg at the input, sry
WANDERER_MAGICIAN_ATK2_DAMAGE = 0.05
WANDERER_MAGICIAN_ATK3_DAMAGE = 0.375 #26
WANDERER_MAGICIAN_SP_DAMAGE = 50

class Wanderer_Magician(Player): #NEXT WORK ON THE SPRITES THEN COPY EVERYTHING SINCE IM DONE 4/6/25 10:30pm
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type # 1 for player 1, 2 for player 2

        self.max_health = 200
        self.max_mana = 200
        self.health = self.max_health
        self.mana = self.max_mana

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20
        # Player Animation Source
        jump_ani = [r'HERO FIGHTING\assets\characters\Wanderer Magican\jump pngs\Jump_', WANDERER_MAGICIAN_JUMP_COUNT, 1]
        run_ani = [r'HERO FIGHTING\assets\characters\Wanderer Magican\run pngs\Run_', WANDERER_MAGICIAN_RUN_COUNT, 1]
        idle_ani= [r'HERO FIGHTING\assets\characters\Wanderer Magican\idle pngs\image_0-', WANDERER_MAGICIAN_IDLE_COUNT, 1]
        atk1_ani= [r'HERO FIGHTING\assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        atk3_ani= [r'HERO FIGHTING\assets\characters\Wanderer Magican\attack 2 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        sp_ani= [r'HERO FIGHTING\assets\characters\Wanderer Magican\charge pngs', WANDERER_MAGICIAN_SP_COUNT, 1]
        death_ani= [r'HERO FIGHTING\assets\characters\Wanderer Magican\dead', WANDERER_MAGICIAN_DEATH_COUNT, 1]

        self.atk1_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3')
        self.sp_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3')
        self.atk1_sound.set_volume(0.4)
        self.atk2_sound.set_volume(0.5)
        self.atk3_sound.set_volume(0.4)
        self.sp_sound.set_volume(0.4)

        # # Player Skill Animations Source
        atk1 = [r'HERO FIGHTING\assets\attacks\wanderer magician\atk1\image_', WANDERER_MAGICIAN_ATK1, 1]
        atk2 = [r'HERO FIGHTING\assets\attacks\wanderer magician\atk2', WANDERER_MAGICIAN_ATK2, 1]
        atk3 = [r'HERO FIGHTING\assets\attacks\wanderer magician\atk3\Explosion_blue_circle', WANDERER_MAGICIAN_ATK3, 0]
        sp = [r'HERO FIGHTING\assets\attacks\wanderer magician\sp atk\vv', WANDERER_MAGICIAN_SP, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wanderer_magician\Icon_06.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wanderer_magician\HealingWindIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wanderer_magician\Icon9.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wanderer_magician\Massive_Rasen.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = self.load_img_frames_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, 90)
        self.atk1_flipped = self.load_img_frames_flipped_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, -90)
        self.atk2 = self.load_img_frames_tile_method(atk2[0], atk2[1], atk2[2], WANDERER_MAGICIAN_ATK2_SIZE)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], WANDERER_MAGICIAN_ATK3_SIZE)
        self.sp = self.load_img_frames(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)
        self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk2 = self.player_idle[:9]
        self.player_atk2_flipped = self.player_idle_flipped[:2]
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp = self.load_img_frames_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp_flipped = self.load_img_frames_flipped_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death = self.load_img_frames_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death_flipped = self.load_img_frames_flipped_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            WANDERER_MAGICIAN_ATK1_MANA_COST,
            WANDERER_MAGICIAN_ATK2_MANA_COST,
            WANDERER_MAGICIAN_ATK3_MANA_COST,
            WANDERER_MAGICIAN_SP_MANA_COST
        ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=WANDERER_MAGICIAN_ATK1_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=WANDERER_MAGICIAN_ATK2_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=WANDERER_MAGICIAN_ATK3_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=WANDERER_MAGICIAN_SP_COOLDOWN,
                mana=self.mana
            )
        ]

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana

    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not self.is_dead():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += self.speed
                    if self.x_pos > width+50 - (self.rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = width+50 - (self.rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= self.speed
                    if self.x_pos < (0-50 + (self.rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (0-50 + (self.rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = DEFAULT_JUMP_FORCE  
                    self.last_atk_time = current_time  # Update the last jump time

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity

        # Stop at the ground level
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False 
        if self.y_pos > DEFAULT_Y_POS - JUMP_LOGIC_EXECUTE_ANIMATION:
            self.player_jump_index = 0
            self.player_jump_index_flipped = 0
            
            
        if not self.jumping and not self.is_dead():
            if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= WANDERER_MAGICIAN_ATK1_MANA_COST and self.attacks[0].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx,
                        y=self.rect.centery + 30,
                        frames=self.atk1 if self.facing_right else self.atk1_flipped,
                        frame_duration=100,
                        repeat_animation=3,
                        speed=7 if self.facing_right else -7,
                        dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 3,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= WANDERER_MAGICIAN_ATK1_MANA_COST
                    self.attacks[0].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    self.atk1_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 1 used')


            elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= WANDERER_MAGICIAN_ATK2_MANA_COST and self.attacks[1].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx, # in front of him
                        y=self.rect.centery + 20,
                        frames=self.atk2,
                        frame_duration=100,
                        repeat_animation=2,
                        speed=5 if self.facing_right else -5,
                        dmg=WANDERER_MAGICIAN_ATK2_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False,
                        heal=True) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= WANDERER_MAGICIAN_ATK2_MANA_COST
                    self.health += WANDERER_MAGICIAN_ATK2_DAMAGE * 2
                    self.attacks[1].last_used_time = current_time
                    self.running = False
                    self.attacking2 = True
                    self.player_atk2_index = 0
                    self.player_atk2_index_flipped = 0
                    self.atk2_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 2 used')

            elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking:
                if self.mana >= WANDERER_MAGICIAN_ATK3_MANA_COST and self.attacks[2].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=hero1.x_pos if self.player_type == 2 else hero2.x_pos, #self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 150, # in front of him
                        y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                        frames=self.atk3,
                        frame_duration=100,
                        repeat_animation=1,
                        speed=5 if self.facing_right else -5,
                        dmg=WANDERER_MAGICIAN_ATK3_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= WANDERER_MAGICIAN_ATK3_MANA_COST
                    self.attacks[2].last_used_time = current_time
                    self.running = False
                    self.attacking3 = True
                    self.player_atk3_index = 0
                    self.player_atk3_index_flipped = 0
                    self.atk3_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 3 used')
            elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3:
                if self.mana >= WANDERER_MAGICIAN_SP_MANA_COST and self.attacks[3].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx, # in front of him
                        y=self.rect.centery,
                        frames=self.sp if self.facing_right else self.sp_flipped,
                        frame_duration=40,
                        repeat_animation=30,
                        speed=5 if self.facing_right else -5,
                        dmg=WANDERER_MAGICIAN_SP_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= WANDERER_MAGICIAN_SP_MANA_COST
                    self.attacks[3].last_used_time = current_time
                    self.running = False
                    self.sp_attacking = True
                    self.player_sp_index = 0
                    self.player_sp_index_flipped = 0
                    self.sp_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')

        # print(self.running)
        # print(self.player_type)
        # print(len(self.player_run), len(self.player_run_flipped))
        # print("Run Animation Index:", self.player_run_index)
    
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

        # Draw skill icons
        for attack in self.attacks:
            attack.draw_skill_icon(screen, self.mana)

        for mana in self.attacks:
            mana.draw_mana_cost(screen, self.mana)

        # Update the player status (health and mana bars)
        self.player_status(self.health, self.mana)
        
        # Update the health and mana bars
        if self.health != 0:
            self.mana += (DEFAULT_MANA_REGENERATION + (DEFAULT_MANA_REGENERATION * 0.15))
            if not DISABLE_HEAL_REGEN:
                self.health += DEFAULT_HEALTH_REGENERATION
        else:
            self.health = 0



    
# Animation Counts
FIRE_KNIGHT_JUMP_COUNT = 20
FIRE_KNIGHT_RUN_COUNT = 8 
FIRE_KNIGHT_IDLE_COUNT = 8
FIRE_KNIGHT_ATK1_COUNT = 11
FIRE_KNIGHT_ATK2_COUNT = 19
FIRE_KNIGHT_ATK3_COUNT = 28
FIRE_KNIGHT_SP_COUNT = 18
FIRE_KNIGHT_DEATH_COUNT = 13

# FIRE_KNIGHT_ATK1 = 11  # 12 - 2
# FIRE_KNIGHT_ATK2 = 19
# FIRE_KNIGHT_ATK3 = 28
# FIRE_KNIGHT_SP = 28

FIRE_KNIGHT_ATK1_MANA_COST = 30
FIRE_KNIGHT_ATK2_MANA_COST = 80
FIRE_KNIGHT_ATK3_MANA_COST = 125
FIRE_KNIGHT_SP_MANA_COST = 160

FIRE_KNIGHT_ATK1_SIZE = 5
FIRE_KNIGHT_ATK2_SIZE = 1.5
FIRE_KNIGHT_ATK3_SIZE = 2
FIRE_KNIGHT_SP_SIZE = 2.5

FIRE_KNIGHT_ATK1_COOLDOWN = 5000
FIRE_KNIGHT_ATK2_COOLDOWN = 10000
FIRE_KNIGHT_ATK3_COOLDOWN = 22000
FIRE_KNIGHT_SP_COOLDOWN = 40000

FIRE_KNIGHT_ATK1_DAMAGE = 0.09
FIRE_KNIGHT_ATK2_DAMAGE = 0.115
FIRE_KNIGHT_ATK3_DAMAGE = 0.15
FIRE_KNIGHT_SP_DAMAGE = 0.4

class Fire_Knight(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type

        # Base Stats
        self.max_health = 220
        self.max_mana = 160
        self.health = self.max_health
        self.mana = self.max_mana

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        # Player Animation Source
        jump_ani = [r'HERO FIGHTING\assets\characters\fire knight\03_jump\jump_', FIRE_KNIGHT_JUMP_COUNT, 0]
        run_ani = [r'HERO FIGHTING\assets\characters\fire knight\02_run\run_', FIRE_KNIGHT_RUN_COUNT, 0]
        idle_ani = [r'HERO FIGHTING\assets\characters\fire knight\01_idle\idle_', FIRE_KNIGHT_IDLE_COUNT, 0]
        atk1_ani = [r'HERO FIGHTING\assets\characters\fire knight\05_1_atk\1_atk_', FIRE_KNIGHT_ATK1_COUNT, 0]
        atk2_ani = [r'HERO FIGHTING\assets\characters\fire knight\06_2_atk\2_atk_', FIRE_KNIGHT_ATK2_COUNT, 0]
        atk3_ani = [r'HERO FIGHTING\assets\characters\fire knight\07_3_atk\3_atk_', FIRE_KNIGHT_ATK3_COUNT, 0]
        sp_ani = [r'HERO FIGHTING\assets\characters\fire knight\08_sp_atk\sp_atk_', FIRE_KNIGHT_SP_COUNT, 0]
        death_ani = [r'HERO FIGHTING\assets\characters\fire knight\11_death\death_', FIRE_KNIGHT_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire knight\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire knight\3rrd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\fire knight\ult.mp3')
        self.atk1_sound.set_volume(0.5)
        self.atk2_sound.set_volume(0.5)
        self.atk3_sound.set_volume(0.5)
        self.sp_sound.set_volume(0.5)

        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'HERO FIGHTING\assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'HERO FIGHTING\assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire knight\3.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire knight\4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire knight\5.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\fire knight\6.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk1_flipped = load_attack_flipped(
        filepath=r"HERO FIGHTING\assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\fire knight\atk2\414.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\fire knight\atk3\D65.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\fire knight\sp\D30.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=13, 
        columns=5, 
        scale=FIRE_KNIGHT_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            FIRE_KNIGHT_ATK1_MANA_COST,
            FIRE_KNIGHT_ATK2_MANA_COST,
            FIRE_KNIGHT_ATK3_MANA_COST,
            FIRE_KNIGHT_SP_MANA_COST
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=FIRE_KNIGHT_ATK1_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=FIRE_KNIGHT_ATK2_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=FIRE_KNIGHT_ATK3_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=FIRE_KNIGHT_SP_COOLDOWN,
                mana=self.mana
            )
        ]

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not self.is_dead():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed - (self.speed * 0.2))
                    if self.x_pos > width+250 - (self.rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = width+250 - (self.rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed - (self.speed * 0.2))
                    if self.x_pos < (0-250 + (self.rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (0-250 + (self.rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE - (DEFAULT_JUMP_FORCE * 0.05))  
                    self.last_atk_time = current_time  # Update the last jump time

        # Apply gravity
        self.y_velocity += (DEFAULT_GRAVITY + (DEFAULT_GRAVITY * 0.03))
        self.y_pos += self.y_velocity

        # Stop at the ground level
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False 
        if self.y_pos > DEFAULT_Y_POS - JUMP_LOGIC_EXECUTE_ANIMATION:
            self.player_jump_index = 0
            self.player_jump_index_flipped = 0
            
            
        if not self.jumping and not self.is_dead():
            if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= FIRE_KNIGHT_ATK1_MANA_COST and self.attacks[0].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80,
                        y=self.rect.centery + 30,
                        frames=self.atk1 if self.facing_right else self.atk1_flipped,
                        frame_duration=20,
                        repeat_animation=1,
                        speed=3.5 if self.facing_right else -3.5,
                        dmg=FIRE_KNIGHT_ATK1_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False,
                        heal=False,
                        continuous_dmg=False,
                        per_end_dmg=(False, False),
                        disable_collide=False,
                        ) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_KNIGHT_ATK1_MANA_COST
                    self.attacks[0].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    self.atk1_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 1 used')


            elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= FIRE_KNIGHT_ATK2_MANA_COST and self.attacks[1].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                    attack = Attack_Display(
                        x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                        y=self.rect.centery + 30,
                        frames=self.atk2,
                        frame_duration=150,
                        repeat_animation=1,
                        speed=5 if self.facing_right else -5,
                        dmg=FIRE_KNIGHT_ATK2_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False,
                        heal=False,
                        continuous_dmg=False,
                        per_end_dmg=(False, False),
                        disable_collide=False,
                        stun=(True, 50)
                    )
                    attack_display.add(attack)
                    self.mana -= FIRE_KNIGHT_ATK2_MANA_COST
                    self.attacks[1].last_used_time = current_time
                    self.running = False
                    self.attacking2 = True
                    self.player_atk2_index = 0
                    self.player_atk2_index_flipped = 0
                    self.atk2_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 2 used')

            elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking:
                if self.mana >= FIRE_KNIGHT_ATK3_MANA_COST and self.attacks[2].is_ready():
                    # Create an attack
                    print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx + 180 if self.facing_right else self.rect.centerx - 180, # in front of him
                        y=self.rect.centery + 30,
                        frames=self.atk3,
                        frame_duration=40,
                        repeat_animation=1,
                        speed=0.5 if self.facing_right else -0.5,
                        dmg=FIRE_KNIGHT_ATK3_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False,
                        continuous_dmg=False) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_KNIGHT_ATK3_MANA_COST
                    self.attacks[2].last_used_time = current_time
                    self.running = False
                    self.attacking3 = True
                    self.player_atk3_index = 0
                    self.player_atk3_index_flipped = 0
                    self.atk3_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 3 used')
            elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3:
                if self.mana >= FIRE_KNIGHT_SP_MANA_COST and self.attacks[3].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                        y=self.rect.centery - 50,
                        frames=self.sp,
                        frame_duration=20,
                        repeat_animation=1,
                        speed=5 if self.facing_right else -5,
                        dmg=FIRE_KNIGHT_SP_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=False) # Replace with the target
                    attack_display.add(attack)
                    self.mana -= FIRE_KNIGHT_SP_MANA_COST
                    self.attacks[3].last_used_time = current_time
                    self.running = False
                    self.sp_attacking = True
                    self.player_sp_index = 0
                    self.player_sp_index_flipped = 0
                    self.sp_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')
            
        
    
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
            if not DISABLE_HEAL_REGEN:
                self.health += (DEFAULT_HEALTH_REGENERATION + (DEFAULT_HEALTH_REGENERATION * 0.3))
        else:
            self.health = 0

         


# Animation Counts
WIND_HASHASHIN_JUMP_COUNT = 6
WIND_HASHASHIN_RUN_COUNT = 8 
WIND_HASHASHIN_IDLE_COUNT = 8
WIND_HASHASHIN_ATK1_COUNT = 7 # using the sp animation
WIND_HASHASHIN_ATK2_COUNT = 7
WIND_HASHASHIN_ATK3_COUNT = 26
WIND_HASHASHIN_SP_COUNT = 30
WIND_HASHASHIN_DEATH_COUNT = 19

# WIND_HASHASHIN_ATK1
# WIND_HASHASHIN_ATK2
# WIND_HASHASHIN_ATK3
# WIND_HASHASHIN_SP =
percen = 0.15
base1 = 50
base2 = 100
base3 = 120
base4 = 150
WIND_HASHASHIN_ATK1_MANA_COST = int(base1 - (base1 * percen))
WIND_HASHASHIN_ATK2_MANA_COST = int(base2 - (base2 * percen))
WIND_HASHASHIN_ATK3_MANA_COST = int(base3 - (base3 * percen))
WIND_HASHASHIN_SP_MANA_COST = int(base4 - (base4 * percen))

WIND_HASHASHIN_ATK1_SIZE = 0.8 # smoke
WIND_HASHASHIN_ATK2_SIZE = 0.8 # tornado
WIND_HASHASHIN_ATK3_SIZE = 1 # circcle
WIND_HASHASHIN_SP_SIZE = 1  # x slash

WIND_HASHASHIN_ATK1_COOLDOWN = 4000
WIND_HASHASHIN_ATK2_COOLDOWN = 120
WIND_HASHASHIN_ATK3_COOLDOWN = 20000
WIND_HASHASHIN_SP_COOLDOWN = 40000

WIND_HASHASHIN_ATK1_DAMAGE = 8
WIND_HASHASHIN_ATK2_DAMAGE = 0.13 #tornado
WIND_HASHASHIN_ATK2_DAMAGE_2ND = 0.18 # x slash
WIND_HASHASHIN_ATK3_DAMAGE = 0.24
WIND_HASHASHIN_SP_DAMAGE = 0.2 # circle
WIND_HASHASHIN_SP_DAMAGE_2ND = 0.4 # x slash

WIND_HASHASHIN_REAL_SP_DAMAGE = 15 #0.225

class Wind_Hashashin(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type

        # Base Stats
        self.max_health = 190
        self.max_mana = 150
        self.health = self.max_health
        self.mana = self.max_mana

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        # Player Animation Source1.png
        jump_ani = [r'HERO FIGHTING\assets\characters\Wind hasashin\PNG\j_up\j_up_', WIND_HASHASHIN_JUMP_COUNT, 0]
        run_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\run\run_', WIND_HASHASHIN_RUN_COUNT, 0]
        idle_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\idle\idle_', WIND_HASHASHIN_IDLE_COUNT, 0]
        atk1_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_ATK1_COUNT, 0]
        atk2_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\air_atk\air_atk_', WIND_HASHASHIN_ATK2_COUNT, 0]
        atk3_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\3_atk\3_atk_', WIND_HASHASHIN_ATK3_COUNT, 0]
        sp_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_SP_COUNT, 0]
        death_ani = [r'HERO FIGHTING\assets\characters\wind hasashin\PNG\death\death_', WIND_HASHASHIN_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\1st.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\3rd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\4th 1, slash.mp3')
        self.atk1_sound.set_volume(0.5)
        self.atk2_sound.set_volume(0.1)
        self.atk3_sound.set_volume(0.5)
        self.sp_sound.set_volume(0.5)
        
        self.x_slash_sound = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\x slash 2nd,3rd, 4th.mp3')
        self.sp_sound2 = pygame.mixer.Sound(r'HERO FIGHTING\assets\sound effects\wind hashashin\4th 2, flesh hit.mp3')
        self.x_slash_sound.set_volume(0.5)
        self.sp_sound2.set_volume(0.5)

        # (The rest of the code follows same structure and renaming logic...)
        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'HERO FIGHTING\assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'HERO FIGHTING\assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wind_hasashin\WindHashira.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wind_hasashin\3yzqiwcug5qc1.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wind_hasashin\What is Danmokou_.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\skill icons\wind_hasashin\download.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load (atk doesn't matter, some attack will be used on other attack)
        self.atk1 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\wind hasashin\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack_flipped(
        filepath=r"HERO FIGHTING\assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\wind hasashin\3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"HERO FIGHTING\assets\attacks\wind hasashin\4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3, 
        columns=5, 
        scale=WIND_HASHASHIN_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )
        

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2) # ?
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)

        #this is the ultimate skill using player sp animation as attack animation
        self.real_sp = self.player_sp

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            WIND_HASHASHIN_ATK1_MANA_COST,
            WIND_HASHASHIN_ATK2_MANA_COST,
            WIND_HASHASHIN_ATK3_MANA_COST,
            WIND_HASHASHIN_SP_MANA_COST
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=WIND_HASHASHIN_ATK1_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=WIND_HASHASHIN_ATK2_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=WIND_HASHASHIN_ATK3_COOLDOWN,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=WIND_HASHASHIN_SP_COOLDOWN,
                mana=self.mana
            )
        ]

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   
        
        self.atk1_move_speed = 1
        self.atk2_move_speed = 1
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if not self.is_dead():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed + (self.speed * 0.2))
                    if self.x_pos > width+250 - (self.rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = width+250 - (self.rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed + (self.speed * 0.2))
                    if self.x_pos < (0-250 + (self.rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (0-250 + (self.rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE + (DEFAULT_JUMP_FORCE * 0.1)) 
                    self.last_atk_time = current_time  # Update the last jump time

        # Apply gravity
        self.y_velocity += (DEFAULT_GRAVITY - (DEFAULT_GRAVITY * 0.02))
        self.y_pos += self.y_velocity

        # Stop at the ground level
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False 
        if self.y_pos > DEFAULT_Y_POS - JUMP_LOGIC_EXECUTE_ANIMATION:
            self.player_jump_index = 0
            self.player_jump_index_flipped = 0
            
        if not self.is_dead():
            if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= WIND_HASHASHIN_ATK1_MANA_COST and self.attacks[0].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                        x=self.rect.centerx,
                        y=self.rect.centery + 60,
                        frames=self.atk1,
                        frame_duration=20,
                        repeat_animation=1,
                        speed=-1 if self.facing_right else 1,
                        dmg=WIND_HASHASHIN_ATK1_DAMAGE,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True) # Replace with the target
                    attack_display.add(attack)
                    #dash  
                    self.mana -= WIND_HASHASHIN_ATK1_MANA_COST
                    self.attacks[0].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    self.atk1_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 1 used')

        if not self.jumping and not self.is_dead(): # can be cast while jumping, I hope...
            if hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking:
                if self.mana >= WIND_HASHASHIN_ATK2_MANA_COST and self.attacks[1].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                    for i in [
                        (self.atk2, True, 30, 30, WIND_HASHASHIN_ATK2_DAMAGE, True), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                        (self.sp, False, 40, 40, WIND_HASHASHIN_ATK2_DAMAGE_2ND, False)
                        ]:
                        attack = Attack_Display(
                            x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                            y=self.rect.centery + 50,
                            frames=i[0],
                            frame_duration=i[3],
                            repeat_animation=1,
                            speed=10 if self.facing_right else -10,
                            dmg=i[4],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=i[1],
                            heal=False,
                            continuous_dmg=i[1],
                            per_end_dmg=(False, False),
                            disable_collide=False,
                            stun=(i[5], 40)

                            ) # Replace with the target
                        attack_display.add(attack)
                    self.mana -= WIND_HASHASHIN_ATK2_MANA_COST
                    self.attacks[1].last_used_time = current_time
                    self.running = False
                    self.attacking2 = True
                    self.player_atk2_index = 0
                    self.player_atk2_index_flipped = 0
                    self.atk2_sound.play()
                    self.x_slash_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")               
                # print('Skill 2 used')

        if not self.jumping and not self.is_dead():
            if hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking:
                if self.mana >= WIND_HASHASHIN_ATK3_MANA_COST and self.attacks[2].is_ready():
                    # Create an attack
                    current_time2 = pygame.time.get_ticks()
                    # print("Z key pressed")  # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg
                    
                    for i in [
                        (self.atk3, True, 120, 40, WIND_HASHASHIN_SP_DAMAGE),
                        (self.sp, False, 120, 50, WIND_HASHASHIN_SP_DAMAGE_2ND)
                        ]:
                        attack = Attack_Display(
                            x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                            y=self.rect.centery + 50,
                            frames=i[0],
                            frame_duration=i[3],
                            repeat_animation=1,
                            speed=0 if self.facing_right else 0,
                            dmg=i[4],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=i[1],
                            heal=False,
                            continuous_dmg=False,
                            per_end_dmg=(False, False),
                            disable_collide=False,
                            stun=(True, 0)
                            )
                        attack_display.add(attack)
                                
                                
                    # if current_time2 - self.last_atk_time > 1500:
                    #     attack_display.add(attack)
                    #     self.last_atk_time = current_time2
                    self.mana -= WIND_HASHASHIN_ATK3_MANA_COST
                    self.attacks[2].last_used_time = current_time
                    self.running = False
                    self.attacking3 = True
                    self.player_atk3_index = 0
                    self.player_atk3_index_flipped = 0
                    self.atk3_sound.play()
                    self.x_slash_sound.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 3 used')
            elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3:
                if self.mana >= WIND_HASHASHIN_SP_MANA_COST and self.attacks[3].is_ready():
                    # Create an attack
                    # print("Z key pressed")
                    attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.atk1, #frames=self.real_sp,
                            frame_duration=0.1,
                            repeat_animation=4,
                            speed=0 if self.facing_right else 0,
                            dmg=WIND_HASHASHIN_REAL_SP_DAMAGE,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=False,
                            heal=False,
                            continuous_dmg=False,
                            per_end_dmg=(False, True),
                            disable_collide=True,
                            stun=False,
                            sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2)
                            )
                            # Replace with the target
                    attack_display.add(attack)
                    self.mana -= WIND_HASHASHIN_SP_MANA_COST
                    self.attacks[3].last_used_time = current_time
                    self.running = False
                    self.sp_attacking = True
                    self.player_sp_index = 0
                    self.player_sp_index_flipped = 0
                    # self.sp_sound.play()
                    # self.x_slash_sound.play()
                    # self.sp_sound2.play()
                    # print("Attack executed")
                else:
                    pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')
            
        
    
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
        elif self.attacking1:
            self.atk1_move_speed += 0.3
            self.y_velocity = 0
            if self.facing_right:
                self.x_pos += self.atk1_move_speed
            else:
                self.x_pos -= self.atk1_move_speed
            self.atk1_animation()
        elif self.jumping:
            self.jump_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
        elif self.running and not self.jumping:
            self.run_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
        
        elif self.attacking2:
            self.atk1_move_speed += 0.2 #just trying, plan is to make this speial move that knokes back enemies
            if self.player_type == 1: # idea for slow, if enemy ffacing right, - x pos, else + x pos
                if self.facing_right:
                    hero2.x_pos += self.atk2_move_speed
                else:
                    hero2.x_pos -= self.atk2_move_speed
            if self.player_type == 2:
                if self.facing_right:
                    hero1.x_pos += self.atk2_move_speed
                else:
                    hero1.x_pos -= self.atk2_move_speed
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation(2) #animation speed increase
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
        elif self.sp_attacking:
            self.x_pos = hero1.x_pos if self.player_type == 2 else hero2.x_pos
            self.y_pos = hero1.y_pos if self.player_type == 2 else hero2.y_pos
            self.sp_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
            
        else:
            self.simple_idle_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

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
            if not DISABLE_HEAL_REGEN:
                self.health += DEFAULT_HEALTH_REGENERATION
        else:
            self.health = 0