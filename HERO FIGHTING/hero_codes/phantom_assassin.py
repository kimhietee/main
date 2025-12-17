import pygame
from player import Player
from heroes import Attacks, Attack_Display

from global_vars import (
    # icon
    ICON_WIDTH, ICON_HEIGHT, 
    # positioning
    X_POS_SPACING, START_OFFSET_X, SKILL_Y_OFFSET, SPACING_X, JUMP_DELAY,
    DEFAULT_X_POS, DEFAULT_Y_POS, DEFAULT_JUMP_FORCE,
    TOTAL_WIDTH, ZERO_WIDTH,
    # .
    DEFAULT_SPECIAL_SKILL_COOLDOWN,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
)
class Phantom_Assasin(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)

        # ----- Core -----
        self.player_type = player_type
        self.name = "Phantom Assasin"
        self.hitbox_rect = pygame.rect(0, 0, 50, 100)
        self.x = 50
        self.y = 50
        self.width = 200

        # ----- Hero Specifications -----
        # Stats
        self.strength = 40
        self.intelligence = 40
        self.agility = 30

        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION

        self.atk1_mana_cost = 20
        self.atk2_mana_cost = 20
        self.atk3_mana_cost = 20
        self.sp_mana_cost = 20
        
        self.atk1_cooldown = 1000
        self.atk2_cooldown = 1000
        self.atk3_cooldown = 1000
        self.sp_cooldown = 1000

        # Add more if damage list is not sufficient
        #   - base_damage, attack_frames, *variable
        #       *refer to the Player's existing variables, or create one if not enough
        #   - [0] = damage, [1] = final damage (applies at last frame)
        self.base_damage = {
            'atk1dmg': (10, 0),
            'atk2dmg': (15, 0),
            'atk3dmg': (10, 0),
            'atk4dmg': (10, 0),
            # For projectile damage
            #'sample': 20
        }

        # Sound Effects
        #   - str [0] file path
        #   - int [1] max volume
        sound1 = [r'sample', 0.7]
        sound2 = [r'sample', 0.7]
        sound3 = [r'sample', 0.7]
        sound4 = [r'sample', 0.7]
        self.sound1 = self.load_sound(sound1[0])
        self.sound2 = self.load_sound(sound2[0])
        self.sound3 = self.load_sound(sound3[0])
        self.sound4 = self.load_sound(sound4[0])


        # Character Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count
        #   - bool [2] starts at zero 
        basic_attack_animation = [r'sample', 5, False]
        jumping_animation = [r'sample', 5, False]
        running_animation = [r'sample', 5, False]
        idle_animation = [r'sample', 5, False]
        death_animation = [r'sample', 5, False]
        atk1_animation = [r'sample', 5, False]
        atk2_animation = [r'sample', 5, False]
        atk3_animiation = [r'sample', 5, False]
        atk4_animation = [r'sample', 5, False]

        # Attack Frame Count
        self.attack_frames = {
            'atk1frames': 24,
            'atk2frames': 14,
            'atk3frames': 34,
            'atk4frames': 52,
        }

        # Attack Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count
        #   - bool [2] starts at zero
        atk1 = [r'sample', self.attack_frames['atk1frames'], False]
        atk2 = [r'sample', self.attack_frames['atk2frames'], False]
        atk3 = [r'sample', self.attack_frames['atk3frames'], False]
        atk4 = [r'sample', self.attack_frames['atk4frames'], False]
        
        # Skill Icons Source
        default_skill_size = (ICON_WIDTH, ICON_HEIGHT)
        sk_1 = [r'sample', default_skill_size]
        sk_2 = [r'sample', default_skill_size]
        sk_3 = [r'sample', default_skill_size]
        sk_4 = [r'sample', default_skill_size]
        sp = [r'sample', default_skill_size]
        sp_sk_1 = [r'sample', default_skill_size]
        sp_sk_2 = [r'sample', default_skill_size]
        sp_sk_3 = [r'sample', default_skill_size]
        sp_sk_4 = [r'sample', default_skill_size]

        skill_1_icon = self.load_img_scaled(sk_1[0], sk_1[1])
        skill_2_icon = self.load_img_scaled(sk_2[0], sk_2[1])
        skill_3_icon = self.load_img_scaled(sk_3[0], sk_3[1])
        skill_4_icon = self.load_img_scaled(sk_4[0], sk_4[1])
        special_icon = self.load_img_scaled(sp[0], sp[1])
        special_skill_1_icon = self.load_img_scaled(sp_sk_1[0], sp_sk_1[1])
        special_skill_2_icon = self.load_img_scaled(sp_sk_2[0], sp_sk_2[1])
        special_skill_3_icon = self.load_img_scaled(sp_sk_3[0], sp_sk_3[1])
        special_skill_4_icon = self.load_img_scaled(sp_sk_4[0], sp_sk_4[1])
        
        # Load Attack Frames (use the frame source)
        self.atk1 = None
        self.atk2 = None
        self.atk3 = None
        self.atk4 = None

        # Load Character Frames (search for the correct method to use in the base class (Player))
        self.player_basic = None
        self.player_basic_flipped = None
        self.player_jump = None
        self.player_jump_flipped = None
        self.player_idle = None
        self.player_idle_flipped = None
        self.player_run = None
        self.player_run_flipped = None
        self.player_death = None
        self.player_death_flipped = None
        self.player_atk1 = None
        self.player_atk1_flipped = None
        self.player_atk2 = None
        self.player_atk2_flipped = None
        self.player_atk3 = None
        self.player_atk3_flipped = None
        self.player_sp = None
        self.player_sp_flipped = None

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

        # Application
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult
        # set to new hp/mana
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana 

        # inherited
        self.atk1_damage = (
            self.base_damage['atk1dmg'][0] / self.attack_frames['atk1frames'],
            self.base_damage['atk1dmg'][0])
        self.atk2_damage = (
            self.base_damage['atk2dmg'][0] / self.attack_frames['atk2frames'],
            self.base_damage['atk2dmg'][0])
        self.atk3_damage = (
            self.base_damage['atk3dmg'][0] / self.attack_frames['atk3frames'],
            self.base_damage['atk3dmg'][0])
        self.sp_damage = (
            self.base_damage['atk4dmg'][0] / self.attack_frames['atk4frames'],
            self.base_damage['atk4dmg'][0])
        # For projectile damage
        # self.sample = self.base_damage['atk4dmg'][0]

        # apply Sound Effect Volume
        self.sound1.set_volume(sound1[1])
        self.sound2.set_volume(sound2[1])
        self.sound3.set_volume(sound3[1])
        self.sound4.set_volume(sound4[1])

        # player Icon Rects
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
                cooldown = self.atk1_cooldown
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

        # --------------- Special Skills ---------------
        self.special_attacks = [
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

        self.skill_1 = self.attacks[0]
        self.skill_2 = self.attacks[1]
        self.skill_3 = self.attacks[2]
        self.skill_4 = self.attacks[3]
        self.basic_attack = self.attacks[4]
        self.activate_special = self.attacks[5]

        self.special_skill_1 = self.special_attacks[0]
        self.special_skill_2 = self.special_attacks[1]
        self.special_skill_3 = self.special_attacks[2]
        self.special_skill_4 = self.special_attacks[3]
        self.special_attack = self.special_attacks[4]

    def player_movement(self, right_hotkey, left_hotkey, jump_hotkey, current_time, speed_modifier=0, special_active_speed=0.1):
        '''
        speed_modifier: base speed = 0
        special_active_speed: increase speed when special mode
        '''
        if self.is_not_attacking():
            if right_hotkey:  # Move right
                self.running = True
                self.facing_right = True
                self.x_pos += (self.speed + ((self.speed * special_active_speed) if self.special_active else speed_modifier))
                if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                    self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
            elif left_hotkey:  # Move left
                self.running = True
                self.facing_right = False
                self.x_pos -= (self.speed + ((self.speed * special_active_speed) if self.special_active else speed_modifier))
                if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                    self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
            else:
                self.running = False

            if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                self.jumping = True
                self.y_velocity = DEFAULT_JUMP_FORCE  
                self.last_atk_time = current_time  # Update the last jump time
        
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
                special_active_speed = 0.1
                )
            
        # ---------- Casting ----------
        if self.is_frozen():
            return
        
        if self.is_silenced() and not basic_hotkey:
            return
            
        
        if not self.is_jumping():
            if self.is_pressing(hotkey1) and not self.is_busy_attacking():
                if self.is_skill_ready(self.mana, self.skill_1):
                    if self.is_in_basic_mode():

                        attack = Attack_Display(
                            x=self.rect.centerx - 20 if self.facing_right else self.rect.centerx + 20,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=6 if self.facing_right else -6,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, 800),
                            sound=(True, self.atk1_sound, None, None),

                            hitbox_scale_x=0.4,
                            hitbox_scale_y=0.4
                            )
                        
                    elif self.is_in_special_mode():
                        pass

            
        

            