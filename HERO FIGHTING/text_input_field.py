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
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))
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

    # ── Public API ─────────────────────────────────────────────
    def get_text(self):
        return self.text

    def set_text(self, value):
        self.text = value[: self.max_chars]

    def clear(self):
        self.text = ""

    def set_position(self, x, y):
        self.rect.topleft = (int(x), int(y))

    def set_size(self, width, height):
        self.rect.size = (int(width), int(height))

    def _char_allowed(self, ch):
        if not ch or not ch.isprintable():
            return False
        if self.allowed_chars is not None:
            return ch in self.allowed_chars
        return True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            self._caret_visible = True
            self._caret_timer = 0
            return None

        if not self.active or event.type != pygame.KEYDOWN:
            return None

        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return "submit"
        if event.key == pygame.K_ESCAPE:
            return "cancel"

        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            self._caret_visible = True
            self._caret_timer = 0
            return None

        ch = event.unicode
        if self._char_allowed(ch) and len(self.text) < self.max_chars:
            self.text += ch
            self._caret_visible = True
            self._caret_timer = 0

        return None

    def update(self, dt_ms):
        if not self.active:
            self._caret_visible = False
            return

        self._caret_timer += dt_ms
        if self._caret_timer >= self.caret_blink_ms:
            self._caret_timer %= self.caret_blink_ms
            self._caret_visible = not self._caret_visible

    def draw(self, surface, anti_alias=True):
        # Box
        pygame.draw.rect(surface, self.bg_color, self.rect)
        border = self.active_border_color if self.active else self.border_color
        if self.border_width > 0:
            pygame.draw.rect(surface, border, self.rect, self.border_width)

        # Text or placeholder
        if self.text:
            shown = self.text + ("|" if (self.active and self._caret_visible) else "")
            color = self.text_color
        elif self.active:
            shown = "|" if self._caret_visible else ""
            color = self.text_color
        else:
            shown = self.placeholder
            color = self.placeholder_color

        txt = self.font.render(shown, anti_alias, color)
        surface.blit(
            txt,
            txt.get_rect(midleft=(self.rect.x + self.padding_x, self.rect.centery)),
        )