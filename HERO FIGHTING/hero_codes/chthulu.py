from global_vars import (IMMEDIATE_RUN,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon, water_princess_icon, forest_ranger_icon, yurei_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img,
    waterfall_icon, lava_icon, dark_forest_icon, trees_icon, 
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size, BASIC_ATK_COOLDOWN, BASIC_FRAME_DURATION, BASIC_ATK_DAMAGE, BASIC_ATK_DAMAGE2, BASIC_ATK_DAMAGE3, BASIC_ATK_DAMAGE4,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION, BASIC_ATK_POSX, BASIC_ATK_POSX_END, BASIC_ATK_POSY, SPECIAL_MULTIPLIER, MAX_SPECIAL, SPECIAL_DURATION, DISABLE_SPECIAL_REDUCE,
    LOW_HP, LITERAL_HEALTH_DEAD, SINGLE_MODE_ACTIVE, SHOW_HITBOX, DRAW_DISTANCE,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED, RUNNING_ANIMATION_SPEED, DEFAULT_BASIC_ATK_DMG_BONUS,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT, MAX_ITEM,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    DISABLE_MANA_REGEN,
    attack_display, MULT, dmg_mult,

    ZERO_WIDTH, TOTAL_WIDTH
)
from heroes import Attacks, Attack_Display
from sprite_loader import load_attack, load_attack_flipped
from player import Player
import global_vars
import pygame
# Animation Counts
# WATER_PRINCESS_BASIC_COUNT = 

# WATER_PRINCESS_JUMP_COUNT = 6
# WATER_PRINCESS_RUN_COUNT = 10
# WATER_PRINCESS_IDLE_COUNT = 8
# WATER_PRINCESS_ATK1_COUNT = 7
# WATER_PRINCESS_ATK2_COUNT = 27
# WATER_PRINCESS_ATK3_COUNT = 12
# WATER_PRINCESS_SP_COUNT = 32
# WATER_PRINCESS_DEATH_COUNT = 16

# WATER_PRINCESS_SURF_COUNT = 8

# # WATER_PRINCESS_ATK1 = 0
# # WATER_PRINCESS_ATK2 = 0
# # WATER_PRINCESS_ATK3 = 0
# # WATER_PRINCESS_SP = 0
# # ---------------------
# # print((WATER_PRINCESS_ATK2 * 0.01) * 4 * 5)

# WATER_PRINCESS_ATK1_SIZE = 2
# WATER_PRINCESS_ATK2_SIZE = 2
# WATER_PRINCESS_ATK3_SIZE = 1
# WATER_PRINCESS_SP_SIZE = 4  

# STILL IN PROGRESS: 11/16/26 6:07PM
class Chthulu(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        self.player_type = player_type
        self.name = "Chthulu"

        self.hitbox_rect = pygame.Rect(0, 0, 80, 115)

        # stat
        self.strength = 40
        self.intelligence = 40
        self.agility = 35 # real agility = 20

        # trait: Increased str potency
        rate = 1.5
        self.str_mult += 0.5
        self.int_mult += 0.5
        self.agi_mult += 0.05

        # Base Stats
        self.max_health = (self.strength * self.str_mult)
        self.max_mana = (self.intelligence * self.int_mult)
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult

        # self.basic_atk1_dmg = self.basic_attack_damage*5
        # self.basic_atk2_dmg = self.basic_attack_damage*1.5

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        self.y_visual_offset = 36

        # SPECIAL TRAIT
            # Mana cost delayed
            # Mana cast high, but mana cost delay reduced by 15%
            #example:
            # if mana cost is 160, reduce mama until end of attack frame, 
            # but that 160 is reduced by 15%
            # total mana depleted = (160*0.85 or 160-(160*0.15)) = 136 total mana cost

            # mana reduce 20% if special active

        self.atk1_mana_cost = 50
        self.atk2_mana_cost = 80
        self.atk3_mana_cost = 100
        self.sp_mana_cost = 200

        #go to attacks section to calculate mana

        self.atk1_cooldown = 10000 + 10000
        self.atk2_cooldown = 20000
        self.atk3_cooldown = 30000
        self.sp_cooldown = 75000

        # self.atk1_damage = (5/40, 0)
        self.atk1_damage_2nd = 10 #----- 2ND SKILL SP ONLY MOVING

        self.atk2_damage = (15/55, 0) # ATK 2

        self.atk2_damage_2nd = (2/40, 5) #ATK 3 POISION LEAVE
        self.atk3_damage = (10/20, 0) #ATK  POISON FOLLOW

        # self.atk3_damage_2nd = 20 #-----

        self.sp_damage = (25/35, 0) #charge (self dmg)
        self.sp_damage_2nd = (20,0) #(30/15, 0) # explosion 
        self.sp_damage_3rd = (20/25, 0) # explosion up
        self.sp_atk1_damage = (20/10, 0) # explosion real
        # TOTAL: 60

        # self.sp_atk2_damage = 0.3#(totaldmg 9*2=18) # =0.4166 (12.5/30, 0) # rain #-----
        # self.sp_atk2_damage_2nd = (5/30, 2) #(*5) #circling #------
        # self.sp_atk2_damage_3rd = (2/15, 5) #(*10) #watershot #-----
        # self.sp_atk3_damage = (15/20, 0) #10+(15*2)= #-----
        # sp_atk3 heal = 20/2:instant=10, 
        # dmg_mult = 0
        # self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        # self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        # self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        # self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)
        
        self.player_fly_index = 0
        self.player_fly_index_flipped = 0

        self.player_atk1_2nd_index = 0
        self.player_atk1_2nd_index_flipped = 0
        
        # Player Animation Source
        basic_ani = [r'assets\characters\soul_destroyer\PNG\1atk\1atk_', 7, 0]

        jump_ani = [r'assets\characters\soul_destroyer\PNG\fly\fly_', 6, 0]
        run_ani = [r'assets\characters\soul_destroyer\PNG\walk\walk_', 12, 0]

        # surf_ani = [r'assets\characters\Water princess\png\03_surf\surf_', WATER_PRINCESS_SURF_COUNT, 0]
        # fly_ani = jump_ani

        idle_ani = [r'assets\characters\soul_destroyer\PNG\idle\idle_', 15, 0]
        # atk1_ani = [r'assets\characters\Water princess\png\07_1_atk\1_atk_', WATER_PRINCESS_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\soul_destroyer\PNG\2atk\2atk_', 9, 0]
        # atk3_ani = [r'assets\characters\Water princess\png\11_heal\heal_', WATER_PRINCESS_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\soul_destroyer\PNG\hurt\hurt_', 5, 0]
        death_ani = [r'assets\characters\soul_destroyer\PNG\death\death_', 11, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\3rrd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\ult.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.1 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        # atk1 = [r'', WATER_PRINCESS_ATK1, 1]
        # atk2 = [r', WATER_PRINCESS_ATK2, 1]
        # atk3 = [r'HERO FIGHTING\assets\attacks\fire knight\atk3\png_', WATER_PRINCESS_ATK3, 1]
        # sp = [r'HERO FIGHTING\assets\attacks\fire knight\sp atk', WATER_PRINCESS_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk1.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk2.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk3.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk4_2.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\soul_destroyer\sp_icon.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\472234276_8613137162147060_446401069957588690_n.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        # special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\tumblr_8ca04de6143efee03f34ea8c32aca437_a117ed18_1280.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk3_2.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets/skill icons/soul_destroyer/sk4.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
    #     self.atk1 = load_attack( # rain
    #     filepath=r"assets\attacks\water princess\1.PNG",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=8, 
    #     columns=5, 
    #     scale=WATER_PRINCESS_ATK1_SIZE, 
    #     rotation=0,
    # )
        self.atk2 = load_attack( #circling water
        filepath=r"assets\attacks\soul destroyer\atk2\slow.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=11, 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        
        self.atk3 = load_attack( # silence smoke
        filepath=r"assets\attacks\soul destroyer\atk3\silence.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=3, 
        rotation=0,
    )
        
        self.sp = load_attack( # charge
        filepath=r"assets\attacks\soul destroyer\atk4\charge.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=5, 
        scale=3, 
        rotation=0,
    )
        self.sp1 = load_attack( # explode
        filepath=r"assets\attacks\soul destroyer\atk4\explode.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3, 
        columns=5, 
        scale=4, 
        rotation=0,
    )
        self.sp2 = load_attack( # explode up
        filepath=r"assets\attacks\soul destroyer\atk4\explode2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=5, 
        columns=5, 
        scale=4, 
        rotation=0,
    )
        self.sp3 = self.load_img_frames(
            folder=r'assets\attacks\soul destroyer\atk4\Explosion_gas_circle\Explosion_gas_circle', 
            count=10,
            size=4
        )
        
    #     self.sp_atk1 = load_attack(
    #     filepath=r"assets\attacks\water princess\sp_atk1.PNG",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=5, 
    #     columns=5, 
    #     scale=1.5, 
    #     rotation=0,
    # )
    #     self.sp_atk2 = load_attack(
    #     filepath=r"assets\attacks\water princess\sp_atk2.PNG",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=6, 
    #     columns=5, 
    #     scale=2, 
    #     rotation=0,
    # )
    #     self.sp_atk3 = load_attack(
    #     filepath=r"assets\attacks\water princess\sp_atk3.PNG",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=4, 
    #     columns=5, 
    #     scale=1.2, 
    #     rotation=0,
    # )
    #     self.sp_atk4 = load_attack(
    #     filepath=r"assets\attacks\water princess\sp_atk4.PNG",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=7, 
    #     columns=5, 
    #     scale=4, 
    #     rotation=0,
    # )
        
        self.blank_frame = [
            pygame.transform.rotozoom(
            pygame.image.load(r"assets\attacks\forest ranger\atk4\blank frame\beam_extension_effect_10.png").convert_alpha(),
            angle=0, scale=3.0)
            ]
    
        # assets\attacks\water princess\basic_atk1\water60000
        # assets\attacks\water princess\atk4\splash big\water400
        # self.sp1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\spiral\water900", 42, starts_at_zero=True,
        # size=0.2)

        # self.sp2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\splash big\water400", 16, starts_at_zero=True,
        # size=0.3)

        # self.basic_atk1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        # rotate=90, size=0.15)

        # self.basic_atk1_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        # rotate=-90, flip=True, size=0.15)

        # self.basic_atk2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        # size=0.5, flip=True)

        # self.basic_atk2_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        # size=0.6)
# (fr'{folder}{str(frame_number).zfill(2)}.png')

        
    

        # Player Animations Load
        inc = 1
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2*inc)

        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2*inc)  

        self.player_fly = self.player_jump
        self.player_fly_flipped = self.player_jump_flipped
        
        # self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)
        # self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2*inc)  
        # self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)
        # self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2*inc)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2*inc)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            self.atk1_mana_cost,
            self.atk2_mana_cost,
            self.atk3_mana_cost,
            self.sp_mana_cost
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=self.atk2_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=self.sp_cooldown,
                mana=self.mana
            )
        ]

        self.attacks.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )

        self.attacks.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.special_rect,
                skill_img=special_icon,
                cooldown=0,
                mana=0,
                special_skill=True
            )
        )

        
        

        #special
        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=skill_2,
                cooldown=self.atk2_cooldown,    
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.special_skill_3_rect,
                skill_img=special_skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.special_skill_4_rect,
                skill_img=special_skill_4,
                cooldown=self.sp_cooldown,
                mana=self.mana
            )
        ]

        self.attacks_special.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana  

        self.flying = False
        self.flying_duration = 0

        self.using_sp = False
        self.using_sp_duration = 0
        self.hp_cost = 1.0
        # self.haste_value = DEFAULT_ANIMATION_SPEED #(120) #default, change in skill 1 config
        # self.default_atk_speed = self.basic_attack_animation_speed



    def run_animation(self, animation_speed=0):
        if not self.flying:
            if self.facing_right:
                self.player_run_index, _ = self.animate(self.player_run, self.player_run_index, loop=True)
            else:
                self.player_run_index_flipped, _ = self.animate(self.player_run_flipped, self.player_run_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_fly_index, _ = self.animate(self.player_fly, self.player_fly_index, loop=True)
            else:
                self.player_fly_index_flipped, _ = self.animate(self.player_fly_flipped, self.player_fly_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
    
    def simple_idle_animation(self, animation_speed=0):
        if not self.flying:
            if self.facing_right:
                self.player_idle_index, _ = self.animate(self.player_idle, self.player_idle_index, loop=True)
            else:
                self.player_idle_index_flipped, _ = self.animate(self.player_idle_flipped, self.player_idle_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_fly_index, _ = self.animate(self.player_fly, self.player_fly_index, loop=True)
            else:
                self.player_fly_index_flipped, _ = self.animate(self.player_fly_flipped, self.player_fly_index_flipped, loop=True)

        self.last_atk_time -= animation_speed

    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed - (self.speed * 0.5)) if not self.flying else (self.speed + (self.speed * 1)) if not self.special_active else (self.speed - (self.speed * 0.4)) if not self.flying else (self.speed + (self.speed * 1.5))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed - (self.speed * 0.5)) if not self.flying else (self.speed + (self.speed * 1))  if not self.special_active else (self.speed - (self.speed * 0.4)) if not self.flying else (self.speed + (self.speed * 1.5))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE - (DEFAULT_JUMP_FORCE * 0.05))
                    self.last_atk_time = current_time  # Update the last jump time
            
        if not self.can_cast():
            # If can't cast skills, still allow basic attacks only when silenced (not frozen)
            # If frozen, block everything immediately
            if getattr(self, 'frozen', False):
                return
            if not (basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking):
                return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        

                        
                        
                        self.mana -= self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        # self.attacking1 = True
                        self.flying = True
                        self.flying_duration = pygame.time.get_ticks() + 10000

                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        target, target_detected = self.target_enemy(200)
                        attack = Attack_Display(
                            x=target,
                            y=self.rect.centery + 15,
                            frames=self.atk2,
                            frame_duration=72.72,
                            repeat_animation=1,
                            dmg=self.atk2_damage[0],
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound, None, None),
                            stop_movement=(True, 3, 2, 0.3),
                            follow=(False, target_detected),
                        )
                        attack_display.add(attack)

                        self.mana -= self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 10,
                                frames=self.atk3,
                                frame_duration=125, # 5 second silence total =+ ?? 3s for spawned
                                repeat_animation=2,
                                speed=0,
                                dmg=self.atk3_damage[0],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                follow_offset=(0, 70),
                                stop_movement=(True, 4, 1),
                                periodic_spawn={
                                                'attack_kwargs': {
                                                    # 'x': width+100,
                                                    # 'y': self.rect.centery + 10,
                                                    'frames': self.atk3,
                                                    'frame_duration': 150,
                                                    'repeat_animation': 1,
                                                    # 'speed': -7 if self.facing_right else 7,
                                                    'dmg': self.atk2_damage_2nd[0],
                                                    'final_dmg': 0,
                                                    'who_attacks': self,
                                                    'who_attacked': self.enemy,
                                                    'sound': (False, self.atk1_sound, None, None),
                                                    'stop_movement': (True, 4, 1)
                                                    # 'delay': (True, 300),
                                                },
                                                'interval': 500,
                                                'repeat_count': 10, # 20 total smoke
                                                'use_attack_pos': True,
                                            }
                                )
                        attack_display.add(attack)
                        
                        self.mana -= self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        # self.running = False
                        # self.attacking3 = True
                        # self.player_atk3_index = 0
                        # self.player_atk3_index_flipped = 0

                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # using_sp = True
                        self.using_sp = True
                        self.using_sp_duration = pygame.time.get_ticks() + 1
                        self.lifesteal -= self.hp_cost
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-trgt&mvng 7-dmg/fnldmg
                    (self.sp, 30, (0, 10), (False, 0), (False, 0), (0.55, 0.5), True, self.sp_damage),#charge 1 
                    (self.sp3, 120, (0, 10), (False, 0), (True, 700), (0.4, 0.4), None, self.sp_atk1_damage),#explode real 4
                    (self.sp1, 50, (0, 10), (False, 0), (True, 1050-270), (0.4, 0.5), 'hit', self.sp_damage_2nd),#explode 2
                    (self.sp2, 80, (0, -80), (False, 0), (True, 1050-270+200), (0.4, 0.6), None, self.sp_damage_3rd),#explode up 3
                    
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[7][0],
                                final_dmg=i[7][1],
                                who_attacks=self,
                                who_attacked=self.enemy if i[6] != True else self,
                                moving=False if i[6] != 'hit' else True,
                                sound=(True, self.sp_sound, None, None),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1], 
                                # consume_mana=[i[6], self.atk4_mana_consume],
                                stop_movement=(False, 1, 2)
                                
                                ) # Replace with the target
                            attack_display.add(attack)

                        # self.lifesteal += 0.5

                        self.mana -=  self.attacks[3].mana_cost
                        self.attacks[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

            if not self.is_dead():
                if basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks[4].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx + 110 if self.facing_right else self.rect.centerx - 110,
                                y=self.rect.centery + 10,
                                frames=self.blank_frame,
                                frame_duration=600,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.basic_attack_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (300    / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                                moving=True,
                                hitbox_scale_x=0.26,
                                hitbox_scale_y=0.6,
                                is_basic_attack=True
                                )
                        attack_display.add(attack)
                        self.mana -= self.attacks[4].mana_cost
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()
                        # print("Attack executed")
                    else:
                        pass

                elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                        self.special_active = True
                        self.special_sound.play()
                    else:
                        pass











                    
        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        

                        # # self.mana -= self.attacks[0].mana_cost
                        # self.attacks_special[0].last_used_time = current_time
                        # self.running = False
                        # self.attacking1 = True
                        # self.player_atk1_2nd_index = 0
                        # self.player_atk1_2nd_index_flipped = 0
                        # # print("Attack executed")

                        self.mana -= self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        # self.attacking1 = True
                        self.flying = True
                        self.flying_duration = pygame.time.get_ticks() + 15000
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # self.single_target()
                        # target, target_detected = self.face_selective_target()
                        # attack1 = Attack_Display(
                        #     x=target,
                        #     y=self.target.rect.centery + 15,
                        #     frames=self.atk2,
                        #     frame_duration=109.09, # 55 frames, 6 seconds
                        #     repeat_animation=1,
                        #     dmg=self.atk2_damage[0]*1.2,
                        #     final_dmg=self.atk2_damage[1]*1.2,
                        #     who_attacks=self,
                        #     who_attacked=self.enemy,
                        #     sound=(True, self.atk3_sound , None, None),
                        #     stop_movement=(True, 3, 2, 0.3),
                        #     follow=(False, target_detected)
                        #     )
                        # attack_display.add(attack1)

                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 10,
                            frames=self.blank_frame,
                            frame_duration=100, # 4 s
                            repeat_animation=40,
                            speed=20 if self.facing_right else -20,
                            dmg=self.atk1_damage_2nd,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            delay=(True, 400),
                            sound=(True, self.atk2_sound , None, None),
                            moving=True,
                            # follow_self=True,
                            follow=(False, False), # some bug happended while i code the attack
                            # follow_offset=(0, 70),
                            hitbox_offset_x=0.1,
                            stop_movement=(False, 3, 3, 0.3),
                            periodic_spawn={
                                            'attack_kwargs': {
                                                # 'x': width+100,
                                                # 'y': self.rect.centery + 10,
                                                'frames': self.atk2, 
                                                'frame_duration': 109.09,  # 6 sec
                                                'repeat_animation': 1,
                                                # 'speed': -7 if self.facing_right else 7,
                                                'dmg': self.atk2_damage[0]/2,
                                                'final_dmg': 0,
                                                'who_attacks': self,
                                                'who_attacked': self.enemy,
                                                'sound': (False, self.atk1_sound, None, None),
                                                'stop_movement': (True, 3, 1, 0.3)
                                                # 'delay': (True, 300),
                                            },
                                            'interval': 50,
                                            'repeat_count': 20, 
                                            'use_attack_pos': True,
                                        }
                                )

                        attack_display.add(attack)
                        self.mana -= self.attacks[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 10,
                                frames=self.atk3,
                                frame_duration=125, # 20frames, 7.5? second silence total =+ ?? 3s for spawned
                                repeat_animation=2,
                                speed=0,
                                dmg=self.atk3_damage[0],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                follow_offset=(0, 70),
                                stop_movement=(True, 4, 1),
                                periodic_spawn={
                                                'attack_kwargs': {
                                                    # 'x': width+100,
                                                    # 'y': self.rect.centery + 10,
                                                    'frames': self.atk3,
                                                    'frame_duration': 150,
                                                    'repeat_animation': 1,
                                                    # 'speed': -7 if self.facing_right else 7,
                                                    'dmg': self.atk2_damage_2nd[0],
                                                    'final_dmg': 0,
                                                    'who_attacks': self,
                                                    'who_attacked': self.enemy,
                                                    'sound': (False, self.atk1_sound, None, None),
                                                    'stop_movement': (True, 4, 1)
                                                    # 'delay': (True, 300),
                                                },
                                                'interval': 300,
                                                'repeat_count': 20, # 40 total smoke
                                                'use_attack_pos': True,
                                            }
                                )
                        attack_display.add(attack)
                        
                        self.mana -= self.attacks[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        # self.running = False
                        # self.attacking3 = True
                        # self.player_atk3_index = 0
                        # self.player_atk3_index_flipped = 0
                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # using_sp = True
                        # self.using_sp = True
                        # self.using_sp_duration = pygame.time.get_ticks() + 1
                        # self.lifesteal -= self.hp_cost
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-trgt&mvng 7-dmg/fnldmg
                    (self.sp, 30, (0, 10), (False, 0), (False, 0), (0.55, 0.5), True, self.sp_damage),#charge 1 
                    (self.sp3, 120, (0, 10), (False, 0), (True, 700), (0.4, 0.4), None, self.sp_atk1_damage),#explode real 4
                    (self.sp1, 50, (0, 10), (False, 0), (True, 1050-270), (0.4, 0.5), 'hit', self.sp_damage_2nd),#explode 2
                    (self.sp2, 80, (0, -80), (False, 0), (True, 1050-270+200), (0.4, 0.6), None, self.sp_damage_3rd),#explode up 3
                    
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[7][0]*1.2,
                                final_dmg=i[7][1]*1.2,
                                who_attacks=self,
                                who_attacked=self.enemy if i[6] != True else self,
                                moving=False if i[6] != 'hit' else True,
                                sound=(True, self.sp_sound, None, None),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1], 
                                # consume_mana=[i[6], self.atk4_mana_consume],
                                stop_movement=(False, 1, 2)
                                
                                ) # Replace with the target
                            attack_display.add(attack)

                        self.mana -=  self.attacks[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks_special[4].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx + 110 if self.facing_right else self.rect.centerx - 110,
                                y=self.rect.centery + 10,
                                frames=self.blank_frame,
                                frame_duration=600,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.basic_attack_damage*DEFAULT_BASIC_ATK_DMG_BONUS,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (300    / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                                moving=True,
                                hitbox_scale_x=0.26,
                                hitbox_scale_y=0.6,
                                is_basic_attack=True
                                )
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()

                        # print("Attack executed")
                    else:
                        pass


    def update(self):
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(self.enemy)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()

        self.inputs()
        self.move_to_screen()

         
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(animation_speed=self.running_animation_speed)
                

        # elif self.attacking1:
            # pass
            # self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation()
        # elif self.attacking3:
            # pass
            # self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation(-5)
        elif self.basic_attacking:
            self.basic_animation()
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

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

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)
        # shift pos
        self.rect.y += self.y_visual_offset
        self.hitbox_rect.y -= self.y_visual_offset*1.4

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type, player=self)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type, player=self)

                if not self.special_active:
                    for mana in self.attacks:
                        mana.draw_mana_cost(screen, self.mana)
                else:
                    for mana in self.attacks_special:
                        mana.draw_mana_cost(screen, self.mana)

        # Update the player status (health and mana bars)
        self.player_status(self.health, self.mana, self.special)
        
        # Update the health and mana bars
        if self.health != 0:
            if not DISABLE_MANA_REGEN:
                self.mana += self.mana_regen
            if not DISABLE_HEAL_REGEN:
                self.health += self.health_regen
        else:
            self.health = 0

        if not global_vars.DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False


        # if self.running:
        #     print('is running')
        # self.update_mana_values()
        '''test code are below, for checking correct mana values'''
        # self.atk1_mana_consume = (self.attacks[0].mana_cost/40) - ((self.attacks[0].mana_cost/40)*self.mana_mult)
        # print(self.attacks[0].mana_cost)


        if self.flying:
            if pygame.time.get_ticks() >= self.flying_duration:
                self.flying = False
        if self.using_sp:
            if pygame.time.get_ticks() >= self.using_sp_duration:
                self.lifesteal += self.hp_cost
                self.using_sp = False
                
        
        super().update()