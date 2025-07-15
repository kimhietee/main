import pygame
from global_vars import (
    screen, width, height, attack_display, DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE
)

class Attacks:
    '''
    This class represents the attack and its properties.
    It contains the attack's damage, animation frames, and other attributes.
    It also handles the attack's cooldown and mana cost.
    The class is designed to be used with Pygame and integrates with the Pygame sprite system.
    '''
    

    def __init__(self, mana_cost, skill_rect, skill_img, cooldown, mana):
        self.mana_cost = mana_cost
        self.skill_rect = skill_rect
        self.skill_img = skill_img
        self.cooldown = cooldown
        self.mana = mana  # Not used
        self.last_used_time = -cooldown # Starts the cooldown at 0
        self.atk_mana_cost = 0

        # Dynamically scaled font sizes
        self.cooldown_font_size = int(height * 0.0416 *1.3)  # ~30 at 720p
        self.mana_font_size = int(height * 0.0208 *1.3)      # ~15 at 720p

        # Offset for positioning mana text (scaled vertically)
        self.mana_y_offset = int(self.skill_rect.height * 0.35)      # ~50 at 720p

    def reduce_cd(self, val=False):
        if val:
            self.last_used_time = -self.cooldown  # Reset cooldown
        return val
         

    def is_ready(self):
        # print(self.reduce_cd())
        current_time = pygame.time.get_ticks()
        # print(f'{current_time} - {self.last_used_time}:[{current_time-self.last_used_time}] >= {self.cooldown}')
        return current_time - self.last_used_time >= self.cooldown

    def draw_skill_icon(self, screen, mana):
        if not self.is_ready():
            dark_overlay = pygame.Surface(self.skill_rect.size)
            dark_overlay.fill((0, 0, 0))
            dark_overlay.set_alpha(128)
            screen.blit(self.skill_img, self.skill_rect)
            screen.blit(dark_overlay, self.skill_rect)

            # Draw scaled cooldown text
            font = pygame.font.Font(fr'HERO FIGHTING\assets\font\slkscr.ttf', self.cooldown_font_size)
            cooldown_time = max(0, (self.cooldown - (pygame.time.get_ticks() - self.last_used_time)) // 1000)
            cooldown_text = font.render(str(cooldown_time), True, 'Red')
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
            mana_font = pygame.font.Font(fr'HERO FIGHTING\assets\font\slkscr.ttf', self.mana_font_size)
            self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', False, 'Red')
            screen.blit(self.atk_mana_cost, (
                self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
                self.skill_rect.top - self.mana_y_offset
            ))
        else:
            screen.blit(self.skill_img, self.skill_rect)

    def draw_mana_cost(self, screen, mana):
        mana_font = pygame.font.Font(fr'HERO FIGHTING\assets\font\slkscr.ttf', self.mana_font_size)
        color = 'Cyan2' if mana >= self.mana_cost else 'Red'
        self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', False, color)

        screen.blit(self.atk_mana_cost, (
            self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
            self.skill_rect.top - self.mana_y_offset
        ))



class Attack_Display(pygame.sprite.Sprite): #The Attack_Display class should handle the visual representation and animation of an attack. Here's the corrected version:
    '''
    This class represents the attack display and its properties.
    It contains the attack's animation frames, duration, and other attributes.
    It also handles the attack's position and movement.
    The class is designed to be used with Pygame and integrates with the Pygame sprite system.
    '''

    def __init__(self, x, y, frames, frame_duration, repeat_animation, speed, 
                dmg, who_attacks, who_attacked, moving, heal=False,
                continuous_dmg=False, per_end_dmg=(False, False),
                disable_collide=False, stun=(False, 0),
                sound=(False, None, None, None)
                ):
        super().__init__()
        self.frames = frames
        self.frame_duration = frame_duration
        self.repeat_animation = repeat_animation
        self.speed = speed
        self.dmg = dmg
        self.who_attacks = who_attacks
        self.who_attacked = who_attacked
        self.moving = moving
        self.heal = heal
        self.continuous_dmg = continuous_dmg
        self.per_end_dmg = per_end_dmg
        self.disable_collide = disable_collide
        self.stun = stun
        self.sound = sound

        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_done = False

        self.current_repeat = 0

        self.damaged = False
        self.damaged_detect = self.damaged
        

    # def detect_collision(self):
    #     if pygame.sprite.spritecollide(self.sprite,fire_wizard_group,False):
    #         return True
    #     else:
    #         return False

    def update(self):
        print(f'who attacks:{self.who_attacks}')
        print(f'who attacked:{self.who_attacked}')
        if self.who_attacked is None:
            print("Error: `who_attacked` is None!")
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
        # print(self.detect_collision())
        """Update the attack animation and position."""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update_time > self.frame_duration:
            self.last_update_time = current_time
            self.frame_index += 1
            # print('reducing dmg')

            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]

            elif self.frame_index >= len(self.frames): # kind of 'else' in my s.py
                self.frame_index = 0
                self.current_repeat += 1
                if self.per_end_dmg[0]:
                    self.damaged_detect = False 
                    self.damaged = False
                    
                # normal logic, damages enemy anywhere
                if not self.damaged and self.per_end_dmg[1]:
                    if not self.continuous_dmg:
                        self.who_attacked.take_damage(self.dmg)

                if self.current_repeat >= self.repeat_animation:
                    #dmg animation
                    self.animation_done = True
                    self.kill() # Remove the sprite from the group  
                    
                if self.sound[0] == True:
                    if self.sound[1] != None:
                        self.sound[1].play()
                    if self.sound[2] != None:
                        self.sound[2].play()
                    if self.sound[3] != None:
                        self.sound[3].play()
                        
                    
                    
        
                    
        #dmg per every frame (too fast)   
        if self.who_attacked is None or not hasattr(self.who_attacked, 'rect'):
            print("Warning: `who_attacked` is None or invalid.")
            self.kill()  # Remove the attack if it has no valid target
            return
        # stun logic
        if not self.heal:
            if pygame.sprite.collide_rect(self, self.who_attacked):
                if not self.continuous_dmg and not self.disable_collide: # end animation will do the damaging
                    if self.stun[0]:
                        self.who_attacked.stunned(self.stun, self.rect.centerx, self.rect.centery, self.stun[1])
                           
            #dmg per frame

            if self.moving: # moving logic
                # Move the attack
                self.rect.x += self.speed
                if self.rect.x > width + 500 or self.rect.x < -500:
                    self.kill()  # Remove the sprite if it goes off-screen

            # main atk logic
            if not self.heal:
                if not self.damaged and pygame.sprite.collide_rect(self, self.who_attacked):
                    if not self.continuous_dmg and not self.disable_collide: # end animation will do the damaging
                        self.who_attacked.take_damage(self.dmg)
                    if self.moving:
                        self.damaged = True
            # heal logic
            else:
                if pygame.sprite.collide_rect(self, self.who_attacks):
                    self.who_attacks.take_heal(self.dmg)
                
            # continuous dmg logic
            if self.continuous_dmg and pygame.sprite.collide_rect(self, self.who_attacked):
                    self.who_attacked.take_damage(self.dmg)

            #for per_end_dmg logic
            # NOW WHY TF DOES THIS WORK SUDDENLY? this is .... good?
            if not self.heal:
                if not self.damaged and pygame.sprite.collide_rect(self, self.who_attacked) and self.per_end_dmg[0] and self.disable_collide:
                    if not self.continuous_dmg:
                        self.who_attacked.take_damage(self.dmg)
                    if self.damaged_detect:
                        self.damaged = True
        
            print(f"Frames length: {len(self.frames)}")