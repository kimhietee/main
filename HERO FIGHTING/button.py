import pygame
from global_vars import get_font, screen, width, height, white, TEXT_ANTI_ALIASING
import math
import time
import global_vars

def draw_black_screen(opacity, color=(0,0,0), size=(0, 0, width, height)):
    base_opacity = 255 * opacity
    rect = pygame.Rect(pygame.Rect(size[0], size[1], size[2], size[3]))
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Fill it with the color + alpha
    overlay.fill((color[0],color[1],color[2], base_opacity))

    # Blit it on the target surface
    screen.blit(overlay, rect.topleft)

def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0, x_offset=width):
    title = pygame.transform.rotozoom(font.render(f'{text}', TEXT_ANTI_ALIASING, color), angle, scale)
    title_rect = title.get_rect(center = (x_offset / 2, y_offset))

    screen.blit(title, title_rect)


class ImageButton:
    def __init__(self, image_path, pos, scale, text, font_path, font_size, text_color, move_y=0, hover_move=2, fku=False, scale_val=(0,0), alpha=(1,1), text_anti_alias=True, y_margin=0):
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
        self.height_from_B = self.rect[3]
        self.text_anti_alias = text_anti_alias
    
        
        
        
        
        # Text
        self.text = text 
        self.font = get_font(int(font_size*7.142857142857143), font_path) # Font size = 100
        self.text_color = text_color

        text_surf = self.font.render(self.text, self.text_anti_alias, self.text_color)
        text_surf.set_alpha(int(self.alpha[1] * 255))

        self.text_surf = pygame.transform.rotozoom(text_surf, 0, 0.2)
        # self.text_surf = text_surf
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.y_margin =  y_margin
        
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
        dy = center[1] - self.rect.centery - self.y_margin

        #----------


        self.rect.move_ip(dx, dy)
        self.hover_pos = (center[0], center[1] + self.y_margin)
        # self.text_rect.move_ip(dx, dy)
        #----------

        
        # print(dx, dy)

        self.rect.center = center

        self.hover_pos = (center)
        # self.hover_pos[1] += dy

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



# class Button:
#     def __init__(self, image_path:str, position:tuple[int, int], image_size:int, text:str, font_path:str, text_size:int, text_color:str):
#         self.image = pygame.transform.rotozoom(pygame.image.load(image_path).convert_alpha(), 0, image_size)
#         self.image_rect = self.image.get_rect(center = position)
        
#         font_size = int(text_size*7.142857142857143)
        
#         self.font = get_font(font_size, font_path)

#         # not scaled (font already scaled)
#         text_surf = self.font.render(self.text, self.text_anti_alias, self.text_color)
#         text_scale = 0.2
#         # scaled again
#         self.text_surf = pygame.transform.rotozoom(text_surf, 0, text_scale)
    

    
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
        self.x = x
        self.y = y
        self.width = width
        self.height_from_B = height + height_position
        self.height = height

        self.button_clicked = False
        self.button_hovered = False

        self.done_clicking = False
        self.enabled = False
    

        

    def set_position(self, pos: tuple):
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1], self.width, self.height)



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
            # print(self.enabled)
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
                # self.do














import global_vars as g






class ModalObject:
    """
    Clickable selector for heroes, items, or maps with smooth movement on select.
    """
    # Default sizes
    PROFILE_SIZE = (75, 75)        # Heroes
    INGAME_SIZE = (50, 50)          # Items (your old size)
    DECOR_SIZE_LARGE = (85, 85)
    DECOR_OFFSET_LARGE = (42, 42)
    DECOR_SIZE_SMALL = (60, 60)
    DECOR_OFFSET_SMALL = (30,30)
    DECOR_SIZE_SMALLEST = (30, 30)

    DESELECT_Y_OFFSET = -45

    def __init__(self, center_pos, size:tuple=(120,120),  inputobject:list=[], buttons:list=[], button_gap = 0.2, button_bottom_gap = 0.2, Title = "", description = " ", opacity = 1):
        """
        Args:
            image: str path or Surface
            center_pos: (x, y) tuple
            class_item: Hero class or Item instance
            small: True for item-sized icons (50x50)
            custom_size: (w, h) tuple for maps/other special sizes (overrides small)
            custom_border: (w, h) if custom_size is used. (for decor)
        """
        # self.class_item = class_item

        # if isinstance(image, str):
        #     original = pygame.image.load(image).convert_alpha()
        # else:
        # original = (100, 900)

        # Determine size
        self.opacity = opacity
        self.size = size
        profile_size = size
        # decor_size = [size[0], size[1]]
        decor_offset = [12, 12]
        self.description = description
        # self.profile = pygame.transform.scale(original, profile_size)
        # self.ingame_profile = pygame.transform.scale(original, (25, 25))  # always keep small version

    # Create profile rectangle (no image)
        self.profile_rect = pygame.Rect(*center_pos, *profile_size)
        self.profile_rect.center = center_pos

        # Create decor rectangle relative to profile
        self.decor_rect = pygame.Rect(
            self.profile_rect.centerx - decor_offset[0],
            self.profile_rect.centery - decor_offset[1],
            *size
            )

        self.button_gap = button_gap
        self.button_bottom_gap = size[1] * button_bottom_gap
        self.hovered = False

        # Initialize position tracking BEFORE using them
        self.original_pos = center_pos
        self.target_pos = center_pos
        self.move_speed = 0.1
        self.is_open = False
        self.selected = False

        self.disable_action = False
        # print(self.original_pos)
        self.highlight_offset = (0, -50)  # Move right 10, up 20 when selected
        if len(buttons) > 1:
            self.button1 = buttons[0]
            self.button2 = buttons[1]
            
        self.inputobject = inputobject


        self.shake_count = 0
        self.shake_dir = False
        self.title = Title

    def open_modal(self):
        """Move modal to center with animation"""
        self.is_open = True
        self.selected = True
        self.move_speed = 0.04  # smooth entry
        self.set_position((width // 2, height // 2), instant=False)


    def close_modal(self):
        """Return modal to original position"""
        self.is_open = False
        self.selected = False
        self.move_speed = 0.04  # smooth exit
        self.set_position(self.original_pos, instant=False)

    def shake_enable(self):
        gap = 0.1 if self.shake_dir else -0.1
        self.target_pos = (self.target_pos[0] * (1 + gap), self.target_pos[1])
        self.shake_dir = not self.shake_dir
        # print(gap)
        # print(self.target_pos)


    def shake(self, times):
        self.move_speed = 0.5
        # print('waw')
        self.shake_count = times
        self.shake_enable()
    
    def set_position(self, new_center, instant=False, selectedval:bool = False):
        """
        Move the selector to a new center position.

        Args:
            new_center (tuple): New (x, y) center.
            instant (bool): If True, snap immediately (bypass lerp).
        """
        self.selected = selectedval
        if instant:
            self.target_pos = new_center
            self._apply_position(new_center)
        else:
            self.target_pos = new_center

    def _apply_position(self, center):
        # print(center)
        
        """Internal: Sync all rects to given center."""
        dx = center[0] - self.profile_rect.centerx
        dy = center[1] - self.profile_rect.centery
        # print(dx, dy)

        self.profile_rect.center = center
        self.decor_rect.move_ip(dx, dy)
        
        # Calculate button gap width and position
        button_gap_width = self.size[0] * self.button_gap / 2
        button_y = center[1] + self.size[1]/2 - self.button_bottom_gap
        
        self.button1.set_position((center[0] * (1-(self.button_gap/2)), (center[1] + self.size[1]/2 - self.button1.height_from_B) - self.button_bottom_gap))
        self.button2.set_position((center[0] * (1+(self.button_gap/2)), (center[1] + self.size[1]/2 - self.button1.height_from_B) - self.button_bottom_gap))
        
        # Position input fields vertically around center
        input_y_offset = -30 if len(self.inputobject) > 0 else 0
        for num, i in enumerate(self.inputobject):
                i.set_position((center[0], center[1] + input_y_offset + 80 * num))
  
    def update(self, mouse_pos, mouse_pressed, other_selectors, max_selected=g.MAX_ITEM):
        # Smooth movement toward target
        

        if self.profile_rect.center != self.target_pos:
            

            current = [float(self.profile_rect.centerx), float(self.profile_rect.centery)]
            dx = self.target_pos[0] - current[0]
            dy = self.target_pos[1] - current[1]

            # If very close, snap exactly to avoid drift
            if abs(dx) <= 2 and abs(dy) <= 2:
                # print("Snapped")
                self.disable_action = self.selected
                self._apply_position(self.target_pos)
                if self.shake_count:
                    self.shake_count -= 1
                    self.shake_enable()

                # self.enable_movement()
            else:
                # Normal smooth movement
                # print(dx, dy)
                if abs(dx) > 10:
                    
                    current[0] += (dx * self.move_speed)
                else:
                    current[0] += (dx * 0.3)
                if abs(dy) > 10:
                    
                    current[1] += (dy * self.move_speed)
                else:
                    current[1] += (dy * 0.3)
                
                self._apply_position((round(current[0]), round(current[1])))
        
        # Draw base
        self.draw()

        # Draw input fields
        for i in self.inputobject:
                i.draw(screen, g.TEXT_ANTI_ALIASING)
        
        # Draw buttons
        self.button1.draw(g.screen, mouse_pos)
        self.button2.draw(g.screen, mouse_pos)
        
        # Draw title and description
        create_title(self.title, g.get_font(60) , 1, self.profile_rect.centery - (height * 0.2), angle=0, x_offset= self.profile_rect.centerx * 2)
        create_title(self.description, g.get_font(60) , 0.8, self.profile_rect.centery, angle=0, x_offset= self.profile_rect.centerx * 2)

            
        if mouse_pressed[0] and self.button1.is_clicked(mouse_pos):
                # Close modal - animate back to original position
                self.is_open = False
                self.selected = False
                self.move_speed = 0.04
                self.target_pos = self.original_pos
        if mouse_pressed[0] and self.button2.is_clicked(mouse_pos):
                self.move_back_variable = True
                self.can_move_back = False
                # print(self.can_move_back)
                # self.set_position(self.original_pos)
                self.selected = False
                # self.close_modal()

                # print(self.target_pos)
                pass
    






    def draw(self):
        """Draw border and profile image based on state."""
        color = g.gold if self.selected else g.white if self.hovered else g.black
        # pygame.draw.rect(g.screen, color, self.decor_rect)
        # g.screen.blit(self.profile_rect, self.profile_rect)
        # pygame.draw.rect(g.screen, (0, 0, 0, 0), self.profile_rect)
        # draw_black_screen(0.2,size=(width*0.05, height * 0.2, width*0.44, height*0.65))
        overlay = pygame.Surface(self.profile_rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 255 * self.opacity))  # RGBA (alpha = 120)

        g.screen.blit(overlay, self.profile_rect.topleft)

        
    def draw_icon(self, center_pos, small=False, hero_sp=False):
        """
        Draw small or large icon with black border (used in-game).
        
        Args:
            center_pos (tuple): Center position for the icon.
            small (bool): If True, use ingame size (25x25).
        """
        profile = self.ingame_profile if small else self.profile
        size = self.INGAME_SIZE if small else self.PROFILE_SIZE
        offset = self.DECOR_OFFSET_SMALL if small else self.DECOR_OFFSET_LARGE
        border = self.DECOR_SIZE_SMALL if small else self.DECOR_SIZE_LARGE
        if small == 'smallest':
            offset = (15, 15)
            border = self.DECOR_SIZE_SMALLEST

        if hero_sp:
            color = g.gold
        elif hero_sp == 'item':
            color = g.cyan2
        else:
            color = g.black

        rect = profile.get_rect(center=center_pos)
        decor = pygame.Rect(rect.centerx - offset[0], rect.centery - offset[1], border[0], border[1])
        pygame.draw.rect(g.screen, color, decor)
        g.screen.blit(profile, rect)

        # Display cooldown if applicable
        if hasattr(self.class_item, 'cooldown') and self.class_item.cooldown > 0 and not g.PAUSED:
            current_time = pygame.time.get_ticks() / 1000 - g.PAUSED_TOTAL_DURATION / 1000
            remaining = self.class_item.cooldown - (current_time - self.class_item.last_used)
            if remaining > 0:
                font = g.get_font(15)
                text = font.render(f"{math.ceil(remaining)}", True, g.red)
                g.screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))
            else:
                font = g.get_font(15)
                text = font.render("ready", True, g.green)
                g.screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))

    
    
    def is_selected(self):
        return self.selected

    def get_associated(self):
        """Return the associated hero class or item."""
        return self.class_item

    # def show_hover_tooltip(self, position):
    #     """Display hero info tooltip on hover (if applicable)."""
    #     if (self.hovered and
    #         isinstance(self.class_item, type) and
    #         issubclass(self.class_item, g.Player)):
    #         hero_name = self.class_item.__name__.replace("_", " ")
    #         if hero_name in g.HERO_INFO:
                # info_bubble = ImageBro(
                #     image_path=text_box_img,
                #     pos=position,
                #     scale=2,
                #     text=f"{hero_name}, {HERO_INFO[hero_name]}",
                #     font_path=global_vars.FONT_PATH,
                #     font_size=font_size * 1.05,
                #     text_color='white',
                #     fku=True,
                #     scale_val=(150, 230),
                #     hover_move=0,
                #     player_info=True
                # )
                # info_bubble = ImageBro(
                #     image_path=g.text_box_img,
                #     pos=position,
                #     text=f"{hero_name}, {HERO_INFO[hero_name]}",
                #     font_path=g.FONT_PATH,
                #     font_size=g.font_size * 1.05,
                #     text_color='white',
                #     player_info=True,
                #     text_scale=1.3,  # Full size
                #     anchor='bottomright'
                # )
                # info_bubble.drawing_info(g.screen)






# forest_ranger_basic_skill = DisplaySkillInfo(
#     image_path=text_box_img,
#     pos=mouse_pos,  # Will be updated based on skill icon position
#     skill_name=self.skill_name,
#     skill_icon_path=self.skill_img,
#     stats=self.skill_stats,
#     info_text=self.skill_desc,
#     font_path=global_vars.FONT_PATH,
#     font_size=12,
#     anchor='midbottom'
# )







class DisplaySkillInfo:
    """
    Enhanced skill info display with icon, name, stats, and description.
    Shows custom formatted information when hovering over skill icons in game.

    Args:
        image_path: Path to background image
        pos: (x, y) position tuple
        skill_name: Name of the skill (displayed in larger font)
        skill_icon_path: Optional path to skill icon (displayed 75% smaller)
        stats: Optional dict of {stat_name: (value, color)} for stats display
               Colors: 'red', 'white', 'cyan', 'green' (default: 'red')
        info_text: Optional info description text with @ as manual line breaker
        font_path: Path to font file
        font_size: Base font size
        text_color: Default text color (default: 'white')
        padding: (pad_x, pad_y) tuple (default: (20, 20))
        min_size: Minimum (width, height) (default: (150, 100))
        anchor: Position anchor like 'topleft', 'topright' (default: 'topleft')
        fixed_size: Optional (width, height) for manual sizing
        text_scale: Font size multiplier (default: 1.0)
    """
    
    # Color palette
    COLOR_MAP = {
        'red': (220, 50, 50), # damage
        'white': (205, 205, 205), # neutral
        'cyan': (0, 255, 255), # mana 
        'green': (100, 200, 100), #heal
        'blueviolet': (138,43,226), # level 1
        'magenta': (255,0,255), # level 2   
        'orange': (255,165,0), # level 3
        'maize': (251,236,93), # mana refund
        'ruby': (224, 17, 95), # level 4
    }
    
    def __init__(self, image_path, pos, skill_name, font_path=None, font_size=16, 
                 skill_icon_path=None, stats=None, info_text=None,
                 text_color='white', padding=(20, 20), min_size=(150, 100), 
                 anchor='topleft', fixed_size=None, text_scale=1.0, columns=1):
        """
        Initialize enhanced skill info display.
        """
        self.original_bg = pygame.image.load(image_path).convert_alpha()
        self.padding = padding
        self.anchor = anchor
        self.pos = pos
        self.columns = max(1, columns)  # Ensure at least 1 column
        
        # Font setup (title larger, base default, stats smaller)
        self.base_font_size = int(font_size * text_scale)
        self.font = global_vars.get_font(self.base_font_size, font_path) if font_path else global_vars.get_font(self.base_font_size)
        self.font_large = global_vars.get_font(int(self.base_font_size * 1.4), font_path) if font_path else global_vars.get_font(int(self.base_font_size * 1.5))
        self.font_small = global_vars.get_font(int(self.base_font_size * 0.92), font_path) if font_path else global_vars.get_font(int(self.base_font_size * 0.9))
        self.text_color = self._parse_color(text_color)
        
        # Load and process skill icon
        self.skill_icon = None
        self.icon_scaled = None
        if skill_icon_path:
            try:
                if isinstance(skill_icon_path, pygame.Surface):
                    self.skill_icon = skill_icon_path
                else:
                    self.skill_icon = pygame.image.load(skill_icon_path).convert_alpha()
                # Scale icon to 75% of original size
                # icon_size = int(self.skill_icon.get_width() * 0.75), int(self.skill_icon.get_height() * 0.75)
                icon_size = 75, 75
                self.icon_scaled = pygame.transform.smoothscale(self.skill_icon, icon_size)
            except Exception as exc:
                print('DisplaySkillInfo icon load error:', exc)
                self.skill_icon = None
                self.icon_scaled = None

        # Title + icon row
        self.title_surface = self.font_large.render(skill_name if skill_name else "", global_vars.TEXT_ANTI_ALIASING, self.text_color) if skill_name else None
        self.max_content_width = 0
        self.total_content_height = 0

        icon_w, icon_h = (0, 0)
        if self.icon_scaled:
            icon_w, icon_h = self.icon_scaled.get_size()

        title_w = self.title_surface.get_width() if self.title_surface else 0
        title_h = self.title_surface.get_height() if self.title_surface else 0

        self.first_row_height = max(icon_h, title_h)
        self.first_row_width = (icon_w + 10 + title_w) if self.icon_scaled and self.title_surface else max(icon_w, title_w)

        self.max_content_width = self.first_row_width
        self.total_content_height = self.first_row_height

        # Stats list (organized by columns)
        self.stat_surfaces = []
        self.stat_columns = []  # List of columns, each column is a list of stat rows
        
        if stats and isinstance(stats, dict):
            # Create stat surfaces
            all_stats = []
            for stat_name, stat_data in stats.items():
                if isinstance(stat_data, tuple) or isinstance(stat_data, list):
                    stat_value, stat_color = stat_data
                else:
                    stat_value = stat_data
                    stat_color = 'red'

                color = self._parse_color(stat_color)
                stat_name_surf = self.font_small.render(f"{stat_name}: ", global_vars.TEXT_ANTI_ALIASING, self.text_color)
                stat_value_surf = self.font_small.render(str(stat_value), global_vars.TEXT_ANTI_ALIASING, color)
                all_stats.append((stat_name_surf, stat_value_surf))
            
            # Distribute stats into columns
            if self.columns > 1:
                stats_per_col = (len(all_stats) + self.columns - 1) // self.columns
                for col_idx in range(self.columns):
                    start_idx = col_idx * stats_per_col
                    end_idx = start_idx + stats_per_col
                    self.stat_columns.append(all_stats[start_idx:end_idx])
            else:
                self.stat_columns = [all_stats]
            
            self.stat_surfaces = all_stats
            
            # Calculate dimensions for multi-column layout
            col_widths = []
            col_heights = []
            for col in self.stat_columns:
                col_width = 0
                col_height = 0
                for stat_name_surf, stat_value_surf in col:
                    row_width = stat_name_surf.get_width() + stat_value_surf.get_width()
                    col_width = max(col_width, row_width)
                    col_height += stat_name_surf.get_height() + 3
                col_widths.append(col_width)
                col_heights.append(col_height if col_height > 0 else 0)
            
            # Total width is sum of column widths (with spacing between columns)
            if col_widths:
                col_spacing = 20
                self.max_content_width = max(self.max_content_width, sum(col_widths) + (len(col_widths) - 1) * col_spacing)
                # Total height is the max height among columns
                self.total_content_height += max(col_heights) if col_heights else 0

        # Info text
        self.info_lines = []
        if info_text and isinstance(info_text, str):
            info_lines = [line.strip() for line in info_text.split('@') if line.strip()]
            for line in info_lines:
                info_surf = self.font.render(line, global_vars.TEXT_ANTI_ALIASING, self.text_color)
                self.info_lines.append(info_surf)
                self.max_content_width = max(self.max_content_width, info_surf.get_width())
                self.total_content_height += info_surf.get_height() + 5

        # gap between sections
        if self.stat_surfaces and self.info_lines:
            self.total_content_height += 2
        
        # Calculate background size
        if fixed_size:
            final_w, final_h = fixed_size
        else:
            needed_w = self.max_content_width + padding[0] * 2
            needed_h = self.total_content_height + padding[1] * 2

            final_w = max(needed_w, min_size[0])
            final_h = max(needed_h, min_size[1])

        self.background = pygame.transform.smoothscale(self.original_bg, (int(final_w), int(final_h*1.09)))

        # Position
        self.rect = self.background.get_rect()
        setattr(self.rect, anchor, pos)
        self.rect.clamp_ip(screen.get_rect())
    
    def _parse_color(self, color):
        """Convert color name or tuple to RGB tuple."""
        if isinstance(color, str):
            return self.COLOR_MAP.get(color.lower(), (255, 255, 255))
        return color
    
    def drawing_info(self, screen):
        """Draw the skill info box with icon + title row, then stats/info below."""
        screen.blit(self.background, self.rect)

        y = self.rect.top + self.padding[1]
        x_base = self.rect.left + self.padding[0]

        # 1) First row: icon + title
        x = x_base
        if self.icon_scaled:
            icon_y = y + (self.first_row_height - self.icon_scaled.get_height()) // 2
            screen.blit(self.icon_scaled, (x, icon_y))
            x += self.icon_scaled.get_width() + 10

        if self.title_surface:
            title_y = y + (self.first_row_height - self.title_surface.get_height()) // 2
            screen.blit(self.title_surface, (x, title_y))

        y += self.first_row_height

        # 2) Stats lines below (multi-column layout)
        if self.stat_columns:
            y += 10
            col_x_positions = []
            current_x = x_base
            col_spacing = 20
            
            # Calculate column positions based on widths
            for col_idx, col in enumerate(self.stat_columns):
                col_x_positions.append(current_x)
                col_width = 0
                for stat_name_surf, stat_value_surf in col:
                    row_width = stat_name_surf.get_width() + stat_value_surf.get_width()
                    col_width = max(col_width, row_width)
                current_x += col_width + col_spacing
            
            # Draw each column
            max_col_height = 0
            for col_idx, col in enumerate(self.stat_columns):
                col_y = y
                for stat_name_surf, stat_value_surf in col:
                    screen.blit(stat_name_surf, (col_x_positions[col_idx], col_y))
                    screen.blit(stat_value_surf, (col_x_positions[col_idx] + stat_name_surf.get_width(), col_y))
                    col_y += stat_name_surf.get_height() + 3
                max_col_height = max(max_col_height, col_y - y)
            
            y += max_col_height

        # 3) Info text lines below
        if self.info_lines:
            y += 10
            for info_surf in self.info_lines:
                screen.blit(info_surf, (x_base, y))
                y += info_surf.get_height() + 5


# ============================================================================
# USAGE EXAMPLES FOR DisplaySkillInfo
# ============================================================================
"""
EXAMPLE 1: Basic skill info with icon, name, and stats
---------------------------------------------------
# Create skill info display with defaults
skill_info = DisplaySkillInfo(
    image_path='assets/text_box.png',
    pos=(400, 300),
    skill_name='Fireball',
    skill_icon_path='assets/skill_icons/fireball.png',
    stats={
        'Damage': (50, 'red'),
        'Cooldown': ('3s', 'white'),
        'Mana': (20, 'cyan')
    },
    info_text='A powerful fire spell @ that damages enemies @ in a small area',
    font_path='assets/fonts/myfont.ttf',
    font_size=12
)

# Draw when hovering
skill_info.drawing_info(screen)


EXAMPLE 2: Custom colors for stats
-----------------------------------
# Available colors: 'red', 'white', 'cyan', 'green'
skill_info = DisplaySkillInfo(
    image_path='assets/text_box.png',
    pos=(400, 300),
    skill_name='Healing Light',
    skill_icon_path='assets/skill_icons/heal.png',
    stats={
        'Healing': (30, 'green'),      # Green for healing
        'Range': ('5m', 'white'),
        'Cast Time': ('2s', 'white'),
        'Cooldown': ('5s', 'red')      # Red for cooldown
    },
    info_text='Restore health to an ally @ Radius: 3 meters',
    font_path='assets/fonts/myfont.ttf',
    font_size=12
)


EXAMPLE 3: No icon, just name and stats
----------------------------------------
skill_info = DisplaySkillInfo(
    image_path='assets/text_box.png',
    pos=(400, 300),
    skill_name='Ice Spike',
    stats={
        'Damage': (35, 'cyan'),
        'Cost': (15, 'cyan')
    },
    info_text='Create a spike of ice @ that pierces through enemies',
    font_path='assets/fonts/myfont.ttf',
    font_size=12
)


EXAMPLE 4: Advanced example with all features
----------------------------------------------
skill_info = DisplaySkillInfo(
    image_path='assets/text_box.png',
    pos=(mouse_pos[0], mouse_pos[1] - 200),  # Follow mouse
    skill_name='Meteor Strike',
    skill_icon_path='assets/skill_icons/meteor.png',
    stats={
        'Damage': (100, 'red'),
        'AoE': ('8m', 'white'),
        'Cast': ('1.5s', 'white'),
        'Cost': (50, 'cyan'),
        'CD': ('10s', 'red')
    },
    info_text='Summon meteors from the sky @ Devastating area damage @ @ Line breaks can be added multiple times',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    padding=(25, 20),
    anchor='center'  # Center the tooltip at mouse position
)


KEY FEATURES:
=============
1. SKILL ICON (75% smaller):
   - Pass skill_icon_path to display skill icon
   - Icon is automatically scaled to 75% of original size
   - Centered horizontally in the info box

2. SKILL NAME (Larger Font):
   - Large font (130% of base size)
   - Displayed first in the info

3. STATS DICTIONARY:
   - Format: {'stat_name': (value, color)}
   - Colors: 'red', 'white', 'cyan', 'green'
   - Multiple stats can have different colors
   - Stats appear after name and icon
   - One space (10px) before stats section

4. INFO TEXT with @ Line Breaker:
   - Use @ to manually break lines
   - Example: 'This is line 1 @ This is line 2'
   - One space (10px) before info section

5. AUTOMATIC SIZING:
   - Automatically sizes based on content width
   - Use fixed_size=(width, height) to override
   - min_size parameter sets minimum dimensions

6. POSITIONING:
   - anchor options: 'topleft', 'topright', 'bottomleft', 'bottomright', 'center'
   - Position is automatically clamped to screen boundaries
   - Perfect for tooltips that follow mouse


COLOR OPTIONS REFERENCE:
=======================
- 'red':   (220, 50, 50)       # For damage, cooldowns, negatives
- 'white': (255, 255, 255)     # For neutral stats
- 'cyan':  (0, 255, 255)       # For mana, energy costs
- 'green': (100, 200, 100)     # For healing, buffs, positives
"""

# ============================================================================
# FOREST RANGER SKILL EXAMPLES (Sample Implementation)
# ============================================================================
"""
# These are example instances for Forest Ranger skill tooltips.
# Add these to your gameloop.py or wherever skill icons are displayed.

# SKILL 1: Piercing Shots (Basic Attack)
forest_ranger_basic_skill = DisplaySkillInfo(
    image_path='assets/UI/text_box_skill.png',
    pos=(0, 0),  # Will be updated based on skill icon position
    skill_name='Piercing Shots',
    skill_icon_path='assets/skill_icons/forest_ranger/basic_attack.png',
    stats={
        'Damage': (18, 'red'),
        'Attack Speed': ('6 frames', 'white'),
        'Range': ('Long', 'white')
    },
    info_text='Fire multiple arrows at enemies @ Arrows can stick and damage again @ High attack speed ranger attack',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    anchor='topleft'
)

# SKILL 2: Power Shot (ATK1)
forest_ranger_atk1_skill = DisplaySkillInfo(
    image_path='assets/UI/text_box_skill.png',
    pos=(0, 0),
    skill_name='Power Shot',
    skill_icon_path='assets/skill_icons/forest_ranger/power_shot.png',
    stats={
        'Damage': (12, 'red'),
        'Cooldown': ('4 frames', 'white'),
        'Type': ('Single Hit', 'white')
    },
    info_text='A powerful charged shot @ Deals moderate damage in a straight line',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    anchor='topleft'
)

# SKILL 3: Explosive Volley (ATK2)
forest_ranger_atk2_skill = DisplaySkillInfo(
    image_path='assets/UI/text_box_skill.png',
    pos=(0, 0),
    skill_name='Explosive Volley',
    skill_icon_path='assets/skill_icons/forest_ranger/explosive_volley.png',
    stats={
        'Damage': (35, 'red'),
        'Cooldown': ('40 frames', 'red'),
        'Area': ('Large', 'white'),
        'Cost': ('30 Mana', 'cyan')
    },
    info_text='Launch a barrage of explosive arrows @ Covers wide area with high damage @ Long cooldown but devastating impact',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    anchor='topleft'
)

# SKILL 4: Trueshot (ATK3)
forest_ranger_atk3_skill = DisplaySkillInfo(
    image_path='assets/UI/text_box_skill.png',
    pos=(0, 0),
    skill_name='Trueshot',
    skill_icon_path='assets/skill_icons/forest_ranger/trueshot.png',
    stats={
        'Damage': (28, 'red'),
        'Cooldown': ('10 frames', 'white'),
        'Critical': ('High', 'red'),
        'Cost': ('20 Mana', 'cyan')
    },
    info_text='A perfectly aimed shot that never misses @ High critical chance @ Excellent for finishing weak enemies',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    anchor='topleft'
)

# SKILL 5: Forest's Wrath (Special)
forest_ranger_special_skill = DisplaySkillInfo(
    image_path='assets/UI/text_box_skill.png',
    pos=(0, 0),
    skill_name=\"Forest's Wrath\",
    skill_icon_path='assets/skill_icons/forest_ranger/forest_wrath.png',
    stats={
        'Damage': (55, 'red'),
        'Duration': ('8 seconds', 'white'),
        'Cost': ('60 Special', 'cyan'),
        'Effect': ('AoE', 'green')
    },
    info_text='Summon the power of the ancient forest @ Rains arrows down on all enemies @ Scales with Intelligence and Mana',
    font_path='assets/fonts/myfont.ttf',
    font_size=12,
    anchor='topleft'
)


# USAGE IN GAMELOOP:
# ==================
# In your game loop, when hovering over Forest Ranger skills:
#
# if skill_icon_rect.collidepoint(mouse_pos):
#     # Update position to follow skill icon
#     forest_ranger_basic_skill.rect.topleft = (skill_icon_x - 200, skill_icon_y - 50)
#     forest_ranger_basic_skill.drawing_info(screen)
#
# Or for dynamic positioning:
#
# class SkillTooltip:
#     def __init__(self, skill_info, skill_icon_rect):
#         self.skill_info = skill_info
#         self.skill_icon_rect = skill_icon_rect
#     
#     def update_position(self, mouse_pos):
#         if self.skill_icon_rect.collidepoint(mouse_pos):
#             # Position tooltip relative to icon
#             pos = (self.skill_icon_rect.right + 10, self.skill_icon_rect.top - 10)
#             self.skill_info.rect.topleft = pos
#             self.skill_info.rect.clamp_ip(screen.get_rect())
#             return True
#         return False
#     
#     def draw(self, screen):
#         self.skill_info.drawing_info(screen)
"""
    