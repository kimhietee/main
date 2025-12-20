import pygame



class ImageButton:
    def __init__(self, image_path, pos, scale, text, font_path, font_size, text_color, move_y=0, hover_move=2, fku=False, scale_val=(0,0), alpha=(1,1), text_anti_alias=True):
        # Load and scale the image
        self.hover_pos = pos
        self.hover_move = hover_move
        self.fku = fku
        self.scale_val = scale_val
        self.alpha = alpha
        if self.fku:
            self.original_image = pygame.transform.scale(
        pygame.image.load(self.original_image).convert_alpha(), (self.scale_val[0], self.scale_val[1]))
        else:
            self.original_image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.image.set_alpha(int(self.alpha[0] * 255))
        self.rect = self.image.get_rect(center=pos)

        self.text_anti_alias = text_anti_alias
    
        
        
        
        
        # Text
        self.text = text
        self.font = pygame.font.Font(font_path, int(font_size*7.142857142857143)) # Font size = 100
        self.text_color = text_color

        text_surf = self.font.render(self.text, self.text_anti_alias, self.text_color)
        text_surf.set_alpha(int(self.alpha[1] * 255))

        self.text_surf = pygame.transform.rotozoom(text_surf, 0, 0.2)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.rect.centery = self.hover_pos[1] + self.hover_move 
            self.text_rect.centery = self.hover_pos[1] + self.hover_move
        else:
            self.rect.centery = self.hover_pos[1]
            self.text_rect.centery = self.hover_pos[1]
        
        # Draw the image and text
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def set_position(self, center): # this is the original position 
        dx = center[0] - self.rect.centerx
        dy = center[1] - self.rect.centery

        self.rect.center = center


        self.text_rect.x += dx
        self.text_rect.y += dy



    # Input below can only be checked at pygame.event.MOUSEBUTTON... or any input involving event
    def is_clicked(self, mouse_pos):
        # Check if button is clicked
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    # self.rect.colliderect()
    def is_hovered(self, mouse_pos):
        # Check if button is hovered
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    

    def animate(self,screen, keyframe):
        self.rect = self.image.get_rect(center=keyframe)
        screen.blit(self.image, self.rect)

        screen.blit(self.text_surf, self.text_rect)




    

    
class ImageInfo:
    def __init__(self, image_path, pos, scale, text, text1, text2, font_path, font_size, text_color, move_y=0, hover_move=2):
        # Load and scale the image
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.rect = self.image.get_rect(center=pos)

        self.hover_pos = pos
        self.hover_move = hover_move
        
        # Text
        self.text = text
        self.text1 = text1
        self.text2 = text2

        self.font = pygame.font.Font(font_path, int(font_size*7.142857142857143)) # Font size = 100
        self.text_color = text_color

        self.text_surf = pygame.transform.rotozoom(self.font.render(self.text, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.text_surf1 = pygame.transform.rotozoom(self.font.render(self.text1, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect1 = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 50))

        self.text_surf2 = pygame.transform.rotozoom(self.font.render(self.text2, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect2 = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 100))

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.rect.centery = self.hover_pos[1] + self.hover_move 
            self.text_rect.centery = self.hover_pos[1] + self.hover_move
        else:
            self.rect.centery = self.hover_pos[1]
            self.text_rect.centery = self.hover_pos[1]
        
        # Draw the image and text
        screen.blit(self.image, self.rect)


        screen.blit(self.text_surf, self.text_rect)
        screen.blit(self.text_surf1, self.text_rect1)
        screen.blit(self.text_surf2, self.text_rect2)

    


    def is_clicked(self, mouse_pos):
        # Check if button is clicked
        if self.rect.collidepoint(mouse_pos):
            return True
        return False




class RectButton:
    def __init__(self, x:int, y:int, font:str, font_size:int, color:str, text:str, width:int=40, height:int=40, height_position:int=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.text = text
        self.height_position = height_position
        self.rect_color = self.color
        


        self.button_clicked = False
        self.button_hovered = False

        self.done_clicking = False
        self.enabled = False
    
    def draw(self, screen:pygame.Surface, text_anti_alias):
        pygame.draw.rect(screen, self.rect_color, self.rect)
        self.text_surf = self.font.render(self.text, text_anti_alias, 'white')
        self.text_rect = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery-self.height_position))
        screen.blit(self.text_surf, self.text_rect)
        # pygame.draw.rect(screen, self.rect_color, self.rect)

    def is_clicked(self, mouse_pos): #only detects if the mouse is in the rect
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def is_switched(self, value=True , switch=True):
        if value and switch:
            self.enabled = not self.enabled
        if not switch:
            self.enabled = value
            print(self.enabled)
        return self.enabled


        return self.enabled
    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    def toggle(self, variable):
        return not variable
    
    def change_color(self, default=False, hovered=False, active=False, active_hovered=False):
        if active_hovered: # 200
            self.rect_color = (self.color[0]/1.275, self.color[1]/1.275, self.color[2]/1.275)
        elif active: # 150  
            self.rect_color = (self.color[0]/1.7, self.color[1]/1.7, self.color[2]/1.7)
        elif hovered: # 75
            self.rect_color = (self.color[0]/3.4, self.color[1]/3.4, self.color[2]/3.4)
        elif default:
            self.rect_color = (30,30,30)

    def update(self, mouse_pos, variable):
        if self.is_hovered(mouse_pos) and variable:
            self.change_color(active_hovered=True)
        elif variable:
            self.change_color(active=True)
        elif self.is_hovered(mouse_pos):
            self.change_color(hovered=True)
        else:
            self.change_color(default=True)
        

        # print(default, hovered, active, active_hovered)
    # def associate_value(self):
    #     return self.variable
    # def mouse_pressed(self, mouse_pos, pressed):
    #     return True if pressed else False

    # def update(self, screen:pygame.Surface, text_anti_alias, text, activate, variable=None, lambda_func=None):
    #     self.text = self.font.render(text, text_anti_alias, 'white')
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if button_hovered:
        #             self.button_clicked = not self.button_clicked

        # keys = pygame.key.get_pressed()
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_press = pygame.mouse.get_pressed()
        # key_press = pygame.key.get_pressed()
        # button_hovered = self.rect.collidepoint(mouse_pos)
        # for event in event_handler:

        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if button_hovered:
        #             self.button_clicked = not self.button_clicked
                # self.done_clicking = True

        # self.rect_color = (self.color[0]/3.4, self.color[1]/3.4, self.color[2]/3.4) if button_hovered else (30,30,30)
        # if self.button_clicked:
        #     self.rect_color = (self.color[0]/1.7, self.color[1]/1.7, self.color[2]/1.7)
        # if self.button_clicked and self.button_hovered:
        #     self.rect_color = (self.color[0]/1.275, self.color[1]/1.275, self.color[2]/1.275)

        # pygame.draw.rect(screen, self.rect_color, self.rect)

        # print(self.button_clicked)

        # rect_color = None
        # if button_hovered :
        #     rect_color = (self.color[0]/3.4, self.color[1]/3.4, self.color[2]/3.4) if button_hovered else (30,30,30)

        #     pygame.draw.rect(screen, rect_color, self.rect)


    