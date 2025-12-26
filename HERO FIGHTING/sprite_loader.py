import pygame


class SpriteSheet:
    def __init__(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0):
        """
        Handles loading and slicing spritesheets into individual frames for animation.

        Args:
            filepath (str): Path to the spritesheet image.
            frame_width (int): Width of each frame in the spritesheet.
            frame_height (int): Height of each frame in the spritesheet.
            rows (int): Number of rows in the spritesheet.
            columns (int): Number of columns in the spritesheet.
            scale (float): Scale factor for resizing the frames (default=1).
            rotation (float): Rotation angle in degrees for the frames (default=0).
        """
        self.spritesheet = pygame.image.load(filepath).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rows = rows
        self.columns = columns
        self.scale = scale
        self.rotation = rotation
        self.frames = self._slice_spritesheet()

    def _slice_spritesheet(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.spritesheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frame = pygame.transform.rotozoom(frame, self.rotation, self.scale)
                frames.append(frame)
        return frames

    def get_frames(self):
        """Returns the sliced frames of the spritesheet."""
        return self.frames

class SpriteSheet_Flipped:
    def __init__(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0):
        """
        Handles loading and slicing spritesheets into individual frames for animation.

        Args:
            filepath (str): Path to the spritesheet image.
            frame_width (int): Width of each frame in the spritesheet.
            frame_height (int): Height of each frame in the spritesheet.
            rows (int): Number of rows in the spritesheet.
            columns (int): Number of columns in the spritesheet.
            scale (float): Scale factor for resizing the frames (default=1).
            rotation (float): Rotation angle in degrees for the frames (default=0).
        """
        self.spritesheet = pygame.image.load(filepath).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.rows = rows
        self.columns = columns
        self.scale = scale
        self.rotation = rotation
        self.frames = self._slice_spritesheet()

    def _slice_spritesheet(self):
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.spritesheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frame = pygame.transform.flip(pygame.transform.rotozoom(frame, self.rotation, self.scale), True, False)
                frames.append(frame)
        return frames

    def get_frames(self):
        """Returns the sliced frames of the spritesheet."""
        return self.frames



def load_attack(filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0, frame_duration=30):
    """
    Utility function to load an attack animation from a spritesheet.

    Args:
        filepath (str): Path to the spritesheet image.
        frame_width (int): Width of each frame in the spritesheet.
        frame_height (int): Height of each frame in the spritesheet.
        rows (int): Number of rows in the spritesheet.
        columns (int): Number of columns in the spritesheet.
        scale (float): Scale factor for resizing the frames.
        rotation (float): Rotation angle in degrees for the frames.
        frame_duration (int): Duration of each frame in milliseconds.

    Returns:
        AnimatedAttack: An instance of the AnimatedAttack class.
    """
    spritesheet = pygame.image.load(filepath).convert_alpha()



    spritesheet_width = spritesheet.get_width()
    spritesheet_height = spritesheet.get_height()

    # Debugging: Print the spritesheet dimensions and frame dimensions
    # print(f"Spritesheet size: {spritesheet_width}x{spritesheet_height}")
    calculated_frame_width = spritesheet_width // columns
    calculated_frame_height = spritesheet_height // rows
    # print(f"Calculated frame size: {calculated_frame_width}x{calculated_frame_height}")

    # Check if the provided frame dimensions match the calculated ones
    if frame_width != calculated_frame_width or frame_height != calculated_frame_height:
        # print(
        #     f"Warning: Provided frame dimensions ({frame_width}x{frame_height}) "
        #     f"do not match calculated dimensions ({calculated_frame_width}x{calculated_frame_height})."
        # )
        frame_width = calculated_frame_width
        frame_height = calculated_frame_height


    spritesheet = SpriteSheet(filepath, frame_width, frame_height, rows, columns, scale, rotation)
    frames = spritesheet.get_frames()
    return frames


def load_attack_flipped(filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0, frame_duration=100):
    """
    Utility function to load an attack animation from a spritesheet.

    Args:
        filepath (str): Path to the spritesheet image.
        frame_width (int): Width of each frame in the spritesheet.
        frame_height (int): Height of each frame in the spritesheet.
        rows (int): Number of rows in the spritesheet.
        columns (int): Number of columns in the spritesheet.
        scale (float): Scale factor for resizing the frames.
        rotation (float): Rotation angle in degrees for the frames.
        frame_duration (int): Duration of each frame in milliseconds.

    Returns:
        AnimatedAttack: An instance of the AnimatedAttack class.
    """
    spritesheet = pygame.image.load(filepath).convert_alpha()



    spritesheet_width = spritesheet.get_width()
    spritesheet_height = spritesheet.get_height()

    # Debugging: Print the spritesheet dimensions and frame dimensions
    # print(f"Spritesheet size: {spritesheet_width}x{spritesheet_height}")
    calculated_frame_width = spritesheet_width // columns
    calculated_frame_height = spritesheet_height // rows
    # print(f"Calculated frame size: {calculated_frame_width}x{calculated_frame_height}")

    # Check if the provided frame dimensions match the calculated ones
    if frame_width != calculated_frame_width or frame_height != calculated_frame_height:
        # print(
        #     f"Warning: Provided frame dimensions ({frame_width}x{frame_height}) "
        #     f"do not match calculated dimensions ({calculated_frame_width}x{calculated_frame_height})."
        # )
        frame_width = calculated_frame_width
        frame_height = calculated_frame_height


    spritesheet = SpriteSheet_Flipped(filepath, frame_width, frame_height, rows, columns, scale, rotation)
    frames = spritesheet.get_frames()
    return frames
