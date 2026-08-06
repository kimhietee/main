from path_helper import resource_path
import pygame
import random
from player import Player
from heroes import Attacks, Attack_Display
import global_vars
from global_vars import (
    DEFAULT_CHAR_SIZE, DEFAULT_GRAVITY, X_POS_SPACING, START_OFFSET_X, 
    SPACING_X, SKILL_Y_OFFSET, DEFAULT_X_POS, ICON_WIDTH, ICON_HEIGHT, 
    BASIC_FRAME_DURATION, DEFAULT_ANIMATION_SPEED, DEFAULT_BASIC_ATK_DMG_BONUS,
    SPECIAL_DURATION, MAX_SPECIAL, DISABLE_MANA_REGEN, DISABLE_HEAL_REGEN,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    RUNNING_ANIMATION_SPEED, attack_display, screen, RUNNING_SPEED
)

class Fire_Wizard(Player):
    # Class-level attribute for hero display data (used by player_selector hover tooltip)
    HERO_DISPLAY_DATA = {
        "str": 40,
        "int": 40,
        "agi": 26,
        "base_atk": 0.1,
        "atk_time": 1750,
        "atk_spd_mod": 0.5,
        "atk_spd": 100,
        "hp_regen": 0.8,
        "mana_regen": 5.45,
        "move_speed": 2.2,
    }
    
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # ----- Core -----
        self.player_type = player_type
        self.name = "Fire Wizard"
        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)
        self.x = 50
        self.y = 50
        self.width = 200
        self.char_size = DEFAULT_CHAR_SIZE
        
        # ----- Hero Specifications -----
        # Stats
        self.strength = 40
        self.intelligence = 40
        self.agility = 26 # real agility = 27
        
        self.base_health_regen = 0.8
        self.base_mana_regen = 5.45
        self.base_attack_damage = 0.1

        self.base_attack_speed = 100
        self.base_attack_time = 1750
        
        self.base_animation_speed = 120
        self.min_animation_speed = 70
        self.attack_speed_modifier = 0.5
        
        # Costs & Cooldowns
        self.atk1_mana_cost = 50
        self.atk2_mana_cost = 75
        self.atk3_mana_cost = 100
        self.sp_mana_cost = 200
        
        self.sp_atk1_mana_cost = 50
        self.sp_atk2_mana_cost = 80
        self.sp_atk3_mana_cost = 80  # 100 - 20%
        self.sp_atk4_mana_cost = 160 # 200 - 20%
        
        self.atk1_cooldown = 7000
        self.atk2_cooldown = 10000
        self.atk3_cooldown = 26000
        self.atk4_cooldown = 60000

        self.special_atk1_cooldown = 7000
        self.special_atk2_cooldown = 18000 # 5000 + 13000
        self.special_atk3_cooldown = 26000
        self.special_atk4_cooldown = 60000

        # Projectile & Skill Settings
        self.fireball_cast_range = 20
        self.special_fireball_cast_range = 20
        self.fire_spire_cast_range = 120
        self.fireblast_cast_range = 200

        self.fireball_speed = 6
        self.special_fireball_speed = 7
        self.fire_spire_speed = 1
        
        self.fireball_frame_duration = 100
        self.fireball_hitbox_size_modifier = 0.4
        self.special_fireball_offsets = [0, 33, 67, 100]
        self.special_fireball_damage_mult = 0.33
        
        self.fire_repeat_default = 6
        self.fire_duration = 20000 / self.fire_repeat_default
        self.special_fire_duration = 15000 / self.fire_repeat_default
        self.special_fire_delay_interval = 50
        self.special_fire_damage_mult = 0.5
        self.fire_count = [60*2, 120*2, 180*2]
        self.special_fire_count = [-200*3, -160*3, -120*3, -80*3, -40*3, 0, 40*3, 80*3, 120*3, 160*3, 200*3]
        
        self.fire_spire_repeat = 2
        self.fire_spire_frame_duration = 60
        self.fire_spire_damage_mult = 0.7
        
        self.fire_blast_count = [-1000, -500, 0, 500, 1000]
        self.fire_blast_damage_mult = 0.9

        # Damage Setup (Applying the 10% multiplier directly here to match PA's static base_damage approach)
        dmg_mult = 0.1
        self.base_damage = {
            'atk1dmg': (13 + (13 * dmg_mult), 0),
            'atk2dmg': (20 + (20 * dmg_mult), 0),
            'atk3dmg': (40 + (40 * dmg_mult), 0),
            'atk4dmg': (50 + (50 * dmg_mult), 10 + (10 * dmg_mult)),

            'sp_atk1dmg': ((13 * self.special_fireball_damage_mult) * 1.1, 0),
            'sp_atk2dmg': ((20 * self.special_fire_damage_mult) * 1.1, 0),
            'sp_atk3dmg': ((40 * self.fire_spire_damage_mult) * 1.1, 0),
            'sp_atk4dmg': ((50 * self.fire_blast_damage_mult) * 1.1, (10 * self.fire_blast_damage_mult) * 1.1)
        }

        # Sound Effects
        sound1 = [resource_path(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3'), 0.8]
        sound2 = [resource_path(r'assets\sound effects\fire_wizard\fire-sound-efftect-21991.mp3'), 0.5]
        sound3 = [resource_path(r'assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3'), 0.8]
        sound4 = [resource_path(r'assets\sound effects\fire_wizard\052168_huge-explosion-85199.mp3'), 0.7]
        
        self.atk1_sound = self.load_sound(sound1[0])
        self.atk2_sound = self.load_sound(sound2[0])
        self.atk3_sound = self.load_sound(sound3[0])
        self.sp_sound = self.load_sound(sound4[0])
        
        self.atk1_sound.set_volume(sound1[1] * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(sound2[1] * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(sound3[1] * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(sound4[1] * global_vars.MAIN_VOLUME)

        # Character Frame Source
        basic_ani = [resource_path(r'assets\characters\Fire wizard\slash pngs\Attack_1_'), 10, 1]
        # basic_ani = [resource_path(r'assets\characters\stickman\attack\Frame0'), 6, 0]

        jump_ani = [resource_path(r'assets\characters\Fire wizard\jump pngs\Jump_'), 6, 1]
        run_ani = [resource_path(r'assets\characters\Fire wizard\run pngs\Run_'), 8, 1]
        idle_ani= [resource_path(r'assets\characters\Fire wizard\idle pngs\image_0-'), 7, 1]
        atk1_ani= [resource_path(r'assets\characters\Fire wizard\fireball pngs\image_0-'), 8, 1]
        sp_ani= [resource_path(r'assets\characters\Fire wizard\flame jet pngs\image_0-'), 14, 1]
        death_ani= [resource_path(r'assets\characters\Fire wizard\dead\tile00'), 6, 1]

        # Attack Frame Source
        atk1 = [resource_path(r'assets\attacks\fire wizard\atk1'), 10, 1, 3] # FIRE_WIZARD_ATK1 reduced from 12 to 10
        atk2 = [resource_path(r'assets\attacks\fire wizard\atk2'), 53, 1, 0.3]
        atk3 = [resource_path(r'assets\attacks\fire wizard\atk3\png_'), 34, 1, 0.3]
        sp_atk = [resource_path(r'assets\attacks\fire wizard\sp atk'), 28, 1, 1.3]

        self.attack_frames = {
            'atk1frames': atk1[1],
            'atk2frames': atk2[1],
            'atk3frames': atk3[1],
            'atk4frames': sp_atk[1],
        }

        # Load Attack Frames (Using Fire Wizard specific loading methods)
        self.atk1 = self.load_img_frames_tile_method(atk1[0], atk1[1], atk1[2], atk1[3])
        self.atk1_flipped = self.load_img_frames_flipped_tile_method(atk1[0], atk1[1], atk1[2], atk1[3])
        self.atk2 = self.load_img_frames_numbering_method(atk2[0], atk2[1], atk2[2], atk2[3])
        self.atk3 = self.load_img_frames_numbering_method_simple(atk3[0], atk3[1], atk3[2], atk3[3])
        self.sp = self.load_img_frames_numbering_method(sp_atk[0], sp_atk[1], sp_atk[2], sp_atk[3])

        # Load Character Frames
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], self.char_size) # for stickman scale = 0.2
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], self.char_size)
        
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], self.char_size)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], self.char_size)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], self.char_size)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], self.char_size)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], self.char_size)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], self.char_size)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], self.char_size)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], self.char_size)  
        self.player_atk2 = self.player_atk1
        self.player_atk2_flipped = self.player_atk1_flipped
        self.player_atk3 = self.player_atk1
        self.player_atk3_flipped = self.player_atk1_flipped
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], self.char_size)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], self.char_size)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], self.char_size)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], self.char_size)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

        # Application
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana
        
        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength)
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence)
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True)

        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()
        self.bonus_type = "strength"
        self.bonus_value = self.strength

        self.speed = RUNNING_SPEED * 1.0  # speed_modifier: 0 (no change)
        self.default_speed = self.speed
        # Set to new hp/mana
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana 

        # Inherited Attack Damages
        self.atk1_damage = (self.base_damage['atk1dmg'][0], self.base_damage['atk1dmg'][1])
        self.atk2_damage = (self.dmg_per_frame(self.base_damage['atk2dmg'][0], self.atk2), self.base_damage['atk2dmg'][1])
        self.atk3_damage = (self.dmg_per_frame(self.base_damage['atk3dmg'][0], self.atk3), self.base_damage['atk3dmg'][1])
        self.sp_damage = (self.dmg_per_frame(self.base_damage['atk4dmg'][0], self.sp), self.base_damage['atk4dmg'][1])
        
        self.sp_atk1_damage = (self.base_damage['sp_atk1dmg'][0], self.base_damage['sp_atk1dmg'][1])
        self.sp_atk2_damage = (self.dmg_per_frame(self.base_damage['sp_atk2dmg'][0], self.atk2), self.base_damage['sp_atk2dmg'][1])
        self.sp_atk3_damage = (self.dmg_per_frame(self.base_damage['sp_atk3dmg'][0], self.atk3), self.base_damage['sp_atk3dmg'][1])
        self.sp_atk4_damage = (self.dmg_per_frame(self.base_damage['sp_atk4dmg'][0], self.sp), self.base_damage['sp_atk4dmg'][1])

        # Distances 
        self.fireball_hitbox_size = self.calculate_hitbox_size(self.atk1, self.fireball_hitbox_size_modifier)
        self.fire_spire_hitbox_size = self.calculate_hitbox_size(self.atk3)
        
        self.fireball_distance = self.calculate_attack_range(-self.fireball_cast_range, self.fireball_hitbox_size, self.fireball_speed, self.attack_frames['atk1frames'], self.fireball_frame_duration)
        self.special_fireball_distance = self.calculate_attack_range(-self.special_fireball_cast_range, self.fireball_hitbox_size, self.special_fireball_speed, self.attack_frames['atk1frames'], self.fireball_frame_duration)
        self.fire_spire_distance = self.calculate_attack_range(self.fire_spire_cast_range, self.fireball_hitbox_size, self.fire_spire_speed, self.attack_frames['atk3frames'], self.fire_spire_frame_duration)

        # Skill Icons Load
        skill_1_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\FireballIcon.webp'), (ICON_WIDTH, ICON_HEIGHT))
        skill_2_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\GlyphOfFireIcon.webp'), (ICON_WIDTH, ICON_HEIGHT))
        skill_3_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\RodOfPower29Icon.webp'), (ICON_WIDTH, ICON_HEIGHT))
        skill_4_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\MeteorIcon.webp'), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\kim special icon.png'), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\FlameReaveIcon29.webp'), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\SmiteIcon.webp'), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4_icon = self.load_img_scaled(resource_path(r'assets\skill icons\fire_wizard\VolcanicOrb29Icon.webp'), (ICON_WIDTH, ICON_HEIGHT))

        # Setup Skill Icon Rects natively like PA
        self.setup_skill_icon_rects(
            skill_icons=[skill_1_icon, skill_2_icon, skill_3_icon, skill_4_icon],
            special_icon=special_icon,
            special_skill_icons=[special_skill_1_icon, skill_2_icon, special_skill_3_icon, special_skill_4_icon],
            x_pos_spacing = X_POS_SPACING,
            start_offset_x = START_OFFSET_X,
            spacing_x = SPACING_X,
            skill_y_offset = SKILL_Y_OFFSET,
            default_x_pos = DEFAULT_X_POS,
        )

        self.mana_cost_list = [self.atk1_mana_cost, self.atk2_mana_cost, self.atk3_mana_cost, self.sp_mana_cost]
        self.special_mana_cost_list = [self.sp_atk1_mana_cost, self.sp_atk2_mana_cost, self.sp_atk3_mana_cost, self.sp_atk4_mana_cost]
        self.lowest_mana_cost = self.mana_cost_list[0]

        # --------------- Basic Skills ---------------
        self.attacks = [
            Attacks(
                skill_rect=self.skill_1_rect, skill_img=skill_1_icon, mana=self.mana,
                mana_cost=self.mana_cost_list[0], cooldown=self.atk1_cooldown, damage=[self.base_damage['atk1dmg'][0], self.base_damage['atk1dmg'][1]],
                skill_name='Fireball',
                skill_stats={'Lv': [1, 'blueviolet'], 'Damage': [0 , 'red'], 'Distance': [f'{self.fireball_distance}' + ' units', 'green']},
                skill_desc='Casts fireball in a short distance.@Enemies hit are damaged.'
            ),
            Attacks(
                skill_rect=self.skill_2_rect, skill_img=skill_2_icon, mana=self.mana,
                mana_cost=self.mana_cost_list[1], cooldown=self.atk2_cooldown, damage=[self.base_damage['atk2dmg'][0], self.base_damage['atk2dmg'][1]],
                skill_name='Inferno Flames',
                skill_stats={'Lv': [1, 'blueviolet'], 'Damage': [0 , 'red']},
                skill_desc=f'Sets the ground on fire, dealing damage@to enemies when in contact. Flames lasts@{self.fire_repeat_default} instances, each lasts {self.fire_duration/1000:.1f} seconds.@- Fire count: {len(self.fire_count)}@- Total Duration: {(self.fire_duration*self.fire_repeat_default)/1000:.1f}'
            ),
            Attacks(
                skill_rect=self.skill_3_rect, skill_img=skill_3_icon, mana=self.mana,
                mana_cost=self.mana_cost_list[2], cooldown=self.atk3_cooldown, damage=[self.base_damage['atk3dmg'][0], self.base_damage['atk3dmg'][1]],
                skill_name='Incineration',
                skill_stats={'Lv': [1, 'blueviolet'], 'Damage': [0 , 'red']},
                skill_desc='Ignites burst of fire on the ground,dealing@damage in a short amount of time.'
            ),
            Attacks(
                skill_rect=self.skill_4_rect, skill_img=skill_4_icon, mana=self.mana,
                mana_cost=self.mana_cost_list[3], cooldown=self.atk4_cooldown, damage=[self.base_damage['atk4dmg'][0], self.base_damage['atk4dmg'][1]],
                skill_name='Fire Blast',
                skill_stats={'Lv': [1, 'blueviolet'], 'Damage': [0 , 'red']},
                skill_desc='Casts fireblast on vicinity. Deals a massive@amount of damage to enemies in the area.'
            ),
            Attacks(
                mana_cost=0, cooldown=self.basic_attack_cooldown, mana=self.mana,
                skill_rect=self.basic_icon_rect, skill_img=self.basic_icon,   
                skill_name='Basic Attack', skill_stats={'Type': ['Melee', 'white']}
            ),
            Attacks(
                skill_rect=self.special_rect, skill_img=special_icon, mana=0, mana_cost=0, special_skill=True, cooldown=0,
                skill_name='Activate Special',
                skill_stats={'Type': ['Special', 'white'], 'Attack Increase': [f'{round((DEFAULT_BASIC_ATK_DMG_BONUS-1)*100,1)}%', 'green'], 'Move Speed': ['+ 10%', 'green'], 'Duration': ['30', 'white']},
                skill_desc='Provides unique buffs and abilities to hero.'
            )
        ]

        # --------------- Special Skills ---------------
        self.attacks_special = [
            Attacks(
                skill_rect=self.special_skill_1_rect, skill_img=special_skill_1_icon, mana=self.mana,
                mana_cost=self.special_mana_cost_list[0], cooldown=self.special_atk1_cooldown, damage=[self.base_damage['sp_atk1dmg'][0], self.base_damage['sp_atk1dmg'][1]],
                skill_name='Fireball',
                skill_stats={'Lv': [2, 'magenta'], 'Damage': [0 , 'red'], 'Distance': [f'{self.special_fireball_distance}' + ' units', 'green']},
                skill_desc=f'Casts a barrage of fireballs in a short@distance but damage is reduced. Enemies@hit are damaged.@- Fireball count: {len(self.special_fireball_offsets)}@- Damage per fireball: {self.special_fireball_damage_mult*100:.0f}%'
            ),
            Attacks(
                skill_rect=self.special_skill_2_rect, skill_img=skill_2_icon, mana=self.mana,
                mana_cost=self.special_mana_cost_list[1], cooldown=self.special_atk2_cooldown, damage=[self.base_damage['sp_atk2dmg'][0], self.base_damage['sp_atk2dmg'][1]],
                skill_name='Inferno Flames',
                skill_stats={'Lv': [2, 'magenta'], 'Damage': [0 , 'red']},
                skill_desc=f'Sets the area on fire around you, dealing half@damage to enemies in larger area. Flames lasts@{self.fire_repeat_default} instances, each lasts {self.special_fire_duration/1000:.1f} seconds.@- Fire count: {len(self.special_fire_count)}@- Total Duration: {(self.special_fire_duration*self.fire_repeat_default)/1000:.1f}'
            ),
            Attacks(
                skill_rect=self.special_skill_3_rect, skill_img=special_skill_3_icon, mana=self.mana,
                mana_cost=self.special_mana_cost_list[2], cooldown=self.special_atk3_cooldown, damage=[self.base_damage['sp_atk3dmg'][0], self.base_damage['sp_atk3dmg'][1]],
                skill_name='Flame Spire',
                skill_stats={'Lv': [2, 'magenta'], 'Damage': [0 , 'red'], 'Distance': [f'{self.fire_spire_distance}' + ' units', 'green']},
                skill_desc=f'Ignites a moving spire of fire on the ground,@dealing damage to enemies in its path. Repeats@{self.fire_spire_repeat} times.'
            ),
            Attacks(
                skill_rect=self.special_skill_4_rect, skill_img=special_skill_4_icon, mana=self.mana,
                mana_cost=self.special_mana_cost_list[3], cooldown=self.special_atk4_cooldown, damage=[self.base_damage['sp_atk4dmg'][0], self.base_damage['sp_atk4dmg'][1]],
                skill_name='Fireblast',
                skill_stats={'Lv': [2, 'magenta'], 'Damage': [0 , 'red']},
                skill_desc=f'Casts multiple fireblasts in whole area.@- Fireblast count: {len(self.fire_blast_count)}@- Damage per fireblast: {self.fire_blast_damage_mult*100:.0f}%'
            ),
            Attacks(
                mana_cost=0, cooldown=self.basic_attack_cooldown, mana=self.mana,
                skill_rect=self.basic_icon_rect, skill_img=self.basic_icon,   
                skill_name='Basic Attack', skill_stats={'Type': ['Melee', 'white']}
            )
        ]

        self.skill_iframes_config = {
            'attacking1': False,   
            'attacking2': False,  
            'attacking3': False,  
            'sp_attacking': True,      
        }

    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.is_dead():
            return
        
        # ---------- Moving ----------
        if self.can_move():
            self.player_movement(right_hotkey, left_hotkey, jump_hotkey, current_time,
                speed_modifier = 0, special_active_speed = 0.1, jump_force = self.jump_force, jump_force_modifier = 0)
            
        # ---------- Casting ----------
        if self.is_frozen(): return
        if self.is_silenced() and not basic_hotkey: return
            
        if self.is_pressing(hotkey1) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 0):
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', -self.fireball_cast_range, True),
                        y=self.attack_position(self.rect, 'y', 30, False),
                        frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
                        frame_duration=self.fireball_frame_duration,
                        repeat_animation=1,
                        speed=self.fireball_speed if self.facing_right else -self.fireball_speed,
                        dmg=self.atk1_damage[0],
                        final_dmg=self.atk1_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        delay=(True, 800),
                        sound=(True, self.atk1_sound, None, None),
                        hitbox_scale_x=self.fireball_hitbox_size_modifier,
                        hitbox_scale_y=self.fireball_hitbox_size_modifier
                    ))
                    
                    self.consume_mana(self.attacks, 0)
                    self.reset_skill_cooldown(self.attacks, 0, current_time)
                    self.modify_current_state(running=False, animation="attacking1", ani_index="player_atk1", ani_index_flipped="player_atk1")

            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 0):
                    for i, (x_off) in enumerate(self.special_fireball_offsets):
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', -x_off, True),
                            y=self.rect.centery - random.randint(-50, 50),
                            frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
                            frame_duration=self.fireball_frame_duration,
                            repeat_animation=1,
                            speed=self.special_fireball_speed if self.facing_right else -self.special_fireball_speed,
                            dmg=self.sp_atk1_damage[0],
                            final_dmg=self.sp_atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound, None, None),
                            delay=(True, 750 + i * self.special_fire_delay_interval),
                            hitbox_scale_x=self.fireball_hitbox_size_modifier,
                            hitbox_scale_y=self.fireball_hitbox_size_modifier
                        ))
                    
                    self.consume_mana(self.attacks_special, 0)
                    self.reset_skill_cooldown(self.attacks_special, 0, current_time)
                    self.modify_current_state(running=False, animation="attacking1", ani_index="player_atk1", ani_index_flipped="player_atk1")

        elif self.is_pressing(hotkey2) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 1):
                    for i in self.fire_count:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', i, True),
                            y=self.attack_position(self.rect, 'y', 30, False),
                            frames=self.attack_frame_count(self.atk2),
                            frame_duration=self.fire_duration / len(self.atk2),
                            repeat_animation=self.fire_repeat_default,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0],
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            delay=(True, 800),
                            sound=(True, self.atk2_sound, None, None)
                        ))
                    
                    self.consume_mana(self.attacks, 1)
                    self.reset_skill_cooldown(self.attacks, 1, current_time)
                    self.modify_current_state(running=False, animation="attacking2", ani_index="player_atk2", ani_index_flipped="player_atk2")
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 1):
                    for i in self.special_fire_count:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', i, True),
                            y=self.attack_position(self.rect, 'y', 30, False),
                            frames=self.attack_frame_count(self.atk2),
                            frame_duration=self.special_fire_duration / len(self.atk2),
                            repeat_animation=self.fire_repeat_default,
                            dmg=self.sp_atk2_damage[0],
                            final_dmg=self.sp_atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            delay=(True, 800)
                        ))
                    self.atk2_sound.play()
                    
                    self.consume_mana(self.attacks_special, 1)
                    self.reset_skill_cooldown(self.attacks_special, 1, current_time)
                    self.modify_current_state(running=False, animation="attacking2", ani_index="player_atk2", ani_index_flipped="player_atk2")

        elif self.is_pressing(hotkey3) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 2):
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', self.fire_spire_cast_range, True),
                        y=self.attack_position(self.rect, 'y', 30, False),
                        frames=self.attack_frame_count(self.atk3),
                        frame_duration=self.fire_spire_frame_duration,
                        repeat_animation=1,
                        speed=0.5 if self.facing_right else -0.5,
                        dmg=self.atk3_damage[0],
                        final_dmg=self.atk3_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        delay=(True, 800),
                        sound=(True, self.atk3_sound, None, None)
                    ))
                    
                    self.consume_mana(self.attacks, 2)
                    self.reset_skill_cooldown(self.attacks, 2, current_time)
                    self.modify_current_state(running=False, animation="attacking3", ani_index="player_atk3", ani_index_flipped="player_atk3")
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 2):
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', self.fire_spire_cast_range, True),
                        y=self.attack_position(self.rect, 'y', 30, False),
                        frames=self.attack_frame_count(self.atk3),
                        frame_duration=self.fire_spire_frame_duration,
                        repeat_animation=self.fire_spire_repeat,
                        speed=self.fire_spire_speed if self.facing_right else -self.fire_spire_speed,
                        dmg=self.sp_atk3_damage[0],
                        final_dmg=self.sp_atk3_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        moving=True,
                        continuous_dmg=True,
                        sound=(True, self.atk3_sound, None, None),
                        delay=(True, 800)
                    ))
                    
                    self.consume_mana(self.attacks_special, 2)
                    self.reset_skill_cooldown(self.attacks_special, 2, current_time)
                    self.modify_current_state(running=False, animation="attacking3", ani_index="player_atk3", ani_index_flipped="player_atk3")

        elif self.is_pressing(hotkey4) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks, 3):
                    attack_display.add(Attack_Display(
                        x=self.attack_position(self.rect, 'x', self.fireblast_cast_range, True),
                        y=self.attack_position(self.rect, 'y', -100, False),
                        frames=self.attack_frame_count(self.sp),
                        frame_duration=80,
                        repeat_animation=1,
                        speed=5 if self.facing_right else -5,
                        dmg=self.sp_damage[0],
                        final_dmg=self.sp_damage[1],
                        who_attacks=self,
                        who_attacked=self.enemy,
                        sound=(True, self.sp_sound, None, None)
                    ))
                    
                    self.consume_mana(self.attacks, 3)
                    self.reset_skill_cooldown(self.attacks, 3, current_time)
                    self.modify_current_state(running=False, animation="sp_attacking", ani_index="player_sp", ani_index_flipped="player_sp")
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.is_skill_ready(self.attacks_special, 3):
                    for i in self.fire_blast_count:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', i, True),
                            y=self.attack_position(self.rect, 'y', -100, False),
                            frames=self.attack_frame_count(self.sp),
                            frame_duration=80,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_atk4_damage[0],
                            final_dmg=self.sp_atk4_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.sp_sound, None, None)
                        ))
                        
                    self.consume_mana(self.attacks_special, 3)
                    self.reset_skill_cooldown(self.attacks_special, 3, current_time)
                    self.modify_current_state(running=False, animation="sp_attacking", ani_index="player_sp", ani_index_flipped="player_sp")

        elif self.is_pressing(basic_hotkey) and not self.is_busy_attacking():
            if self.is_in_basic_mode() and not self.is_jumping():
                if self.can_basic_attack():
                    for i in [200, 900]:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', 40, True),
                            y=self.attack_position(self.rect, 'y', 40, False),
                            frames=self.attack_frame_count(self.basic_slash, self.basic_slash_flipped),
                            frame_duration=BASIC_FRAME_DURATION,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, self.calculate_attack_delay(i)),
                            sound=(True, self.basic_sound, None, None),
                            is_basic_attack=True
                        ))
                    self.consume_mana(self.attacks, 4)
                    self.reset_skill_cooldown(self.attacks, 4, current_time)
                    self.modify_current_state(running=False, animation="basic_attacking", ani_index="player_basic", ani_index_flipped="player_basic")
                    self.modify_attack_state(current_time, 'basic')
                    
            elif self.is_in_special_mode() and not self.is_jumping():
                if self.can_basic_attack(): # Reusing can_basic_attack since it relies on the unified basic attack timer
                    for i in [200, 900]:
                        attack_display.add(Attack_Display(
                            x=self.attack_position(self.rect, 'x', 40, True),
                            y=self.attack_position(self.rect, 'y', 40, False),
                            frames=self.attack_frame_count(self.basic_slash, self.basic_slash_flipped),
                            frame_duration=BASIC_FRAME_DURATION,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage * DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, self.calculate_attack_delay(i)),
                            sound=(True, self.basic_sound, None, None),
                            is_basic_attack=True
                        ))
                    self.consume_mana(self.attacks_special, 4)
                    self.reset_skill_cooldown(self.attacks_special, 4, current_time)
                    self.modify_current_state(running=False, animation="basic_attacking", ani_index="player_basic", ani_index_flipped="player_basic")
                    self.modify_attack_state(current_time, 'basic')

        elif self.is_pressing(special_hotkey) and not self.is_busy_attacking():
            if self.special >= MAX_SPECIAL:
                self.special_active = True
                self.special_sound.play()

    # def _trigger_attack_display_for_p2(self):
    #     """Spawns visual-only Attack_Display on the non-host client (P2) when
    #     apply_hero_state() detects a skill-start (False→True) transition.

    #     Rules:
    #     - dmg=0, final_dmg=0, disable_collide=True  →  purely cosmetic.
    #     - Mana / cooldowns are NOT touched here; the host snapshot owns those.
    #     - _p2_atk_just_triggered values: 1=atk1, 2=atk2, 3=atk3, 4=sp(atk4), 5=basic
    #     - _p2_atk_special_active: host-embedded special_active at cast-time (not stale snapshot).
    #     """
    #     import random as _rand
    #     sk = getattr(self, '_p2_atk_just_triggered', 0)
    #     if sk == 0:
    #         return

    #     # Use the host-embedded value, not self.special_active which may be
    #     # up to 50 ms stale due to the interpolated snapshot delay.
    #     _special = getattr(self, '_p2_atk_special_active', self.special_active)

    #     _vis = dict(dmg=0, final_dmg=0, disable_collide=True,
    #                 who_attacks=self, who_attacked=self.enemy)

    #     if sk == 1:
    #         if not _special:
    #             attack_display.add(Attack_Display(
    #                 x=self.attack_position(self.rect, 'x', -self.fireball_cast_range, True),
    #                 y=self.attack_position(self.rect, 'y', 30, False),
    #                 frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
    #                 frame_duration=self.fireball_frame_duration, repeat_animation=1,
    #                 speed=self.fireball_speed if self.facing_right else -self.fireball_speed,
    #                 moving=True, delay=(True, 800),
    #                 sound=(True, self.atk1_sound, None, None),
    #                 hitbox_scale_x=self.fireball_hitbox_size_modifier,
    #                 hitbox_scale_y=self.fireball_hitbox_size_modifier,
    #                 **_vis))
    #         else:
    #             for i, x_off in enumerate(self.special_fireball_offsets):
    #                 attack_display.add(Attack_Display(
    #                     x=self.attack_position(self.rect, 'x', -x_off, True),
    #                     y=self.rect.centery - _rand.randint(-50, 50),
    #                     frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
    #                     frame_duration=self.fireball_frame_duration, repeat_animation=1,
    #                     speed=self.special_fireball_speed if self.facing_right else -self.special_fireball_speed,
    #                     moving=True,
    #                     sound=(True, self.atk1_sound, None, None),
    #                     delay=(True, 750 + i * self.special_fire_delay_interval),
    #                     hitbox_scale_x=self.fireball_hitbox_size_modifier,
    #                     hitbox_scale_y=self.fireball_hitbox_size_modifier,
    #                     **_vis))

    #     elif sk == 2:
    #         if not _special:
    #             for i in self.fire_count:
    #                 attack_display.add(Attack_Display(
    #                     x=self.attack_position(self.rect, 'x', i, True),
    #                     y=self.attack_position(self.rect, 'y', 30, False),
    #                     frames=self.attack_frame_count(self.atk2),
    #                     frame_duration=self.fire_duration / len(self.atk2),
    #                     repeat_animation=self.fire_repeat_default,
    #                     speed=5 if self.facing_right else -5,
    #                     delay=(True, 800),
    #                     sound=(True, self.atk2_sound, None, None),
    #                     **_vis))
    #         else:
    #             for i in self.special_fire_count:
    #                 attack_display.add(Attack_Display(
    #                     x=self.attack_position(self.rect, 'x', i, True),
    #                     y=self.attack_position(self.rect, 'y', 30, False),
    #                     frames=self.attack_frame_count(self.atk2),
    #                     frame_duration=self.special_fire_duration / len(self.atk2),
    #                     repeat_animation=self.fire_repeat_default,
    #                     delay=(True, 800),
    #                     **_vis))
    #             self.atk2_sound.play()

    #     elif sk == 3:
    #         if not _special:
    #             attack_display.add(Attack_Display(
    #                 x=self.attack_position(self.rect, 'x', self.fire_spire_cast_range, True),
    #                 y=self.attack_position(self.rect, 'y', 30, False),
    #                 frames=self.attack_frame_count(self.atk3),
    #                 frame_duration=self.fire_spire_frame_duration, repeat_animation=1,
    #                 speed=0.5 if self.facing_right else -0.5,
    #                 delay=(True, 800),
    #                 sound=(True, self.atk3_sound, None, None),
    #                 **_vis))
    #         else:
    #             attack_display.add(Attack_Display(
    #                 x=self.attack_position(self.rect, 'x', self.fire_spire_cast_range, True),
    #                 y=self.attack_position(self.rect, 'y', 30, False),
    #                 frames=self.attack_frame_count(self.atk3),
    #                 frame_duration=self.fire_spire_frame_duration,
    #                 repeat_animation=self.fire_spire_repeat,
    #                 speed=self.fire_spire_speed if self.facing_right else -self.fire_spire_speed,
    #                 moving=True,
    #                 sound=(True, self.atk3_sound, None, None),
    #                 delay=(True, 800),
    #                 **_vis))

    #     elif sk == 4:
    #         if not _special:
    #             attack_display.add(Attack_Display(
    #                 x=self.attack_position(self.rect, 'x', self.fireblast_cast_range, True),
    #                 y=self.attack_position(self.rect, 'y', -100, False),
    #                 frames=self.attack_frame_count(self.sp),
    #                 frame_duration=80, repeat_animation=1,
    #                 speed=5 if self.facing_right else -5,
    #                 sound=(True, self.sp_sound, None, None),
    #                 **_vis))
    #         else:
    #             for i in self.fire_blast_count:
    #                 attack_display.add(Attack_Display(
    #                     x=self.attack_position(self.rect, 'x', i, True),
    #                     y=self.attack_position(self.rect, 'y', -100, False),
    #                     frames=self.attack_frame_count(self.sp),
    #                     frame_duration=80, repeat_animation=1,
    #                     speed=5 if self.facing_right else -5,
    #                     sound=(True, self.sp_sound, None, None),
    #                     **_vis))

    #     elif sk == 5:
    #         for i in [200, 900]:
    #             attack_display.add(Attack_Display(
    #                 x=self.attack_position(self.rect, 'x', 40, True),
    #                 y=self.attack_position(self.rect, 'y', 40, False),
    #                 frames=self.attack_frame_count(self.basic_slash, self.basic_slash_flipped),
    #                 frame_duration=BASIC_FRAME_DURATION, repeat_animation=1,
    #                 speed=0, moving=True,
    #                 delay=(True, self.calculate_attack_delay(i)),
    #                 sound=(True, self.basic_sound, None, None),
    #                 **_vis))

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
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation()
        elif self.basic_attacking:
            self.basic_animation()
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

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

        super().update()