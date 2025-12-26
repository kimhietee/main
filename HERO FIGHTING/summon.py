# summon.py (REPLACED VERSION - Full Hero-Like Animations)
import pygame
from player import Player
from global_vars import *  # DEFAULT_GRAVITY, etc.
from heroes import Attack_Display, attack_display
from sprite_loader import *  # YOUR LOADER (import it!)

class Summon(Player):
    def __init__(self, player_type, enemy, summon_type='basic'):
        super().__init__(player_type, enemy)
        
        self.name = f"Summoned {summon_type.capitalize()}"
        self.summon_type = summon_type
        
        # Stats (same)
        self.strength = 20
        self.agility = 15
        self.max_health = self.strength * self.str_mult
        self.health = self.max_health
        self.basic_attack_damage = self.agility * self.agi_mult
        self.mana = self.max_mana = 0
        self.special = self.special_active = 0
        
        # Position/physics (same)
        self.x_pos = DEFAULT_X_POS // 2 if player_type == 1 else DEFAULT_X_POS + 100
        self.y_pos = DEFAULT_Y_POS
        self.y_velocity = 0
        self.jumping = self.running = False
        self.facing_right = player_type == 1
        
        # AI/combat (same)
        self.speed = RUNNING_SPEED * 0.8
        self.attack_range = 50
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.attacking = False
        
        # Hitbox/rect (same)
        self.hitbox_rect = pygame.Rect(0, 0, 40, 80)
        self.rect = self.hitbox_rect.copy()
        self.rect.midbottom = (self.x_pos, self.y_pos)
        
        # **ANIMATIONS: Hero-Style (Load in SUBCLASS!)**
        self.idle_frames = []  # Right
        self.idle_frames_flipped = []
        self.run_frames = []
        self.run_frames_flipped = []
        self.attack_frames = []
        self.attack_frames_flipped = []
        self.death_frames = []
        
        # **INDICES: Like heroes**
        self.idle_index = self.idle_index_flipped = 0
        self.run_index = self.run_index_flipped = 0
        self.attack_index = self.attack_index_flipped = 0
        self.death_index = self.death_index_flipped = 0
        
        self.animation_speed = DEFAULT_ANIMATION_SPEED
        
        # States (same)
        self.items = []
        self.stunned = self.frozen = self.rooted = self.slowed = False
    
    # **COPY animate() FROM Player.py (Exact)**
    def animate(self, frames, index, loop=True):
        if len(frames) == 0:
            return index, False
        index += 1
        if index >= len(frames):
            index = 0 if loop else len(frames) - 1
        self.image = pygame.transform.scale(frames[index], (int(self.rect.width * 1.2), int(self.rect.height * 1.2)))
        return index, index >= len(frames) - 1
    
    # **State Anim Methods (Like heroes)**
    def idle_animation(self):
        frames = self.idle_frames if self.facing_right else self.idle_frames_flipped
        index_attr = 'idle_index' if self.facing_right else 'idle_index_flipped'
        index = getattr(self, index_attr)
        setattr(self, index_attr, self.animate(frames, index)[0])
    
    def run_animation(self, anim_speed=RUNNING_ANIMATION_SPEED):
        frames = self.run_frames if self.facing_right else self.run_frames_flipped
        index_attr = 'run_index' if self.facing_right else 'run_index_flipped'
        index = getattr(self, index_attr)
        setattr(self, index_attr, self.animate(frames, index)[0])
    
    def attack_animation(self):
        frames = self.attack_frames if self.facing_right else self.attack_frames_flipped
        index_attr = 'attack_index' if self.facing_right else 'attack_index_flipped'
        index = getattr(self, index_attr)
        new_index, done = self.animate(frames, index)
        setattr(self, index_attr, new_index)
        if done:
            self.attacking = False
    
    # take_damage, die, move_towards_enemy (UNCHANGED - same as before)
    def take_damage(self, dmg):
        dmg -= self.damage_reduce
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.die()
    
    def die(self):
        self.kill()
    
    def move_towards_enemy(self):
        if not self.can_move() or not self.enemy:
            return
        target = min(self.enemy, key=lambda e: abs(self.rect.centerx - e.rect.centerx))
        dx = target.rect.centerx - self.rect.centerx
        if abs(dx) > self.attack_range:
            self.running = True
            move_speed = self.speed * (0.5 if self.slowed else 1)
            self.x_pos += move_speed if dx > 0 else -move_speed
            self.facing_right = dx > 0
        else:
            self.running = False
    
    def attack_if_ready(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown and not self.attacking:
            # Spawn attack (NOW uses correct frames!)
            attack_frames = self.attack_frames if self.facing_right else self.attack_frames_flipped
            attack = Attack_Display(
                x=self.rect.centerx + (40 if self.facing_right else -40),
                y=self.rect.centery,
                frames=attack_frames[:],  # Copy list
                frame_duration=BASIC_FRAME_DURATION,
                repeat_animation=1,
                speed=0,
                dmg=self.basic_attack_damage,
                final_dmg=0,
                who_attacks=self,
                who_attacked=self.enemy,
                moving=False
            )
            attack_display.add(attack)
            self.last_attack_time = current_time
            self.attacking = True
    
    def update(self):
        if self.is_dead():
            return
        if SHOW_HITBOX:
            self.draw_hitbox(screen)
        
        self.move_towards_enemy()
        if not self.running:
            self.attack_if_ready()
        
        # Physics (same)
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False
        
        self.rect.midbottom = (self.x_pos, self.y_pos)
        
        # **ANIMATIONS: Hero-Style Priority (Like update() in fire_wizard.py)**
        if self.attacking:
            self.attack_animation()
        elif self.running:
            self.run_animation()
        else:
            self.idle_animation()
        
        # HP bar (same)
        if SHOW_MINI_HEALTH_BAR:
            self.draw_health_bar(screen)
        
        self.update_hitbox()
        self.move_to_screen()
        # NO super().update() - avoids hero-specific anim conflicts

# create_summon_bot (UNCHANGED)
def create_summon_bot(summon_class, player_type, enemy):
    class SummonBot(summon_class):
        def __init__(self, player_type, enemy):
            super().__init__(player_type, enemy)
            self.state = 'chase'
        
        def update(self):
            super().update()
            # Skill hook (override for advanced AI)
    
    return SummonBot(player_type, enemy)