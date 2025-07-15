class Player6(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global width, height
        
        self.mouse_pos = pygame.mouse.get_pos()
        self.key_press = pygame.key.get_pressed()
        self.mouse_press = pygame.mouse.get_pressed()


        self.player_idle = self.load_img('idle', 8)
        self.player_idle_index = 0
        
        self.player_atk = self.load_img('2_atk', 18)#1 shoot arrow
        self.player_atk_index = 0

        self.player_atk2 = self.load_img('3_atk', 26)#3 arrow rain
        self.player_atk_index2 = 0

        self.player_atk3 = self.load_img('sp_atk', 8)#ult slice
        self.player_atk_index3 = 0

        self.player_atk4 = self.load_img('air_atk', 7)#2 jump shoot arrow
        self.player_atk_index4 = 0

        self.player_atk121 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\sp_atk\sp_atk_28.png').convert_alpha(), True, False), 0, 1.5)
        self.player_atk122 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\sp_atk\sp_atk_29.png').convert_alpha(), True, False), 0, 1.5)
        self.player_atk123 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\sp_atk\sp_atk_30.png').convert_alpha(), True, False), 0, 1.5)
        
        
        self.player_atk5 = [self.player_atk121, self.player_atk122, self.player_atk123]
        self.player_atk_index5 = 0

        # Ain't touching this one (nvm)
        # v v v v v v v v v v v v
        
        self.player_death = self.load_img2(19)
        self.player_death_index = 0

        self.player_death_final = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\death\death_19.png').convert_alpha(), True, False), 0, 1.5)

        #declaring the size
        self.x_pos = (int(width)) - 100
        self.y_pos = (int(height)) * 0.76 #preferred location for y position

        self.image = self.player_idle[self.player_idle_index]
        # self.rect = self.image.get_rect(midbottom = (1060, 470))  #need to be modified based on the screen width and height 
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

        #timer
        self.last_atk_time = 0
        self.attacking = False

        self.last_atk_time2 = 0
        self.attacking2 = False

        self.last_atk_time3 = 0
        self.attacking3 = False

        self.last_atk_time4 = 0 # yep this is inconsistent but i hope no error
        self.attacking4 = False

        self.last_atk_time_test = pygame.time.get_ticks()
        self.attacking_test = True
        

        self.last_atk_time_add = 0
        self.attacking_add = False

        self.last_atk_time4 = 0 # :/

    def load_img2(self, count):
        images = []
        for i in range(count):
            img_path = (fr'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\death\death_{i + 1}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, 0, 1.5)
            images.append(image)
        return images

    def load_img(self, folder, count):
        images = []
        for i in range(count): #lol i fixed it myself.. I'd say basic :o (sounds cool)
            img_path = (fr'PYTHON WITH KIM  NEW!\characters\2ND PAGE\elementals\wind\elementals_wind_hashashin_FREE_v1.1\PNG\{folder}\{folder}_{i + 1}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, 0, 1.5)#rather not to combine these (things might get confusing)
            images.append(image)
        return images

    def input(self):
        global skill_21_rect, skill_22_rect, skill_23_rect, skill_24_rect, player_turn
        keys = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if player_turn == 1:
            if (keys[pygame.K_KP1] or keys[pygame.K_u]):
                self.attacking = True
            if (keys[pygame.K_KP2] or keys[pygame.K_i]):
                self.attacking4 = True
            if (keys[pygame.K_KP3] or keys[pygame.K_o]):
                self.attacking2 = True
            if (keys[pygame.K_KP_ENTER] or keys[pygame.K_p]):
                self.attacking3 = True


            if skill_21_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking = True
            if skill_22_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking4 = True
            if skill_23_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking2 = True
            if skill_24_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking3 = True
                

    def animation(self):#1st
        current_time = pygame.time.get_ticks()
         
        if self.attacking:
            if current_time - self.last_atk_time > 80:
                self.last_atk_time = current_time
                self.image = self.player_atk[int(self.player_atk_index)]
                self.player_atk_index += 1

                if self.player_atk_index >= len(self.player_atk):
                    self.attacking = False
                    self.attacking_add = True
                    self.player_atk_index = 0
                    self.last_atk_time = current_time

        else:
            if current_time - self.last_atk_time > 110:
                self.last_atk_time = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]

    def animation2(self): #3rd
        current_time = pygame.time.get_ticks()
         
        if self.attacking2:
            if current_time - self.last_atk_time2 > 80:
                self.last_atk_time2 = current_time
                self.image = self.player_atk2[int(self.player_atk_index2)]
                self.player_atk_index2 += 1

                if self.player_atk_index2 >= len(self.player_atk2):
                    self.attacking2 = False
                    self.attacking_add = True
                    self.player_atk_index2 = 0
                    self.last_atk_time2 = current_time

        else:
            if current_time - self.last_atk_time2 > 110:
                self.last_atk_time2 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]
    
    def animation3(self): #ultimate
        current_time = pygame.time.get_ticks()
         
        if self.attacking3:
            if current_time - self.last_atk_time3 > 40:
                self.last_atk_time3 = current_time
                self.image = self.player_atk3[int(self.player_atk_index3)]
                self.player_atk_index3 += 1

                if self.player_atk_index3 >= len(self.player_atk3):
                    self.attacking3 = False
                    self.attacking_test = True
                    self.player_atk_index3 = 0 #resetting the index here
                    self.last_atk_time3 = current_time
                    
                    

        else:
            if current_time - self.last_atk_time3 > 110:
                self.last_atk_time3 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]

    def animation4(self): #2nd
        current_time = pygame.time.get_ticks()
        
        if self.attacking4:
            self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos - 60))
            if current_time - self.last_atk_time4 > 100:
                self.last_atk_time4 = current_time
                self.image = self.player_atk4[int(self.player_atk_index4)]
                self.player_atk_index4 += 1

                if self.player_atk_index4 >= len(self.player_atk4):
                    self.attacking4 = False
                    self.attacking_add = True
                    self.player_atk_index4 = 0
                    self.last_atk_time4 = current_time
                    self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos
                    ))

        else:
            if current_time - self.last_atk_time4 > 110: #this is inconsistent
                self.last_atk_time4 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]


    # def test_animation(self): #this function vanishes the player into the oblivion (screen)
    #     current_time = pygame.time.get_ticks()
         
    #     if self.attacking_test and (not self.attacking3):
    #         if current_time - self.last_atk_time_test > 4000:
    #             self.last_atk_time_test = pygame.time.get_ticks()
    #             self.attacking_test = False
    #             self.attacking_add = True #executing the additional animation
                
                
    #         else:
    #             self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    #             if current_time - self.last_atk_time_test > 4000:
    #                 self.attacking_test = False
    #                 self.last_atk_time_test = pygame.time.get_ticks()

    #     if not self.attacking_test:
    #         if current_time - self.last_atk_time_add > 110: #this is inconsistent
    #             self.last_atk_time_add = current_time
    #             self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
    #             self.image = self.player_idle[int(self.player_idle_index)]




    def additional_animation(self): #jump shoot
        current_time = pygame.time.get_ticks()
        
        if self.attacking_add:
            if current_time - self.last_atk_time_add > 100:
                self.last_atk_time_add = current_time
                self.image = self.player_atk5[int(self.player_atk_index5)]
                self.player_atk_index5 += 1

                if self.player_atk_index5 >= len(self.player_atk5):
                    self.attacking_add = False
                    self.player_atk_index5 = 0
                    
                    self.last_atk_time_add = current_time

        else:
            if current_time - self.last_atk_time_add > 110: #this is inconsistent
                self.last_atk_time_add = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]







    def play_death_animation(self): #only change the globals
        global player6_dead, player6_dead_complete, player6_revert_death_index
        if player6_dead:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_atk_time4 > 80:
                self.last_atk_time4 = current_time
                self.image = self.player_death[self.player_death_index]
                self.player_death_index += 1
                
                if self.player_death_index >= len(self.player_death):
                    player6_dead_complete = True
                    self.last_atk_time4 = current_time
                    self.player_death_index = player6_revert_death_index
        else:
            if current_time - self.last_atk_time2 > 110:
                self.last_atk_time2 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]
          
        if player6_dead_complete:
            # Keep the last frame of the death animation (MANUALLY!!!)
            self.image = self.player_death_final
            
    # def reset_player(self):
    #     global for_vanish_player6
    #     if for_vanish_player6:
    #         self.attacking = False
    #         self.attacking2 = False
    #         self.attacking3 = False
    #         self.attacking4 = False
    #         self.attacking_test = False  # Reset vanish animation
    #         self.attacking_add = False

    #         self.player_atk_index = 0
    #         self.player_atk_index2 = 0
    #         self.player_atk_index3 = 0
    #         self.player_atk_index4 = 0
    #         self.player_atk_index5 = 0

    #         self.image = self.player_idle[0]

    def update(self):
        global player6_dead
        # global for_vanish_player6
        
        # NOTE: dont forget to make the playerX_dead False (when the player dies) it is in the game loop, find it :D
        #LITERALLY DONT FORGET AND ALSO check up the try_again function since it holds 'RETRY' button (which means, again)
        self.input()
        # self.reset_player()
        # print(for_vanish_player6)
        
            
        if player6_dead: #I MODIFIED THIS ON ORDER (execution order)
            self.play_death_animation()
        
        elif self.attacking3:
            self.animation3()#4th skill
        elif self.attacking2:
            self.animation2()#3rd skill
        elif self.attacking:
            self.animation()#1st skill  
        elif self.attacking4:
            self.animation4()#2nd skill, need to enable if using the literal player to attack (eg. moving the player to the enemy)
        elif self.attacking_add:
            self.additional_animation()
        # elif self.attacking_test:
        #     self.test_animation()
        else:
            self.animation()#back to normal attack (1st skill)