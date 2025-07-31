import pygame
import random
import heroes as main
from pprint import pprint

bg_paths = [
    (r'assets\backgrounds\animated_bg\Ocean_2\2.png', 'static', 0, 'left'),
    (r'assets\backgrounds\animated_bg\Ocean_2\3.png', 'dynamic', 30, 'right'),
    (r'assets\backgrounds\animated_bg\Ocean_2\4.png', 'dynamic', 30, 'right')
]
# (r'assets\backgrounds\animated_bg\Ocean_2\compiled img.png', 'dynamic', 500, 'right')
class BackgroundHandler:
    def __init__(self, img_paths: list):
        self.layers = []
        for image in img_paths:
            try:
                img = pygame.transform.scale(
                    pygame.image.load(image[0]).convert_alpha(),
                    (main.width, main.DEFAULT_Y_POS + int(720 * 0.1))
                )
                self.layers.append({
                    'img': img,
                    'type': image[1],
                    'interval': image[2],       # how often to move (in ms)
                    'direction': image[3],      # 'left' or 'right'
                    'x': 0,
                    'last_move_time': pygame.time.get_ticks()  # initialize timer
                })
            except Exception as e:
                pprint(f"Error loading background image {image[0]}: {e}")

    def update(self):
        current_time = pygame.time.get_ticks()
        for layer in self.layers:
            if layer['type'] == 'dynamic':
                if current_time - layer['last_move_time'] >= layer['interval']:
                    if layer['direction'] == 'left':
                        layer['x'] -= 1
                        if layer['x'] <= -main.width:
                            layer['x'] = 0
                    elif layer['direction'] == 'right':
                        layer['x'] += 1
                        if layer['x'] >= main.width:
                            layer['x'] = 0
                    layer['last_move_time'] = current_time  # reset timer

    def draw(self, screen):
        for layer in self.layers:
            x = layer['x']
            img = layer['img']

            screen.blit(img, (x, 0))
            if layer['type'] == 'dynamic':
                if layer['direction'] == 'left':
                    screen.blit(img, (x + main.width, 0))
                elif layer['direction'] == 'right':
                    screen.blit(img, (x - main.width, 0))

    
# main background preferred size:
# (main.width, main.DEFAULT_Y_POS + int(720 * 0.1))

class AnimatedBackground:
    '''
    Make sure the name of frames starts at 1
    '''
    def __init__(self, path, count, size=(main.width, int(main.height * 0.798)), pos=(0,0)):  # 0.798 = 574 / 720):
        self.path = path if path.endswith(("\\", "/")) else path + "/"
        self.count = count
        self.size = size
        self.pos = pos
        self.frames = []
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()

    def load_frames(self, extension=".gif") -> pygame.Surface:
        self.frames.clear()
        for i in range(self.count):
            img_path = f"{self.path}{i+1}{extension}"
            image = pygame.transform.scale(
                pygame.image.load(img_path).convert(),
                self.size
            )
            image.set_alpha(50)
            self.frames.append(image)

    def display(self, surface, speed=150):
        """
        surface: pygame.Surface to blit to
        speed: milliseconds per frame
        """
        now = pygame.time.get_ticks()
        if now - self.last_update_time > speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = now

        surface.blit(self.frames[self.current_frame], (self.pos[0], self.pos[1]))


# background = main.pygame.transform.scale(
#     pygame.image.load(bg_list[random.randint(0, len(bg_list)-1)]).convert(), 
#     (main.width, main.DEFAULT_Y_POS + (720*1.1 - 720)))

waterfall_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall\\",
    8,
    # size=(main.width, main.height)
    # (main.width, int(main.height * 0.825)) # 594
)

lava_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Magma Chamber\\",
    8,
    size=(main.width, main.height)
    # (main.width, int(main.height * 0.825)) # 594
)

dark_forest_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Dark Forest\\",
    8,
    size=(main.width, main.height)
    # (main.width, int(main.height * 0.825)) # 594
)


dragon_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Dragon\\",
    35,
    size=(main.width, main.height-100),
    pos=(0,50)
    # (main.width, int(main.height * 0.825)) # 594
)






waterfall_day_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall - Day\\",
    7,
    size=(main.width, main.height)
    # (main.width, int(main.height * 0.825)) # 594
)




#Game Background
waterfall_bg.load_frames()
lava_bg.load_frames()
dark_forest_bg.load_frames()

# Main
dragon_bg.load_frames()



# UI
waterfall_day_bg.load_frames()