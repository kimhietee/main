import pygame
from player import Player
from heroes import Attacks, Attack_Display, load_attack, load_attack_flipped

import global_vars
from global_vars import (
    # icon
    ICON_WIDTH, ICON_HEIGHT, 
    # positioning
    X_POS_SPACING, START_OFFSET_X, SKILL_Y_OFFSET, SPACING_X, JUMP_DELAY,
    DEFAULT_X_POS, DEFAULT_Y_POS, DEFAULT_JUMP_FORCE,
    TOTAL_WIDTH, ZERO_WIDTH,
    # .
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2,
    # .
    DEFAULT_SPECIAL_SKILL_COOLDOWN,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,

    RUNNING_ANIMATION_SPEED, RUNNING_SPEED, DEFAULT_GRAVITY,
    DISABLE_MANA_REGEN, DISABLE_HEAL_REGEN,
    SPECIAL_DURATION, BASIC_FRAME_DURATION,

    BASIC_SLASH_ANIMATION, BASIC_SLASH_SIZE,

    MAX_SPECIAL,

    screen,

    attack_display
)
class Phantom_Assassin(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # ----- Core -----
        self.player_type = player_type
        self.name = "Phantom Assasin"
        self.hitbox_rect = pygame.Rect(0, 0, 45, 90)
        self.x = 50
        self.y = 50
        self.width = 200
        self.y_visual_offset = 108

        self.char_size = 1.4    


        # ----- Hero Specifications -----
        # Stats
        self.strength = 40
        self.intelligence = 40
        self.agility = 30

        self.base_health_regen = 0.8
        self.base_mana_regen = 5.5
        self.base_attack_damage = 0.3

        self.base_attack_speed = 110
        self.base_attack_time = 1600
        
        self.base_animation_speed = 120
        self.min_animation_speed = 50
        self.attack_speed_modifier = 1.2
        
        self.atk1_mana_cost = 40
        self.atk2_mana_cost = 60
        self.atk3_mana_cost = 90
        self.sp_mana_cost = 120
        
        self.atk1_cooldown = 8000
        self.atk2_cooldown = 15000
        self.atk3_cooldown = 20000
        self.atk4_cooldown = 30000

        self.sp_atk1_mana_cost = 40
        self.sp_atk2_mana_cost = 60
        self.sp_atk3_mana_cost = 90
        self.sp_atk4_mana_cost = 120

        self.special_atk1_cooldown = 8000
        self.special_atk2_cooldown = 15000
        self.special_atk3_cooldown = 20000
        self.special_atk4_cooldown = 30000

        

        # Add more if damage list is not sufficient
        #   - base_damage, attack_frames, *variable
        #       *refer to the Player's existing variables, or create one if not enough
        #   - [0] = damage, [1] = final damage (applies at last frame)
        self.base_damage = {
            'atk1dmg': (12, 0), # 12
            'atk2dmg': (14, 5), # 19
            'atk3dmg': (20, 5), # [1] is 2x dmg (30 dmg)
            'atk4dmg': (40, 0), #

            'atk5dmg': (9, 0), # 12 + 9 = 21 
            'atk6dmg': (15, 10), # 25
            'atk7dmg': (25, 5), # 35
            'atk8dmg': (45, 0), # 

            # For projectile damage
            #'sample': 20
        }

        # Sound Effects
        #   - str [0] file path
        #   - int [1] max volume
        sound1 = [r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3', 0.07]
        sound2 = [r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3', 0.07]
        sound3 = [r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3', 0.07]
        sound4 = [r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3', 0.07]
        self.sound1 = self.load_sound(sound1[0])
        self.sound2 = self.load_sound(sound2[0])
        self.sound3 = self.load_sound(sound3[0])
        self.sound4 = self.load_sound(sound4[0])


        # Character Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count - turn it into tuple to make it column and rows
        #   - bool [2] starts at zero 
        basic_attack_animation = [r'assets\attacks\Basic Attack\wanderer magician\basic atk\basic atk_', 5, False, 'frames']
        jumping_animation = [r'assets\characters\Phantom Assassin\Jump.png', (1,2), False, 'spritesheet']
        falling_animation = [r'assets\characters\Phantom Assassin\Fall.png', (1,2), False, 'spritesheet']

        running_animation = [r'assets\characters\Phantom Assassin\Run.png', (1,8), False, 'spritesheet']
        idle_animation = [r'assets\characters\Phantom Assassin\Idle.png', (1,8), False, 'spritesheet']
        death_animation = [r'assets\characters\Phantom Assassin\Death.png', (1,6), False, 'spritesheet']
        atk1_animation = [r'assets\characters\Phantom Assassin\Attack1.png', (1,6), False, 'spritesheet']
        atk2_animation = [r'assets\characters\Phantom Assassin\Attack2.png', (1,6), False, 'spritesheet']
        # atk3_animation = [r'assets\characters\Phantom Assassin\Attack3.png', (1,6), False, 'spritesheet']
        # atk4_animation = [r'assets\characters\Phantom Assassin\Attack4.png', (1,6), False, 'spritesheet']


        # Attack Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count
        #   - bool [2] starts at zero
        #   - int [3] size multiplier
        #   - str [4] type: 'frames' or 'spritesheet'
        #   - bool [5] flipped
        # file path,                            frame count, starts at zero, size, type, flipped

        # circle slash 
        atk1 = [r'assets\attacks\Phantom Assassin\circle slash.png', (4, 5), False, 1.5, 'spritesheet', False]
        # cool slashes
        atk2 = [r'assets\attacks\Phantom Assassin\cool slashes.png', (4, 5), False, 3, 'spritesheet', False]
        # dash slash
        atk3 = [r'assets\attacks\Phantom Assassin\dash slash.png', (6, 5), False, 1, 'spritesheet', False]
        # dash
        atk4 = [r'assets\attacks\Phantom Assassin\dash.png', (1, 6), False, 2, 'spritesheet', False]
        # slashes
        atk5 = [r'assets\attacks\Phantom Assassin\slashes.png', (4, 5), False, 3, 'spritesheet', False]
        # x slash
        atk6 = [r'assets\attacks\Phantom Assassin\x slash.png', (3, 5), False, 1, 'spritesheet', False]
        # cool x slash
        atk7 = [r'assets\attacks\Phantom Assassin\cool x slash.png', (2, 5), False, 1, 'spritesheet', False]
        # cool dash slash
        atk8 = [r'assets\attacks\Phantom Assassin\cool dash slash.png', (3, 5), False, 1, 'spritesheet', False]

        # Attack Frame Count
        #   - if not spritesheet, use actual attack count
        self.attack_frames = {
            'atk1frames': atk1[1][0] * atk1[1][1], # 20
            'atk2frames': atk2[1][0] * atk2[1][1], # 20
            'atk3frames': atk3[1][0] * atk3[1][1], # 30
            'atk4frames': atk4[1][0] * atk4[1][1], # 6
            'atk5frames': atk5[1][0] * atk5[1][1], # 20
            'atk6frames': (atk6[1][0] * atk6[1][1]) - 1, # 14 # -1 frame is deleted
            'atk7frames': atk7[1][0] * atk7[1][1], # 10
            'atk8frames': atk8[1][0] * atk8[1][1], # 45

        }

        


        # For projectile damage
        # self.sample = self.base_damage['atk4dmg'][0]

        # apply Sound Effect Volume
        self.sound1.set_volume(sound1[1])
        self.sound2.set_volume(sound2[1])
        self.sound3.set_volume(sound3[1])
        self.sound4.set_volume(sound4[1])

        # basic slash animation frames
        basic_slash = [r'assets\attacks\Basic Attack\1', BASIC_SLASH_ANIMATION, 1, BASIC_SLASH_SIZE, 0]
        self.basic_slash = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], basic_slash[3], basic_slash[4], True, False)
        self.basic_slash_flipped = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], basic_slash[3], basic_slash[4], True, True)
        
        # Skill Icons Source
        default_skill_size = (ICON_WIDTH, ICON_HEIGHT) #touple type shi
        sk_1 = [r'assets\skill icons\phantom_assassin\1.jpg', default_skill_size]
        sk_2 = [r'assets\skill icons\phantom_assassin\2.jpg', default_skill_size]
        sk_3 = [r'assets\skill icons\phantom_assassin\3.jpg', default_skill_size]
        sk_4 = [r'assets\skill icons\phantom_assassin\4.jpg', default_skill_size]
        sp = [r'assets\skill icons\phantom_assassin\sp.jpg', default_skill_size]
        sp_sk_1 = [r'assets\skill icons\phantom_assassin\1 sp.jpg', default_skill_size]
        # sp_sk_2 = [r'assets\skill icons\phantom_assassin\2 sp.jpg', default_skill_size]
        sp_sk_3 = [r'assets\skill icons\phantom_assassin\3 sp.jpg', default_skill_size]
        sp_sk_4 = [r'assets\skill icons\phantom_assassin\4 sp.jpg', default_skill_size]

        skill_1_icon = self.load_img_scaled(sk_1[0], sk_1[1])
        skill_2_icon = self.load_img_scaled(sk_2[0], sk_2[1])
        skill_3_icon = self.load_img_scaled(sk_3[0], sk_3[1])
        skill_4_icon = self.load_img_scaled(sk_4[0], sk_4[1])
        special_icon = self.load_img_scaled(sp[0], sp[1])
        special_skill_1_icon = self.load_img_scaled(sp_sk_1[0], sp_sk_1[1])
        special_skill_2_icon = skill_2_icon # same
        special_skill_3_icon = self.load_img_scaled(sp_sk_3[0], sp_sk_3[1])
        special_skill_4_icon = self.load_img_scaled(sp_sk_4[0], sp_sk_4[1])
        
        # Load Attack Frames (use the frame source)
        self.atk1 = self.load_img_frames_v2(atk1[0], atk1[1], atk1[2], atk1[3], atk1[4], atk1[5])
        self.atk1_flipped = self.load_img_frames_v2(atk1[0], atk1[1], atk1[2], atk1[3], atk1[4], True)

        self.atk2 = self.load_img_frames_v2(atk2[0], atk2[1], atk2[2], atk2[3], atk2[4], atk2[5])
        self.atk2_flipped = self.load_img_frames_v2(atk2[0], atk2[1], atk2[2], atk2[3], atk2[4], True)

        self.atk3 = self.load_img_frames_v2(atk3[0], atk3[1], atk3[2], atk3[3], atk3[4], atk3[5])
        self.atk4 = self.load_img_frames_v2(atk4[0], atk4[1], atk4[2], atk4[3], atk4[4], atk4[5])
        self.atk4_flipped = self.load_img_frames_v2(atk4[0], atk4[1], atk4[2], atk4[3], atk4[4], True)

        self.atk5 = self.load_img_frames_v2(atk5[0], atk5[1], atk5[2], atk5[3], atk5[4], atk5[5])
        self.atk6 = self.load_img_frames_v2(atk6[0], atk6[1], atk6[2], atk6[3], atk6[4], atk6[5])
        self.atk6.pop(-2)
        self.atk7 = self.load_img_frames_v2(atk7[0], atk7[1], atk7[2], atk7[3], atk7[4], atk7[5])
        self.atk8 = self.load_img_frames_v2(atk8[0], atk8[1], atk8[2], atk8[3], atk8[4], atk8[5])

        # inherited (please confirm the atk_frames if the attack is correct)
        self.atk1_damage = (
            self.base_damage['atk1dmg'][0],
            self.base_damage['atk1dmg'][1]
        )

        self.atk2_damage = (
            self.dmg_per_frame(self.base_damage['atk2dmg'][0], self.atk6),
            self.base_damage['atk2dmg'][1]
        )

        self.atk3_damage = (
            self.dmg_per_frame(self.base_damage['atk3dmg'][0], self.atk3),
            self.base_damage['atk3dmg'][1]
        )

        self.sp_damage = (
            self.dmg_per_frame(self.base_damage['atk4dmg'][0], self.atk5),
            self.base_damage['atk4dmg'][1]
        )

        
        self.sp_atk1_damage = (
            self.base_damage['atk5dmg'][0],
            self.base_damage['atk5dmg'][1]
        )

        self.sp_atk2_damage = (
            self.dmg_per_frame(self.base_damage['atk6dmg'][0], self.atk7),
            self.base_damage['atk6dmg'][1]
        )

        self.sp_atk3_damage = (
            self.dmg_per_frame(self.base_damage['atk7dmg'][0], self.atk8),
            self.base_damage['atk7dmg'][1]
        )

        self.sp_atk4_damage = (
            self.dmg_per_frame(self.base_damage['atk8dmg'][0], self.atk2),
            self.base_damage['atk8dmg'][1]
        )

        
        self.blank_frame = [
            pygame.transform.rotozoom(
            pygame.image.load(r"assets\attacks\forest ranger\atk4\blank frame\beam_extension_effect_10.png").convert_alpha(),
            angle=0, scale=1.0)
            ]

        # Load Character Frames (search for the correct method to use in the base class (Player))
        self.player_jump = self.load_img_frames_v2(jumping_animation[0], jumping_animation[1], jumping_animation[2], self.char_size, jumping_animation[3])
        self.player_jump_flipped = self.load_img_frames_v2(jumping_animation[0], jumping_animation[1], jumping_animation[2], self.char_size, jumping_animation[3], True)
        self.player_falling = self.load_img_frames_v2(falling_animation[0], falling_animation[1], falling_animation[2], self.char_size, falling_animation[3])
        self.player_falling_flipped = self.load_img_frames_v2(falling_animation[0], falling_animation[1], falling_animation[2], self.char_size, falling_animation[3], True)  

        self.player_jump = self.player_jump + self.player_falling
        self.player_jump_flipped = self.player_jump_flipped + self.player_falling_flipped
         
        self.player_idle = self.load_img_frames_v2(idle_animation[0], idle_animation[1], idle_animation[2], self.char_size, idle_animation[3])
        self.player_idle_flipped = self.load_img_frames_v2(idle_animation[0], idle_animation[1], idle_animation[2], self.char_size, idle_animation[3], True)
        self.player_run = self.load_img_frames_v2(running_animation[0], running_animation[1], running_animation[2], self.char_size, running_animation[3])
        self.player_run_flipped = self.load_img_frames_v2(running_animation[0], running_animation[1], running_animation[2], self.char_size, running_animation[3], True)
        self.player_death = self.load_img_frames_v2(death_animation[0], death_animation[1], death_animation[2], self.char_size, death_animation[3])
        self.player_death_flipped = self.load_img_frames_v2(death_animation[0], death_animation[1], death_animation[2], self.char_size, death_animation[3], True)
        self.player_atk1 = self.load_img_frames_v2(atk1_animation[0], atk1_animation[1], atk1_animation[2], self.char_size, atk1_animation[3])
        self.player_atk1_flipped = self.load_img_frames_v2(atk1_animation[0], atk1_animation[1], atk1_animation[2], self.char_size, atk1_animation[3], True)
        self.player_atk2 = self.player_atk1
        self.player_atk2_flipped = self.player_atk1_flipped
        self.player_atk3 = self.load_img_frames_v2(atk2_animation[0], atk2_animation[1], atk2_animation[2], self.char_size, atk2_animation[3])
        self.player_atk3_flipped = self.load_img_frames_v2(atk2_animation[0], atk2_animation[1], atk2_animation[2], self.char_size, atk2_animation[3], True)
        self.player_sp = self.player_atk3
        self.player_sp_flipped = self.player_atk3_flipped

        self.player_basic = self.player_atk1
        self.player_basic_flipped = self.player_atk1_flipped

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

        # Application
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 40 * 0.01 = 1.2
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.3 + 40 * 0.01 = 5.7
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.1 + 26 * 0.1 = 2.7

        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()
        
        # set to new hp/mana
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana 

        # Player Icon Rects
        self.setup_skill_icon_rects(
            skill_icons=[
                skill_1_icon,
                skill_2_icon,
                skill_3_icon,
                skill_4_icon
            ],
            special_icon=special_icon,
            special_skill_icons=[
                special_skill_1_icon,
                special_skill_2_icon,
                special_skill_3_icon,
                special_skill_4_icon
            ],
            x_pos_spacing = X_POS_SPACING,
            start_offset_x = START_OFFSET_X,
            spacing_x = SPACING_X,
            skill_y_offset = SKILL_Y_OFFSET,
            default_x_pos = DEFAULT_X_POS,
        )

        # mana values
        self.mana_cost_list = [
            self.atk1_mana_cost,
            self.atk2_mana_cost,
            self.atk3_mana_cost,
            self.sp_mana_cost
        ]
        self.special_mana_cost_list = [
            self.sp_atk1_mana_cost,
            self.sp_atk2_mana_cost,
            self.sp_atk3_mana_cost,
            self.sp_atk4_mana_cost
        ]
        # modify the index on which skill has lowest mana cost
        self.lowest_mana_cost = self.mana_cost_list[0]

        # apply Attacks class (responsible for all skills)
        # --------------- Basic Skills ---------------
        self.attacks = [
            # Skills
            Attacks(
                skill_rect = self.skill_1_rect,
                skill_img = skill_1_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[0],
                cooldown = self.atk1_cooldown,
                skill_name="Void Slash",
                skill_stats="- Damage:12@- Mana Cost:40",
                skill_desc="Damages enemies hit in vicinity.@- Distance: Short"
            ),
            Attacks(
                skill_rect = self.skill_2_rect,
                skill_img = skill_2_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[1],
                cooldown = self.atk2_cooldown
            ),
            Attacks(
                skill_rect = self.skill_3_rect,
                skill_img = skill_3_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[2],
                cooldown = self.atk3_cooldown
            ),
            Attacks(
                skill_rect = self.skill_4_rect,
                skill_img = skill_4_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[3],
                cooldown = self.atk4_cooldown
            ),
            # Basic Attack (icon can be changed)
            Attacks(
                mana_cost=0,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana,
                # ----------------------
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,   
            ),
            # Special Skill
            Attacks(
                skill_rect=self.special_rect,
                skill_img=special_icon,
                mana=0,
                mana_cost=0,
                special_skill=True,
                # ----------------------
                cooldown=DEFAULT_SPECIAL_SKILL_COOLDOWN,
            )
        ]
     
        for n, atk in enumerate(self.attacks):
            atk.skill_count = n


        # --------------- Special Skills ---------------
        self.attacks_special = [
            # Skills
            Attacks(
                skill_rect = self.special_skill_1_rect,
                skill_img = special_skill_1_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[0],
                cooldown = self.special_atk1_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_2_rect,
                skill_img = special_skill_2_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[1],
                cooldown = self.special_atk2_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_3_rect,
                skill_img = special_skill_3_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[2],
                cooldown = self.special_atk3_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_4_rect,
                skill_img = special_skill_4_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[3],
                cooldown = self.special_atk4_cooldown
            ),
            # Basic Attack (icon can be changed)
            Attacks(
                mana_cost=0,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana,
                # ----------------------
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,   
            )
        ]

        # Define which skills have i-frames (invulnerability)
        self.skill_iframes_config = {
            'attacking1': False,   
            'attacking2': False,  
            'attacking3': False,  
            'sp_attacking': True,      
        }

        # Apply speed modifier to base speed
        self.speed = RUNNING_SPEED * 1.1  # speed_modifier: 0.1
        self.default_speed = self.speed

        self.skill_1 = self.attacks[0]
        self.skill_2 = self.attacks[1]
        self.skill_3 = self.attacks[2]
        self.skill_4 = self.attacks[3]
        self.basic_attack = self.attacks[4]
        self.activate_special = self.attacks[5]

        self.special_skill_1 = self.attacks_special[0]
        self.special_skill_2 = self.attacks_special[1]
        self.special_skill_3 = self.attacks_special[2]
        self.special_skill_4 = self.attacks_special[3]
        self.special_attack = self.attacks_special[4]
        

    def atk1_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk1_index, anim_active = self.animate(self.player_atk1, self.player_atk1_index, loop=False, basic_atk=True)
        else:
            self.player_atk1_index_flipped, anim_active = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False, basic_atk=True)

        self.last_atk_time -= animation_speed

        if not anim_active:
            self.attacking1 = False
            self.basic_attacking = False  # Only matters if this was a basic attack
            self.player_atk1_index = 0
            self.player_atk1_index_flipped = 0    

            
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        """The most crucial part of collecting user input.
        - Processes player input each frame, handling movement and skill casting based on state."""
        # ---------- Core ----------        
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.is_dead():
            return
        
        # ---------- Moving ----------
        if self.can_move():
            self.player_movement(right_hotkey, left_hotkey, jump_hotkey, current_time,
                speed_modifier = 0,
                special_active_speed = 0.1,
                jump_force = self.jump_force,
                jump_force_modifier = 0.04
                )
            
        # ---------- Casting ----------
        if self.is_frozen():
            return
        
        if self.is_silenced() and not basic_hotkey:
            return
            
        
    
        if self.is_pressing(hotkey1) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 0):
                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 500),
                        frame_count = self.count_atk_frames(self.atk1),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=100
                    )
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 30, True),
                        y=self.attack_position(self.rect, 'y', -3, False),
                        frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=10 if self.facing_right else -10  ,
                        dmg=self.atk1_damage[0],
                        final_dmg=self.atk1_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound1, None, None),

                        hitbox_scale_x=0.4,
                        hitbox_scale_y=0.4
                        ))
                    
                    self.consume_mana(self.attacks, 0)
                    self.reset_skill_cooldown(self.attacks, 0, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking1",
                        ani_index="player_atk1", ani_index_flipped="player_atk1")
        



            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 0):
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 500),
                        frame_count = self.count_atk_frames(self.atk1),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=100
                    )
                    for i in [(500, 10, self.atk1_damage[0]), (1000, 5, self.sp_atk1_damage[0])]:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', 30, True),
                            y=self.attack_position(self.rect, 'y', -3, False),
                            frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
                            frame_duration=frame_duration,
                            repeat_animation=repeat_animation,
                            speed=i[1] if self.facing_right else -i[1],
                            dmg=i[2],
                            final_dmg=self.sp_atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, i[0]),
                            sound=(True, self.sound1, None, None),

                            hitbox_scale_x=0.4,
                            hitbox_scale_y=0.4
                            ))
                    
                    self.consume_mana(self.attacks_special, 0)
                    self.reset_skill_cooldown(self.attacks_special, 0, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking1",
                        ani_index="player_atk1", ani_index_flipped="player_atk1")


















        elif self.is_pressing(hotkey2) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 1):
                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1000),
                        frame_count = self.count_atk_frames(self.atk6),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=100
                    )
                    
                    # BLANK FRAME
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', 0, False),
                        frames=self.attack_frame_count(self.blank_frame),
                        frame_duration=50,
                        repeat_animation=20,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(False, 0),
                        sound=(True, self.sound2, None, None),
                        follow=(False,True),
                        follow_self=True,
                        stop_movement=(True, 1, 2),


                        hitbox_scale_x=0.2,
                        hitbox_scale_y=0.4,

                        spawn_attack={
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.atk6,
                                'frame_duration': frame_duration,
                                'repeat_animation': repeat_animation,
                                'speed': 0,
                                'dmg': self.atk2_damage[0],
                                'final_dmg': self.atk2_damage[1], # also used by blank frame
                                'who_attacks': self,
                                'who_attacked': self.enemy,
                                'moving': False,
                                'sound': (True, self.sound2, None, None),
                                'delay': (False, 500),
                                'stop_movement': (True, 1, 2),
                                'follow': (False, True),
                                'follow_offset': (0, 20),
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.4,
                            }
                        }
                    ))
                    
                    self.consume_mana(self.attacks, 1)
                    self.reset_skill_cooldown(self.attacks, 1, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking2",
                        ani_index="player_atk2", ani_index_flipped="player_atk2")


                   
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 1):
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 700),
                        frame_count = self.count_atk_frames(self.atk7),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=100
                    )
                    
                    # BLANK FRAME
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', 0, False),
                        frames=self.attack_frame_count(self.blank_frame),
                        frame_duration=50,
                        repeat_animation=20,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(False, 0),
                        sound=(True, self.sound2, None, None),
                        follow=(False,True),
                        follow_self=True,
                        stop_movement=(True, 1, 2),


                        hitbox_scale_x=0.2,
                        hitbox_scale_y=0.4,

                        spawn_attack={
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.atk7,
                                'frame_duration': frame_duration,
                                'repeat_animation': repeat_animation,
                                'speed': self.directional_speed(5),
                                'dmg': self.sp_atk2_damage[0],
                                'final_dmg': self.sp_atk2_damage[1], # also used by blank frame
                                'who_attacks': self,
                                'who_attacked': self.enemy,
                                'moving': True,
                                'continuous_dmg': True,
                                'sound': (True, self.sound2, None, None),
                                'delay': (False, 200),
                                'stop_movement': (True, 1, 2),
                                # 'follow': (False, True),
                                'stun':(True, 10),
                                'follow_offset': (0, 20),
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.4,
                            }
                        }
                    ))

                    self.consume_mana(self.attacks_special, 1)
                    self.reset_skill_cooldown(self.attacks_special, 1, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking2",
                        ani_index="player_atk2", ani_index_flipped="player_atk2")

        





















        elif self.is_pressing(hotkey3) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 2):
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.count_atk_frames(self.atk2),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )
                    # dash ani
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', -15, True),
                        y=self.attack_position(self.rect, 'y', -30, False),
                        frames=self.attack_frame_count(self.atk4, self.atk4_flipped),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),


                        hitbox_scale_x=0.4,
                        hitbox_scale_y=0.4
                        ))
                    

                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1000),
                        frame_count = self.count_atk_frames(self.atk3),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )

                    # BLANK FRAME
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', 0, False),
                        frames=self.attack_frame_count(self.blank_frame),
                        frame_duration=50,
                        repeat_animation=20,
                        speed=0,
                        dmg=self.atk3_damage[1],
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),
                        follow=(False,True),
                        follow_self=True,
                        stop_movement=(True, 1, 2),


                        hitbox_scale_x=0.2,
                        hitbox_scale_y=0.4,

                        spawn_attack={
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.atk3,
                                'frame_duration': frame_duration,
                                'repeat_animation': repeat_animation,
                                'speed': 0,
                                'dmg': self.atk3_damage[0],
                                'final_dmg': self.atk3_damage[1], # also used by blank frame
                                'who_attacks': self,
                                'who_attacked': self.enemy,
                                'moving': False,
                                'sound': (True, self.sound3, None, None),
                                'delay': (True, 500),
                                'stop_movement': (True, 1, 2),
                                'follow': (False, True),
                                'follow_offset': (0, 20),
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.4,
                            }
                        }
                        ))
                    
                    self.consume_mana(self.attacks, 2)
                    self.reset_skill_cooldown(self.attacks, 2, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking3",
                        ani_index="player_atk3", ani_index_flipped="player_atk3")
                    

                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 2):
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.count_atk_frames(self.atk2),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )
                    # dash ani
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', -15, True),
                        y=self.attack_position(self.rect, 'y', -30, False),
                        frames=self.attack_frame_count(self.atk4, self.atk4_flipped),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),


                        hitbox_scale_x=0.4,
                        hitbox_scale_y=0.4
                        ))
                    

                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1000),
                        frame_count = self.count_atk_frames(self.atk8),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )

                    # BLANK FRAME
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', 0, False),
                        frames=self.attack_frame_count(self.blank_frame),
                        frame_duration=50,
                        repeat_animation=20,
                        speed=0,
                        dmg=self.sp_atk3_damage[1],
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),
                        follow=(False,True),
                        follow_self=True,
                        stop_movement=(True, 1, 2),


                        hitbox_scale_x=0.2,
                        hitbox_scale_y=0.4,

                        spawn_attack={
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.atk8,
                                'frame_duration': frame_duration,
                                'repeat_animation': repeat_animation,
                                'speed': 0,
                                'dmg': self.sp_atk3_damage[0],
                                'final_dmg': self.sp_atk3_damage[1], # also used by blank frame
                                'who_attacks': self,
                                'who_attacked': self.enemy,
                                'moving': False,
                                'sound': (True, self.sound3, None, None),
                                'delay': (True, 500),
                                'stop_movement': (True, 1, 2),
                                'follow': (False, True),
                                'follow_offset': (0, 20),
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.4,
                            }
                        }
                        ))
                    
                    self.consume_mana(self.attacks_special, 2)
                    self.reset_skill_cooldown(self.attacks_special, 2, current_time)
                    self.modify_current_state(
                        running=False, animation="attacking3",
                        ani_index="player_atk3", ani_index_flipped="player_atk3")





















        elif self.is_pressing(hotkey4) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 3):
                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.count_atk_frames(self.atk4),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )
                    # dash ani
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', -70, False),
                        frames=self.attack_frame_count(self.atk4, self.atk4_flipped),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),


                        hitbox_scale_x=0.4,
                        hitbox_scale_y=0.4
                        ))
                    

                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.count_atk_frames(self.atk5),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )

                    # slashes
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 260, True),
                        y=self.attack_position(self.rect, 'y', -110, False),
                        frames=self.attack_frame_count(self.atk5),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=self.sp_damage[0],
                        final_dmg=self.sp_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=False,
                        delay=(True, 900),
                        sound=(True, self.sound4, None, None),
                        stun=(True, -30),

                        hitbox_scale_x=0.5,
                        hitbox_scale_y=0.3
                        ))
                    self.consume_mana(self.attacks, 3)
                    self.reset_skill_cooldown(self.attacks, 3, current_time)
                    self.modify_current_state(
                        running=False, animation="sp_attacking",
                        ani_index="player_sp", ani_index_flipped="player_sp")
                    


                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 3):

                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.count_atk_frames(self.atk4),
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )
                    # dash ani
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 0, True),
                        y=self.attack_position(self.rect, 'y', -70, False),
                        frames=self.attack_frame_count(self.atk4, self.atk4_flipped),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=0,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 500),
                        sound=(True, self.sound3, None, None),

                        hitbox_scale_x=0.4,
                        hitbox_scale_y=0.4
                        ))
                    

                    
                    frame_duration, repeat_animation = self.skill_duration(
                        set_mode = ('seconds', 1300),
                        frame_count = self.attack_frames['atk2frames'],
                        repeat_animation=1,
                        frame_divisor=1,
                        set_max_frame_duration=80
                    )

                    # slashes
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 260, True),
                        y=self.attack_position(self.rect, 'y', -110, False),
                        frames=self.attack_frame_count(self.atk2),
                        frame_duration=frame_duration,
                        repeat_animation=repeat_animation,
                        speed=0,
                        dmg=self.sp_atk4_damage[0],
                        final_dmg=self.sp_atk4_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=False,
                        delay=(True, 900),
                        sound=(True, self.sound4, None, None),
                        stun=(True, -30),

                        hitbox_scale_x=0.5,
                        hitbox_scale_y=0.3
                        ))
                    self.consume_mana(self.attacks_special, 3)
                    self.reset_skill_cooldown(self.attacks_special, 3, current_time)
                    self.modify_current_state(
                        running=False, animation="sp_attacking",
                        ani_index="player_sp", ani_index_flipped="player_sp")

        























        elif self.is_pressing(basic_hotkey) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.can_basic_attack():
                    
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 85, True),
                        y=self.attack_position(self.rect, 'y', -35, False),
                        frames=self.attack_frame_count(self.basic_slash, self.basic_slash_flipped),
                        frame_duration=BASIC_FRAME_DURATION,
                        repeat_animation=1,
                        speed=0,
                        dmg=self.basic_attack_damage,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, self.calculate_attack_delay(500)),
                        sound=(True, self.basic_sound, None, None),

                        hitbox_scale_x=0.7,
                        hitbox_scale_y=0.4,

                        is_basic_attack=True
                        ))
                    self.consume_mana(self.attacks, 4)
                    self.reset_skill_cooldown(self.attacks, 4, current_time)
                    self.modify_current_state(
                        running=False, animation="basic_attacking",
                        ani_index="player_basic", ani_index_flipped="player_basic")
                        
                    
                    self.modify_attack_state(current_time, 'basic')
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 4):
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', 85, True),
                        y=self.attack_position(self.rect, 'y', -35, False),
                        frames=self.attack_frame_count(self.basic_slash, self.basic_slash_flipped),
                        frame_duration=BASIC_FRAME_DURATION,
                        repeat_animation=1,
                        speed=0,
                        dmg=self.basic_attack_damage,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, self.calculate_attack_delay(500)),
                        sound=(True, self.basic_sound, None, None),

                        hitbox_scale_x=0.7,
                        hitbox_scale_y=0.4,

                        is_basic_attack=True
                        ))
                    self.consume_mana(self.attacks_special, 4)
                    self.reset_skill_cooldown(self.attacks_special, 4, current_time)
                    self.modify_current_state(
                        running=False, animation="basic_attacking",
                        ani_index="player_basic", ani_index_flipped="player_basic")
                        
                    
                    self.modify_attack_state(current_time, 'basic')

        elif self.is_pressing(special_hotkey) and not self.is_busy_attacking():
            if self.special >= MAX_SPECIAL:
                self.special_active = True
                self.special_sound.play()

            



    def update(self):
       
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.trigger_dash('attacking2', speed=-7, max_distance=200, delay=100)
            self.atk2_animation()
        elif self.attacking3:
            self.trigger_dash('attacking3', speed=30, max_distance=300, delay=500)
            self.atk3_animation()
        elif self.sp_attacking:
            self.y_velocity = -2.5
            self.trigger_dash('sp_attacking', speed=50, max_distance=500, delay=500)

            self.sp_animation()
        elif self.basic_attacking:
            self.basic_animation()
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # dash fix
        if not self.attacking2 and not self.attacking3 and not self.sp_attacking:
            self.reset_dash()



        # if self.dashing:
        #     print('DASSSHING!')
        # print(self.dash_delay_triggered)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity


        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)
        self.rect.y += self.y_visual_offset


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

        
        super().update()
        # hitbox visual bug fix
        self.hitbox_rect.y -= self.y_visual_offset
        if global_vars.SHOW_HITBOX:
            self.draw_hitbox(screen)