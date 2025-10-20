
'''
step 1: copy hero

step 2: set unique values like animation frames, sound, constants,
        input position, frame duration, repeats on attacks using Attack_Display
(this step takes a while and confusing since you need to path images correctly)

step 3: on player selection function,
        create new value on the p1/p2_select lists using PlayerSelector class.
        Last image pathing, for the profile image 

step 4: i will try that now.
        I just did.

step 5: test if works...

step.. done
'''


'''
Based on what I remembered:

step 1: add to player selector
        for drawing and selection of the hero icon
'''



'''
Guide on making an attack:

sample code from wind hashashin atk 4

attack = Attack_Display(
    x=hero1.x_pos if self.player_type == 1 else hero2.x_pos, # in front of him
    y=hero1.y_pos - 100 if self.player_type == 1 else hero2.y_pos - 100,
    frames=self.sp, #frames=self.real_sp,
    frame_duration=40,
    repeat_animation=4,
    speed=0 if self.facing_right else 0,
    dmg=WIND_HASHASHIN_REAL_SP_DAMAGE,
    who_attacks=self,
    who_attacked=hero1 if self.player_type == 2 else hero2,
    moving=False,
    heal=False,
    continuous_dmg=False,
    per_end_dmg=(False, True))

from fire knight atk2

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
    stun=True)

    
x                 x pos for the attack
y                 y pos for the attack
frames            attack animation path
frame_duration    how long each frame in ms(millisecond)
repeat_animation  animate again
speed             if moving, set speed, else, nothing
dmg               damage amount (make sure if only hit dmg(projectile), or every frame(none, or if moving and continuous dmg), or specific(per_end_dmg))
who_attacks       self
who_attacked      enemy
moving            projectile
heal              heal self
continuous_dmg    damages every frame if moving is true, if collide
per_end_dmg       damages every specific repeat animation, guide below:
disable_collide   don't apply damage when attack rect collides enemy
stun              toggle jump for the enemy, making it stun (stun logic for me :))
sound             play sound when attack is done
kill_collide      kill enemy when attack rect collides with enemy

guide:
 0 = when the attack collides with the enemy, apply dmg
 1 = damages enemy anyway (collide or not, don't matter)

 
 nahh ignore these notes, this was my fixing arc that I'm losing my mind working on it,
 ain't touching it until bug again.
 (
current notice: 4/10/25, 8:30pm
YES it finally worked, if you set per_end_dmg[1] to true, deals damage every attack animation ends,
damage depends on repeat animation on how many time. if per_end_dmg[0] is true, damages enemy whether the attack collided or not,
but this still apply the damage every animation ends, it just don't require any collision.


 note: if you collide with the original rect, occur bug where colliding damages you(a lot)
 wrong fix: turn moving to true and speed to 0 (if you dont want to move)
 fix: i removed the collide sprite, idk whats going on now. I fix a lot, etc...
 update: I deleted it (IM MAD!)
 )
'''


# AS OF 4/23/25 (12:11 AM)
'''
Some player info:
Fire Wizard:
- 
+ 5% damage
SPECIAL
+ 10% move speed
+ 8 projectiles (skill 1) 16.7% damage each attack - 83% damage (skill 1)
+ 5 explosions (skill 4) 33% damage each attack - 67% damage (skill 4)
+ 11 fires (skill 2) - 50% damage
+ 3 times repeats (skill 3) + moving - 20% damage

Wanderer Magician:
- 
+ 20% mana regeneration
+ atk2 heal
+ ranged basic attack
+ 300% damage atk1 (random damage) [2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10]
SPECIAL
+ 3 projectiles (skill 1) + 20% damage each attack
+ faster healing (skill 2) 2/ + heal
+ 10% move speed
+ 10% mana regeneration
+ 40 max mana
+ 250% damage/heal
- short range atk3 but + damage (25%)

Fire Knight:
- 20% move speed
- 5% jump boost
- 40 max mana
- +3% gravity
+ 20 max health
+ 20% health regeneration
+ atk2 long stun
SPECIAL
+ 10% move speed
+ 0 cd skill_1
+ 2 slashes (skill 1) 30% damage each attack + 40% mana cost reduction
+ 3 attacks (skill 2) 60% damage each attack   - 60% end damage (skill 2) 
+ fire tornado attack with stun + small amount dmg
+ 50% damage (skill 4)
+ 20% final damage (skill 4)
+ all skill BURN damage [# damage] (only 20% for skill 1) 
    (only 40% for skill 2) (50% for skill 4) (10% for basic attack)

Wind Hashashin:
- 10 max health
- 50 max mana
+ 20% move speed
+ 10% jump boost
+ -2% gravity
+ 15% mana cost reduction
+ atk3 short stun
SPECIAL
+ skill 1 8 attacks (75% damage each) jumping high
+ atk2 short stun
+ atk3 fire tornado + knockback and damage
+ 10% damage, multiple attacks (1st atk 57%, 2nd & 3rd atks 30%)

'''


# from global_vars import (
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

# import pygame
# import pygame.sprite
# import random
# from attack import Attacks, Attack_Display
# from sprite_loader import (SpriteSheet, SpriteSheet_Flipped, load_attack, load_attack_flipped)
# from player import Player
# from heroes import Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin
# from gameloop import create_title
# from gameloop import menu
# from gameloop import menu_button


import pygame
import random
import time
import math
import pygame.sprite
from global_vars import (IMMEDIATE_RUN,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon, water_princess_icon, forest_ranger_icon,
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
# from attack import Attacks, Attack_Display
from sprite_loader import SpriteSheet, SpriteSheet_Flipped, load_attack, load_attack_flipped
from player import Player
# from heroes import Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin
from button import ImageButton

from bot_ai import create_bot

import Animate_BG

import global_vars

# from chance import Chance

pygame.init()

pygame.display.set_icon(icon)
pygame.display.set_caption("HERO FIGHTING")

# botchance = Chance(0.3) # ticks every 0.3 seconds

# while True:
#     botchance.update(50)
#=-------------------
# Font Sizes
FONT = pygame.font.Font(fr'assets\font\slkscr.ttf', 30)

# Icons
#positions, formula : spec_pos/size, eg 50/720 = 0.0695
cstm_pos = 0.039 #width 50
cstm_pos2 = 0.222 #160
cstm_pos3 = 0.291 #210
hp_icon = pygame.transform.rotozoom(pygame.image.load(r'assets\icons\health icon.png').convert_alpha(), 0, 0.05)
mana_icon = pygame.transform.rotozoom(pygame.image.load(r'assets\icons\mana icon.png').convert_alpha(), 0, 0.065)
hp_icon_p1_rect = hp_icon.get_rect(center=(int(width*cstm_pos)+1, int(height*cstm_pos2)+1))
mana_icon_p1_rect = mana_icon.get_rect(center=(int(width*cstm_pos)+1, int(height*cstm_pos3)+1))
hp_icon_p2_rect = hp_icon.get_rect(center=(width - int(width*cstm_pos)-1, int(height*cstm_pos2)+1))
mana_icon_p2_rect = mana_icon.get_rect(center=(width - int(width*cstm_pos)-1, int(height*cstm_pos3)+1))

def draw_hp_mana_icons():
    screen.blit(hp_icon, hp_icon_p1_rect)
    screen.blit(hp_icon, hp_icon_p2_rect)
    screen.blit(mana_icon, mana_icon_p1_rect)
    screen.blit(mana_icon, mana_icon_p2_rect)


        # print(self.health)
        # self.regenerate_mana()



        
                        
                    

            # print(f"{self.who_attacked} took {self.dmg} damage! Current HP: {self.who_attacked.health}")






class Attacks:
    '''
    This class represents the attack and its properties.
    It contains the attack's damage, animation frames, and other attributes.
    It also handles the attack's cooldown and mana cost.
    The class is designed to be used with Pygame and integrates with the Pygame sprite system.
    '''
    

    def __init__(self, mana_cost, skill_rect, skill_img, cooldown, mana, special_skill=False):
        self.mana_cost = mana_cost
        self.skill_rect = skill_rect
        self.skill_img = skill_img
        self.cooldown = cooldown
        self.mana = mana  # Not used
        # Internally store raw last-used timestamp and a snapshot of paused-total at that moment
        self._last_used_time = -cooldown  # raw pygame.time.get_ticks() value when used
        self._last_used_paused_total = 0   # global_vars.PAUSED_TOTAL_DURATION snapshot at use
        
        self.atk_mana_cost = 0
        self.special_skill = special_skill

        # Dynamically scaled font sizes
        self.cooldown_font_size = int(height * 0.0416 *1.3)  # ~30 at 720p
        self.mana_font_size = int(height * 0.0208 *1.3)      # ~15 at 720p

        self.special_font_size = int(height * 0.0208 *1.3)

        # Offset for positioning mana text (scaled vertically)
        self.mana_y_offset = int(self.skill_rect.height * 0.35)      # ~50 at 720p
        
        self.special_y_offset = int(self.skill_rect.height * 0.35)

        self.button_icon = pygame.image.load(r'assets\icons\button.png').convert_alpha()

    def reduce_cd(self, val=False):
        if val:
            # Reset cooldown: set last_used_time such that the attack is ready now
            now = pygame.time.get_ticks()
            # store raw timestamp and snapshot paused total
            self._last_used_time = now - self.cooldown
            self._last_used_paused_total = global_vars.PAUSED_TOTAL_DURATION
        return val
         

    @property
    def last_used_time(self):
        # expose raw stored timestamp for backward compatibility
        return self._last_used_time

    @last_used_time.setter
    def last_used_time(self, value):
        # whenever code sets last_used_time, capture the current paused-total snapshot
        self._last_used_time = value
        self._last_used_paused_total = global_vars.PAUSED_TOTAL_DURATION

    def time_since_use(self):
        """Return milliseconds elapsed since last use, excluding paused durations."""
        effective_now = pygame.time.get_ticks() - global_vars.PAUSED_TOTAL_DURATION
        effective_last = self._last_used_time - self._last_used_paused_total
        return effective_now - effective_last

    def is_ready(self):
        return self.time_since_use() >= self.cooldown

    def draw_skill_icon(self, screen, mana, special=0, player_type=0, max_special=MAX_SPECIAL):
        # Determine the key to display based on the player type
        key_text = ""
        if player_type == 1:
            key_text = "Z" if self.skill_rect == hero1.skill_1_rect else \
                    "X" if self.skill_rect == hero1.skill_2_rect else \
                    "C" if self.skill_rect == hero1.skill_3_rect else \
                    "V" if self.skill_rect == hero1.skill_4_rect else \
                    "E" if self.skill_rect == hero1.basic_icon_rect else \
                    "F" if self.skill_rect == hero1.special_rect else ""
        elif player_type == 2:
            key_text = "U" if self.skill_rect == hero2.skill_1_rect else \
                    "I" if self.skill_rect == hero2.skill_2_rect else \
                    "O" if self.skill_rect == hero2.skill_3_rect else \
                    "P" if self.skill_rect == hero2.skill_4_rect else \
                    "L" if self.skill_rect == hero2.basic_icon_rect else \
                    "K" if self.skill_rect == hero2.special_rect else ""

        # Existing logic for drawing the skill icon
        if not self.special_skill:
            if not self.is_ready():
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                # Draw scaled cooldown text
                font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.cooldown_font_size)
                # Use time_since_use() so display matches actual cooldown logic and accounts for pauses
                remaining_ms = max(0, self.cooldown - self.time_since_use())
                cooldown_time = max(0, remaining_ms // 1000)
                cooldown_text = font.render(str(cooldown_time), global_vars.TEXT_ANTI_ALIASING, 'Red')
                screen.blit(cooldown_text, (
                    self.skill_rect.centerx - cooldown_text.get_width() // 2,
                    self.skill_rect.centery - cooldown_text.get_height() // 2
                ))

            elif mana < self.mana_cost:
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                # Mana cost when not enough mana
                mana_font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.mana_font_size)
                self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', global_vars.TEXT_ANTI_ALIASING, 'Red')
                screen.blit(self.atk_mana_cost, (
                    self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
                    self.skill_rect.top - self.mana_y_offset
                ))
            else:
                screen.blit(self.skill_img, self.skill_rect)

        else:
            if not special >= max_special:
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                special_font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.special_font_size)
                self.atk_special_cost = special_font.render(f'[{max_special}]', global_vars.TEXT_ANTI_ALIASING, 'azure3')
                screen.blit(self.atk_special_cost, (
                    self.skill_rect.centerx - self.atk_special_cost.get_width() // 2,
                    self.skill_rect.top - self.special_y_offset
                ))
            else:
                special_font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.special_font_size)
                self.atk_special_cost = special_font.render(f'[{max_special}]', global_vars.TEXT_ANTI_ALIASING, 'yellow')
                screen.blit(self.atk_special_cost, (
                    self.skill_rect.centerx - self.atk_special_cost.get_width() // 2,
                    self.skill_rect.top - self.special_y_offset
                ))
                screen.blit(self.skill_img, self.skill_rect)

        # Draw the key text below the skill icon
        key_font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.mana_font_size)
        button_icon = pygame.transform.scale(self.button_icon, (90, 70))
        # button_icon_rect = button_icon.get_rect(topleft=(key_pos_x - 10, key_pos_y - 5))

        key_text_render = key_font.render(key_text, True, 'azure3')
        
        screen.blit(button_icon, (
            self.skill_rect.centerx - 45,
            self.skill_rect.bottom - 20  # Position below the skill icon
        ))
        # print(key_font.size(key_text)[0])
        screen.blit(key_text_render, (
            self.skill_rect.centerx - key_text_render.get_width() // 2,
            self.skill_rect.bottom + 5  # Position below the skill icon
        ))


        

    def draw_mana_cost(self, screen, mana):
        if not self.special_skill:
            mana_font = pygame.font.Font(fr'assets\font\slkscr.ttf', self.mana_font_size)
            color = 'Cyan2' if mana >= self.mana_cost else 'Red'
            self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', global_vars.TEXT_ANTI_ALIASING, color)

            screen.blit(self.atk_mana_cost, (
                self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
                self.skill_rect.top - self.mana_y_offset
            ))


class Attack_Display(pygame.sprite.Sprite): #The Attack_Display class should handle the visual representation and animation of an attack. Here's the corrected version:
   
    """
        This class represents the attack display and its properties.
        It contains the attack's animation frames, duration, and other attributes.
        It also handles the attack's position and movement.

        Attack_Display Class Parameter Descriptions:

        1. x (int): 
        - The initial horizontal position (x-coordinate) of the attack on the screen.

        2. y (int): 
        - The initial vertical position (y-coordinate) of the attack on the screen.

        3. frames (list of Surface): 
        - A list of images (frames) that represent the attack's animation.

        4. frame_duration (int): 
        - Duration in milliseconds each frame is displayed before switching to the next one.

        5. repeat_animation (int): 
        - Number of times the animation should loop. After the final loop, the attack ends.

        6. speed (int): 
        - Horizontal movement speed of the attack. If zero, the attack is stationary.

        7. dmg (int): 
        - The amount of damage dealt per hit or frame, depending on other flags.

        8. final_dmg (int): 
        - Damage that is applied at the end of the animation (used for finishers or strong final hits).

        9. who_attacks (object): 
        - The entity (e.g. player or enemy) initiating the attack.

        10. who_attacked (object): 
            - The target of the attack, to receive damage or effects.

        11. moving (bool): 
            - If True, the attack moves horizontally according to 'speed'. If False, it's static.

        12. heal (bool): 
            - If True, instead of dealing damage, the attack heals the one who cast it.

        13. continuous_dmg (bool): 
            - If True, the attack deals damage continuously every frame while colliding with the target.

        14. per_end_dmg (tuple(bool, bool)): 
            - Two boolean flags:
                * [0] – Enables damage to occur at the end of each animation cycle.
                * [1] – Applies damage when animation ends, regardless of collision. (1 set of damage)

        15. disable_collide (bool): 
            - If True, the attack does not deal damage upon direct collision.

        16. stun (tuple(bool, int)): 
            - A tuple that enables stun and defines its duration:
                * [0] – Enables/disables stun logic.
                * [1] – Stun duration or intensity (custom logic may vary).

        17. sound (tuple(bool, Sound, Sound, Sound)): 
            - A tuple that defines if sound plays and includes up to 3 sound objects:
                * [0] – Enables/disables sound playback.
                * [1-3] – Sound effects to play when animation ends.

        18. kill_collide (bool): 
            - If True, the attack sprite disappears instantly upon colliding with the target.

        NEW PARAMETERS (to be added to class):

        19. follow (tuple(bool, bool)):
            - Controls if the attack should follow another sprite:
                * [0] – If True, the attack will stick to the enemy upon collision and follow them.
                * [1] – If True, the attack always follows the enemy, even without collision.

        20. delay (tuple(bool, int)):
            - Delays the attack’s animation and effect:
                * [0] – If True, delay is enabled.
                * [1] – Time in milliseconds to wait before the attack becomes active (e.g. (True, 1000) delays by 1 second).

        UPDATE

        21. stop_movement (bool, int, int)
            - Prevents enemy from moving (and using skills)
                * [0] – If True, activates status.
                * [1] – Status
                    1 - Freeze
                    2 - Root
                * [2] – Status mode/type
                    1 - While collides player, effect active, else none (collision only)
                    2 - When collides player, effect active, until attack ends (if hit once)
                    3 - Effect active, until attack ends (full duration)
        '''
        """

    def __init__(self, x, y, frames:pygame.Surface=list, frame_duration=100, repeat_animation=1, speed=0, 
                dmg=0, final_dmg=0, who_attacks:object=None, who_attacked:object=None, moving=False, heal=False,
                continuous_dmg=False, per_end_dmg=(False, False),
                disable_collide=False, stun=(False, 0),
                sound=(False, None, None, None), kill_collide=False,
                follow=(False, False), delay=(False, 0), follow_offset=(0, 0), repeat_sound=False, follow_self=False, use_live_position_on_delay=False,
                hitbox_scale_x=0.6, hitbox_scale_y=0.6,
                hitbox_offset_x=0, hitbox_offset_y=0, heal_enemy=False, self_kill_collide=False, self_moving=False,
                consume_mana=[False, 0],
                stop_movement=(False, 0, 0),
                spawn_attack:dict=None, periodic_spawn:dict=None
                ):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = frames
        self.frame_duration = frame_duration
        self.repeat_animation = repeat_animation
        self.speed = speed
        self.dmg = dmg
        self.final_dmg = final_dmg
        self.who_attacks = who_attacks
        self.who_attacked = who_attacked
        self.moving = moving
        self.heal = heal
        self.continuous_dmg = continuous_dmg
        self.per_end_dmg = per_end_dmg
        self.disable_collide = disable_collide
        self.stun = stun
        self.sound = sound
        self.kill_collide = kill_collide
        self.follow = follow
        self.delay = delay
        self.follow_offset = follow_offset
        self.repeat_sound = repeat_sound
        self.follow_self = follow_self
        self.use_live_position_on_delay = use_live_position_on_delay
        self.heal_enemy = heal_enemy
        self.self_kill_collide = self_kill_collide
        self.self_moving = self_moving # applies some logic to moving to self
        self.consume_mana = consume_mana # [0] = bool, [1] = how much mana (still same as how dmg is applied)
        self.stop_movement = stop_movement

        self.spawn_attack = spawn_attack # dict or callable
        self.periodic_spawn = periodic_spawn # dict or None

        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()

        if not delay[0]:
            self.image = self.frames[self.frame_index]
        else:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # Invisible placeholder
        
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_done = False

        self.current_repeat = 0

        # some logic flags
        self.damaged = False
        self.damaged_detect = self.damaged

        self.following_target = False  # set to True when collided if follow[0] is true
        

        self.delay_start_time = pygame.time.get_ticks()
        self.delay_triggered = False


        self.hitbox_scale_x = hitbox_scale_x
        self.hitbox_scale_y = hitbox_scale_y

        self.hitbox_width = int(self.rect.width * hitbox_scale_x)
        self.hitbox_height = int(self.rect.height * hitbox_scale_y)


        self.hitbox_rect = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)
        
        #spawn attack
        self._has_spawned_on_collide = False
        self._last_periodic_spawn = pygame.time.get_ticks()
        self._periodic_spawn_count = 0


    def update_hitbox(self):
        self.hitbox_rect.center = self.rect.center
        # self.hitbox_rect.x = self.rect.x - self.hitbox_offset_x
        # self.hitbox_rect.y = self.rect.y + self.hitbox_offset_y


    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)  # Red outline for debugging
        # print("Hitbox drawn")
        # print(self.rect.width)

    def kill_self(self):
        # remove only this attack's status
        if self.stop_movement[0]:
            status_type = self.stop_movement[1]
            # remove only this source
            self.who_attacked.remove_movement_status(status_type, source=self)
        # finally kill the sprite
        self.kill()

    def update(self):
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()
        
        '''
        Update the attack display's position and animation.
        This method is called every frame to update the attack display's state.
        It handles the animation frames, movement, and collision detection.
        It also plays the attack sound if specified.
        The method checks for collisions with the target and applies damage if necessary.
        The method also handles the stun effect if specified.
        The method is designed to be used with Pygame and integrates with the Pygame sprite system.
        The method is called by the main game loop to update the attack display's state.
        '''
        # print(self.following_target)
        # print(self.detect_collision())
        """Update the attack animation and position."""
        current_time = pygame.time.get_ticks()

        #delay logic
        if self.delay[0] and not self.delay_triggered:
            if current_time - self.delay_start_time < self.delay[1]:
                return
            else:
                if self.use_live_position_on_delay:
                    self.x = self.who_attacks.x_pos + self.follow_offset[0]
                    self.y = self.who_attacks.y_pos + self.follow_offset[1]

                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=(self.x, self.y))

                self.hitbox_width = int(self.rect.width * self.hitbox_scale_x)
                self.hitbox_height = int(self.rect.height * self.hitbox_scale_y)
                self.hitbox_rect = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)

                if self.sound[0] == True and not self.repeat_sound:
                    if self.sound[1] != None:
                        self.sound[1].play()
                    if self.sound[2] != None:
                        self.sound[2].play()
                    if self.sound[3] != None:
                        self.sound[3].play()

                self.delay_triggered = True

        elif not self.delay[0] and not self.delay_triggered:
            if self.sound[0] == True and not self.repeat_sound:
                if self.sound[1] != None:
                    self.sound[1].play()
                if self.sound[2] != None:
                    self.sound[2].play()
                if self.sound[3] != None:
                    self.sound[3].play()

            self.delay_triggered = True

        # Same flag so that I dont have to write this again!!
        collided = self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect)

        if self.delay_triggered:
            # MAIN LOGIC 1
            # Every frame tick (uses current fps)
            
            # Must at be the top (bug)
            # Spawn attack when collide
            # 'use_attack_onhit_pos': bool, spawns attack when enemy collides with the attack
            if collided and self.spawn_attack and not self._has_spawned_on_collide:
                spec = self.spawn_attack
                if callable(spec):
                    new = spec(self)
                    if new:
                        attack_display.add(new)
                else:
                    ak = spec.get('attack_kwargs', {}).copy()
                    if spec.get('use_attack_onhit_pos', True):
                        ak['x'], ak['y'] = self.rect.center
                    attack_display.add(Attack_Display(**ak))
                self._has_spawned_on_collide = True

            # Spawns attack periodically
            # 'interval': int, spaws attack between intervals
            # 'repeat_count': int, total attack(s) to spawn
            # 'use_attack_pos': bool, uses current pos of attack and spawns attack every interval
            if self.periodic_spawn:
                now = pygame.time.get_ticks()
                interval = self.periodic_spawn.get('interval', 2000)
                max_times = self.periodic_spawn.get('repeat_count', None)
                if now - self._last_periodic_spawn >= interval:
                    ak = self.periodic_spawn.get('attack_kwargs', {}).copy()
                    if self.periodic_spawn.get('use_attack_pos', False):
                        ak['x'], ak['y'] = self.rect.center
                    attack_display.add(Attack_Display(**ak))
                    self._last_periodic_spawn = now
                    self._periodic_spawn_count += 1
                    if max_times is not None and self._periodic_spawn_count >= max_times:
                        self.periodic_spawn = None



            # apply type 3 freeze/root first only once
            if self.stop_movement[0] and self.stop_movement[2] == 3 and not getattr(self, "status_applied", False):
                self.who_attacked.movement_status(self.stop_movement[1], source=self)
                self.status_applied = True

            if current_time - self.last_update_time > self.frame_duration:
                self.last_update_time = current_time
                self.frame_index += 1
                
                # print('reducing dmg')

                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.frame_index]

                # Every attack frame (depends on frame duration)
                elif self.frame_index >= len(self.frames): # kind of 'else' in my s.py
                    self.frame_index = 0
                    self.current_repeat += 1

                    # EVERY FRAME ATTACK LOGIC --------------------------

                    if self.per_end_dmg[0]:
                        self.damaged_detect = False 
                        self.damaged = False
                        
                    # normal logic, damages enemy anywhere
                    if not self.damaged and self.per_end_dmg[1]:
                        if not self.continuous_dmg:
                            self.who_attacked.take_damage(self.dmg)
                            self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)

                            if self.who_attacks.lifesteal > 0:
                                lifesteal_amount = self.dmg * self.who_attacks.lifesteal
                                self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)







                    # MAIN LOGIC 2
                    # Final animation end
                    if self.current_repeat >= self.repeat_animation:
                        # warning: inside these block of codes only runs per frames, not fps frames, 
                        # which might prone to errors if not read carefully.
                        # if self.freeze:
                        #     self.who_attacked.speed = RUNNING_SPEED
                        
                                
                        #dmg animation
                        self.animation_done = True
                        self.kill_self() # Remove the sprite from the group  

                    # EVERY END FRAME ATTACK LOGIC -----------------------------
                        
                    if self.sound[0] == True and self.repeat_sound:
                        if self.sound[1] != None:
                            self.sound[1].play()
                        if self.sound[2] != None:
                            self.sound[2].play()
                        if self.sound[3] != None:
                            self.sound[3].play()

                    #final dmg
                    if not self.damaged and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                        if self.follow[0] and not self.following_target:
                            self.following_target = True
                        if not self.disable_collide: # end animation will do the damaging
                            self.who_attacked.take_damage(self.final_dmg)
                            self.who_attacks.take_special(self.final_dmg * SPECIAL_MULTIPLIER)

                            if self.who_attacks.lifesteal > 0:
                                lifesteal_amount = self.final_dmg * self.who_attacks.lifesteal
                                self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)

                    


                    
                            








            # EVERY FRAME ATTACK LOGIC --------------------------

                # EVERY GAME FPS ATTACK LOGIC --------------------------
                
                #dmg per every frame (too fast)  <-- indent  

                # stun logic
                if not self.heal and not self.heal_enemy:
                    
                                
                    #dmg per frame

                    # main atk logic
                    if not self.damaged and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                        if self.follow[0] and not self.following_target:
                            self.following_target = True
                        if not self.continuous_dmg and not self.disable_collide: # end animation will do the damaging
                            self.who_attacked.take_damage(self.dmg)
                            self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)

                            if self.who_attacks.lifesteal > 0:
                                lifesteal_amount = self.dmg * self.who_attacks.lifesteal
                                self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)
                    
                        # #combine for moving dmg [1]:
                        # if not self.continuous_dmg and not self.disable_collide: # end animation will do the damaging
                        #     self.who_attacked.take_damage(self.final_dmg)

                        if self.moving:
                            self.damaged = True
                        
                        
                    # continuous dmg logic
                    if self.continuous_dmg and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                        if self.follow[0] and not self.following_target:
                            self.following_target = True
                        self.who_attacked.take_damage(self.dmg)
                        self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)

                        if self.who_attacks.lifesteal > 0:
                            lifesteal_amount = self.dmg * self.who_attacks.lifesteal
                            self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)

                    #for per_end_dmg logic
                    # NOW WHY TF DOES THIS WORK SUDDENLY? this is .... good?
                    if not self.damaged and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect) and self.per_end_dmg[0] and self.disable_collide:
                        if self.follow[0] and not self.following_target:
                            self.following_target = True
                        if not self.continuous_dmg:
                            self.who_attacked.take_damage(self.dmg)
                            self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                            
                            if self.who_attacks.lifesteal > 0:
                                lifesteal_amount = self.dmg * self.who_attacks.lifesteal
                                self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)
                            
                            # if self.who_attacks.lifesteal > 0:
                            #     lifesteal_amount = self.final_dmg * self.who_attacks.lifesteal
                            #     self.who_attacks.health = min(self.who_attacks.max_health, self.who_attacks.health + lifesteal_amount)

                        if self.damaged_detect:
                            self.damaged = True

                    #whenn collide, kill
                    if self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                        if self.kill_collide:
                            self.rect.x += 10000
                            self.kill_self()
                    if self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                        if self.self_kill_collide:
                            self.rect.x += 10000
                            self.kill_self()

                    

                # heal logic
                else:
                    if self.self_moving:
                        if not self.damaged and self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                            if self.heal_enemy:
                                if not self.damaged and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                                    if self.follow[0] and not self.following_target:
                                        self.following_target = True
                                    self.who_attacked.take_heal(self.dmg)
                                    self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                            else:
                                if not self.damaged and self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                                    if self.follow[0] and not self.following_target:
                                        self.following_target = True
                                    self.who_attacks.take_heal(self.dmg)
                                    self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)

                        if self.self_moving:
                            self.damaged = True

                    else:#normal stuff
                        if self.heal_enemy:
                            if not self.damaged and self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                                if self.follow[0] and not self.following_target:
                                    self.following_target = True
                                self.who_attacked.take_heal(self.dmg)
                                self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                        else:
                            if not self.damaged and self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                                if self.follow[0] and not self.following_target:
                                    self.following_target = True
                                self.who_attacks.take_heal(self.dmg)
                                self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)


                if self.consume_mana[0]:
                    self.who_attacks.take_mana(self.consume_mana[1])

            # ALWAYS AFFECTED
            
            if self.moving: # moving logic
                # Move the attack
                self.rect.x += self.speed
                if self.rect.x > width + 500 or self.rect.x < -500:
                    self.kill_self()  # Remove the sprite if it goes off-screen

            #stun logic
            if self.hitbox_rect.colliderect(self.who_attacked.hitbox_rect):
                if self.follow[0] and not self.following_target:
                    self.following_target = True
                if True: # end animation will do the damaging
                    if self.stun[0]:
                        self.who_attacked.stun(self.stun, self.rect.centerx, self.rect.centery, self.stun[1])
                        # self.who_attacked.stunned = True


            #follow logic
            if not self.follow_self:
                if self.follow[1]: # FOLLOW ENEMY
                    self.rect.centerx = self.who_attacked.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacked.rect.centery + self.follow_offset[1]
                elif self.follow[0] and self.following_target:
                    self.rect.centerx = self.who_attacked.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacked.rect.centery + self.follow_offset[1]

            else:
                if self.follow[1]: # FOLLOW SELF
                    self.rect.centerx = self.who_attacks.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacks.rect.centery + self.follow_offset[1]
                elif self.follow[0] and self.following_target:
                    self.rect.centerx = self.who_attacks.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacks.rect.centery + self.follow_offset[1]

            # print(self.follow_self)

            #freeze and root
            # [0] = enable
            # [1] = status type (freeze/root)
            # [2] = type
            if self.stop_movement[0] : # enable status
                if self.stop_movement[2] in (1,2): # if either type == 1 or 2
                    # type 2
                    # always run code below if type == 2
                    if collided:
                        self.who_attacked.movement_status(self.stop_movement[1], source=self)
                    # type 1 
                    # run code below if type == 1
                    elif self.stop_movement[2] == 1:
                        # removes status
                        self.who_attacked.remove_movement_status(self.stop_movement[1], source=self)

            if self.current_repeat >= self.repeat_animation:
                if self.stop_movement[0]:
                    status_type = self.stop_movement[1]
                    mode = self.stop_movement[2]
                    if mode in (1, 2, 3):  # remove if type 2 or 3, added type 1 just in case type 1 status removal didn't work.
                        self.who_attacked.remove_movement_status(status_type, source=self)

            
            

            

            



'''
Hero Stats



Fire Wizard:

Strength: 40
Intelligence: 40
Agility: 27



Wanderer Magician:

Strength: 40
Intelligence: 36
Agility: 32



Fire Knight:

Strength: 40
Intelligence: 40
Agility: 65



Wind Hashashin:

Strength: 38
Intelligence: 40
Agility: 12

'''




















# Animation Counts
FIRE_WIZARD_BASIC_COUNT = 10
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
FIRE_WIZARD_ATK1_MANA_COST = 50
FIRE_WIZARD_ATK2_MANA_COST = 80
FIRE_WIZARD_ATK3_MANA_COST = 100
FIRE_WIZARD_SP_MANA_COST = 200

FIRE_WIZARD_ATK1_SIZE = 3
FIRE_WIZARD_ATK2_SIZE = 0.3
FIRE_WIZARD_ATK3_SIZE = 0.3
FIRE_WIZARD_SP_SIZE = 1.3

class Fire_Wizard(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Fire Wizard"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 40
        self.intelligence = 40
        self.agility = 27

        # Base Stats
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult
        # BASIC_ATK_DAMAGE2

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        # Update log for heroes

        #wind hashashin
        # Skill 1: (10, 0) = 10 -> (8, 0) = 8
        # Skill 2: (35/45, 0):tornado = 5-6 + (15/15, 5):slash = 20 = 25-26 -> (35/45, 0):tornado = 5-6 + (12/15, 4):slash = 16 = 21-22
        # Skill 3: (200/20, 25):whirl = 10 + (15/15, 5):slash = 10 = 30 -> (35/45, 0):whirl = 5-6 + (12/15, 4):slash = 16 = 26
        # Skill 4: 18 * 4 = 72 -> 14.5 * 4 = 58

        # Skill 1: 3 * 6:per smoke = 0-18 -> 2.4 * 6:per smoke = 0-14.4
        # Skill 2: 30 -> 26
        # Skill 3: 37 = 37
        # Skill 4: 86 -> 69

        #fire knight nerf
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: (26/20, 2) = 30 -> (26/20, 2) = 28
        # Skill 3: (35/60, 10) = 45 -> (35/60, 7) = 42
        # Skill 4: 80 = 80

        #Skill 4: 
            # Swapped damage explosion
        # (10/10, 50):start + (25/10, 5):explosion = 90
        # -> (25/10, 5):start + (10/10, 45):explosion = 85



        # Wind hashashin buff
        # 8 -> 10 (dash speed and distance: 10 -> 12 (400 -> 500), sp: 12 -> 15 (600 -> 800))
        # x slashes (both slashes) (12/15, 4) -> (13/15, 5) total=(23-24 dmg)
        # 26 -> 28 (due to x slash)
        # 58 -> 64 (16)

        #fire knight nerf and wind hashashin buff
        #fire knight:
        # Trait: +20% Health Regen -> +15% Health Regen
        # Intelligence: 40 = 40, 180 -> 200 (removed -20 max mana)
        # Skill 1: 0
        # Skill 2: cd 16s - > 20s, mana cost 80 -> 100
        # Skill 3: cd 26s - > 30s, mana cost 140 -> 160
        # Skill 4: mana cost 180 -> 200, dmg = (65/65, 15) = 80 -> (60/65, 15) = 75 
        #            -> (25/10, 5):start = (10/10, 40):explosion = 80

        #wind hashashin:
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: (26/20, 2) = 30 -> (26/20, 2) = 28
        # Skill 3: (35/60, 10) = 45 -> (35/60, 7) = 42
        # Skill 4: 80 = 80

        #fire knight buff/nerf
        # Trait: +15% Health Regen -> +20% Health Regen
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: cd 20s - > 18s, mana cost 80 -> 100
        # Skill 3: cd 30s - > 26s, mana cost 160 -> 150
        # Skill 4: 0


        #wanderer magician nerf
        # special basic attack: (3.2/2.4)3 = 4 -> (3.2/2.5)3 = 3.84 per hit
        # special skill 3:  Damage Multiplier 25% -> 15%

        #mana cost
        self.atk1_mana_cost = 50
        self.atk2_mana_cost = 80
        self.atk3_mana_cost = 100
        self.sp_mana_cost = 200
        
        #dmg
        self.atk1_cooldown = 7000 # 7000
        self.atk2_cooldown = 5000 + 13000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000
        #FORMULA = DESIRED DMG / TOTAL FRAME EX. dmg=25/34 == 0.6944
        self.damage_list = [
            (13, 0),
            (23/53, 0),
            (35/34, 0),
            (50/28, 10)
        ]
        self.atk1_damage = self.damage_list[0]
        self.atk2_damage = self.damage_list[1]
        self.atk3_damage = self.damage_list[2]
        self.sp_damage = self.damage_list[3] 
        dmg_mult = 0.05
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        basic_ani = [r'assets\characters\Fire wizard\slash pngs\Attack_1_', FIRE_WIZARD_BASIC_COUNT, 1]
        
        jump_ani = [r'assets\characters\Fire wizard\jump pngs\Jump_', FIRE_WIZARD_JUMP_COUNT, 1]
        run_ani = [r'assets\characters\Fire wizard\run pngs\Run_', FIRE_WIZARD_RUN_COUNT, 1]
        idle_ani= [r'assets\characters\Fire wizard\idle pngs\image_0-', FIRE_WIZARD_IDLE_COUNT, 1]
        atk1_ani= [r'assets\characters\Fire wizard\fireball pngs\image_0-', FIRE_WIZARD_ATK1_COUNT, 1]
        sp_ani= [r'assets\characters\Fire wizard\flame jet pngs\image_0-', FIRE_WIZARD_SP_COUNT, 1]
        death_ani= [r'assets\characters\Fire wizard\dead\tile00', FIRE_WIZARD_DEATH_COUNT, 1]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-efftect-21991.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\052168_huge-explosion-85199.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.1 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        atk1 = [r'assets\attacks\fire wizard\atk1', FIRE_WIZARD_ATK1, 1]
        atk2 = [r'assets\attacks\fire wizard\atk2', FIRE_WIZARD_ATK2, 1]
        atk3 = [r'assets\attacks\fire wizard\atk3\png_', FIRE_WIZARD_ATK3, 1]
        sp = [r'assets\attacks\fire wizard\sp atk', FIRE_WIZARD_SP, 1]

        self.bonus_type = "strength"
        self.bonus_value = self.strength

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\FireballIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\GlyphOfFireIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\RodOfPower29Icon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\MeteorIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\kim special icon.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\FlameReaveIcon29.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\SmiteIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\VolcanicOrb29Icon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

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
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE)

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
                skill_img=special_skill_1,
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
                mana_cost=int(self.mana_cost_list[2] - (self.mana_cost_list[2] * 0.2)),
                skill_rect=self.special_skill_3_rect,
                skill_img=special_skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=int(self.mana_cost_list[3] - (self.mana_cost_list[3] * 0.2)),
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
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = DEFAULT_JUMP_FORCE  
                    self.last_atk_time = current_time  # Update the last jump time
            
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        
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
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,
                            delay=(True, 800),
                            sound=(True, self.atk1_sound, None, None),

                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -= self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [60*2, 120*2, 180*2]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=50,
                                repeat_animation=4,
                                speed=5 if self.facing_right else -5,
                                dmg=self.atk2_damage[0],
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 800),
                                sound=(True, self.atk2_sound, None, None)
                                ) # Replace with the target
                            attack_display.add(attack)
                        self.mana -= self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
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
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=60,
                            repeat_animation=1,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            delay=(True, 800),
                            sound=(True, self.atk3_sound , None, None)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -= self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                            y=self.rect.centery - 100,
                            frames=self.sp,
                            frame_duration=80,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.sp_sound, None, None)
                            ) # Replace with the target
                        attack_display.add(attack)
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks[4].is_ready():
                        for i in [200, 900]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 40 if self.facing_right else self.rect.centerx - 40,
                                y=self.rect.centery + 40,
                                frames=self.basic_slash if self.facing_right else self.basic_slash_flipped,
                                frame_duration=BASIC_FRAME_DURATION,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.basic_attack_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, i),
                                moving=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
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
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [-50, 0, 50, 100]:
                            attack = Attack_Display(
                                x=self.rect.centerx - i if self.facing_right else self.rect.centerx + i,
                                y=self.rect.centery - i,
                                frames=self.atk1 if self.facing_right else self.atk1_flipped,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=7 if self.facing_right else -7,
                                dmg=self.atk1_damage[0]/3,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack)
                            

                            attack2 = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i,
                                y=self.rect.centery - i,
                                frames=self.atk1_flipped if self.facing_right else self.atk1,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=-7 if self.facing_right else 7,
                                dmg=self.atk1_damage[0]/6,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack2)
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [-200*3, -160*3, -120*3, -80*3, -40*3, 0, 40*3, 80*3, 120*3, 160*3, 200*3]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=50,
                                repeat_animation=4,
                                speed=5 if self.facing_right else -5,
                                dmg=self.atk2_damage[0]/2,
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack)
                        self.atk2_sound.play()
                        self.mana -=  self.attacks_special[1].mana_cost
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
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=60,
                            repeat_animation=2,
                            speed=1 if self.facing_right else -1,
                            dmg=self.atk3_damage[0] * 0.7,
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,
                            continuous_dmg=True,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [-1000, -500, 0, 500, 1000]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery - 100,
                                frames=self.sp,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=self.sp_damage[0]/1.1,
                                final_dmg=self.sp_damage[1]/1.1,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.sp_sound , None, None)) # Replace with the target
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[3].mana_cost
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
                            x=self.rect.centerx + 40 if self.facing_right else self.rect.centerx - 40,
                            y=self.rect.centery + 40,
                            frames=self.basic_slash if self.facing_right else self.basic_slash_flipped,
                            frame_duration=BASIC_FRAME_DURATION,
                            repeat_animation=2,
                            speed=0,
                            dmg=self.basic_attack_damage * DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            sound=(True, self.basic_sound, None, None),
                            delay=(True, 200),
                            moving=True,

                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            )
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass

                
     
            
        
    
    def update(self):
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)
        
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

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False
        # if self.running:
        #     print('is running')

        
        super().update()
        


        

        
# MULT = 0.7

WANDERER_MAGICIAN_JUMP_COUNT = 6
WANDERER_MAGICIAN_RUN_COUNT = 8
WANDERER_MAGICIAN_IDLE_COUNT = 8
WANDERER_MAGICIAN_ATK1_COUNT = 7
WANDERER_MAGICIAN_ATK3_COUNT = 9
WANDERER_MAGICIAN_SP_COUNT = 16
WANDERER_MAGICIAN_DEATH_COUNT = 4

WANDERER_MAGICIAN_BASIC = 6
WANDERER_MAGICIAN_ATK1 = 4
WANDERER_MAGICIAN_ATK2 = 40
WANDERER_MAGICIAN_ATK3 = 10
WANDERER_MAGICIAN_SP = 3

WANDERER_MAGICIAN_SPECIAL_ATK3 = 10
# ---------------------
# WANDERER_MAGICIAN_ATK1_MANA_COST = 70
# WANDERER_MAGICIAN_ATK2_MANA_COST = 125
# WANDERER_MAGICIAN_ATK3_MANA_COST = 125
# WANDERER_MAGICIAN_SP_MANA_COST = 170

WANDERER_MAGICIAN_BASIC_SIZE = 1.5
WANDERER_MAGICIAN_ATK1_SIZE = 2
WANDERER_MAGICIAN_ATK2_SIZE = 1
WANDERER_MAGICIAN_ATK3_SIZE = 1.5
WANDERER_MAGICIAN_SP_SIZE = 1.3

WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE = 2
WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE = 2

# WANDERER_MAGICIAN_ATK1_COOLDOWN = 8000
# WANDERER_MAGICIAN_ATK2_COOLDOWN = 15000 + 9000
# WANDERER_MAGICIAN_ATK3_COOLDOWN = 26000
# WANDERER_MAGICIAN_SP_COOLDOWN = 60000

# WANDERER_MAGICIAN_ATK1_DAMAGE = 0 # dmg at the input, sry
# WANDERER_MAGICIAN_ATK2_DAMAGE = (18/40, 0)
# WANDERER_MAGICIAN_ATK3_DAMAGE = (30/10, 5) #26
# WANDERER_MAGICIAN_SP_DAMAGE = (55, 0)


class Wanderer_Magician(Player): #NEXT WORK ON THE SPRITES THEN COPY EVERYTHING SINCE IM DONE 4/6/25 10:30pm
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Wanderer Magician"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 40
        self.intelligence = 36
        self.agility = 32
        

        self.base_max_mana = self.intelligence * self.int_mult
        
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.base_max_mana
        # self.special_default_max_mana = self.max_mana # max mana and this variable mustt  be the same
        self.special_bonus_mana = 240
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20

        self.atk1_mana_cost = 70
        self.atk2_mana_cost = 150
        self.atk3_mana_cost = 125
        self.sp_mana_cost = 175

        self.atk1_cooldown = 8000
        self.atk2_cooldown = 20000 + 9000
        self.atk3_cooldown = 26000  
        self.sp_cooldown = 60000

        self.atk1_damage = (0, 0)
        self.atk2_damage = (15/40, 0) # 30 heal, slow -> 37 heal if special, quick
        self.atk3_damage = (26/10, 8) #26
        self.sp_damage = (55, 0) # 68.75 is the special dmg 
        self.sp_damage_2nd = (4.5/16, 0) # * 30 = 67.5

        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        jump_ani = [r'assets\characters\Wanderer Magican\jump pngs\Jump_', WANDERER_MAGICIAN_JUMP_COUNT, 1]
        run_ani = [r'assets\characters\Wanderer Magican\run pngs\Run_', WANDERER_MAGICIAN_RUN_COUNT, 1]
        idle_ani= [r'assets\characters\Wanderer Magican\idle pngs\image_0-', WANDERER_MAGICIAN_IDLE_COUNT, 1]
        atk1_ani= [r'assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        atk3_ani= [r'assets\characters\Wanderer Magican\attack 2 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        sp_ani= [r'assets\characters\Wanderer Magican\charge pngs', WANDERER_MAGICIAN_SP_COUNT, 1]
        death_ani= [r'assets\characters\Wanderer Magican\dead', WANDERER_MAGICIAN_DEATH_COUNT, 1]

        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3')
        self.atk1_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)

        # # Player Skill Animations Source
        basic = [r'assets\attacks\Basic Attack\wanderer magician\Charge_1_', WANDERER_MAGICIAN_BASIC, 1]
        atk1 = [r'assets\attacks\wanderer magician\atk1\image_', WANDERER_MAGICIAN_ATK1, 1]
        atk2 = [r'assets\attacks\wanderer magician\atk2', WANDERER_MAGICIAN_ATK2, 1]
        atk3 = [r'assets\attacks\wanderer magician\atk3\Explosion_blue_circle', WANDERER_MAGICIAN_ATK3, 0]
        sp = [r'assets\attacks\wanderer magician\sp atk\vv', WANDERER_MAGICIAN_SP, 0]

        special_atk3 = [r'assets\attacks\wanderer magician\special1\Explosion_blue_oval', WANDERER_MAGICIAN_SPECIAL_ATK3, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_06.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_08.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon9.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Massive_Rasen.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\special.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\ChatGPT Image Apr 18, 2025, 07_46_01 AM.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\HealingWindIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_02.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.basic = self.load_img_frames(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)
        self.basic_flipped = self.load_img_frames_flipped(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)

        self.atk1 = self.load_img_frames_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, 90)
        self.atk1_flipped = self.load_img_frames_flipped_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, -90)
        self.atk2 = self.load_img_frames_tile_method(atk2[0], atk2[1], atk2[2], WANDERER_MAGICIAN_ATK2_SIZE)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], WANDERER_MAGICIAN_ATK3_SIZE)
        self.sp = self.load_img_frames(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)
        self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)

        self.special_atk3 = self.load_img_frames(special_atk3[0], special_atk3[1], special_atk3[2], WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE)

        self.special_basic = load_attack(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.special_basic_flipped = load_attack_flipped(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        
        self.sp_special = load_attack(
        filepath=r"assets\attacks\wanderer magician\sp atk special\2.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=8, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )

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
                skill_img=self.basic_icon2,
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

        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=special_skill_2,
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
                skill_img=self.basic_icon2,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )
   
        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana

        self.jump_attack_pending = False
        self.jump_attack_time = 0

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
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = DEFAULT_JUMP_FORCE  
                    self.last_atk_time = current_time  # Update the last jump time
            
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=7 if self.facing_right else -7,
                            dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 3,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=100,
                            repeat_animation=2,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0], 
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
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
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        self.jumping = True
                        self.y_velocity = DEFAULT_JUMP_FORCE  # adjust jump strength as needed
                        self.jump_attack_pending = True
                        self.jump_attack_time = pygame.time.get_ticks() + 200  # 500ms later
                        # Create an attack
                        # print("Z key pressed")
                        # if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
                        #     self.jump_attack_pending = False
                        #     attack = Attack_Display(
                        #         x=hero1.x_pos if self.player_type == 2 else hero2.x_pos, #self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 150, # in front of him
                        #         y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                        #         frames=self.atk3,
                        #         frame_duration=100,
                        #         repeat_animation=1,
                        #         speed=5 if self.facing_right else -5,
                        #         dmg=self.atk3_damage[0],
                        #         final_dmg=self.atk3_damage[1],
                        #         who_attacks=self,
                        #         who_attacked=hero1 if self.player_type == 2 else hero2,
                        #         sound=(True, self.atk3_sound , None, None),
                        #         delay=(True, 800)
                        #         ) # Replace with the target
                        #     attack_display.add(attack)
                        #     # self.mana -=  self.attacks[2].mana_cost
                        #     # self.attacks[2].last_used_time = current_time
                        #     self.running = False
                        #     self.attacking3 = True
                        #     self.player_atk3_index = 0
                        #     self.player_atk3_index_flipped = 0
                        #     # self.y_velocity = 0  # optional: cancel gravity impulse if you want freeze in air

                            # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery,
                            frames=self.sp if self.facing_right else self.sp_flipped,
                            frame_duration=40,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.sp_sound , None, None),
                            delay=(True, 5000)
                            ) 
                        attack_display.add(attack)
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

            if not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.mana >= 0 and self.attacks[4].is_ready():
                    attack = Attack_Display(
                        x=self.rect.centerx,
                        y=self.rect.centery + random.randint(0, 40),
                        frames=self.basic if self.facing_right else self.basic_flipped,
                        frame_duration=100,
                        repeat_animation=5,
                        speed=7 if self.facing_right else -7,
                        dmg=self.basic_attack_damage,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True,

                        sound=(True, self.atk1_sound, None, None),
                        kill_collide=True,
                        delay=(True, 500),
                    )

                        # Experiment Codes
                        # plan: when attack longer moving, greater damage
                        # periodic_spawn={
                        #     'attack_kwargs': {
                        #         'x': width+100,
                        #         'y': self.rect.centery + random.randint(0, 40),
                        #         'frames': self.atk1 if self.facing_right else self.atk1_flipped,
                        #         'frame_duration': 100,
                        #         'repeat_animation': 5,
                        #         'speed': -7 if self.facing_right else 7,
                        #         'dmg': random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 3,
                        #         'final_dmg': 0,
                        #         'who_attacks': self,
                        #         'who_attacked': hero1 if self.player_type == 2 else hero2,
                        #         'moving': True,
                        #         'sound': (False, self.atk1_sound, None, None),
                        #         'delay': (True, 300),
                        #         'kill_collide': True
                        #     },
                        #     'interval': 1000,
                        #     'repeat_count': 5,
                        #     'use_attack_pos': False,
                        # }
                        

                    #     periodic_spawn= {
                    #         'attack_kwargs': {
                    #             'frames': self.atk3,
                    #             'frame_duration': 100,
                    #             'repeat_animation': 3,
                    #             'speed': 0,
                    #             'dmg': self.atk3_damage[0],
                    #             'final_dmg': self.atk3_damage[1],
                    #             'who_attacks': self,
                    #             'who_attacked': hero1 if self.player_type == 2 else hero2,
                    #             'moving': False,
                    #             'sound': (False, self.atk3_sound, None, None),
                    #             'delay': (False, 0)
                    #         },
                    #         'interval': 500,
                    #         'repeat_count': 20,
                    #         'use_attack_pos': True,
                    #     }
                    # )
                    attack_display.add(attack)
                    self.mana -= 0
                    self.attacks[4].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0

                    self.basic_attacking = True

                    

                    # print("Attack executed")
                else:
                    pass

            elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                    self.special_active = True
                    self.basic_sound.play()
                else:
                    pass






        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(0, 30), (40, 60), (40, 0)]:
                            attack = Attack_Display(
                                x=self.rect.centerx - i[0] if self.facing_right else self.rect.centerx + i[0],
                                y=self.rect.centery + i[1] if self.facing_right else self.rect.centery + i[1],
                                frames=self.atk1 if self.facing_right else self.atk1_flipped,
                                frame_duration=100,
                                repeat_animation=5,
                                speed=7 if self.facing_right else -7,
                                dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 1.2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,

                                kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500)) # Replace with the target
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=40,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=(self.atk2_damage[0]*2) + ((self.atk2_damage[0]*2) * (SPECIAL_MULTIPLIER * 0.25)),
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
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
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=hero1.x_pos if self.player_type == 2 else hero2.x_pos,
                            y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                            frames=self.special_atk3,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk3_damage[0] + (self.atk3_damage[0] * (SPECIAL_MULTIPLIER * 0.15)),
                            final_dmg=self.atk3_damage[1] + (self.atk3_damage[1] * (SPECIAL_MULTIPLIER * 0.15)),
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=hero1.x_pos if self.player_type == 2 else hero2.x_pos,
                            y=hero1.y_pos + 40,
                            frames=self.sp_special,
                            frame_duration=160,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage_2nd[0],
                            final_dmg=self.sp_damage_2nd[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=False,
                            follow=(False, True),
                            follow_offset=(0, 50),

                            kill_collide=False,
                            sound=(True, self.sp_sound , self.atk3_sound, None),
                            delay=(True, 800)
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

            if not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.mana >= 0 and self.attacks_special[4].is_ready():
                    for i in [(500, random.randint(0, 30)), (700, random.randint(0, 30)), (900, random.randint(0, 30))]:
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + i[1],
                            frames=self.special_basic if self.facing_right else self.special_basic_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=8 if self.facing_right else -8,
                            dmg=self.basic_attack_damage/2.5,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            sound=(True, self.basic_sound, self.atk1_sound, None),
                            kill_collide=True,
                            delay=(True, i[0]),

                            hitbox_scale_x=0.2,
                            hitbox_scale_y=0.2,
                            spawn_attack= {
                            'attack_kwargs': {
                                'frames': self.atk3,
                                'frame_duration': 100,
                                'repeat_animation': 1,
                                'speed': 0,
                                'dmg': self.atk3_damage[0],
                                'final_dmg': self.atk3_damage[1],
                                'who_attacks': self,
                                'who_attacked': hero1 if self.player_type == 2 else hero2,
                                'moving': False,
                                'sound': (False, self.atk3_sound, None, None),
                                'delay': (False, 0)
                            },
                            'use_attack_onhit_pos': True
                            
                        }
                        )
                            
                        attack_display.add(attack)


                    

                    self.mana -= 0
                    self.attacks_special[4].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    
                    self.basic_attacking = True

                    # print("Attack executed")
                else:
                    pass

        # print(self.running)
        # print(self.player_type)
        # print(len(self.player_run), len(self.player_run_flipped))
        # print("Run Animation Index:", self.player_run_index)

     
        
    def update(self):
        if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
            self.jump_attack_pending = False
            attack = Attack_Display(
                x=hero1.x_pos if self.player_type == 2 else hero2.x_pos, #self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 150, # in front of him
                y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                frames=self.atk3,
                frame_duration=100,
                repeat_animation=1,
                speed=5 if self.facing_right else -5,
                dmg=self.atk3_damage[0],
                final_dmg=self.atk3_damage[1],
                who_attacks=self,
                who_attacked=hero1 if self.player_type == 2 else hero2,
                sound=(True, self.atk3_sound , None, None),
                delay=(True, 800)
                ) # Replace with the target
            attack_display.add(attack)
            # self.mana -=  self.attacks[2].mana_cost
            # self.attacks[2].last_used_time = current_time
            self.running = False
            self.attacking3 = True
            self.player_atk3_index = 0
            self.player_atk3_index_flipped = 0
            self.y_velocity -= DEFAULT_GRAVITY*7  # optional: cancel gravity impulse if you want freeze in air
        # print(self.stunned)
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()
        
        self.keys = pygame.key.get_pressed()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking2:
            self.atk2_animation()
        
        elif self.sp_attacking:
            self.sp_animation(-11)

        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # Apply gravity
        if not self.jump_attack_pending:
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

        # print(self.basic_attack_animation_speed)
        # print(f'cd:{self.basic_attack_cooldown}')
        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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
                self.mana += (self.mana_regen + (self.mana_regen * (0.20 if not self.special_active else 0.30)))
            if not DISABLE_HEAL_REGEN:
                self.health += self.health_regen
        else:
            self.health = 0

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                self.max_mana = min(self.special_bonus_mana, self.max_mana + 10)
                if self.special <= 0:
                    self.special_active = False
                    self.max_mana = min(self.base_max_mana, self.max_mana + 10)
                    #self.apply_item_bonuses()
        # print(self.basic_attack_damage)
                # self.max_mana = min(200, self.max_mana + 10)

        # self.special += 0.1
        # print(self.special)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        super().update()
        


    
# Animation Counts
FIRE_KNIGHT_JUMP_COUNT = 20
FIRE_KNIGHT_RUN_COUNT = 8 
FIRE_KNIGHT_IDLE_COUNT = 8
FIRE_KNIGHT_ATK1_COUNT = 11
FIRE_KNIGHT_ATK2_COUNT = 19
FIRE_KNIGHT_ATK3_COUNT = 28
FIRE_KNIGHT_SP_COUNT = 18
FIRE_KNIGHT_DEATH_COUNT = 13


FIRE_KNIGHT_ATK1_MANA_COST = 30
FIRE_KNIGHT_ATK2_MANA_COST = 80
FIRE_KNIGHT_ATK3_MANA_COST = 140
FIRE_KNIGHT_SP_MANA_COST = 180

FIRE_KNIGHT_ATK1_SIZE = 5
FIRE_KNIGHT_ATK2_SIZE = 1.5
FIRE_KNIGHT_ATK3_SIZE = 2
FIRE_KNIGHT_SP_SIZE = 2.5

#1=49, 2=20, 3=60, 4=65 atk frames

FIRE_KNIGHT_ATK1_COOLDOWN = 5000
FIRE_KNIGHT_ATK2_COOLDOWN = 16000
FIRE_KNIGHT_ATK3_COOLDOWN = 26000
FIRE_KNIGHT_SP_COOLDOWN = 60000

FIRE_KNIGHT_ATK1_DAMAGE = (10/49, 0)
FIRE_KNIGHT_ATK2_DAMAGE = (25/20, 5)
FIRE_KNIGHT_ATK3_DAMAGE = (40/60, 10) #35
FIRE_KNIGHT_SP_DAMAGE = (60/65, 15) # 55

FIRE_KNIGHT_BURN_DAMAGE = 10

class Display_Text: # display damage taken text previously (not working for now)
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.num_txt = ''
        self.health = health
        self.health_detect = 0

        self.font = pygame.font.SysFont('Times New Roman', 25)
        self.text = self.font.render(self.num_txt, global_vars.TEXT_ANTI_ALIASING, 'Red')
        
        self.health_now = self.health
        if self.health_now >= self.health_detect:
            self.health_detect = self.health
        else:
            self.num_txt = str(self.health_detect - self.health_now)
            screen.blit(self.num_txt, (self.x, self.y - 100))
            self.health_detect = self.health
        
  

class Fire_Knight(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        self.player_type = player_type
        self.name = "Fire Knight"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 42
        self.intelligence = 40
        self.agility = 65

        # Base Stats
        self.max_health = (self.strength * self.str_mult) + 20
        self.max_mana = (self.intelligence * self.int_mult)
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        self.atk1_mana_cost = 30
        self.atk2_mana_cost = 100
        self.atk3_mana_cost = 150   
        self.sp_mana_cost = 200

        self.atk1_cooldown = 5000
        self.atk2_cooldown = 18000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000

        self.atk1_damage = (10/49, 1)
        self.atk2_damage = (26/20, 2) #27 = 32, 3 = 29, 26 = 28
        self.atk3_damage = (35/60, 7)
        self.sp_damage = (60/65, 15) 
        self.special_sp_damage2 = (10/10, 40) # 60
        self.special_sp_damage1 = (25/10, 5) # 30, total 80 damage

        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)
        self.special_sp_damage1 = self.special_sp_damage1[0] + (self.special_sp_damage1[0] * dmg_mult), self.special_sp_damage1[1] + (self.special_sp_damage1[1] * dmg_mult)
        self.special_sp_damage2 = self.sp_damage[0] + (self.special_sp_damage2[0] * dmg_mult), self.special_sp_damage2[1] + (self.special_sp_damage2[1] * dmg_mult)
        
        
        # Player Animation Source
        jump_ani = [r'assets\characters\fire knight\03_jump\jump_', FIRE_KNIGHT_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\fire knight\02_run\run_', FIRE_KNIGHT_RUN_COUNT, 0]
        idle_ani = [r'assets\characters\fire knight\01_idle\idle_', FIRE_KNIGHT_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\fire knight\05_1_atk\1_atk_', FIRE_KNIGHT_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\fire knight\06_2_atk\2_atk_', FIRE_KNIGHT_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\fire knight\07_3_atk\3_atk_', FIRE_KNIGHT_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\fire knight\08_sp_atk\sp_atk_', FIRE_KNIGHT_SP_COUNT, 0]
        death_ani = [r'assets\characters\fire knight\11_death\death_', FIRE_KNIGHT_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\3rrd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\ult.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        self.burn_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3')
        self.burn_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\3.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\5.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\6.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\special icon.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\FirebrandIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\ForgeStrikeIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\InfernalLegacyIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\FireShieldIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = load_attack(
        filepath=r"assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk1_flipped = load_attack_flipped(
        filepath=r"assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"assets\attacks\fire knight\atk2\414.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"assets\attacks\fire knight\atk3\D65.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"assets\attacks\fire knight\sp\D30.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=13, 
        columns=5, 
        scale=FIRE_KNIGHT_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )
        



        # 10 FRAMES INITIAL EXPLOSION
        self.sp_special1 = load_attack(
        filepath=r"assets\attacks\fire knight\021.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=2, 
        columns=5, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )
        # 10 FRAMES EXPLOSION
        self.sp_special2 = load_attack(
        filepath=r"assets\attacks\fire knight\038.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=2, 
        columns=5, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )
        
        self.burn = load_attack(
        filepath=r"assets\attacks\fire knight\D65 cropped.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=1, 
        rotation=0,
        frame_duration=100 
    )
        self.atk3_special = load_attack(
        filepath=r"assets\attacks\fire knight\083.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK2_SIZE, 
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

        self.attacks_special = [
            Attacks(
                mana_cost=int(self.mana_cost_list[0] - (self.mana_cost_list[0] * 0.3)),
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=int(self.atk1_cooldown/2),
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=special_skill_2,
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

        # self.health_detect = 0

        #health = 20, if health > prev health = prev health - health 

    
    
    
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
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed - ((self.speed * 0.2) if not self.special_active else (self.speed * 0.1)))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed - ((self.speed * 0.2) if not self.special_active else (self.speed * 0.1)))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE - (DEFAULT_JUMP_FORCE * 0.05))  
                    self.last_atk_time = current_time  # Update the last jump time  
            
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=3.5 if self.facing_right else -3.5,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 700),
                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -= self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
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
                            dmg=self.atk2_damage[0],
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            stun=(True, 50),
                            sound=(True, self.atk2_sound , None, None),
                            delay=(True, 700)
                        )
                        attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
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
                    if self.mana >=  self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 180 if self.facing_right else self.rect.centerx - 180, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 700)
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                            y=self.rect.centery - 50,
                            frames=self.sp,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.sp_sound , None, None)
                            ) # Replace with the target
                        attack_display.add(attack)
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks[4].is_ready():
                        attack = Attack_Display(
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70,
                            y=self.rect.centery + 90,
                            frames=self.basic_slash_big if self.facing_right else self.basic_slash_flipped_big,
                            frame_duration=BASIC_FRAME_DURATION + 50,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            sound=(True, self.basic_sound, None, None),
                            delay=(True, 700),
                            moving=True

                            )
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        self.basic_attacking = True
 
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
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=5,
                            repeat_animation=1,
                            speed=3.5 if self.facing_right else -3.5,
                            dmg=self.atk1_damage[0]* 0.6,
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 700),
                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            ) # Replace with the target
                        attack_display.add(attack)

                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.2,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, 700),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)

                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(130, 700), (250, 1700), (370, 2700)]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx - i[0], # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=150,
                                repeat_animation=1,
                                speed=1 if self.facing_right else -1,
                                dmg=self.atk2_damage[0] * 0.4,
                                final_dmg=self.atk2_damage[1] * 0.4,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                stun=(True, 50),
                                sound=(True, self.atk2_sound , None, None),
                                delay=(True, i[1]),

                                moving=True,
                                continuous_dmg=True
                                ) # Replace with the target
                            attack_display.add(attack)

                            burn_attack = Attack_Display(
                            x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx - i[0], # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.4,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, i[1]),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                            attack_display.add(burn_attack)
                        
                        self.mana -=  self.attacks_special[1].mana_cost
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
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3_special,
                            frame_duration=200,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0]*1.6,
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            stun=(True, 100),
                            sound=(True, self.atk2_sound , None, None),
                            delay=(True, 700)
                        )
                        
                        attack_display.add(attack)

                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, 700),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)
                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        
                        for i in [
                            (self.sp_special1, False, 100, 230, self.special_sp_damage1[0], self.special_sp_damage1[1]),
                            (self.sp_special2, True, 90, 200, self.special_sp_damage2[0], self.special_sp_damage2[1])]: # special 1 = gold explode
                            attack = Attack_Display(
                                x=self.rect.centerx + 250 if self.facing_right else self.rect.centerx - 250, # in front of him
                                y=self.rect.centery + i[2],
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                sound=(True, self.sp_sound , None, None),
                                delay=(i[1], 1200),
                                follow=(True, False)
                                ) # Replace with the target
                            attack_display.add(attack)

                            burn_attack = Attack_Display(
                                x=self.rect.centerx + i[3] if self.facing_right else self.rect.centerx - i[3], # in front of him
                                y=self.rect.centery + i[2],
                                frames=self.burn,
                                frame_duration=200,
                                repeat_animation=2,
                                speed=0.5 if self.facing_right else -0.5,
                                dmg=0,
                                final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.5,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                sound=(True, self.burn_sound, None, None),
                                delay=(i[1], 100),
                                follow=(True, False),
                                follow_offset=(0, 80)
                                )
                            attack_display.add(burn_attack)

                        self.mana -=  self.attacks_special[3].mana_cost
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
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70,
                            y=self.rect.centery + 90,
                            frames=self.basic_slash_big if self.facing_right else self.basic_slash_flipped_big,
                            frame_duration=BASIC_FRAME_DURATION + 50,
                            repeat_animation=1,
                            speed=0 if self.facing_right else 0,
                            dmg=self.basic_attack_damage*DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            
                            sound=(True, self.basic_sound, None, None),
                            moving=True

                            
                            )
                        attack_display.add(attack)

                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.1,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, 700),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        self.basic_sound.play()

                        self.basic_attacking = True
                        # print("Attack executed")
                    else:
                        pass
                
     
            

    def update(self):
        self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()

        self.keys = pygame.key.get_pressed()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)

        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed-2)
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation()
        elif self.basic_attacking:
            pass
            # self.basic_animation(self.basic_attack_animation_speed)
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        
        

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

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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
                self.health += (self.health_regen + (self.health_regen * 0.2))
        else:
            self.health = 0

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False

        
        super().update()

        

         


# Animation Counts
WIND_HASHASHIN_BASIC_COUNT = 4
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

# WIND_HASHASHIN_ATK1_MANA_COST = int(base1 - (base1 * percen))
# WIND_HASHASHIN_ATK2_MANA_COST = int(base2 - (base2 * percen))
# WIND_HASHASHIN_ATK3_MANA_COST = int(base3 - (base3 * percen))
# WIND_HASHASHIN_SP_MANA_COST = int(base4 - (base4 * percen))

#atk rank doesn't matter here
WIND_HASHASHIN_ATK1_SIZE = 0.8 # smoke
WIND_HASHASHIN_ATK2_SIZE = 0.8 # tornado
WIND_HASHASHIN_ATK3_SIZE = 1 # circcle
WIND_HASHASHIN_SP_SIZE = 1  # x slash

WIND_HASHASHIN_ATK3_SPECIAL_SIZE = 2

#1=60, 2=45, 3=20, 4=15

# WIND_HASHASHIN_ATK1_COOLDOWN = 7000
# WIND_HASHASHIN_ATK2_COOLDOWN = 14000
# WIND_HASHASHIN_ATK3_COOLDOWN = 26000
# WIND_HASHASHIN_SP_COOLDOWN = 60000

# WIND_HASHASHIN_ATK1_DAMAGE = (10, 0) #smoke dmg
# WIND_HASHASHIN_ATK2_DAMAGE = (35/45, 0) #tornado
# WIND_HASHASHIN_ATK2_DAMAGE_2ND = (15/15, 5) # x slash
# WIND_HASHASHIN_ATK3_DAMAGE = 0.24 #not used
# WIND_HASHASHIN_SP_DAMAGE = (200/20, 25) # circle
# WIND_HASHASHIN_SP_DAMAGE_2ND = (15/15, 5) # x slash

# WIND_HASHASHIN_REAL_SP_DAMAGE = 16 #0.225

#skl  = atk1 fraame
#skl2 = atk2 frame, sp frame
#skl3 = atk3 frame, sp frame


class Wind_Hashashin(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type
        self.name = "Wind Hashashin"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 80)

        # stat
        self.strength = 38
        self.intelligence = 40
        self.agility = 13

        # Base Stats
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        percen = 0.15
        base1 = 50
        base2 = 80
        base3 = 140
        base4 = 200

        self.atk1_mana_cost = int(base1 - (base1 * percen))
        self.atk2_mana_cost = int(base2 - (base2 * percen))
        self.atk3_mana_cost = int(base3 - (base3 * percen))
        self.sp_mana_cost = int(base4 - (base4 * percen))


        self.atk1_cooldown = 7000
        self.atk2_cooldown = 14000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000

        self.atk1_damage = (10, 0) #smoke dmg
        self.atk2_damage = (35/45, 0) #tornado
        self.atk2_damage_2nd = (13/15, 5) # x slash
        self.atk3_damage = (0, 0) #not used
        self.sp_damage = (200/20, 25) # circle
        self.sp_damage_2nd = (13/15, 5) # x slash
        self.real_sp_damage = 16 # times 4

        #SKILL DAMAGE before
        #10
        #26
        #30
        #72

        #sp
        #3 each
        #30
        #37
        #86

        # Player Animation Source1.png
        basic_ani = [r'assets\characters\wind hasashin\PNG\3_atk\3_atk_', WIND_HASHASHIN_BASIC_COUNT, 0]

        jump_ani = [r'assets\characters\Wind hasashin\PNG\j_up\j_up_', WIND_HASHASHIN_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\wind hasashin\PNG\run\run_', WIND_HASHASHIN_RUN_COUNT, 0]
        idle_ani = [r'assets\characters\wind hasashin\PNG\idle\idle_', WIND_HASHASHIN_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\wind hasashin\PNG\air_atk\air_atk_', WIND_HASHASHIN_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\wind hasashin\PNG\3_atk\3_atk_', WIND_HASHASHIN_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_SP_COUNT, 0]
        death_ani = [r'assets\characters\wind hasashin\PNG\death\death_', WIND_HASHASHIN_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\1st.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\3rd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\4th 1, slash.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        
        self.x_slash_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\x slash 2nd,3rd, 4th.mp3')
        self.sp_sound2 = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\4th 2, flesh hit.mp3')
        self.x_slash_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        self.sp_sound2.set_volume(0.4 * global_vars.MAIN_VOLUME)

        self.atk3_sound_special = pygame.mixer.Sound(r'assets\sound effects\fire knight\3rrd.mp3')
        self.atk3_sound_special.set_volume(0.5 * global_vars.MAIN_VOLUME)
        # (The rest of the code follows same structure and renaming logic...)
        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\WindHashira.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\3yzqiwcug5qc1.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\What is Danmokou_.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\download.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\aleksey-bayura-sketch-ninja1.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\7316955-HSC00001-7.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\wmremove-transformed.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\MarkForDeathIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))
            
            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))
            
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load (atk doesn't matter, some attack will be used on other attack)
        self.atk1 = load_attack(
        filepath=r"assets\attacks\wind hasashin\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack_flipped(
        filepath=r"assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"assets\attacks\wind hasashin\3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"assets\attacks\wind hasashin\4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3, 
        columns=5, 
        scale=WIND_HASHASHIN_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )
        



        self.atk3_special = load_attack(
        filepath=r"assets\attacks\fire knight\083.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK3_SPECIAL_SIZE, 
        rotation=0,
        frame_duration=100
    )
        

        # Player Animations Load
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        
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

        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=int(self.mana_cost_list[1]*1.5),
                skill_rect=self.special_skill_2_rect,
                skill_img=skill_3,
                cooldown=int(self.atk2_cooldown*1.5),
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
        
        self.atk1_move_speed = 1
        self.atk2_move_speed = 1
        self.atk3_move_speed = 4

        # Skill 1  configuration
        self.default_dash_speed = 12
        self.default_max_distance = 500

        self.special_dash_speed = 15
        self.special_max_distance = 800

        self.activate_dash = False
        self.distance_covered = 0
        self.dash_speed = 5
        self.max_distance = 600 #(400 -> 600)
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move(): # fully working
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed + ((self.speed * 0.2) if not self.special_active else (self.speed * 0.25)))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed + ((self.speed * 0.2) if not self.special_active else (self.speed * 0.25)))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE + (DEFAULT_JUMP_FORCE * 0.1)) 
                    self.last_atk_time = current_time  # Update the last jump time

        
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.atk1,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=-1.5 if self.facing_right else 1.5,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,
                            sound=(True, self.atk1_sound , None, None)
                            ) # Replace with the target
                        attack_display.add(attack)
                        #dash  
                        self.mana -=  self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')

            if not self.jumping and not self.is_dead(): # can be cast while jumping, I hope...
                if hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                        for i in [
                            (self.atk2, True, 30, 30, self.atk2_damage[0], False, self.atk2_damage[1]), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 70, 40, self.atk2_damage_2nd[0], False, self.atk2_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=10 if self.facing_right else -10,
                                dmg=i[4],
                                final_dmg=i[6],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=i[1],
                                continuous_dmg=i[1],
                                stun=(i[5], 40),
                                # sound=(True, self.atk2_sound , self.x_slash_sound, None),
                                # stop_movement=(True, 1, 2)
                                ) # Replace with the target
                            attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

            if not self.jumping and not self.is_dead():
                if hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        current_time2 = pygame.time.get_ticks()
                        # print("Z key pressed")  # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg
                        
                        for i in [
                            (self.atk3, True, 100, 70, self.sp_damage[0], self.sp_damage[1]), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 100, 50, self.sp_damage_2nd[0], self.sp_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0 if self.facing_right else 0,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=i[1],
                                stun=(True, 0),
                                sound=(True, self.atk3_sound , self.x_slash_sound, None)
                                )
                            attack_display.add(attack)
                                    
                                    
                        # if current_time2 - self.last_atk_time > 1500:
                        #     attack_display.add(attack)
                        #     self.last_atk_time = current_time2
                        self.mana -=  self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=0.1,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True
                                )
                                # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[3].mana_cost
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks[4].is_ready():
                        for i in [0, 300]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 60 if self.facing_right else self.rect.centerx - 60,
                                y=self.rect.centery + 50,
                                frames=self.basic_slash2 if self.facing_right else self.basic_slash2_flipped,
                                frame_duration=BASIC_FRAME_DURATION / 2,
                                repeat_animation=1,
                                speed=4 if self.facing_right else -4,
                                dmg=self.basic_attack_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                sound=(True, self.basic_sound, None, None),
                                moving=True,
                                delay=(True, i),

                                hitbox_scale_y=0.3,
                                hitbox_scale_x=0.3,
                                # hitbox_offset_x=30 if self.facing_right else -30,
                                # hitbox_offset_y=60
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

                elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                        self.special_active = True
                        self.special_sound.play()
                    else:
                        pass

        else:
            if not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [0, 200, 400, 600, 800, 1000]: # 6
                            attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1,
                                frame_duration=10,
                                repeat_animation=1,
                                speed=-1 if self.facing_right else 1,
                                dmg=self.atk1_damage[0] * 0.3,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,
                                sound=(True, self.atk1_sound, None, None),
                                delay=(True, i),
                                use_live_position_on_delay=True
                                ) # Replace with the target
                            attack_display.add(attack)
                        #dash  
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')

            if not self.jumping and not self.is_dead(): # can be cast while jumping, I hope...
                if hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:

                        for i in [
                            (self.atk3, True, 100, 70, self.sp_damage[0], self.sp_damage[1]/2), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 100, 50, self.sp_damage_2nd[0], self.sp_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0 if self.facing_right else 0,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=i[1],
                                stun=(True, 0),
                                sound=(True, self.atk3_sound , self.x_slash_sound, None)
                                )
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

            if not self.jumping and not self.is_dead():
                if hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        current_time2 = pygame.time.get_ticks()
                        # print("Z key pressed")  # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg
                        
                        for i in [
                            (self.atk3_special, True, 130, 100, self.atk2_damage[0] * 2.4, True, self.atk2_damage[1], -20), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 70, 40, self.atk2_damage_2nd[0] * 2, False, self.atk2_damage_2nd[1], 50)
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + i[7],
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=7 if self.facing_right else -7,
                                dmg=i[4],
                                final_dmg=i[6],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=i[1],
                                continuous_dmg=i[1],
                                stun=(i[5], 40),
                                sound=(True, self.atk3_sound_special , self.x_slash_sound, None)
                                ) # Replace with the target
                            attack_display.add(attack)

                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=5,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage * 0.4,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True
                                )
                        attack_display.add(attack)

                        for i in [1500, 3000, 4500, 6000]:
                            attack1 = Attack_Display(
                                    x=hero1.x_pos if self.player_type == 2 else hero2.x_pos,
                                    y=hero1.y_pos if self.player_type == 2 else hero2.y_pos - 150,
                                    frames=self.real_sp, #frames=self.real_sp,
                                    frame_duration=120,
                                    repeat_animation=1,
                                    speed=0 if self.facing_right else 0,
                                    dmg=self.real_sp_damage * 0,
                                    final_dmg=0,
                                    who_attacks=self,
                                    who_attacked=hero1 if self.player_type == 2 else hero2,
                                    per_end_dmg=(False, True),
                                    disable_collide=False,
                                    sound=(True, self.sp_sound, self.sp_sound2, self.x_slash_sound),
                                    repeat_sound=True,
                                    delay=(True, i),
                                    follow=(False, True)
                                    )
                                    # Replace with the target
                            attack_display.add(attack1)

                            attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=5,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage * 0.2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True,
                                delay=(True, i)
                                )
                            attack_display.add(attack2)

                        




                        self.mana -=  self.attacks_special[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks_special[4].is_ready():
                        for i in [0, 300]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 60 if self.facing_right else self.rect.centerx - 60,
                                y=self.rect.centery + 50,
                                frames=self.basic_slash2 if self.facing_right else self.basic_slash2_flipped,
                                frame_duration=BASIC_FRAME_DURATION / 2,
                                repeat_animation=2,
                                speed=6 if self.facing_right else -6,
                                dmg=self.basic_attack_damage*DEFAULT_BASIC_ATK_DMG_BONUS,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,
                                heal=False,
                                continuous_dmg=False,
                                per_end_dmg=(False, False),
                                disable_collide=False,
                                stun=(False, 0),
                                sound=(True, self.basic_sound, None, None),
                                kill_collide=False,
                                delay=(True, i),

                                hitbox_scale_y=0.4,
                                hitbox_scale_x=0.4,
                                hitbox_offset_x=170,
                                hitbox_offset_y=60
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()
                        # print("Attack executed")
                    else:
                        pass
            
          
        
    # def activate_skill_1(self):
    #     if not self.special_active:
    #         self.atk1_move_speed += 0.3
    #         self.y_velocity = 0
    #         if self.facing_right:
    #             self.x_pos += self.atk1_move_speed
    #         else:
    #             self.x_pos -= self.atk1_move_speed
    #     else:
    #         self.atk1_move_speed += 0.3
    #         self.y_pos -= 0.2
    #         self.y_velocity = 0
    #         if self.facing_right:
    #             self.x_pos += self.atk1_move_speed
    #         else:
    #             self.x_pos -= self.atk1_move_speed
    #         self.jumping = True
    #         self.y_velocity = (DEFAULT_JUMP_FORCE * 0.5)

    def trigger_dash(self): # this thing so buggy, fix this soon
        

        if self.distance_covered < self.max_distance:
            if self.facing_right:
                self.x_pos += self.dash_speed
                self.distance_covered += self.dash_speed
            elif not self.facing_right:
                self.x_pos -= self.dash_speed
                self.distance_covered += self.dash_speed
        else:
            self.distance_covered = 0
        # print(self.distance_covered)
        
        
    
    
    def update(self):
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()

        self.keys = pygame.key.get_pressed()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed+3)
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        elif self.attacking1: # fixing the damn bug for this hero
            self.activate_dash = True
            
            if not self.special_active:
                self.dash_speed = self.default_dash_speed
                self.max_distance = self.default_max_distance
            else:
                self.dash_speed = self.special_dash_speed
                self.max_distance = self.special_max_distance

            if self.distance_covered >= self.max_distance:
                self.activate_dash = False
                self.attacking1 = False
                self.distance_covered = 0
            else: 
                if self.activate_dash:
                    self.trigger_dash()
            self.atk1_animation()  

        elif self.jumping:
            self.jump_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
            
        elif self.attacking2: # not special, used by skill2, when special, used by skill 3
            self.atk1_move_speed += 0.4 #just trying, plan is to make this special move that knokes back enemies 
            if not self.special_active:
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
            elif self.special_active:
                if self.player_type == 1: # idea for slow, if enemy ffacing right, - x pos, else + x pos
                    if self.facing_right:
                        hero2.x_pos += self.atk3_move_speed
                    else:
                        hero2.x_pos -= self.atk3_move_speed
                if self.player_type == 2:
                    if self.facing_right:
                        hero1.x_pos += self.atk3_move_speed
                    else:
                        hero1.x_pos -= self.atk3_move_speed
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation(2) #animation speed increase
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
        elif self.sp_attacking:
            self.x_pos = hero1.x_pos if self.player_type == 2 else hero2.x_pos
            self.y_pos = hero1.y_pos if self.player_type == 2 else hero2.y_pos
            self.sp_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        elif self.basic_attacking:
            self.basic_animation()
            
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED+3)
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        # Apply gravity
        # if not self.attacking2:
        self.y_velocity += (DEFAULT_GRAVITY - (DEFAULT_GRAVITY * 0.02))
        self.y_pos += self.y_velocity
        # else:
        #     self.jumping = False

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

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False

        
        super().update()


















# Animation Counts
# WATER_PRINCESS_BASIC_COUNT = 
WATER_PRINCESS_JUMP_COUNT = 6
WATER_PRINCESS_RUN_COUNT = 10
WATER_PRINCESS_IDLE_COUNT = 8
WATER_PRINCESS_ATK1_COUNT = 7
WATER_PRINCESS_ATK2_COUNT = 27
WATER_PRINCESS_ATK3_COUNT = 12
WATER_PRINCESS_SP_COUNT = 32
WATER_PRINCESS_DEATH_COUNT = 16

WATER_PRINCESS_SURF_COUNT = 8

# WATER_PRINCESS_ATK1 = 0
# WATER_PRINCESS_ATK2 = 0
# WATER_PRINCESS_ATK3 = 0
# WATER_PRINCESS_SP = 0
# ---------------------
# print((WATER_PRINCESS_ATK2 * 0.01) * 4 * 5)

WATER_PRINCESS_ATK1_SIZE = 2
WATER_PRINCESS_ATK2_SIZE = 2
WATER_PRINCESS_ATK3_SIZE = 1
WATER_PRINCESS_SP_SIZE = 4  


class Water_Princess(Player):
    def __init__(self, player_type):
        super().__init__(player_type)
        self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        self.player_type = player_type
        self.name = "Water Princess"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 40
        self.intelligence = 48
        self.agility = 20

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

        # SPECIAL TRAIT
            # Mana cost delayed
            # Mana cast high, but mana cost delay reduced by 15%
            #example:
            # if mana cost is 160, reduce mama until end of attack frame, 
            # but that 160 is reduced by 15%
            # total mana depleted = (160*0.85 or 160-(160*0.15)) = 136 total mana cost

            # mana reduce 20% if special active



        self.atk1_mana_cost = 100
        self.atk2_mana_cost = 160
        self.atk3_mana_cost = 200
        self.sp_mana_cost = 240

        #go to attacks section to calculate mana

        self.atk1_cooldown = 15000
        self.atk2_cooldown = 26000
        self.atk3_cooldown = 40000
        self.sp_cooldown = 65000

        self.atk1_damage = (5/40, 0)
        self.atk1_damage_2nd = 20 #-----
        self.atk2_damage = (12.5/40, 0) # total dmg 40 #rain
        self.atk2_damage_2nd = (3/40, 5) #circling
        self.atk3_damage = (15/25, 0) 
        self.atk3_damage_2nd = 20 #-----

        self.sp_damage = (20/35, 0) 
        self.sp_damage_2nd = (10/42, 20) 
        self.sp_damage_3rd = (10/15, 0) #-----

        self.sp_atk1_damage = 0.2 # (5/25, 0) #-----
        self.sp_atk2_damage = 0.3#(totaldmg 9*2=18) # =0.4166 (12.5/30, 0) # rain #-----
        self.sp_atk2_damage_2nd = (5/30, 2) #(*5) #circling #------
        self.sp_atk2_damage_3rd = (2/15, 5) #(*10) #watershot #-----
        self.sp_atk3_damage = (15/20, 0) #10+(15*2)= #-----
        # sp_atk3 heal = 20/2:instant=10, 
        # dmg_mult = 0
        # self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        # self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        # self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        # self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)
        
        self.player_surf_index = 0
        self.player_surf_index_flipped = 0

        self.player_atk1_2nd_index = 0
        self.player_atk1_2nd_index_flipped = 0
        
        # Player Animation Source
        basic_ani = [r'assets\characters\Water princess\png\08_2_atk\2_atk_', 21, 0]
        atk1_ani_2nd = [r'assets\characters\Water princess\png\12_defend\defend_', 12, 0]

        jump_ani = [r'assets\characters\Water princess\png\04_j_up\j_up_', WATER_PRINCESS_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\Water princess\png\02_walk\walk_', WATER_PRINCESS_RUN_COUNT, 0]

        surf_ani = [r'assets\characters\Water princess\png\03_surf\surf_', WATER_PRINCESS_SURF_COUNT, 0]

        idle_ani = [r'assets\characters\Water princess\png\01_idle\idle_', WATER_PRINCESS_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\Water princess\png\07_1_atk\1_atk_', WATER_PRINCESS_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\Water princess\png\09_3_atk\3_atk_', WATER_PRINCESS_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\Water princess\png\11_heal\heal_', WATER_PRINCESS_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\Water princess\png\10_sp_atk\sp_atk_', WATER_PRINCESS_SP_COUNT, 0]
        death_ani = [r'assets\characters\Water princess\png\14_death\death_', WATER_PRINCESS_DEATH_COUNT, 0]

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
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\472234276_8613137162147060_446401069957588690_n.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\tumblr_8ca04de6143efee03f34ea8c32aca437_a117ed18_1280.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Screenshot 2025-01-26 221227.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Untitled (1 x 1 in).png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\placeholder.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\472234276_8613137162147060_446401069957588690_n.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\tumblr_8ca04de6143efee03f34ea8c32aca437_a117ed18_1280.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Screenshot 2025-01-26 221227.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Untitled (1 x 1 in).png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = load_attack( # rain
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=WATER_PRINCESS_ATK1_SIZE, 
        rotation=0,
    )
        self.atk2 = load_attack( #circling water
        filepath=r"assets\attacks\water princess\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=WATER_PRINCESS_ATK2_SIZE, 
        rotation=0,
    )
        self.atk2_rain = load_attack(
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=6, 
        rotation=-45,
    )
        self.atk2_rain_flipped = load_attack(
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=6, 
        rotation=45,
    )
        
        self.atk3 = load_attack( # healing frames
        filepath=r"assets\attacks\water princess\3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=5, 
        columns=5, 
        scale=WATER_PRINCESS_ATK3_SIZE, 
        rotation=0,
    )
        
        self.sp = load_attack( # bubbles
        filepath=r"assets\attacks\water princess\4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=5, 
        scale=WATER_PRINCESS_SP_SIZE, 
        rotation=0,
    )
        
        self.watershot = load_attack(
        filepath=r"assets\attacks\water princess\watershot.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3 , 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        self.watershot_flipped = load_attack_flipped(
        filepath=r"assets\attacks\water princess\watershot.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3 , 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        

        self.sp_atk1 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=5, 
        columns=5, 
        scale=1.5, 
        rotation=0,
    )
        self.sp_atk2 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=6, 
        columns=5, 
        scale=2, 
        rotation=0,
    )
        self.sp_atk3 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=1.2, 
        rotation=0,
    )
        self.sp_atk4 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=5, 
        scale=4, 
        rotation=0,
    )
    
        # assets\attacks\water princess\basic_atk1\water60000
        # assets\attacks\water princess\atk4\splash big\water400
        self.sp1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\spiral\water900", 42, starts_at_zero=True,
        size=0.2)

        self.sp2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\splash big\water400", 16, starts_at_zero=True,
        size=0.3)

        self.basic_atk1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        rotate=90, size=0.15)

        self.basic_atk1_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        rotate=-90, flip=True, size=0.15)

        self.basic_atk2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        size=0.5, flip=True)

        self.basic_atk2_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        size=0.6)
# (fr'{folder}{str(frame_number).zfill(2)}.png')

        
    

        # Player Animations Load
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)

        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)  

        self.player_surf = self.load_img_frames(surf_ani[0], surf_ani[1], surf_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_surf_flipped = self.load_img_frames_flipped(surf_ani[0], surf_ani[1], surf_ani[2], DEFAULT_CHAR_SIZE_2)

        self.player_atk1_2nd = self.load_img_frames(atk1_ani_2nd[0], atk1_ani_2nd[1], atk1_ani_2nd[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_2nd_flipped = self.load_img_frames_flipped(atk1_ani_2nd[0], atk1_ani_2nd[1], atk1_ani_2nd[2], DEFAULT_CHAR_SIZE_2)

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
                skill_img=special_skill_1,
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


        
        # make sure the divisor aligned with how many frames the attack is, 
        # (you can refer to the dmg since they are the same)
        # print(self.attacks[0].mana_cost)
        '''the calculations are correct, must test with mana_reduce items'''
        '''calculated mana is not correct, need to update correct values to apply mana_reduce items'''
        '''refer to the new function below'''

        '''good, the values are now correct.'''

    def update_mana_values(self):
        self.mana_mult = 0.2 if not self.special_active else 0.25
        self.atk1_mana_consume = (self.attacks[0].mana_cost/40) - ((self.attacks[0].mana_cost/40)*self.mana_mult)
        self.atk2_mana_consume = (self.attacks[1].mana_cost/40) - ((self.attacks[1].mana_cost/40)*self.mana_mult)
        self.atk3_mana_consume = (self.attacks[2].mana_cost/25) - ((self.attacks[2].mana_cost/25)*self.mana_mult)
        self.atk4_mana_consume = (self.attacks[3].mana_cost/35) - ((self.attacks[3].mana_cost/35)*self.mana_mult)

        self.atk1_special_mana_consume = (self.attacks_special[0].mana_cost/25) - ((self.attacks_special[0].mana_cost/25)*self.mana_mult)
        self.atk2_special_mana_consume = (self.attacks[1].mana_cost/40) - ((self.attacks[1].mana_cost/40)*self.mana_mult)
        self.atk3_special_mana_consume = (self.attacks[2].mana_cost/25) - ((self.attacks[2].mana_cost/25)*self.mana_mult)
        self.atk4_special_mana_consume = (self.attacks[3].mana_cost/35) - ((self.attacks[3].mana_cost/35)*self.mana_mult)
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed - (self.speed * 0.075)) if not self.special_active else (self.speed + (self.speed * 0.4))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed - (self.speed * 0.075)) if not self.special_active else (self.speed + (self.speed * 0.4))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = (DEFAULT_JUMP_FORCE - (DEFAULT_JUMP_FORCE * 0.05))
                    self.last_atk_time = current_time  # Update the last jump time
            
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        for i in [
                            (80, 40, 100, self.atk1_damage[0], self.atk1_damage[1], self.atk1_sound, False, 0.4, 0.4, True, True, True, True, (self.atk1, self.atk1)),
                            (70, 80, 100, self.atk1_damage_2nd, 0, self.atk1_sound, True, 0.7, 0.6, False, False, False, False, (self.basic_slash, self.basic_slash_flipped)) # this is so inefficient
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx -i[0],
                                y=self.rect.centery + i[1],
                                frames=i[13][0] if self.facing_right else i[13][1],
                                frame_duration=i[2],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[3],
                                final_dmg=i[4],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 300),
                                sound=(True, i[5], None, None),

                                moving=i[6],
                                hitbox_scale_x=i[7],
                                hitbox_scale_y=i[8],

                                heal=i[9],
                                heal_enemy=i[10],

                                continuous_dmg=i[11],

                                consume_mana=[i[12], self.atk1_mana_consume]

                            )
                            attack_display.add(attack)

                        
                        
                        # self.mana -= self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(300,True), (1000,False)]: # WATER RAIN
                            attack = Attack_Display(
                                x=self.rect.centerx + 350 if self.facing_right else self.rect.centerx -350,
                                y=self.rect.centery,
                                frames=self.atk2_rain if self.facing_right else self.atk2_rain_flipped,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk2_damage[0],
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                consume_mana=[i[1], self.atk2_mana_consume]
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,170), (800, 340), (1300,0), (1800, 680), (2300, 510)]:
                            attack = Attack_Display( # CIRCLING WATERS
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.atk2,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk2_damage_2nd[0],
                                final_dmg=self.atk2_damage_2nd[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4
                                ) # Replace with the target
                            attack_display.add(attack)
                        # self.mana -= self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
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
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage_2nd,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                heal=True,
                                self_moving=True,
                                self_kill_collide=True,
                                follow_offset=(0, 70)
                                )
                        attack_display.add(attack)

                        attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage[0],
                                final_dmg=self.atk3_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[True, self.atk3_mana_consume]
                                )
                        attack_display.add(attack2)
                        
                        # self.mana -= self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-cnsm mana 7-dmg/fnldmg
                     (self.sp, 100, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage),#bubble
                     (self.sp1, 40, (120, 60), (True, 60), (True, 50), (0.3, 0.5), False, self.sp_damage_2nd),#spiral
                     (self.sp2, 80, (120, 60), (True, 5), (True, 1500), (0.3, 0.5), False, self.sp_damage_3rd)#splash
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=i[7][0],
                                final_dmg=i[7][1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                sound=(True, self.sp_sound, None, None),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1], 
                                consume_mana=[i[6], self.atk4_mana_consume],
                                stop_movement=(True, 1, 2)
                                
                                ) # Replace with the target
                            attack_display.add(attack)


                        # self.mana -=  self.attacks[3].mana_cost
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.attacks[4].is_ready():
                        for i in [
                            (200, self.basic_atk2, self.basic_atk2_flipped, 30, (50, 60, 0.4, 0.2), self.basic_attack_damage*1.5),
                            (1000, self.basic_slash, self.basic_slash_flipped, 100, (70, 80, 0.8, 0.6), self.basic_attack_damage),
                            (2000, self.basic_atk1, self.basic_atk1_flipped, 80, (60, 75, 0.75, 0.2), self.basic_attack_damage*5)
                            
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[4][0] if self.facing_right else self.rect.centerx - i[4][0],
                                y=self.rect.centery + i[4][1],
                                frames=i[1] if self.facing_right else i[2],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[5],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, i[0]),
                                moving=True,
                                hitbox_scale_x=i[4][2],
                                hitbox_scale_y=i[4][3]
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
                        for i in [
                            (80, 40, 100, self.sp_atk1_damage, 0, self.atk1_sound, False, 0.2, 0.4, False, False, True, True, (self.sp_atk1, self.sp_atk1)),
                            (70, 80, 100, self.atk1_damage_2nd, 0, self.atk1_sound, True, 0.7, 1.2, False, False, False, False, (self.basic_slash, self.basic_slash_flipped)) # this is so inefficient
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx -i[0],
                                y=self.rect.centery + i[1],
                                frames=i[13][0] if self.facing_right else i[13][1],
                                frame_duration=i[2],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[3],
                                final_dmg=i[4],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 300),
                                sound=(True, i[5], None, None),

                                moving=i[6],
                                hitbox_scale_x=i[7],
                                hitbox_scale_y=i[8],

                                heal=i[9],
                                heal_enemy=i[10],

                                continuous_dmg=i[11],
                                stun=(i[11], 40),

                                consume_mana=[i[12], self.atk1_special_mana_consume],

                                stop_movement=(True, 1, 2)

                            )
                            attack_display.add(attack)

                        # self.mana -= self.attacks[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_2nd_index = 0
                        self.player_atk1_2nd_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(300,True), (1000,False)]: # WATER RAIN
                            attack = Attack_Display(
                                x=self.rect.centerx + 350 if self.facing_right else self.rect.centerx -350,
                                y=self.rect.centery,
                                frames=self.atk2_rain if self.facing_right else self.atk2_rain_flipped,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                consume_mana=[i[1], self.atk2_special_mana_consume]
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,170), (800, 340), (1300,0), (1800, 680), (2300, 510)]:
                            attack = Attack_Display( # CIRCLING WATERS
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.sp_atk2,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_2nd[0],
                                final_dmg=self.sp_atk2_damage_2nd[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,510), (1300, 680), (1800,0), (2300, 340), (2800, 170)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=50,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[0],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(600,680), (1600, 510), (1900,0), (2200, 170), (2500, 340)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=50,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[0],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        
                        # self.mana -= self.attacks[1].mana_cost
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
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage_2nd/2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                heal=True,
                                self_moving=True,
                                self_kill_collide=True,
                                follow_offset=(0, 70)
                                )
                        attack_display.add(attack)

                        attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=0,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[True, self.atk3_special_mana_consume]
                                )
                        attack_display.add(attack2)

                        attack3 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.sp_atk3,
                                frame_duration=120,
                                repeat_animation=2,
                                speed=0,
                                dmg=self.sp_atk3_damage[0],
                                final_dmg=self.sp_atk3_damage[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                delay=(True, 400),
                                sound=(True, self.atk3_sound , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[False, self.atk3_mana_consume]
                                )
                        attack_display.add(attack3)
                        
                        # self.mana -= self.attacks[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-cnsm mana 7-dmg/fnldmg 8-moving
                     (self.sp, 100, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage, (False,0)),#bubble
                     (self.sp_atk4, 50, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage, (False,0)),#bubble2ndfront
                     (self.sp_atk4,50,(550, -100),(False, 0),(True, 1600), (0.55, 0.5), False, self.sp_damage, (False,0)),#bubble2ndend
                     (self.sp1, 40, (120, 60), (True, 60), (True, 50), (0.3, 0.5), False, self.sp_damage_2nd, (True, 4.5)),#spiral
                     (self.sp2, 80, (550, 60), (True, 5), (True, 1500), (0.3, 0.5), False, self.sp_damage_3rd, (False,0))#splash
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=i[8][1] if self.facing_right else -i[8][1],
                                dmg=i[7][0],
                                final_dmg=i[7][1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                sound=(True, self.sp_sound, None, None),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1],
                                consume_mana=[i[6], self.atk4_special_mana_consume],
                                moving=i[8][0],
                                stop_movement=(True, 1, 2)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(100,130*1.23), (300, 191.1*1.23), (700,275*1.23), (1100, 369.5*1.23), (1500, 550*1.23)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 30,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=40,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[1],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7
                                ) # Replace with the target
                            attack_display.add(attack)

                        # self.mana -=  self.attacks[3].mana_cost
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
                        for i in [
                            (200, self.basic_atk2, self.basic_atk2_flipped, 30, (50, 60, 0.4, 0.2), self.basic_attack_damage*1.5,(False, 1, 1)),
                            (1000, self.basic_slash, self.basic_slash_flipped, 100, (70, 80, 0.8, 0.6), self.basic_attack_damage,(False, 1, 1)),
                            (2000, self.basic_atk1, self.basic_atk1_flipped, 80, (60, 75, 0.75, 0.2), self.basic_attack_damage*5,(True, 1, 1))
                            
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[4][0] if self.facing_right else self.rect.centerx - i[4][0],
                                y=self.rect.centery + i[4][1],
                                frames=i[1] if self.facing_right else i[2],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[5],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, i[0]),
                                moving=True,
                                hitbox_scale_x=i[4][2],
                                hitbox_scale_y=i[4][3],
                                stop_movement=i[6]
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

                
     
            
    def run_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_run_index, _ = self.animate(self.player_run, self.player_run_index, loop=True)
            else:
                self.player_run_index_flipped, _ = self.animate(self.player_run_flipped, self.player_run_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_surf_index, _ = self.animate(self.player_surf, self.player_surf_index, loop=True)
            else:
                self.player_surf_index_flipped, _ = self.animate(self.player_surf_flipped, self.player_surf_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
    
    def simple_idle_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_idle_index, _ = self.animate(self.player_idle, self.player_idle_index, loop=True)
            else:
                self.player_idle_index_flipped, _ = self.animate(self.player_idle_flipped, self.player_idle_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_surf_index, _ = self.animate(self.player_surf, self.player_surf_index, loop=True)
            else:
                self.player_surf_index_flipped, _ = self.animate(self.player_surf_flipped, self.player_surf_index_flipped, loop=True)

        self.last_atk_time -= animation_speed

    def atk1_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_atk1_index, self.attacking1 = self.animate(self.player_atk1, self.player_atk1_index, loop=False)
            else:
                self.player_atk1_index_flipped, self.attacking1 = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False)

        else:
            if self.facing_right:
                self.player_atk1_2nd_index, self.attacking1 = self.animate(self.player_atk1_2nd, self.player_atk1_2nd_index, loop=False)
            else:
                self.player_atk1_2nd_index_flipped, self.attacking1 = self.animate(self.player_atk1_2nd_flipped, self.player_atk1_2nd_index_flipped, loop=False)
        self.last_atk_time -= animation_speed

    def update(self):
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(animation_speed=self.running_animation_speed)
                

        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation(-4)
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

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False


        # if self.running:
        #     print('is running')
        self.update_mana_values()
        '''test code are below, for checking correct mana values'''
        # self.atk1_mana_consume = (self.attacks[0].mana_cost/40) - ((self.attacks[0].mana_cost/40)*self.mana_mult)
        # print(self.attacks[0].mana_cost)

        
        super().update()





'''Forest Ranger Config'''
FR_JUMP_COUNT = 6
FR_RUN_COUNT = 8
FR_IDLE_COUNT = 8
FR_ATK1_COUNT = 7
FR_ATK3_COUNT = 9
FR_SP_COUNT = 16
FR_DEATH_COUNT = 4

FR_BASIC = 6
FR_ATK1 = 4
FR_ATK2 = 40
FR_ATK3 = 10
FR_SP = 3

FR_SPECIAL_ATK3 = 10
# ---------------------
# WANDERER_MAGICIAN_ATK1_MANA_COST = 70
# WANDERER_MAGICIAN_ATK2_MANA_COST = 125
# WANDERER_MAGICIAN_ATK3_MANA_COST = 125
# WANDERER_MAGICIAN_SP_MANA_COST = 170

FR_BASIC_SIZE = 1.5
FR_ATK1_SIZE = 2
FR_ATK2_SIZE = 1
FR_ATK3_SIZE = 1.5
FR_SP_SIZE = 1.3

FR_SPECIAL_ATK3_SIZE = 2
FR_SPECIAL_BASICATK1_SIZE = 2

# WANDERER_MAGICIAN_ATK1_COOLDOWN = 8000
# WANDERER_MAGICIAN_ATK2_COOLDOWN = 15000 + 9000
# WANDERER_MAGICIAN_ATK3_COOLDOWN = 26000
# WANDERER_MAGICIAN_SP_COOLDOWN = 60000

# WANDERER_MAGICIAN_ATK1_DAMAGE = 0 # dmg at the input, sry
# WANDERER_MAGICIAN_ATK2_DAMAGE = (18/40, 0)
# WANDERER_MAGICIAN_ATK3_DAMAGE = (30/10, 5) #26
# WANDERER_MAGICIAN_SP_DAMAGE = (55, 0)

class Forest_Ranger(Player): #NEXT WORK ON THE SPRITES THEN COPY EVERYTHING SINCE IM DONE 4/6/25 10:30pm
    def __init__(self, player_type):
        super().__init__(player_type)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Forest Ranger"

        self.hitbox_rect = pygame.Rect(0, 0, 45, 100)

        # stat
        self.strength = 32
        self.intelligence = 60
        self.agility = 38
        
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        # self.special_default_max_mana = self.max_mana # max mana and this variable mustt  be the same
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = self.agility * self.agi_mult

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20

        self.atk1_mana_cost = 70
        self.atk2_mana_cost = 150
        self.atk3_mana_cost = 125
        self.sp_mana_cost = 175

        self.atk1_cooldown = 8000
        self.atk2_cooldown = 20000 + 9000
        self.atk3_cooldown = 26000  
        self.sp_cooldown = 60000

        self.atk1_damage = (0, 0)
        self.atk2_damage = (15/40, 0)
        self.atk3_damage = (26/10, 8)
        self.sp_damage = (55, 0)
        self.sp_damage_2nd = (4.5/16, 0)
        
        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        jump_ani = [r'assets\characters\Forest Ranger\PNG\jump_full\jump_', 22, 0]
        run_ani = [r'assets\characters\Forest Ranger\PNG\run\run_', 10, 0]
        idle_ani= [r'assets\characters\Forest Ranger\PNG\idle\idle_', 12, 0]
        atk1_ani= [r'assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 0]
        atk2_ani= [r'assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 0]
        atk3_ani= [r'assets\characters\Wanderer Magican\attack 2 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 0]
        sp_ani= [r'assets\characters\Wanderer Magican\charge pngs', WANDERER_MAGICIAN_SP_COUNT, 0]
        death_ani= [r'assets\characters\Forest Ranger\PNG\death\death_', 19, 0]

        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3')
        self.atk1_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        
        # # Player Skill Animations Source
        basic = [r'assets\attacks\Basic Attack\wanderer magician\Charge_1_', WANDERER_MAGICIAN_BASIC, 1]
        atk1 = [r'assets\attacks\wanderer magician\atk1\image_', WANDERER_MAGICIAN_ATK1, 1]
        atk2 = [r'assets\attacks\wanderer magician\atk2', WANDERER_MAGICIAN_ATK2, 1]
        atk3 = [r'assets\attacks\wanderer magician\atk3\Explosion_blue_circle', WANDERER_MAGICIAN_ATK3, 0]
        sp = [r'assets\attacks\wanderer magician\sp atk\vv', WANDERER_MAGICIAN_SP, 0]

        special_atk3 = [r'assets\attacks\wanderer magician\special1\Explosion_blue_oval', WANDERER_MAGICIAN_SPECIAL_ATK3, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_06.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_08.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon9.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Massive_Rasen.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\special.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\ChatGPT Image Apr 18, 2025, 07_46_01 AM.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\HealingWindIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_02.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.basic = self.load_img_frames(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)
        self.basic_flipped = self.load_img_frames_flipped(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)

        self.atk1 = self.load_img_frames_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, 90)
        self.atk1_flipped = self.load_img_frames_flipped_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, -90)
        self.atk2 = self.load_img_frames_tile_method(atk2[0], atk2[1], atk2[2], WANDERER_MAGICIAN_ATK2_SIZE)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], WANDERER_MAGICIAN_ATK3_SIZE)
        self.sp = self.load_img_frames(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)
        self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)

        self.special_atk3 = self.load_img_frames(special_atk3[0], special_atk3[1], special_atk3[2], WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE)

        self.special_basic = load_attack(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.special_basic_flipped = load_attack_flipped(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        
        self.sp_special = load_attack(
        filepath=r"assets\attacks\wanderer magician\sp atk special\2.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=8, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE)
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
                skill_img=self.basic_icon2,
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

        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=special_skill_2,
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
                skill_img=self.basic_icon2,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )
   
        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana

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
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.can_move():
            if not (self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking):
                if right_hotkey:  # Move right
                    self.running = True
                    self.facing_right = True #if self.player_type == 1 else False
                    self.x_pos += (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos > TOTAL_WIDTH - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                        self.x_pos = TOTAL_WIDTH - (self.hitbox_rect.width/2)
                elif left_hotkey:  # Move left
                    self.running = True
                    self.facing_right = False #if self.player_type == 1 else True
                    self.x_pos -= (self.speed + ((self.speed * 0.1) if self.special_active else 0))
                    if self.x_pos < (ZERO_WIDTH + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                        self.x_pos = (ZERO_WIDTH + (self.hitbox_rect.width/2))
                else:
                    self.running = False

                if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                    self.jumping = True
                    self.y_velocity = DEFAULT_JUMP_FORCE  
                    self.last_atk_time = current_time  # Update the last jump time
            
        if not self.can_cast():
            return
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=7 if self.facing_right else -7,
                            dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 3,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=100,
                            repeat_animation=2,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0], 
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
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
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=hero1.x_pos if self.player_type == 2 else hero2.x_pos, #self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 150, # in front of him
                            y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                            frames=self.atk3,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)
                            ) # Replace with the target
                        attack_display.add(attack)
                        # print(WANDERER_MAGICIAN_ATK3_DAMAGE[0], WANDERER_MAGICIAN_ATK3_DAMAGE[1])
                        self.mana -=  self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery,
                            frames=self.sp if self.facing_right else self.sp_flipped,
                            frame_duration=40,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.sp_sound , None, None),
                            delay=(True, 5000)
                            ) 
                        attack_display.add(attack)
                        self.mana -=  self.attacks[3].mana_cost
                        self.attacks[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

            if not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.mana >= 0 and self.attacks[4].is_ready():
                    attack = Attack_Display(
                        x=self.rect.centerx,
                        y=self.rect.centery + 30,
                        frames=self.basic if self.facing_right else self.basic_flipped,
                        frame_duration=100,
                        repeat_animation=5,
                        speed=7 if self.facing_right else -7,
                        dmg=self.basic_attack_damage,
                        final_dmg=0,
                        who_attacks=self,
                        who_attacked=hero1 if self.player_type == 2 else hero2,
                        moving=True,

                        sound=(True, self.atk1_sound, None, None),
                        kill_collide=True,
                        delay=(True, 500)
                        )
                    attack_display.add(attack)
                    self.mana -= 0
                    self.attacks[4].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0

                    self.basic_attacking = True

                    # print("Attack executed")
                else:
                    pass

            elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                    self.special_active = True
                    self.basic_sound.play()
                else:
                    pass






        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(0, 30), (40, 60), (40, 0)]:
                            attack = Attack_Display(
                                x=self.rect.centerx - i[0] if self.facing_right else self.rect.centerx + i[0],
                                y=self.rect.centery + i[1] if self.facing_right else self.rect.centery + i[1],
                                frames=self.atk1 if self.facing_right else self.atk1_flipped,
                                frame_duration=100,
                                repeat_animation=5,
                                speed=7 if self.facing_right else -7,
                                dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 1.2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=hero1 if self.player_type == 2 else hero2,
                                moving=True,

                                kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500)) # Replace with the target
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=40,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=(self.atk2_damage[0]*2) + ((self.atk2_damage[0]*2) * (SPECIAL_MULTIPLIER * 0.25)),
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
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
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=hero1.x_pos if self.player_type == 2 else hero2.x_pos,
                            y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
                            frames=self.special_atk3,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk3_damage[0] + (self.atk3_damage[0] * (SPECIAL_MULTIPLIER * 0.25)),
                            final_dmg=self.atk3_damage[1] + (self.atk3_damage[1] * (SPECIAL_MULTIPLIER * 0.25)),
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=hero1.x_pos if self.player_type == 2 else hero2.x_pos,
                            y=hero1.y_pos + 40,
                            frames=self.sp_special,
                            frame_duration=160,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage_2nd[0],
                            final_dmg=self.sp_damage_2nd[1],
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=False,
                            follow=(False, True),
                            follow_offset=(0, 50),

                            kill_collide=False,
                            sound=(True, self.sp_sound , self.atk3_sound, None),
                            delay=(True, 800)
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

            if not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.mana >= 0 and self.attacks_special[4].is_ready():
                    for i in [(500, 50), (700, 30), (900, 10)]:
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + i[1],
                            frames=self.special_basic if self.facing_right else self.special_basic_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=8 if self.facing_right else -8,
                            dmg=self.basic_attack_damage/2.4,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=hero1 if self.player_type == 2 else hero2,
                            moving=True,

                            sound=(True, self.basic_sound, self.atk1_sound, None),
                            kill_collide=True,
                            delay=(True, i[0]),

                            hitbox_scale_x=0.2,
                            hitbox_scale_y=0.2
                            )
                        attack_display.add(attack)


                    

                    self.mana -= 0
                    self.attacks_special[4].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    
                    self.basic_attacking = True

                    # print("Attack executed")
                else:
                    pass

        # print(self.running)
        # print(self.player_type)
        # print(len(self.player_run), len(self.player_run_flipped))
        # print("Run Animation Index:", self.player_run_index)

     
        
    def update(self):
        super().update()
        # print(self.stunned)
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(hero1 if self.player_type == 2 else hero2)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()
        
        self.keys = pygame.key.get_pressed()

        self.inputs()
        self.move_to_screen()

        self.detect_and_display_damage()
        self.update_damage_numbers(screen)
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.attacking1:
            self.atk1_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking2:
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation(-11)

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

        # print(self.basic_attack_animation_speed)
        # print(f'cd:{self.basic_attack_cooldown}')
        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        if not self.is_dead():
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type)

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
                self.mana += (self.mana_regen + (self.mana_regen * (0.20 if not self.special_active else 0.30)))
            if not DISABLE_HEAL_REGEN:
                self.health += self.health_regen
        else:
            self.health = 0

        if not DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                self.max_mana = min(self.special_bonus_mana, self.max_mana + 10)
                if self.special <= 0:
                    self.special_active = False
                    self.max_mana = min(self.base_max_mana, self.max_mana + 10)
                    #self.apply_item_bonuses()
        # print(self.basic_attack_damage)
                # self.max_mana = min(200, self.max_mana + 10)

        # self.special += 0.1
        # print(self.special)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
# class Button:
#     def __init__(self, x, y, width, height, text, color, text_color):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.color = color
#         self.text_color = text_color
#         self.font = pygame.font.SysFont("Times New Roman", 16)

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, self.rect)
#         text_surf = self.font.render(self.text, global_vars.TEXT_ANTI_ALIASING, self.text_color)
#         text_rect = text_surf.get_rect(center=self.rect.center)
#         screen.blit(text_surf, text_rect)

#     def is_clicked(self, pos):
#         return self.rect.collidepoint(pos)


# button1 = Button(
#     x=50,
#     y=50,
#     width=50,
#     height=50,
#     text='START!',
#     color='Green',
#     text_color='Blue'
# )


   

# #-------------------------------------
# #if have time to make, make the players more centralized

# #inside player class
# def set_opponent(self, opponent):
#     self.opponent = opponent

# #call after initializing both heroes
# PLAYER_1_SELECTED_HERO.set_opponent(PLAYER_2_SELECTED_HERO)
# PLAYER_2_SELECTED_HERO.set_opponent(PLAYER_1_SELECTED_HERO)

# # simplify/modify attack logic inside input, attack.
# who_attacked=self.opponent,

# #instead of this :l
# who_attacked=PLAYER_1_SELECTED_HERO if self.player_type == 2 else PLAYER_2_SELECTED_HERO,

# #----------------------------------------------------
# Declaration of the object sprites (Single instance)

# fire_wizard_copy = Fire_Wizard(2)

# fire_wizard = Fire_Wizard(PLAYER_1)
# wanderer_magician = Wanderer_Magician(PLAYER_2)

# # Group of objects sprites (Multiple instances)
# fire_wizard_group = pygame.sprite.Group()
# fire_wizard_group.add(fire_wizard)

# wanderer_magician_group = pygame.sprite.Group()
# wanderer_magician_group.add(wanderer_magician)


# fire_wizard = None
# wanderer_magician = None

# fire_wizard_group = None
# wanderer_magician_group = None

# def detect_collision():
#     for attack in wanderer_magician_group:  # Loop through each sprite in the group
#         if pygame.sprite.spritecollide(attack, fire_wizard_group, False):
#             return True
#     return False



























from gameloop import game
from gameloop import reset_all
from gameloop import menu
from gameloop import fade

scale = 0.8
center_pos = (width / 2, height / 2)

# class ImageButton:
#     def __init__(self, image_path, pos, scale, text, font_path, font_size, text_color, move_y=0, hover_move=2, fku=False, scale_val=(0,0)):
#         # Load and scale the image
#         self.hover_pos = pos
#         self.hover_move = hover_move
#         self.fku = fku
#         self.scale_val = scale_val
#         if self.fku:
#             self.original_image = pygame.transform.scale(
#         pygame.image.load(self.original_image).convert_alpha(), (self.scale_val[0], self.scale_val[1]))
#         else:
#             self.original_image = pygame.image.load(image_path).convert_alpha()

#         self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
#         self.rect = self.image.get_rect(center=pos)

#         # Text
#         self.text = text
#         self.font = pygame.font.Font(font_path, int(font_size*7.142857142857143)) # Font size = 100
#         self.text_color = text_color
#         self.text_surf = pygame.transform.rotozoom(self.font.render(self.text, global_vars.TEXT_ANTI_ALIASING, self.text_color), 0, 0.2)
            
#         self.text_rect = self.text_surf.get_rect(center=self.rect.center)

#     def draw(self, screen, mouse_pos):
#         if self.rect.collidepoint(mouse_pos):
#             self.rect.centery = self.hover_pos[1] + self.hover_move 
#             self.text_rect.centery = self.hover_pos[1] + self.hover_move
#         else:
#             self.rect.centery = self.hover_pos[1]
#             self.text_rect.centery = self.hover_pos[1]
        
#         # Draw the image and text
#         screen.blit(self.image, self.rect)
#         screen.blit(self.text_surf, self.text_rect)

#     def is_clicked(self, mouse_pos):
#         # Check if button is clicked
#         if self.rect.collidepoint(mouse_pos):
#             return True
#         return False
    








class Item:
    def __init__(self, name, image_path, bonus_type, bonus_value):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (75, 75))
        self.bonus_type = bonus_type  # e.g., 'hp', 'mana', 'atk'
        self.bonus_value = bonus_value
        self.rect = self.image.get_rect(center=center_pos)

        self.info = {type_: value for type_, value in zip(self.bonus_type, self.bonus_value)}

                                    # (items[5].image, (75, height - 300), items[5], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30))
        # self.decor_rect = pygame.Rect(self.rect.centerx - 30, self.rect.centery - 30, 60, 60)
    
    def update(self, position):
        stats = ',-> '.join(f"{key}: {'' if val < 0 else '+'}{val * (100 if type(val) == float else 1):.0f}{('%' if type(val) == float else '')}" for key, val in self.info.items()) if '@' not in [v for k, v in self.info.items()] else 'haha'
        arh = (f"{self.name} ,-> {stats}")
        
            
           
        info_bubble_item = ImageBro(
            image_path=text_box_img,
            pos=position,
            scale=2,
            text=arh,
            font_path=r'assets\font\slkscr.ttf',  # or any other font path
            font_size=font_size*1.05,  # dynamic size ~29 at 720p
            text_color='white',
            fku=True,
            scale_val=(150, 200),
            hover_move=0
            
            
        )
        info_bubble_item.drawing_info(screen, pygame.mouse.get_pos())

    # def draw(self, pos):
    #     self.decor = pygame.draw.rect(screen, black, self.decor_rect)
    #     screen.blit(self.image, pos)
        
        
    
# Update log for items

# Nerf:
# Crimson Crystal: 10% spell dmg, 5% mana reduce, 5% cd reduce -> 10% spell dmg, 3% mana reduce, 3% cd reduce
# Red Crystal: 20% mana reduce, 5% cd reduce, 3% spell dmg -> 15% mana reduce, 3% cd reduce, 2% spell dmg
# Ruby: 20% cd reduce, 5% mana reduce, 3% spell dmg -> 15% cd reduce, 3% mana reduce, 2% spell dmg


items = [
    Item("War Helmet", r"assets\item icons\in use\Icons_40.png", ["str", "str flat", "hp regen"], [0.05, 1, 0.04]),  
    Item("Emblem Necklace", r"assets\item icons\in use\Icons_26.png", ["int", "mana flat", "mana regen"], [0.08, 8, 0.04]), 
    Item("Old Axe", r"assets\item icons\in use\Icons_09.png", ["atk", "hp flat", "agi flat"], [0.1, 5, 2]),
    Item("Spirit Feather", r"assets\item icons\in use\Icons_11.png", ["move speed", "attack speed", "agi flat"], [0.1, 150, 3]), 
    Item("Vitality Booster", r"assets\item icons\new items\2 Icons with back\Icons_23.png", ["hp", "hp flat"], [0.1, 5]), 
    Item("Mysterious Mushroom", r"assets\item icons\in use\Icons_08.png", ["hp regen", "mana regen"], [-0.3, 0.3]), 
    Item("Elixir", r"assets\item icons\in use\Icons_30.png", ["hp regen", "mana regen", "move speed"], [0.06, 0.06, 0.06]),
    Item("Flower Locket", r"assets\item icons\in use\Icons_13.png", ["hp regen", "mana regen", "move speed", "attack speed", "int flat"], [0.02, 0.02, 0.02, 100, 4]),
    Item("Energy Booster", r"assets\item icons\new items\2 Icons with back\Icons_12.png", ["str flat", "int flat", "agi flat"], [4, 4, 3]),
    Item("Undead Marrow", r"assets\item icons\new items\2 Icons with back\Icons_40.png", ["lifesteal"], [0.15]),

    Item("Crimson Crystal", r"assets\item icons\new items\2 Icons with back\Icons_24.png", ['spell dmg', 'mana reduce', 'cd reduce'], [0.1, 0.03, 0.03]),
    Item("Red Crystal", r"assets\item icons\new items\2 Icons with back\Icons_06.png", ['mana reduce', 'cd reduce', 'spell dmg'], [0.15, 0.03, 0.02]),
    Item("Ruby", r"assets\item icons\new items\2 Icons with back\Icons_07.png", ['cd reduce', 'mana reduce', 'spell dmg'], [0.15, 0.03, 0.02]),
    Item("Tough Stone", r"assets\item icons\in use\Icons_14.png", ['dmg reduce', 'hp flat', "move speed"], [0.15, 5, -0.1]),
    Item("Cheese", r"assets\item icons\2 Icons with back\Icons_12.png", ['sp increase'], [0.25])
     
]

# doc
'''
War Helmet: 10% str, 1 str flat, 0.02 hp regen
Emblem Necklace: 12% int, 8 mana flat, 0.04 mana regen
Old Axe: 7% atk, 3 hp flat
Spirit Feather: 5% move speed, 150 attack speed, 3 agi flat
Vitality Booster: 15% hp, 10 hp flat
Mysterious Mushroom: -35% hp regen, 35% mana regen
Elixir: 8% hp regen, 8% mana regen, 4% move speed
Flower Locket: 12% hp regen, 12% mana regen
Energy Booster: 3 str flat, 3 int flat, 3 agi flat
'''

HERO_INFO = {
    "Fire Wizard": "Strength: 40, Intelligence: 40, Agility: 27, HP: 200, Mana: 200, Damage: 5.4, Attack Speed: -200, , Trait: 5% spell dmg",
    "Wanderer Magician": "Strength: 40, Intelligence: 36, Agility: 32, HP: 200, Mana: 180, Damage: 3.2, Attack Speed: -500, , Trait: 20%->30% mana, regen",
    "Fire Knight": "Strength: 44, Intelligence: 40, Agility: 65, HP: 220, Mana: 200, Damage: 6.5, Attack Speed: -700, , Trait: 20% hp regen",
    "Wind Hashashin": "Strength: 38, Intelligence: 40, Agility: 13, HP: 190, Mana: 200, Damage: 2.6, Attack Speed: 0, , Trait: 15% mana, reduce",
    "Water Princess": "Strength: 40, Intelligence: 48, Agility: 20, HP: 200, Mana: 240, Damage: 2.0*(1.5/5), Attack Speed: -3200, , Trait: 15%->20% mana, cost/delay"
}


class PlayerSelector:
    def __init__(self, image, rect, class_item, size=(75,75), decorxsize=85, decorysize=85, offsetdecor=(42, 42)):
        self.image = image
        self.rect = rect
        self.class_item = class_item

        # self.real_class_item = self.class_item

        # Check if the image is a file path or a pygame.Surface
        if isinstance(image, str):  # If it's a file path, load the image
            self.profile = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
            self.ingame_profile = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (25,25))
        else:  # If it's already a pygame.Surface, use it directly
            self.profile = pygame.transform.scale(image, size)
            self.ingame_profile = pygame.transform.scale(image, (25,25))
        self.profile_rect = self.profile.get_rect(center = self.rect)

        self.decor_rect = pygame.Rect(self.profile_rect.centerx - offsetdecor[0], self.profile_rect.centery - offsetdecor[1], decorxsize, decorysize)
        
        self.hovered = False
        self.selected = False
        

        self.back = ImageButton(
            image_path=text_box_img,
            pos=(self.profile_rect.centerx, self.profile_rect.top - 25),
            scale=0.5,
            text='Deselect',
            font_path=r'assets\font\slkscr.ttf',  # or any other font path
            font_size=font_size * 0.6,  # dynamic size ~29 at 720p
            text_color='white',
            text_anti_alias=global_vars.TEXT_ANTI_ALIASING
        )


        # bro said does not work
        # self.dd = self.class_item(1)
              #^^^^^^^^^^^^^^^^^^^^^^^
        #TypeError: 'Item' object is not callable
        # self.info = {'bro': 69}
        # self.dd = self.class_item(1)
        # self.name = self.dd.name


    def draw(self):
        if self.selected:
            self.decor = pygame.draw.rect(screen, gold, self.decor_rect)

        elif self.hovered:
            self.decor = pygame.draw.rect(screen, white, self.decor_rect)
        
        else:
            self.decor = pygame.draw.rect(screen, black, self.decor_rect)

        screen.blit(self.profile, self.profile_rect)

    def draw_icon(self, size:tuple=(0,0), item_pos:tuple=(0,0), hero_icon=True):
        if hero_icon:
            border_size = 85
            offset_decor = 42
            profile_rect = self.profile.get_rect(center = size) #use the prof rect as pos (hero icons)
        else:
            border_size = 30
            offset_decor = 15
            profile_rect = self.ingame_profile.get_rect(center = item_pos) #use provided pos for item icons
        decor_rect = pygame.Rect(profile_rect.centerx - offset_decor, profile_rect.centery - offset_decor, border_size, border_size)
        pygame.draw.rect(screen, black, decor_rect)
        if hero_icon:
            screen.blit(self.profile, profile_rect)
        else:
            screen.blit(self.ingame_profile, profile_rect)
        # print(item_pos)

    def is_selected(self):
        return self.selected
    
    def associate_value(self):
        return self.class_item
    
    def the_info(self, position):
         # Display hero info if hovered
        if self.hovered and isinstance(self.class_item, type) and issubclass(self.class_item, Player):
            hero_name = self.class_item.__name__.replace("_", " ")
            if hero_name in HERO_INFO:
                # Separate the hero's name and stats
                hero_name_text = hero_name
                hero_stats_text = HERO_INFO[hero_name]
                
                # Display the name and stats in separate lines
                info_bubble = ImageBro(
                    image_path=text_box_img,
                    pos=position,
                    scale=2,
                    text=f"{hero_name_text}, {hero_stats_text}",
                    font_path=r'assets\font\slkscr.ttf',
                    font_size=font_size * 1.05,
                    text_color='white',
                    fku=True,
                    scale_val=(150, 230),
                    hover_move=0
                )
                info_bubble.drawing_info(screen, pygame.mouse.get_pos())

    def update(self, mouse_pos, mouse_press, other_selectors, max_selected=MAX_ITEM):
        self.draw()

        selected_count = sum(1 for selector in other_selectors if selector.selected)
        if not self.selected:
            if self.decor_rect.collidepoint(mouse_pos) and selected_count < max_selected:
                self.hovered = True
                if mouse_press[0]:
                    self.selected = True
                    self.hovered = False
            else:
                self.hovered = False
        else:
            self.back.draw(screen, mouse_pos)
            if mouse_press[0] and self.back.is_clicked(mouse_pos):  # Check if "Deselect" button is clicked
                self.selected = False
        

       


class ImageBro:
    def __init__(self, image_path, pos, scale, text, font_path, font_size, text_color, move_y=0, hover_move=2, fku=False, scale_val=(0, 0)):
        # Load and scale the image
        self.hover_pos = pos
        self.hover_move = hover_move
        self.fku = fku
        self.scale_val = scale_val
        if self.fku:
            self.original_image = pygame.transform.scale(
        pygame.image.load(image_path).convert_alpha(), (self.scale_val[0], self.scale_val[1]))
        else:
            self.original_image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.rect = self.image.get_rect(center=pos)
        # Text
        self.text = text
        self.font = pygame.font.Font(font_path, int(font_size*7.142857142857143)) # Font size = 100
        self.text_color = text_color
    
        self.hovered = False
        self.text_lines = self.text.split(',')
        self.text_lines.insert(1, '')


    def drawing_info(self, screen, mouse_pos):
        # Draw the image and text
        screen.blit(self.image, (self.hover_pos[0] * 0.63 - (self.hover_pos[0] * 0.05), self.hover_pos[1] - (self.hover_pos[1] * 0.29)))

        for i, line in enumerate(self.text_lines):
            self.text_surf = pygame.transform.rotozoom(self.font.render(line, global_vars.TEXT_ANTI_ALIASING, self.text_color), 0, 0.2)
            screen.blit(self.text_surf, (self.hover_pos[0] * 0.63 - (self.hover_pos[0] * 0.04), self.hover_pos[1] + i * 30))


font_size = int(height * 0.02) # = 100
scale = 0.8
center_pos = (width / 2, height / 2)


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

fight = ImageButton(
    image_path=text_box_img,
    pos=(width/2, height*0.9),
    scale=0.8,
    text='FIGHT!',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

done = ImageButton(
    image_path=text_box_img,
    pos=(width/2, height*0.9),
    scale=0.8,
    text='select',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0):
    title = pygame.transform.rotozoom(font.render(f'{text}', global_vars.TEXT_ANTI_ALIASING, color), angle, scale)
    title_rect = title.get_rect(center = (width / 2, y_offset))
    screen.blit(title, title_rect)

# print('opening player selection')
# print(global_vars.SMOOTH_BG)

# from global_vars import quick_run_hero1, quick_run_hero2
def player_selection():
    global map_selected
    # print('player selection opened')
    # print(global_vars.SMOOTH_BG)
    global PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, hero1, hero2, hero1_group, hero2_group, bot, bot_group
    global p1_select, p2_select, p1_items, p2_items
    # global_vars.SMOOTH_BG = not global_vars.SMOOTH_BG
    background = pygame.transform.scale(
        pygame.image.load(r'assets\backgrounds\12.png').convert(), (width, height))

    font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
    default_size = ((width * DEFAULT_HEIGHT) / (height * DEFAULT_WIDTH))

    #upper position PlayerSelector(wind_hashashin_icon, (75, height - 75 * 3), Wind_Hashashin)
    p1_select = [
        PlayerSelector(fire_wizard_icon, (75, height - 75), Fire_Wizard),
        PlayerSelector(wanderer_magician_icon, (75 * 3, height - 75), Wanderer_Magician),
        PlayerSelector(fire_knight_icon, (75 * 5, height - 75), Fire_Knight),
        PlayerSelector(wind_hashashin_icon, (width - (75 * 5), height - 75), Wind_Hashashin),
        PlayerSelector(water_princess_icon, (width - (75 * 3), height - 75), Water_Princess),
        PlayerSelector(forest_ranger_icon, (width - (75), height - 75), Forest_Ranger)
    ]

    p2_select = [
        PlayerSelector(fire_wizard_icon, (width - 75, height - 75), Fire_Wizard),
        PlayerSelector(wanderer_magician_icon, (width - (75 * 3), height - 75), Wanderer_Magician),
        PlayerSelector(fire_knight_icon, (width - (75 * 5), height - 75), Fire_Knight),
        PlayerSelector(wind_hashashin_icon, (75 * 5, height - 75), Wind_Hashashin),
        PlayerSelector(water_princess_icon, (75 * 3, height - 75), Water_Princess),
        PlayerSelector(forest_ranger_icon, (75, height - 75), Forest_Ranger)
    ]
    
    # Item selection
    p1_items = [
        PlayerSelector(items[0].image, (75, height - 400), items[0], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[1].image, (75 * 2, height - 400), items[1], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[2].image, (75 * 3, height - 400), items[2], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[3].image, (75 * 4, height - 400), items[3], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[4].image, (75 * 5, height - 400), items[4], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[13].image, (75 * 6, height - 400), items[13], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[14].image, (75 * 7, height - 400), items[14], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        
        PlayerSelector(items[5].image, (75, height - 300), items[5], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[6].image, (75 * 2, height - 300), items[6], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[7].image, (75 * 3, height - 300), items[7], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[8].image, (75 * 4, height - 300), items[8], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[9].image, (75 * 5, height - 300), items[9], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[10].image, (75 * 6, height - 300), items[10], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[11].image, (75 * 7, height - 300), items[11], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[12].image, (75 * 8, height - 300), items[12], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),

    ]

    p2_items = [
        PlayerSelector(items[0].image, (width - 75, height - 400), items[0], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[1].image, (width - (75 * 2), height - 400), items[1], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[2].image, (width - (75 * 3), height - 400), items[2], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[3].image, (width - (75 * 4), height - 400), items[3], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[4].image, (width - (75 * 5), height - 400), items[4], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[13].image, (width - (75 * 6), height - 400), items[13], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[14].image, (width - (75 * 7), height - 400), items[14], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),

        PlayerSelector(items[5].image, (width - 75, height - 300), items[5], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[6].image, (width - (75 * 2), height - 300), items[6], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[7].image, (width - (75 * 3), height - 300), items[7], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[8].image, (width - (75 * 4), height - 300), items[8], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[9].image, (width - (75 * 5), height - 300), items[9], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[10].image, (width - (75 * 6), height - 300), items[10], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[11].image, (width - (75 * 7), height - 300), items[11], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
        PlayerSelector(items[12].image, (width - (75 * 8), height - 300), items[12], size=(50, 50), decorxsize=60, decorysize=60, offsetdecor=(30, 30)),
    ]
        
    map_select = [
        PlayerSelector(waterfall_icon, (75*2, height - (75*5)), Animate_BG.waterfall_bg, size=(200, 125), decorxsize=220, decorysize=145, offsetdecor=(110, 72)),
        PlayerSelector(lava_icon, (width/2 - (55 * 3), height - (75*5)), Animate_BG.lava_bg, size=(200, 125), decorxsize=220, decorysize=145, offsetdecor=(110, 72)),
        PlayerSelector(dark_forest_icon, (width/2 + (55 * 3), height - (75*5)), Animate_BG.dark_forest_bg, size=(200, 125), decorxsize=220, decorysize=145, offsetdecor=(110, 72)),
        PlayerSelector(trees_icon, (width - (75 * 2), height - (75*5)), Animate_BG.trees_bg, size=(200, 125), decorxsize=220, decorysize=145, offsetdecor=(110, 72))
    ]
    
    player_1_choose = True
    player_2_choose = False
    map_choose = False

    map_selected = Animate_BG.dark_forest_bg # Default

    go = False

    immediate_run = IMMEDIATE_RUN # for dev option only
    

    while True:
        if immediate_run: # DEV OPTION ONLY
            PLAYER_1_SELECTED_HERO = Wanderer_Magician
            PLAYER_2_SELECTED_HERO = Wind_Hashashin
            bot = create_bot(Wanderer_Magician) if global_vars.SINGLE_MODE_ACTIVE else None
            player_1_choose = False
            map_choose = True
            go = True
        


        # print('running')
        # print(global_vars.MAIN_VOLUME)
        # return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        screen.fill((0, 0, 0))
        
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

        # screen.blit(background, (0, 0))
        Animate_BG.waterfall_night_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
        create_title('Hero Selection', font, default_size, height * 0.1) if not map_choose else None
        menu_button.draw(screen, mouse_pos)
        

        if player_1_choose:                      
            create_title('PLAYER 1 CHOOSE HERO', font, default_size - 0.55, height * 0.19)
            # fire_wizard_select.update(mouse_pos, mouse_press)
            # wanderer_magician_select.update(mouse_pos, mouse_press)

            for selector in p1_select:
                selector.update(mouse_pos, mouse_press, p1_select, max_selected=1)
                


            for selector in p1_select:
                if selector.hovered:
                    selector.the_info((width + (width * 0.322), height - 525))
                if selector.is_selected():
                    PLAYER_1_SELECTED_HERO = selector.associate_value()

                    # Draw item selection
                    for item in p1_items:
                        item.update(mouse_pos, mouse_press, p1_items, max_selected=MAX_ITEM)
                    for item in p1_items:
                        item.draw()
                        
                    for item in p1_items:
                        if item.hovered:
                            item.class_item.update((width + (width * 0.322), height - 500))

                    # print(selector.associate_value())
                    go = True
                    break  # Only one can be selected
                else:
                    go = False
                    

            if go:
                done.draw(screen, mouse_pos)
                if pygame.mouse.get_pressed()[0] and done.is_clicked(mouse_pos) or keys[pygame.K_SPACE]:
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    pygame.time.delay(500)

                    player_1_choose = False
                    player_2_choose = True
                    go = False


        if player_2_choose:
            create_title('PLAYER 2 CHOOSE HERO', font, default_size - 0.55, height * 0.19)
            for selector in p2_select:
                selector.update(mouse_pos, mouse_press, p2_select, max_selected=1)

            for selector in p2_select:
                if selector.hovered:
                    selector.the_info((-(width * 0.0001), height - 525))
                if selector.is_selected():
                    PLAYER_2_SELECTED_HERO = selector.associate_value()

                    # Draw item selection
                    for item in p2_items:
                        item.update(mouse_pos, mouse_press, p2_items, max_selected=MAX_ITEM)
                    for item in p2_items:
                        item.draw()

                    for item in p2_items:
                        if item.hovered:
                            item.class_item.update((-(width * 0.0001), height - 500))
  
                    # print(PLAYER_2_SELECTED_HERO)
                    go = True
                    break
                else:
                    go = False
                    
                    

            if go:
                done.draw(screen, mouse_pos)
                if pygame.mouse.get_pressed()[0] and done.is_clicked(mouse_pos) or keys[pygame.K_SPACE]:
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    pygame.time.delay(500)

                    player_2_choose = False
                    map_choose = True
                    go = False


        if map_choose:
            create_title('MAP SELECT', font, default_size, height * 0.1)
            for selector in map_select:
                selector.update(mouse_pos, mouse_press, map_select, max_selected=1)

            for selector in map_select:
                # if selector.hovered:
                #     selector.the_info((-(width * 0.0001), height - 500))
                if selector.is_selected():
                    map_selected = selector.associate_value()

                    # # Draw item selection
                    # for item in p2_items:
                    #     item.update(mouse_pos, mouse_press, p2_items, max_selected=MAX_ITEM)
                    # for item in p2_items:
                    #     item.draw()

                    # for item in p2_items:
                    #     if item.hovered:
                    #         item.class_item.update((-(width * 0.0001), height - 500))
  
                    # print(PLAYER_2_SELECTED_HERO)
                    go = True
                    break
                elif not immediate_run:
                    go = False
                
            if go:
                fight.draw(screen, mouse_pos)
                if pygame.mouse.get_pressed()[0] and fight.is_clicked(mouse_pos) or keys[pygame.K_SPACE] or immediate_run:
                    # print(PLAYER_1_SELECTED_HERO)
                    # print(PLAYER_2_SELECTED_HERO)
                    screen.blit(background, (0, 0))
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    # pygame.time.delay(500)  # Wait for 2 seconds before showing the player selection screen
                    
                    hero1 = PLAYER_1_SELECTED_HERO(PLAYER_1)
                    hero2 = PLAYER_2_SELECTED_HERO(PLAYER_2)

                    if global_vars.SINGLE_MODE_ACTIVE:
                        # bot1_class = create_bot(PLAYER_1_SELECTED_HERO, PLAYER_1)
                        # hero1 = bot1_class(hero2)  # pass live hero2 reference

                        bot2_class = create_bot(PLAYER_2_SELECTED_HERO, PLAYER_2)
                        hero2 = bot2_class(hero1)  # pass live hero1 reference


                    for item in p1_items:
                        if item.is_selected():
                            hero1.items.append(item.associate_value())

                    for item in p2_items:
                        if item.is_selected():
                            hero2.items.append(item.associate_value())

                    hero1.apply_item_bonuses()
                    hero2.apply_item_bonuses()

                    hero1_group = pygame.sprite.Group()
                    hero1_group.add(hero1)

                    hero2_group = pygame.sprite.Group()
                    hero2_group.add(hero2)

                    pygame.mixer.music.fadeout(1000)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

                    

                    reset_all()
                    fade(background, game) #lez go it worked
                    # pygame.mixer.fadeout(1500)
                    
                    
                    return

        pygame.display.update()
        clock.tick(FPS)


bot = object




# ONLY PLACE HOLDER VALUE, CHANGES LATER
# fire_wizard = Fire_Wizard(PLAYER_1)
# wanderer_magician = Wanderer_Magician(PLAYER_2)

# fire_wizard_select = PlayerSelector(fire_wizard_icon, (75, height -75), Fire_Wizard)
# wanderer_magician_select = PlayerSelector(wanderer_magician_icon, (75*3, height -75), Wanderer_Magician)

# p1_select_icon = [
#         PlayerSelector(fire_wizard_icon, (75, height - 75), Fire_Wizard),
#         PlayerSelector(wanderer_magician_icon, (75 * 3, height - 75), Wanderer_Magician),
#         PlayerSelector(fire_knight_icon, (75 * 5, height - 75), Fire_Knight),
#         PlayerSelector(wind_hashashin_icon, (75, height - 75 * 3), Wind_Hashashin)
#     ]




        # self.player_death = self.load_attack_class(
        #     filepath=r"PYTHON WITH KIM  NEW!\characters\skeleton\craftpix-net-957123-free-skeleton-pixel-art-sprite-sheets\Skeleton_Warrior\Dead.png",
        #     frame_width=192, 
        #     frame_height=192, 
        #     rows=1, 
        #     columns=4, 
        #     scale=1, 
        #     rotation=0,
        #     frame_duration=100
        # )
    

# NEXT TO DO IS TO CONTINUE WORKING ON THE SKILLS
from gameloop import main_menu
if __name__ == '__main__':
    main_menu()
