import pygame
from global_vars import (
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LOW_HP, LITERAL_HEALTH_DEAD,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    attack_display, MULT, dmg_mult
)
from button import ImageButton
class PlayerSelector:
    def __init__(self, image, rect, player_instance, size=(75,75)):
        self.image = image
        self.rect = rect
        self.player_instance = player_instance

        self.profile = pygame.transform.scale(pygame.image.load(image).convert_alpha(), size)
        self.profile_rect = self.profile.get_rect(center = self.rect)

        self.decor_rect = pygame.Rect(self.profile_rect.centerx - 42, self.profile_rect.centery - 42, 85, 85)
        
        self.hovered = False
        self.selected = False
        self.locked = False

        self.back = ImageButton(
            image_path=text_box_img,
            pos=(self.profile_rect.centerx, self.profile_rect.top - 25),
            scale=0.5,
            text='Deselect',
            font_path=r'HERO FIGHTING\assets\font\slkscr.ttf',  # or any other font path
            font_size=font_size * 0.6,  # dynamic size ~29 at 720p
            text_color='white'
        )



    def draw(self):
        if self.selected:
            self.decor = pygame.draw.rect(screen, gold, self.decor_rect)

        elif self.hovered:
            self.decor = pygame.draw.rect(screen, white, self.decor_rect)
        
        else:
            self.decor = pygame.draw.rect(screen, black, self.decor_rect)

        screen.blit(self.profile, self.profile_rect)

    def draw_icon(self, rect):
        profile_rect = self.profile.get_rect(center = rect)
        decor_rect = pygame.Rect(profile_rect.centerx - 42, profile_rect.centery - 42, 85, 85)
        pygame.draw.rect(screen, black, decor_rect)
        screen.blit(self.profile, profile_rect)


    def is_selected(self):
        return self.selected
    
    def associate_value(self):
        return self.player_instance

    def update(self, mouse_pos, mouse_press, other_selectors):
        self.draw()
        if not self.selected:
            if self.decor_rect.collidepoint(mouse_pos):
                self.hovered = True
                if mouse_press[0]:
                    for selector in other_selectors:
                        selector.selected = False  # unselect others
                    self.selected = True 
            else:
                self.hovered = False
        else:
            self.back.draw(screen, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back.is_clicked(event.pos):
                        self.selected = False