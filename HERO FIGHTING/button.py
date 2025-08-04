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
    def __init__(self, x:int, y:int, font:str, font_size:int, color:str, variable, width:int=40, height:int=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.variable = variable

        self.button_clicked = False
        self.button_hovered = False
    
    def associate_value(self):
        return self.variable

    def update(self, screen:pygame.Surface, mouse_press, mouse_pos, text_anti_alias, text, variable=None, lambda_func=None):
        self.text = self.font.render(text, text_anti_alias, 'white')
        button_hovered = self.rect.collidepoint(mouse_pos)
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if button_hovered:
        #             self.button_clicked = not self.button_clicked
        if mouse_press[0] == pygame.MOUSEBUTTONUP and button_hovered:
            self.button_clicked = not self.button_clicked

        rect_color = (self.color[0]/3.4, self.color[1]/3.4, self.color[2]/3.4) if button_hovered else (30,30,30)
        if self.button_clicked:
            rect_color = (self.color[0]/1.7, self.color[1]/1.7, self.color[2]/1.7)
        if self.button_clicked and self.button_hovered:
            rect_color = (self.color[0]/1.275, self.color[1]/1.275, self.color[2]/1.275)

        pygame.draw.rect(screen, rect_color, self.rect)
            
        print(self.button_clicked)



    