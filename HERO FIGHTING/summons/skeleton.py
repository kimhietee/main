"""
Skeleton Summon - Follows Fire_Wizard (hero) structure for easy reading.
Same pattern: constants, animation counts, load frames, input, update, animations.
"""

import pygame
from summon import Summon, create_summon_bot
from global_vars import (
    DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, RUNNING_ANIMATION_SPEED,
    DEFAULT_GRAVITY, DEFAULT_Y_POS, BASIC_FRAME_DURATION,
    SHOW_HITBOX, screen
)
from heroes import Attack_Display, attack_display

# ============================================================================
# SKELETON CONSTANTS (Like FIRE_WIZARD_ATK1_COOLDOWN, etc.)
# ============================================================================

SKELETON_IDLE_COUNT = 8
SKELETON_RUN_COUNT = 8
SKELETON_ATTACK_COUNT = 7
SKELETON_DEATH_COUNT = 6

SKELETON_ATTACK_COOLDOWN = 1000  # ms between attacks
SKELETON_ATTACK_DAMAGE = 3.0
SKELETON_HEALTH = 60
SKELETON_AGILITY = 15

# Paths to animation folders
SKELETON_IDLE_PATH = r'assets\characters\others\crystal\Elementals_Crystal_Mauler_Free_v1.0\animations\PNG\idle\idle_'
SKELETON_RUN_PATH = r'assets\characters\others\crystal\Elementals_Crystal_Mauler_Free_v1.0\animations\PNG\run\run_'
SKELETON_ATTACK_PATH = r'assets\characters\others\crystal\Elementals_Crystal_Mauler_Free_v1.0\animations\PNG\1_atk\1_atk_'

# ============================================================================
# SKELETON CLASS
# ============================================================================

class Skeleton(Summon):
    """Skeleton summon—uses same hero-style code as Fire_Wizard for readability."""

    def __init__(self, player_type, enemy, **kwargs):
        super().__init__(player_type, enemy, 'skeleton')
        
        # ---- STATS ----
        self.name = "Skeleton"
        self.strength = 20
        self.agility = SKELETON_AGILITY
        self.max_health = SKELETON_HEALTH
        self.health = self.max_health
        self.basic_attack_damage = SKELETON_ATTACK_DAMAGE
        
        # ---- COOLDOWNS & DAMAGE ----
        self.attack_cooldown = SKELETON_ATTACK_COOLDOWN
        
        # ---- ANIMATION FRAMES (hero-style: right + flipped) ----
        self.idle_frames = self.load_img_frames(
            SKELETON_IDLE_PATH, SKELETON_IDLE_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        self.idle_frames_flipped = self.load_img_frames_flipped(
            SKELETON_IDLE_PATH, SKELETON_IDLE_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        
        self.run_frames = self.load_img_frames(
            SKELETON_RUN_PATH, SKELETON_RUN_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        self.run_frames_flipped = self.load_img_frames_flipped(
            SKELETON_RUN_PATH, SKELETON_RUN_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        
        self.attack_frames = self.load_img_frames(
            SKELETON_ATTACK_PATH, SKELETON_ATTACK_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        self.attack_frames_flipped = self.load_img_frames_flipped(
            SKELETON_ATTACK_PATH, SKELETON_ATTACK_COUNT, size=DEFAULT_CHAR_SIZE_2
        )
        
        # ---- ANIMATION INDICES (hero-style) ----
        self.idle_index = 0
        self.idle_index_flipped = 0
        self.run_index = 0
        self.run_index_flipped = 0
        self.attack_index = 0
        self.attack_index_flipped = 0
        
        # ---- SET INITIAL IMAGE ----
        if self.facing_right:
            self.image = self.idle_frames[0] if self.idle_frames else pygame.Surface((40, 80))
        else:
            self.image = self.idle_frames_flipped[0] if self.idle_frames_flipped else pygame.Surface((40, 80))
    
    # ========================================================================
    # ANIMATION METHODS (Exact copy of hero pattern)
    # ========================================================================
    
    def idle_animation(self):
        """Idle animation—uses hero pattern."""
        if self.facing_right:
            self.idle_index, _ = self.animate(self.idle_frames, self.idle_index, loop=True)
        else:
            self.idle_index_flipped, _ = self.animate(self.idle_frames_flipped, self.idle_index_flipped, loop=True)
    
    def run_animation(self, animation_speed=0):
        """Run animation—uses hero pattern."""
        if self.facing_right:
            self.run_index, _ = self.animate(self.run_frames, self.run_index, loop=True)
        else:
            self.run_index_flipped, _ = self.animate(self.run_frames_flipped, self.run_index_flipped, loop=True)
        # Optional: adjust animation speed (like heroes)
        self.last_atk_time -= animation_speed
    
    def attack_animation(self, animation_speed=0):
        """Attack animation—loops=False, stops when done."""
        if self.facing_right:
            self.attack_index, self.attacking = self.animate(self.attack_frames, self.attack_index, loop=False)
        else:
            self.attack_index_flipped, self.attacking = self.animate(self.attack_frames_flipped, self.attack_index_flipped, loop=False)
        # Optional: adjust speed
        self.last_atk_time -= animation_speed
    
    # ========================================================================
    # INPUT (overridable if needed)
    # ========================================================================
    
    def input(self):
        """Skeleton doesn't use keyboard input (it's a summon/NPC)."""
        pass
    
    # ========================================================================
    # UPDATE (hero-style main loop)
    # ========================================================================
    
    def update(self):
        """Main update loop—exactly like Fire_Wizard.update()."""
        
        # Dead check
        if self.is_dead():
            return
        
        # Draw hitbox (debug)
        if SHOW_HITBOX:
            self.draw_hitbox(screen)
        
        # Update hitbox
        self.update_hitbox()
        
        # Summon AI: move towards enemy or attack
        self.move_towards_enemy()
        if not self.running:
            self.attack_if_ready()
        
        # ---- PHYSICS (gravity) ----
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity
        
        # Stop at ground
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False
        
        # Update rect position
        self.rect.midbottom = (self.x_pos, self.y_pos)
        
        # ---- ANIMATION PRIORITY (like heroes) ----
        if self.attacking:
            self.attack_animation()
        elif self.running:
            self.run_animation()
        else:
            self.idle_animation()
        
        # Keep summon in bounds
        self.move_to_screen()
