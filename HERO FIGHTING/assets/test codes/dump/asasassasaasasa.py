import pygame

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global width, height
        self.mouse_pos = pygame.mouse.get_pos()
        self.key_press = pygame.key.get_pressed()
        self.mouse_press = pygame.mouse.get_pressed()


        self.player_idle = self.load_img('idle pngs', 7)
        self.player_idle_index = 0
        
        self.player_atk = self.load_img('attack 1 pngs', 7)
        self.player_atk_index = 0

        self.player_atk2 = self.load_img('charge pngs', 16)
        self.player_atk_index2 = 0

        self.player_atk3 = self.load_img('attack 2 pngs', 9)
        self.player_atk_index3 = 0


        # Ain't touching this one 
        # v v v v v v v v v v v v
        self.player_death1 = pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\dead\tile000.png').convert_alpha(), True, False)
        self.player_death2 = pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\dead\tile001.png').convert_alpha(), True, False)
        self.player_death3 = pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\dead\tile002.png').convert_alpha(), True, False)
        self.player_death4 = pygame.transform.flip(pygame.image.load(r'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\dead\tile003.png').convert_alpha(), True, False)
   
        self.player_death = [self.player_death1, self.player_death2, self.player_death3, self.player_death4]
        self.player_death_index = 0

        #declaring the size
        x_pos = (int(width)) - 100
        y_pos = (int(height)) * 0.76 #preferred location for y position

        self.image = self.player_idle[self.player_idle_index]
        # self.rect = self.image.get_rect(midbottom = (1060, 470))  #need to be modified based on the screen width and height 
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))

        #timer
        self.last_atk_time = 0
        self.attacking = False

        self.last_atk_time2 = 0
        self.attacking2 = False

        self.last_atk_time3 = 0
        self.attacking3 = False

        self.last_atk_time_test = 0
        self.attacking_test = False

        self.last_atk_time4 = 0

    def load_img(self, folder, count):
        images = []
        for i in range(count):
            img_path = (fr'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\{folder}\image_0-{i}.png')
            try: #only for this code (I hope) since the naming of the files is not redundant (Player2)
                image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
                images.append(image)
            except FileNotFoundError: #it's working properly now :) (happi_)
                img_path = (fr'PYTHON WITH KIM  NEW!\characters\wizard\Wanderer Magican\{folder}\tile{str(i).zfill(3)}.png') #zfill is smart move :D
                image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
                images.append(image)
                  
        return images

    def input(self):
        global skill_5_rect, skill_6_rect, skill_7_rect, skill_8_rect, player_turn
        keys = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if player_turn == 1:
            if (keys[pygame.K_KP1] or keys[pygame.K_u]): #no animation for healing
                self.attacking = True
            if (keys[pygame.K_KP_ENTER] or keys[pygame.K_p]):
                self.attacking2 = True
            if (keys[pygame.K_KP3] or keys[pygame.K_o]):
                self.attacking3 = True
            # if (keys[pygame.K_KP2]): #vanish code
            #     self.attacking_test = True

            if skill_5_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking = True
            # if skill_6_rect.collidepoint(mouse_pos) and mouse_press[0]: #vanish code
            #     self.attacking_test = True
            if skill_7_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking3 = True
            if skill_8_rect.collidepoint(mouse_pos) and mouse_press[0]:
                self.attacking2 = True

    def animation(self): #cicle attack
        current_time = pygame.time.get_ticks()
         
        if self.attacking:
            if current_time - self.last_atk_time > 140:
                self.last_atk_time = current_time
                self.image = self.player_atk[int(self.player_atk_index)]
                self.player_atk_index += 1

                if self.player_atk_index >= len(self.player_atk):
                    self.attacking = False
                    self.player_atk_index = 0
                    self.last_atk_time = current_time

        else:
            if current_time - self.last_atk_time > 140:
                self.last_atk_time = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]

    def animation2(self): #pop attack
        current_time = pygame.time.get_ticks()
         
        if self.attacking2:
            if current_time - self.last_atk_time2 > 180:
                self.last_atk_time2 = current_time
                self.image = self.player_atk2[int(self.player_atk_index2)]
                self.player_atk_index2 += 1

                if self.player_atk_index2 >= len(self.player_atk2):
                    self.attacking2 = False
                    self.player_atk_index2 = 0
                    self.last_atk_time2 = current_time

        else:
            if current_time - self.last_atk_time2 > 140:
                self.last_atk_time2 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]
    
    def animation3(self): #rasengan
        current_time = pygame.time.get_ticks()
         
        if self.attacking3:
            if current_time - self.last_atk_time3 > 130:
                self.last_atk_time3 = current_time
                self.image = self.player_atk3[int(self.player_atk_index3)]
                self.player_atk_index3 += 1

                if self.player_atk_index3 >= len(self.player_atk3):
                    self.attacking3 = False
                    self.player_atk_index3 = 0
                    self.last_atk_time3 = current_time

        else:
            if current_time - self.last_atk_time3 > 140:
                self.last_atk_time3 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]

    def test_animation(self): #this function vanishes the player into the oblivion (screen)
        current_time = pygame.time.get_ticks()
         
        if self.attacking_test:
            if current_time - self.last_atk_time_test > 3000:
                self.last_atk_time_test = current_time
                self.attacking_test = False
                self.image = self.player_idle[self.player_idle_index]
            else:
                self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        else:
            if current_time - self.last_atk_time3 > 140:
                self.last_atk_time3 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]
    
    def play_death_animation(self): #only change the globals
        global player2_dead, player2_dead_complete, player2_revert_death_index
        if player2_dead:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_atk_time4 > 300:
                self.last_atk_time4 = current_time
                self.image = self.player_death[self.player_death_index]
                self.player_death_index += 1
                
                if self.player_death_index >= len(self.player_death):
                    player2_dead_complete = True
                    self.player_death_index = player2_revert_death_index
        else:
            if current_time - self.last_atk_time2 > 140:
                self.last_atk_time2 = current_time
                self.player_idle_index = (self.player_idle_index + 1) % len(self.player_idle)
                self.image = self.player_idle[int(self.player_idle_index)]
          
        if player2_dead_complete:
            # Keep the last frame of the death animation (MANUALLY!!!)
            self.image = self.player_death4 
            
    def update(self):
        global player2_dead
        # NOTE: dont forget to make the playerX_dead False (when the player dies) it is in the game loop, find it :D
        #LITERALLY DONT FORGET AND ALSO check up the try_again function since it holds 'RETRY' button (which means, again)
        #self.input()
        
        if player2_dead: #always first
            self.play_death_animation()
        elif self.attacking2:
            self.animation2()#4th skill
        elif self.attacking:
            self.animation()#1st skill
        elif self.attacking3:
            self.animation3()#3rd skill
        elif self.attacking_test:
            self.test_animation()#2nd skill, need to enable if using the literal player to attack (eg. moving the player to the enemy)
        
        else:
            self.animation()#back to normal attack (1st skill)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('PYTHON WITH KIM  NEW!\png gojos\gojo3walk.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1, 0, 0.15)
        player_walk_2 = pygame.image.load('PYTHON WITH KIM  NEW!\png gojos\gojo4walk.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2, 0, 0.15)
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.player_jump = pygame.image.load('PYTHON WITH KIM  NEW!\png gojos\gojo1.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(self.player_jump, 0, 0.15)
        # self.player_jump_2 = pygame.image.load('PYTHON WITH KIM  NEW!\png gojos\gojo3.png').convert_alpha()
        # self.player_jump_2 = pygame.transform.rotozoom(self.player_jump_2, 0, 0.15)
        # self.player_jump_switch = 0  

        self.image = self.player_walk[self.player_index] 
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('PYTHON WITH KIM  NEW!\Audios\jump.swing-whoosh-110410.mp3')
        self.jump_sound.set_volume(0.5)
        #self.jump_sound_land = pygame.mixer.Sound('PYTHON WITH KIM  NEW!\audios\land2-43790.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1 
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

player2_dead_complete = False
player2_dead = False
player_turn = 1

pygame.init()
icon = pygame.image.load(r'PYTHON WITH KIM  NEW!\miku.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("HERO FIGHTING")

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()

player = pygame.sprite.Group()
player.add(Player())





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
        
        player.draw(screen)
        player.update()

        #main.Fire_Wizard.update(self='je')
        #main.fire_wizard.update()
        #main.screen.blit(main.fire_wizard, (0,0))


        

        pygame.display.update()
        clock.tick(60)

game()