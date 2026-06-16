"""Reusable, configurable text input field for pygame menus.

The goal of this module is a single, flexible widget you can drop in anywhere a
typed value is needed (room name, IP address, username, etc.) and restyle freely
(size, colors, font, char limit, allowed characters, placeholder) without
duplicating event/draw code.

Example
-------
    from text_input_field import TextInputField

    name_field = TextInputField(
        x=100, y=200, width=400, height=70,
        max_chars=16,
        placeholder="Enter room name",
    )

    # in your loop:
    for event in pygame.event.get():
        name_field.handle_event(event)
    name_field.update(dt_ms)            # advances the blinking caret
    name_field.draw(surface)
    value = name_field.get_text()

Nothing here depends on the rest of the game, so it stays import-light and easy
to reuse. It only needs pygame.
"""
import pygame



class TextInputField:
    """
    A reusable text input widget for Pygame.

    Features
    --------
    - Click to focus / unfocus
    - Keyboard typing with optional character filtering
    - Blinking caret (cursor)
    - Placeholder text when empty
    - Fully customizable styling

    Parameters
    ----------
    x, y : int
        Top-left position of the input field.

    width, height : int
        Size of the input field.

    font : pygame.font.Font, optional
        Preloaded font object. If provided, overrides `font_path`.

    font_path : str, optional
        Path to a font file.

    font_size : int, default=40
        Font size (used if `font` is not provided).

    text : str, default=""
        Initial text value.

    max_chars : int, default=20
        Maximum number of characters allowed.

    allowed_chars : iterable, optional
        Set or iterable of allowed characters.
        If None, all printable characters are allowed.

    placeholder : str, default=""
        Text shown when input is empty and inactive.

    text_color : tuple, default=(255, 255, 255)
        Color of the input text.

    placeholder_color : tuple, default=(130, 130, 130)
        Color of the placeholder text.

    bg_color : tuple, default=(25, 25, 25)
        Background color of the input box.

    border_color : tuple, default=(200, 200, 200)
        Border color when inactive.

    active_border_color : tuple, default=(255, 215, 0)
        Border color when active (focused).

    border_width : int, default=3
        Thickness of the border.

    padding_x : int, default=18
        Horizontal padding for text inside the box.

    caret_color : tuple, optional
        Color of the caret. Defaults to `text_color`.

    caret_blink_ms : int, default=500
        Time interval (in milliseconds) for caret blinking.

    active : bool, default=True
        Whether the input starts focused.
    """

    def __init__(
        self,
        x,
        y,
        width,
        height,
        *,
        font=None,
        font_path=None,
        font_size=40,
        text="",
        max_chars=20,
        allowed_chars=None,
        placeholder="",
        text_color=(255, 255, 255),
        placeholder_color=(130, 130, 130),
        bg_color=(25, 25, 25),
        border_color=(200, 200, 200),
        active_border_color=(255, 215, 0),
        border_width=3,
        padding_x=18,
        caret_color=None,
        caret_blink_ms=500,
        active=True,
    ):
        # Geometry
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))

        # Text behavior
        self.text = text
        self.max_chars = max_chars
        self.allowed_chars = set(allowed_chars) if allowed_chars is not None else None
        self.placeholder = placeholder

        # Styling
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.border_width = border_width
        self.padding_x = padding_x
        self.caret_color = caret_color if caret_color is not None else text_color
        self.caret_blink_ms = caret_blink_ms

        # State
        self.active = active
        self._caret_timer = 0
        self._caret_visible = True

        # Font
        if font is not None:
            self.font = font
        else:
            self.font = pygame.font.Font(font_path, int(font_size))

    # ─────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────

    def get_text(self):
        """Return the current text value."""
        return self.text

    def set_text(self, value):
        """
        Set the text value.

        Text is automatically truncated to `max_chars`.
        """
        self.text = value[: self.max_chars]

    def clear(self):
        """Clear all text."""
        self.text = ""

    def set_position(self, x, y):
        """Move the input field to a new position."""
        self.rect.topleft = (int(x), int(y))

    def set_size(self, width, height):
        """Resize the input field."""
        self.rect.size = (int(width), int(height))

    # ─────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────

    def _char_allowed(self, ch):
        """Check if a character is allowed."""
        if not ch or not ch.isprintable():
            return False
        if self.allowed_chars is not None:
            return ch in self.allowed_chars
        return True

    # ─────────────────────────────────────────────
    # Event handling
    # ─────────────────────────────────────────────

    def handle_event(self, event):
        """
        Handle Pygame events.

        Returns
        -------
        str or None
            "submit" → Enter pressed
            "cancel" → Escape pressed
            None     → otherwise
        """

        # Mouse click → focus/unfocus
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self._caret_visible = True
            self._caret_timer = 0
            return None

        # Ignore if not active or not a key press
        if not self.active or event.type != pygame.KEYDOWN:
            return None

        # Special keys
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return "submit"

        if event.key == pygame.K_ESCAPE:
            return "cancel"

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self._caret_visible = True
            self._caret_timer = 0
            return None

        # Character input
        ch = event.unicode
        if self._char_allowed(ch) and len(self.text) < self.max_chars:
            self.text += ch
            self._caret_visible = True
            self._caret_timer = 0

        return None

    # ─────────────────────────────────────────────
    # Update & Render
    # ─────────────────────────────────────────────

    def update(self, dt_ms):
        """
        Update internal state.

        Handles caret blinking.

        Parameters
        ----------
        dt_ms : int
            Time elapsed since last frame (in milliseconds).
        """
        if not self.active:
            self._caret_visible = False
            return

        self._caret_timer += dt_ms
        if self._caret_timer >= self.caret_blink_ms:
            self._caret_timer %= self.caret_blink_ms
            self._caret_visible = not self._caret_visible

    def draw(self, surface, anti_alias=True):
        """
        Draw the input field.

        Parameters
        ----------
        surface : pygame.Surface
            Surface to draw on.

        anti_alias : bool, default=True
            Whether to render text with anti-aliasing.
        """

        # Background
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Border
        border = self.active_border_color if self.active else self.border_color
        if self.border_width > 0:
            pygame.draw.rect(surface, border, self.rect, self.border_width)

        # Text / Placeholder / Caret
        if self.text:
            shown = self.text + ("|" if (self.active and self._caret_visible) else "")
            color = self.text_color
        elif self.active:
            shown = "|" if self._caret_visible else ""
            color = self.text_color
        else:
            shown = self.placeholder
            color = self.placeholder_color

        # Render text
        txt = self.font.render(shown, anti_alias, color)
        surface.blit(
            txt,
            txt.get_rect(midleft=(self.rect.x + self.padding_x, self.rect.centery)),
        )