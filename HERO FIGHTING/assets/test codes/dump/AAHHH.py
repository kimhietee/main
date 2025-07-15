import pygame

pygame.init()
import main as self

class Display_Status:
    def __init__(self, lowest_mana_cost, health, mana, player_type):
        self.lowest_mana_cost = lowest_mana_cost
        self.health = health
        self.mana = mana
        self.player_type = player_type
        
        #PLACEHOLDER VALUES
        self.p1_hp_num = self.health
        self.p1_hp_num2 = self.health
        self.p1_hp_num_end = self.health
        self.p1_hp_num_end2 = self.health

        self.p1_mana_num = self.mana
        self.p1_mana_num2 = self.mana
        self.p1_mana_num_end = self.mana
        self.p1_mana_num_end2 = self.mana

        self.p2_hp_num = (int(width) - 300)
        self.p2_hp_num2 = (int(width) - 300)
        self.p2_hp_num_end = self.health
        self.p2_hp_num_end2 = self.health

        self.p2_mana_num = (int(width) - 300)
        self.p2_mana_num2 = (int(width) - 300)
        self.p2_mana_num_end = self.mana
        self.p2_mana_num_end2 = self.mana#IM SLEEPY, WORK ON THE MAX HEALTH, MAX MANA, THE POSITION OF THE HEALTH AND MANA RECTS, UPDATE THEM IN THE CHARACTER, THATS IT.


        self.p2_hp_posx_left = int(width) - 300 - 5
        self.p2_mana_posx_left = int(width) - 300 - 5
        self.p2_mana_posx_right = self.mana+10
        self.p2_hp_posx_right = self.health+10


        self.p1_hp_posx_right = self.health+10
        self.p1_mana_posx_right = self.mana+10

    def health_status(self, amount, max_health):
        """Increase health by a specified amount, ensuring it does not exceed max_health."""
        self.health = min(self.health + amount, max_health)
        return self.health

    def mana_status(self, amount, max_mana):
        """Increase mana by a specified amount, ensuring it does not exceed max_mana."""
        self.mana = min(self.mana + amount, max_mana)
        return self.mana
#----------------
    def update_status(self, health, mana,):

        self.health = health
        self.mana = mana

        pass

    def player1_status(self, screen, health, mana, max_health, max_mana):
        # print(self.mana)
        self.health = health
        self.mana = mana
        self.max_health = max_health
        self.max_mana = max_mana

        self.p1_hp_num = self.health
        self.p1_hp_num2 = self.health
        self.p1_hp_num_end = self.health
        self.p1_hp_num_end2 = self.health

        self.p1_mana_num = self.mana
        self.p1_mana_num2 = self.mana
        self.p1_mana_num_end = self.mana
        self.p1_mana_num_end2 = self.mana

        

        self.p1_hp_posx_right = self.max_health+10
        self.p1_mana_posx_right = self.max_mana+10

        self.redx_p1 = self.health
        self.whitex_p1 = self.health
        self.redx_p1_end = self.health #not used :)
        self.whitex_p1_end = self.health # not used :)

        self.manax_p1 = self.mana
        self.manawhitex_p1 = self.mana
        self.manax_p1_end = self.mana # not used
        self.manawhitex_p1_end = self.mana #not used


        self.hp_bar_p1_rect = pygame.Rect(101, 150, self.redx_p1, 20)
        self.hp_bar_p1_after_rect = pygame.Rect(101, 150, self.whitex_p1, 20)
        self.mana_bar_p1_rect = pygame.Rect(101, 200, self.manax_p1, 20)
        self.mana_bar_p1_after_rect = pygame.Rect(101, 200, self.manawhitex_p1, 20)

        self.hp_decor_p1 = pygame.Rect(96, 145, self.p1_hp_posx_right, 30)
        self.mana_decor_p1 = pygame.Rect(96, 145+50, self.p1_mana_posx_right, 30)

        if self.redx_p1 < self.whitex_p1:
            self.whitex_p1 -= 0.2
            self.whitex_p1_end += 0.2
        if self.manax_p1 < self.manawhitex_p1:
            self.manawhitex_p1 -= 1
            self.manawhitex_p1_end += 1

        if self.redx_p1 <= 0:
            self.health = 0
            self.winner = 2

        if self.redx_p1 > self.whitex_p1:
            self.whitex_p1 += 0.2
            self.whitex_p1_end -= 0.2

        if self.redx_p1 > self.p1_hp_num: #hp heal limit p1
            self.redx_p1 = self.p1_hp_num
            self.redx_p1_end = self.p1_hp_num_end

        if self.manax_p1 > self.manawhitex_p1:
            self.manawhitex_p1 += 1
            self.manawhitex_p1_end -= 1

        if self.manax_p1 > self.p1_mana_num: #mana heal limit p1 (NEED TO MODIFY BASED ON manawhitex)
            self.manax_p1 = self.p1_mana_num
            self.manax_p1_end = self.p1_mana_num_end

        self.hp1 = int(self.redx_p1)

        if self.hp1 > LOW_HP:
            hp_display_txt1 = FONT.render(f'[{self.hp1}]', False, white)
        else:
            hp_display_txt1 = FONT.render(f'[{self.hp1}]', False, red)
        screen.blit(hp_display_txt1, ((self.hp_decor_p1.centerx - hp_display_txt1.get_width() // 2) + 150, 
                                self.hp_decor_p1.top + (self.hp_decor_p1.height // 2 - hp_display_txt1.get_height() // 2)))

        self.mana1 = int(self.manax_p1) 
        if self.mana1 > self.lowest_mana_cost:
            self.mana_display_txt1 = FONT.render(f'[{self.mana1}]', False, white) 
        else:
            self.mana_display_txt1 = FONT.render(f'[{self.mana1}]', False, red)
        screen.blit(self.mana_display_txt1, ((self.mana_decor_p1.centerx - self.mana_display_txt1.get_width() // 2) + 150, 
                                self.mana_decor_p1.top + (self.mana_decor_p1.height // 2 - self.mana_display_txt1.get_height() // 2)))
        
        pygame.draw.rect(screen, black, self.hp_decor_p1)

        pygame.draw.rect(screen, red, self.hp_bar_p1_after_rect) if self.hp1 > 20 else pygame.draw.rect(screen, white, self.hp_bar_p1_after_rect)

        pygame.draw.rect(screen, 'Green', self.hp_bar_p1_rect) if self.hp1 > 20 else pygame.draw.rect(screen, red, self.hp_bar_p1_rect)
        pygame.draw.rect(screen, black, self.mana_decor_p1)
        pygame.draw.rect(screen, white, self.mana_bar_p1_after_rect)
        pygame.draw.rect(screen, 'Cyan2', self.mana_bar_p1_rect)

        return [self.health, self.mana]
        
        # print('player1 status executed')
    def player2_status(self, screen, health, mana, max_health, max_mana):
        self.health = health
        self.mana = mana
        self.max_health = max_health
        self.max_mana = max_mana

        self.p2_hp_num = (int(width) - 300)
        self.p2_hp_num2 = (int(width) - 300)
        self.p2_hp_num_end = self.health
        self.p2_hp_num_end2 = self.health

        self.p2_mana_num = (int(width) - 300)
        self.p2_mana_num2 = (int(width) - 300)
        self.p2_mana_num_end = self.mana
        self.p2_mana_num_end2 = self.mana

        self.p2_hp_posx_left = int(width) - 300 - 5
        self.p2_mana_posx_left = int(width) - 300 - 5
        
        self.p2_mana_posx_right = self.max_mana+10
        self.p2_hp_posx_right = self.max_health+10

        self.redx_p2 = (int(width) - self.mana) #red
        self.whitex_p2 = (int(width) - self.mana) #green hp
        self.redx_p2_end = self.mana #red
        self.whitex_p2_end = self.mana #green hp

        self.manax_p2 = (int(width) - self.mana)
        self.manawhitex_p2 = (int(width) - self.mana)
        self.manax_p2_end = self.mana
        self.manawhitex_p2_end = self.mana
        
        self.hp_bar_p2_rect = pygame.Rect(self.redx_p2, 150, self.redx_p2_end, 20)
        self.hp_bar_p2_after_rect = pygame.Rect(self.whitex_p2, 150, self.whitex_p2_end, 20)
        self.mana_bar_p2_rect = pygame.Rect(self.manax_p2, 200, self.manax_p2_end, 20)
        self.mana_bar_p2_after_rect = pygame.Rect(self.manawhitex_p2, 200, self.manawhitex_p2_end, 20)
        
        self.hp_decor_p2 = pygame.Rect(self.p2_hp_posx_left, 145, self.p2_mana_posx_right, 30 ) # i only added 100 but need to modify       
        self.mana_decor_p2 = pygame.Rect(self.p2_mana_posx_left, 145+50, self.p2_mana_posx_right, 30) # i only added 100 but need to modify     

        if self.redx_p2 > self.whitex_p2:
            self.whitex_p2 += 0.2
            self.whitex_p2_end -= 0.2
        if self.manax_p2 > self.manawhitex_p2:
            self.manawhitex_p2 += 1
            self.manawhitex_p2_end -= 1
        
        if self.redx_p2 >= self.p2_hp_num + self.p2_hp_num_end:
            self.health = 0
            self.winner = 1
        
        if self.redx_p2 < self.whitex_p2:
            self.whitex_p2 -= 0.2
            self.whitex_p2_end += 0.2

        if self.redx_p2 < self.p2_hp_num: #hp heal limit p2
            self.redx_p2 = self.p2_hp_num
            self.redx_p2_end = self.p2_hp_num_end     

        if self.manax_p2 < self.manawhitex_p2: #(good i think)
            self.manawhitex_p2 -= 1
            self.manawhitex_p2_end += 1  

        if self.manax_p2 < self.p2_mana_num: #mana heal limit p2
            self.manax_p2 = self.p2_mana_num
            self.manax_p2_end = self.p2_mana_num_end
        
        self.hp2 = int(self.redx_p2_end)
        #hehe = 2
        if self.hp2 > LOW_HP:
            hp_display_txt2 = FONT.render(f'[{self.hp2}]', False, white)
        else:
            hp_display_txt2 = FONT.render(f'[{self.hp2}]', False, red)
        screen.blit(hp_display_txt2, ((self.hp_decor_p2.centerx - hp_display_txt2.get_width() // 2) - 150, 
                                self.hp_decor_p2.top + (self.hp_decor_p2.height // 2 - hp_display_txt2.get_height() // 2)))
        
        self.mana2 = int(self.manax_p2_end) 
        if self.mana2 > self.lowest_mana_cost:
            self.mana_display_txt2 = FONT.render(f'[{self.mana2}]', False, white)     
        else:
            self.mana_display_txt2 = FONT.render(f'[{self.mana2}]', False, red) 
        screen.blit(self.mana_display_txt2, ((self.mana_decor_p2.centerx - self.mana_display_txt2.get_width() // 2) - 150, 
                                    self.mana_decor_p2.top + (self.mana_decor_p2.height // 2 - self.mana_display_txt2.get_height() // 2)))  
        
        pygame.draw.rect(screen, black, self.hp_decor_p2)

       
        pygame.draw.rect(screen, red, self.hp_bar_p2_after_rect) if self.hp2 > 20 else pygame.draw.rect(screen, white, self.hp_bar_p2_after_rect)
                
        
        pygame.draw.rect(screen, 'Green', self.hp_bar_p2_rect) if self.hp2 > 20 else pygame.draw.rect(screen, red, self.hp_bar_p2_rect)
        

        pygame.draw.rect(screen, black, self.mana_decor_p2)


        pygame.draw.rect(screen, 'White', self.mana_bar_p2_after_rect)


        pygame.draw.rect(screen, 'Cyan2', self.mana_bar_p2_rect) 

        # print(self.mana)

        return [self.health, self.mana]


if self.player_type == 2:
    # Player 2 Health and Mana Bars
    self.health_bar_p2_starting = int(width) - 300  # Start from the right
    self.mana_bar_p2_starting = int(width) - 300
    self.healthdecor_p2_starting = int(width) - 300 - 5
    self.manadecor_p2_starting = int(width) - 300 - 5

    self.hpdecor_end_p2 = self.max_health + 10
    self.manadecor_end_p2 = self.max_mana + 10

    self.health_bar_p2 = pygame.Rect(self.health_bar_p2_starting, 150, self.health, 20)
    self.health_bar_p2_after = pygame.Rect(self.health_bar_p2_starting, 150, self.white_health_p2, 20)
    self.mana_bar_p2 = pygame.Rect(self.mana_bar_p2_starting, 200, self.mana, 20)
    self.mana_bar_p2_after = pygame.Rect(self.mana_bar_p2_starting, 200, self.white_mana_p2, 20)

    self.hp_decor_p2 = pygame.Rect(self.healthdecor_p2_starting, 145, self.hpdecor_end_p2, 30)
    self.mana_decor_p2 = pygame.Rect(self.manadecor_p2_starting, 195, self.manadecor_end_p2, 30)

    # White rects
    if self.health > self.white_health_p2:
        self.white_health_p2 += WHITE_BAR_SPEED_HP
    if self.health < self.white_health_p2:
        self.white_health_p2 -= WHITE_BAR_SPEED_HP
    if self.mana > self.white_mana_p2:
        self.white_mana_p2 += WHITE_BAR_SPEED_MANA
    if self.mana < self.white_mana_p2:
        self.white_mana_p2 -= WHITE_BAR_SPEED_MANA

    # Health and Mana Limits
    self.health = min(self.health, self.max_health)
    self.mana = min(self.mana, self.max_mana)

    # Health and Mana Text
    self.health_display_text_p2 = font.render(f'[{int(self.health)}]', False, white if self.health > LOW_HP else red)
    self.mana_display_text_p2 = font.render(f'[{int(self.mana)}]', False, white if self.mana > self.lowest_mana_cost else red)

    # Render Health and Mana Bars
    screen.blit(self.health_display_text_p2, ((self.hp_decor_p2.centerx - self.health_display_text_p2.get_width() // 2) - 150,
                                            self.hp_decor_p2.top + (self.hp_decor_p2.height // 2 - self.health_display_text_p2.get_height() // 2)))
    screen.blit(self.mana_display_text_p2, ((self.mana_decor_p2.centerx - self.mana_display_text_p2.get_width() // 2) - 150,
                                            self.mana_decor_p2.top + (self.mana_decor_p2.height // 2 - self.mana_display_text_p2.get_height() // 2)))

    pygame.draw.rect(screen, black, self.hp_decor_p2)  # Decor
    pygame.draw.rect(screen, red if self.health > LOW_HP else white, self.health_bar_p2_after)  # Design when hp is low
    pygame.draw.rect(screen, red if self.health < LOW_HP else green, self.health_bar_p2)  # Design when hp is low

    pygame.draw.rect(screen, black, self.mana_decor_p2)  # Decor
    pygame.draw.rect(screen, white, self.mana_bar_p2_after)  # Design when mana is low
    pygame.draw.rect(screen, cyan2, self.mana_bar_p2)  # Design when mana is low

# class Player(pygame.sprite.Sprite):


#     def __init__(self,
#                 idle_ani,
#                 atk1_ani,
#                 sp_ani,
#                 death_ani,
#                 skill_1_rect,
#                 skill_2_rect,
#                 skill_3_rect,
#                 skill_4_rect):
#         super().__init__()

#         self.skill_1_rect = skill_1_rect
#         self.skill_2_rect = skill_2_rect
#         self.skill_3_rect = skill_3_rect
#         self.skill_4_rect = skill_4_rect
        
#         self.mouse_pos = pygame.mouse.get_pos()
#         self.keys = pygame.key.get_pressed()
#         self.mouse_press = pygame.mouse.get_pressed()

#         self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2])
#         self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2])
#         self.player_atk2 = self.player_atk1
#         self.player_atk3 = self.player_atk1
#         self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2])
#         self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2])

#         self.image = self.player_idle[self.player_idle_index]
#         self.rect = self.image.get_rect(midbottom = (100, self.y_pos)) #(for p1)
        
#         self.player_idle_index = 0
#         self.player_atk1_index = 0
#         self.player_atk2_index = 0
#         self.player_atk3_index = 0
#         self.player_sp_index = 0
#         self.player_death_index = 0
#         self.attacking1 = False
#         self.attacking2 = False
#         self.attacking3 = False
#         self.sp_attacking = False

#         self.y_pos = (int(height)) * 0.76

        

#         self.x_pos = 0 # if p2 else remove (int(width)) - 100
#         self.y_pos = 0 # (int(height)) * 0.76

        

         

#         self.last_atk_time = 0

#         #Attack-------------------------------------------------------------

#         #Attack-------------------------------------------------------------

#     def load_img_frames(self, folder, count, starts_at_zero=False):
        
#         images = []
#         for i in range(count):
#             print('HA' * i)
#             # img_path = (fr'HERO FIGHTING\assets\characters\{folder}{i + 1 - starts_at_zero}.png')
#             img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
#             image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
#             image = pygame.transform.rotozoom(image, 0, 1.5)
#             images.append(image)
#         return images
    
#     def load_attack_class(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0, frame_duration=30):
#         """
#         Utility function to load an attack animation from a spritesheet.

#         Args:
#             filepath (str): Path to the spritesheet image.
#             frame_width (int): Width of each frame in the spritesheet.
#             frame_height (int): Height of each frame in the spritesheet.
#             rows (int): Number of rows in the spritesheet.
#             columns (int): Number of columns in the spritesheet.
#             scale (float): Scale factor for resizing the frames.
#             rotation (float): Rotation angle in degrees for the frames.
#             frame_duration (int): Duration of each frame in milliseconds.

#         Returns:
#             AnimatedAttack: An instance of the AnimatedAttack class.
#         """
#         spritesheet = pygame.image.load(filepath).convert_alpha()

#         spritesheet_width = spritesheet.get_width()
#         spritesheet_height = spritesheet.get_height()
#         # Debugging: Print the spritesheet dimensions and frame dimensions
#         print(f"Spritesheet size: {spritesheet_width}x{spritesheet_height}")
#         calculated_frame_width = spritesheet_width // columns
#         calculated_frame_height = spritesheet_height // rows
#         print(f"Calculated frame size: {calculated_frame_width}x{calculated_frame_height}")
#         # Check if the provided frame dimensions match the calculated ones
#         if frame_width != calculated_frame_width or frame_height != calculated_frame_height:
#             print(
#                 f"Warning: Provided frame dimensions ({frame_width}x{frame_height}) "
#                 f"do not match calculated dimensions ({calculated_frame_width}x{calculated_frame_height})."
#             )
#             frame_width = calculated_frame_width
#             frame_height = calculated_frame_height


#         spritesheet = SpriteSheet(filepath, frame_width, frame_height, rows, columns, scale, rotation)
#         frames = spritesheet.get_frames()
#         return frames
    
#     def simple_idle_animation(self):
#         current_time = pygame.time.get_ticks() 
#         if current_time - self.last_atk_time > 140:
#             self.last_atk_time = current_time
#             self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#             self.image = self.player_idle[int(self.player_idle_index)]
   
#     def atk1_animation(self):
#         current_time = pygame.time.get_ticks()       
#         if self.attacking1:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.image = self.player_atk1[int(self.player_atk1_index)]
#                 self.player_atk1_index += 1
#                 if self.player_atk1_index >= len(self.player_atk1):
#                     self.attacking1 = False
#                     self.player_atk1_index = 0
#                     self.last_atk_time = current_time
#         else:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#                 self.image = self.player_idle[int(self.player_idle_index)]

#     def atk2_animation(self):
#         current_time = pygame.time.get_ticks()       
#         if self.attacking2:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.image = self.player_atk2[int(self.player_atk2_index)]
#                 self.player_atk2_index += 1
#                 if self.player_atk2_index >= len(self.player_atk2):
#                     self.attacking2 = False
#                     self.player_atk1_index = 0
#                     self.last_atk_time = current_time
#         else:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#                 self.image = self.player_idle[int(self.player_idle_index)]

#     def atk3_animation(self):
#         current_time = pygame.time.get_ticks()       
#         if self.attacking3:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.image = self.player_atk3[int(self.player_atk3_index)]
#                 self.player_atk3_index += 1
#                 if self.player_atk3_index >= len(self.player_atk3):
#                     self.attacking3 = False
#                     self.player_atk3_index = 0
#                     self.last_atk_time = current_time
#         else:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#                 self.image = self.player_idle[int(self.player_idle_index)]

#     def sp_animation(self):
#         current_time = pygame.time.get_ticks()       
#         if self.sp_attacking:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.image = self.player_sp[int(self.player_sp_index)]
#                 self.player_sp_index += 1
#                 if self.player_sp_index >= len(self.player_sp):
#                     self.attacking3 = False
#                     self.player_sp_index = 0
#                     self.last_atk_time = current_time
#         else:
#             if current_time - self.last_atk_time > 140:
#                 self.last_atk_time = current_time
#                 self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#                 self.image = self.player_idle[int(self.player_idle_index)]

#     def play_death_animation(self, player_dead, player_dead_complete, player_revert_death_index): #only change the globals
        
#         if player_dead:
#             self.attacking4 = False
#             self.player_atk_index4 = 0
#             self.ani_done_4 = 0
#             current_time = pygame.time.get_ticks()
#             if current_time - self.last_atk_time4 > 110:
#                 self.last_atk_time4 = current_time
#                 self.image = self.player_death[self.player_death_index]
#                 self.player_death_index += 1
                
#                 if self.player_death_index >= len(self.player_death):
#                     player7_dead_complete = True
#                     self.last_atk_time4 = current_time
#                     self.player_death_index = player_revert_death_index
             
#         else:
#             if current_time - self.last_atk_time2 > 140:
#                 self.last_atk_time2 = current_time
#                 self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
#                 self.image = self.player_idle[int(self.player_idle_index)]

#         if player7_dead_complete:
#             self.player_death_index = (len(self.player_death) - 1)
#             self.image = self.player_death[int(self.player_death_index)]

#     # def input(self, skill_1_rect, skill_2_rect, skill_3_rect, skill_4_rect, player_turn):
#     #     if player_turn == 1:
#     #         if (self.keys[pygame.K_KP1] or self.keys[pygame.K_u]):
#     #             self.attacking1 = True
#     #         if (self.keys[pygame.K_KP2] or self.keys[pygame.K_i]):
#     #             self.attacking2 = True
#     #         if (self.keys[pygame.K_KP3] or self.keys[pygame.K_o]):
#     #             self.attacking3 = True
#     #         if (self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_p]):
#     #             self.sp_attacking = True

#     #         if skill_1_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
#     #             self.attacking1 = True
#     #         if skill_2_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
#     #             self.attacking2 = True
#     #         if skill_3_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
#     #             self.attacking3 = True
#     #         if skill_4_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
#     #             self.sp_attacking = True

#     def update(self):


#         self.input()
#         if self.attacking1:
#             self.atk1_animation()
#         elif self.attacking2:
#             self.atk2_animation()
#         elif self.attacking3:
#             self.atk3_animation()
#         elif self.sp_attacking:
#             self.sp_animation()
#         else:

#             self.simple_idle_animation()

# class SpriteSheet:
#     def __init__(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0):
#         """
#         Handles loading and slicing spritesheets into individual frames for animation.

#         Args:
#             filepath (str): Path to the spritesheet image.
#             frame_width (int): Width of each frame in the spritesheet.
#             frame_height (int): Height of each frame in the spritesheet.
#             rows (int): Number of rows in the spritesheet.
#             columns (int): Number of columns in the spritesheet.
#             scale (float): Scale factor for resizing the frames (default=1).
#             rotation (float): Rotation angle in degrees for the frames (default=0).
#         """
#         self.spritesheet = pygame.image.load(filepath).convert_alpha()
#         self.frame_width = frame_width
#         self.frame_height = frame_height
#         self.rows = rows
#         self.columns = columns
#         self.scale = scale
#         self.rotation = rotation
#         self.frames = self._slice_spritesheet()

#     def _slice_spritesheet(self):
#         frames = []
#         for row in range(self.rows):
#             for col in range(self.columns):
#                 x = col * self.frame_width
#                 y = row * self.frame_height
#                 frame = self.spritesheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
#                 frame = pygame.transform.rotozoom(frame, self.rotation, self.scale)
#                 frames.append(frame)
#         return frames

#     def get_frames(self):
#         """Returns the sliced frames of the spritesheet."""
#         return self.frames














































































DELAY = 500

class Attacks(pygame.sprite.Sprite):
    def __init__(self, x, y, img_paths, frame_duration, repeat_animation, speed, moving, dmg, mana_cost, who_attacks, who_attacked, skill_rect, skill_img, hotkey, attack_display, cd_logic=0, cd_time=0):
        super().__init__()
        
        self.frames = img_paths
        self.frame_duration = frame_duration
        self.repeat_animation = repeat_animation
        self.speed = speed
        self.moving = moving
        self.dmg = dmg
        self.mana_cost = mana_cost
        self.who_attacks = who_attacks
        self.who_attacked = who_attacked
        self.skill_rect = skill_rect
        self.skill_img = skill_img
        self.hotkey = hotkey
        self.cd_logic = cd_logic
        self.cd_time = cd_time

        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (x, y))

        self.current_repeat = 0 #how many times animation repeats b4 ends
        self.animation_done = False

        self.mana_font = pygame.font.Font(None, 30)
        self.cd_font = pygame.font.Font(None, 30)
        self.last_atk_time = 0
        

    def atk_cd_logic(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        

        if self.mana >= self.mana_cost:
            self.atk_mana_cost = self.mana_font.render(f'[{self.mana_cost_atk1}]', False, 'Cyan2')
        else:
            self.atk_mana_cost = self.mana_font.render(f'[{self.mana_cost_atk1}]', False, 'Cyan2')

        screen.blit(self.atk_mana_cost, (self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2, 
                               self.skill_rect.top + (self.skill_rect.height // 2 - self.atk_mana_cost.get_height() // 2) - 50))

        if self.who_attacks == 1 and self.cd_logic > 0:
            current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
            if current_time - self.last_atk_time >= 1000:  # 1 second has passed
                self.cd_logic -= 1  # Reduce cooldown by 1 second
                self.last_atk_time = current_time  # Update the last time cooldown was reduced
        
        # Display the cooldown overlay and text
        if self.cd_logic > 0:
            # Draw dark overlay and cooldown text when skill is on cooldown
            dark_overlay = pygame.Surface(self.skill_rect.size)  
            dark_overlay.fill((0, 0, 0))  # Black overlay
            dark_overlay.set_alpha(128)  # Semi-transparent overlay
            screen.blit(self.skill_img, self.skill_rect)  # Draw the skill icon
            screen.blit(dark_overlay, self.skill_rect)  # Overlay on top

            self.cd_text = self.cd_font.render(str(self.cd_logic), True, 'Red')  # Cooldown text
            screen.blit(self.cd_text, (self.skill_rect.centerx - self.cd_text.get_width() // 2, 
                                self.skill_rect.top + (self.skill_rect.height // 2 - self.cd_text.get_height() // 2)))

        #no mana overlay________________________________________
        elif self.mana < self.mana_cost:
            # If there's not enough mana, darken the skill icon like cooldown
            dark_overlay = pygame.Surface(self.skill_rect.size)  
            dark_overlay.fill((0, 0, 0))  # Black overlay
            dark_overlay.set_alpha(128)  # Semi-transparent overlay
            screen.blit(self.skill_img, self.skill_rect)  # Draw the skill icon
            screen.blit(dark_overlay, self.skill_rect)  # Overlay on top
        #_____________________________________________

        else:
            # If cooldown is over, just show the skill icon without overlay
            screen.blit(self.skill_img, self.skill_rect)

        if self.cd_logic == 0:
            if self.mana >= self.mana_cost:  # Check if player has enough mana
                if self.skill_rect.collidepoint(mouse_pos) and mouse_press[0] or self.hotkey:
                    current_time_ = pygame.time.get_ticks()
                    # activate_delay = True

                    if (current_time_ - self.last_atk_time > DELAY):
                            
                        print(f"{self} used Attack 1")
                        # if pygame.time.wait(1000) == True:#pause
                        # if event.type == WAIT:
                        # Instantiate attack or perform action related to Attack 1 here
                        attack = self.attack_func()
                        self.attack_display.add(attack)  # Add attack to the group
                        self.cd_logic = self.cd_time  # Reset cooldown
                        self.last_atk_time = current_time

                        self.mana -= self.mana_cost  # Deduct mana cost
                        # manax_p1_end += manax_p1

                        # activate_delay = False

                        # player_turn = 2  # Switch to Player 2 after Player 1 uses the skill      

    def attack_func(self, x, y, img_paths, frame_duration, repeat_animation):
        current_time = pygame.time.get_ticks()
        self.rect.x += self.speed if self.moving else 0
        
        if current_time - self.last_update_time > self.frame_duration:
            self.frame_index += 1
            self.last_update_time = current_time

            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.frame_index = 0
                self.current_repeat += 1

                if self.current_repeat >= self.repeat_animation:
                    #dmg animation
                    # self.who_attacked += self.dmg
                    self.who_attacked.take_damage(self.dmg)
                    self.animation_done = True
                    self.kill()
                    # if pygame.sprite.spritecollide(self, player2, False):
                    #     self.speed = 0
                        
        if self.rect.x > width + 300 or self.rect.x < -300:
            self.animation_done = True
            self.kill()

    def update(self):
        self.atk_cd_logic()

        
class Attack_Display(pygame.sprite.Sprite, Attacks):
    def __init__(self, x, y, img_paths, frame_duration, repeat_animation, speed, moving, dmg, mana_cost, who_attacks, who_attacked, skill_rect, skill_img, hotkey):
        super().__init__()
        pass
    def update(self):
        super().update()
        



icon = pygame.image.load(r'PYTHON WITH KIM  NEW!\miku.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("HERO FIGHTING")

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
attack_display = pygame.sprite.Group()
# attack_display.add(Attack_Display)
atk1 = Attacks(
            x=self.rect.centerx + 50 if self.facing_right else self.rect.centerx - 50,
            y=self.rect.centery,
            img_paths=self.player_atk1,
            frame_duration=100,
            repeat_animation=1,
            speed=5,
            moving=True,
            dmg=20,
            mana_cost=30,
            who_attacks=self,  # Pass the Fire_Wizard instance
            who_attacked=target,  # Pass the Wanderer_Magician instance
            skill_rect=self.skill_1_rect,
            skill_img=self.skill_1,
            hotkey=keys[pygame.K_q],
            attack_display=attack_display,
            cd_logic=3000,
            cd_time=5,
        )
attack_display.append(atk1)

# player = pygame.sprite.Group()
# player.add(Player())

def game():
    background = pygame.transform.scale(pygame.image.load(r'HERO FIGHTING\assets\backgrounds\1.png').convert(), (width, height))
    while True:
        screen.fill((100,100,100))
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0,0))
        attack_display.update()
        
        # player.draw(screen)
        # player.update()

        #main.Fire_Wizard.update(self='je')
        #main.fire_wizard.update()
        #main.screen.blit(main.fire_wizard, (0,0))


        

        pygame.display.update()
        clock.tick(60)

game()