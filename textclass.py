# text_box.py
import pygame
import sys
from collections import deque

class TextBox:
    """
    A reusable Pygame text-input box with:
        - cursor
        - selection (Ctrl+A)
        - copy / cut / paste (Ctrl+C/X/V)
        - undo / redo (Ctrl+Z/Y)
        - word-delete (Ctrl+Backspace)
        - navigation (Home/End/Left/Right)
    """
    def __init__(self,
                 rect: pygame.Rect,
                 font: pygame.font.Font,
                 text_color=(0, 0, 0),
                 bg_color=(255, 255, 255),
                 active_color=(200, 200, 255),
                 inactive_color=(200, 200, 200),
                 max_history=50):
        """
        rect            – pygame.Rect(x, y, w, h) for the box
        font            – pygame.font.Font
        text_color      – color of the typed text
        bg_color        – background of the box when active
        active_color    – border color when focused
        inactive_color  – border color when not focused
        max_history     – how many undo steps to keep
        """
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.active_color = active_color
        self.inactive_color = inactive_color

        self._text = ""
        self._cursor_pos = 0                # index inside self._text
        self._selection_start = None        # None = no selection
        self._active = False

        # Undo / Redo
        self._history = deque(maxlen=max_history)
        self._history.append(("", 0))       # (text, cursor)
        self._redo_stack = deque(maxlen=max_history)

        # Clipboard (system)
        pygame.scrap.init()
        # pygame.scrap.set_mode(pygame.scrap.SCRAP_CLIPBOARD)

        # Pre-render cache
        self._rendered_text = None
        self._rendered_width = 0

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._set_text(value, len(value))

    def is_active(self) -> bool:
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False
        self._selection_start = None

    def clear(self):
        self._set_text("", 0)

    # ------------------------------------------------------------------ #
    # Core handling
    # ------------------------------------------------------------------ #
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Call this for every pygame event.
        Returns True if the event was consumed.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.activate()
                # set cursor by pixel position
                self._cursor_pos = self._pixel_to_index(event.pos[0] - self.rect.x - 5)
                self._selection_start = None
            else:
                self.deactivate()
            return True

        if not self._active:
            return False

        consumed = False
        if event.type == pygame.KEYDOWN:
            consumed = self._handle_keydown(event)
        elif event.type == pygame.TEXTINPUT:
            # pygame.TEXTINPUT gives already-processed unicode (handles dead-keys etc.)
            self._insert_text(event.text)
            consumed = True

        

        return consumed

    def update(self, event=None):
        """Call each frame – handles blinking cursor, auto-scroll, etc."""
        # Auto-scroll logic could be added here if the box is scrollable.
        # self.is_hovered(event)
        pass

    # def is_hovered(self, event):
    #     if hasattr(event,'pos'):
    #         print('collide')
    #         return self.rect.collidepoint(event.pos)

    def draw(self, surface: pygame.Surface):
        """Draw the box, text, cursor and selection."""
        # background
        bg = self.bg_color if self._active else self.inactive_color
        pygame.draw.rect(surface, bg, self.rect)

        # render text (cached)
        if self._rendered_text is None or self._rendered_width != self.rect.w:
            self._render_text()

        txt_surf = self._rendered_text
        txt_rect = txt_surf.get_rect()
        txt_rect.centery = self.rect.centery
        txt_rect.left = self.rect.x + 5
        surface.blit(txt_surf, txt_rect)

        # selection highlight
        if self._selection_start is not None:
            self._draw_selection(surface)

        # cursor (blink)
        if self._active and pygame.time.get_ticks() % 1000 < 500:
            self._draw_cursor(surface)

        # border
        border_color = self.active_color if self._active else self.inactive_color
        pygame.draw.rect(surface, border_color, self.rect, 2)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _set_text(self, new_text: str, cursor_pos: int):
        """Replace current text, push undo, reset redo."""
        self._history.append((self._text, self._cursor_pos))
        self._redo_stack.clear()
        self._text = new_text
        self._cursor_pos = max(0, min(cursor_pos, len(new_text)))
        self._selection_start = None
        self._rendered_text = None

    def _push_undo(self):
        self._history.append((self._text, self._cursor_pos))
        self._redo_stack.clear()

    def _insert_text(self, txt: str):
        self._push_undo()
        if self._selection_start is not None:
            a, b = sorted([self._selection_start, self._cursor_pos])
            self._text = self._text[:a] + txt + self._text[b:]
            self._cursor_pos = a + len(txt)
        else:
            self._text = (self._text[:self._cursor_pos] +
                          txt +
                          self._text[self._cursor_pos:])
            self._cursor_pos += len(txt)
        self._selection_start = None
        self._rendered_text = None

    def _delete_selection(self):
        if self._selection_start is None:
            return
        a, b = sorted([self._selection_start, self._cursor_pos])
        self._push_undo()
        self._text = self._text[:a] + self._text[b:]
        self._cursor_pos = a
        self._selection_start = None
        self._rendered_text = None

    def _handle_keydown(self, event) -> bool:
        mod = pygame.key.get_mods()
        ctrl = mod & pygame.KMOD_CTRL

        # ----- Ctrl shortcuts -----
        if ctrl:
            if event.key == pygame.K_a:                     # Select all
                self._selection_start = 0
                self._cursor_pos = len(self._text)
                return True
            if event.key == pygame.K_c:                     # Copy
                self._copy_selection()
                return True
            if event.key == pygame.K_x:                     # Cut
                self._copy_selection()
                self._delete_selection()
                return True
            if event.key == pygame.K_v:                     # Paste
                clip = pygame.scrap.get(pygame.scrap.SCRAP_TEXT)
                if clip:
                    self._insert_text(clip.decode('utf-8', errors='ignore').rstrip('\x00'))
                return True
            if event.key == pygame.K_z:                     # Undo
                self._undo()
                return True
            if event.key == pygame.K_y:                     # Redo
                self._redo()
                return True

        # ----- Normal keys -----
        if event.key == pygame.K_RETURN:
            # You can decide what Enter does – here we just ignore it
            return True

        if event.key == pygame.K_BACKSPACE:
            if self._selection_start is not None:
                self._delete_selection()
            elif ctrl:                                      # Ctrl+Backspace = delete word
                self._delete_word_backward()
            elif self._cursor_pos > 0:
                self._push_undo()
                self._text = self._text[:self._cursor_pos-1] + self._text[self._cursor_pos:]
                self._cursor_pos -= 1
                self._rendered_text = None
            return True

        if event.key == pygame.K_DELETE:
            if self._selection_start is not None:
                self._delete_selection()
            elif self._cursor_pos < len(self._text):
                self._push_undo()
                self._text = self._text[:self._cursor_pos] + self._text[self._cursor_pos+1:]
                self._rendered_text = None
            return True

        if event.key == pygame.K_LEFT:
            if self._selection_start is not None and not ctrl:
                self._cursor_pos = min(self._selection_start, self._cursor_pos)
                self._selection_start = None
            else:
                self._cursor_pos = max(0, self._cursor_pos - 1)
            return True

        if event.key == pygame.K_RIGHT:
            if self._selection_start is not None and not ctrl:
                self._cursor_pos = max(self._selection_start, self._cursor_pos)
                self._selection_start = None
            else:
                self._cursor_pos = min(len(self._text), self._cursor_pos + 1)
            return True

        if event.key == pygame.K_HOME:
            self._cursor_pos = 0
            if not ctrl:
                self._selection_start = None
            return True

        if event.key == pygame.K_END:
            self._cursor_pos = len(self._text)
            if not ctrl:
                self._selection_start = None
            return True

        return False

    # ------------------------------------------------------------------ #
    # Clipboard helpers
    # ------------------------------------------------------------------ #
    def _copy_selection(self):
        if self._selection_start is None:
            return
        a, b = sorted([self._selection_start, self._cursor_pos])
        sel = self._text[a:b]
        pygame.scrap.put(pygame.scrap.SCRAP_TEXT, sel.encode('utf-8'))

    # ------------------------------------------------------------------ #
    # Undo / Redo
    # ------------------------------------------------------------------ #
    def _undo(self):
        if len(self._history) <= 1:
            return
        self._redo_stack.append((self._text, self._cursor_pos))
        prev_text, prev_pos = self._history.pop()
        self._text = prev_text
        self._cursor_pos = prev_pos
        self._selection_start = None
        self._rendered_text = None

    def _redo(self):
        if not self._redo_stack:
            return
        self._history.append((self._text, self._cursor_pos))
        self._text, self._cursor_pos = self._redo_stack.pop()
        self._selection_start = None
        self._rendered_text = None

    # ------------------------------------------------------------------ #
    # Word deletion
    # ------------------------------------------------------------------ #
    def _delete_word_backward(self):
        if self._cursor_pos == 0:
            return
        self._push_undo()
        # find start of word
        i = self._cursor_pos
        while i > 0 and self._text[i-1].isspace():
            i -= 1
        while i > 0 and not self._text[i-1].isspace():
            i -= 1
        self._text = self._text[:i] + self._text[self._cursor_pos:]
        self._cursor_pos = i
        self._rendered_text = None

    # ------------------------------------------------------------------ #
    # Rendering helpers
    # ------------------------------------------------------------------ #
    def _render_text(self):
        """Render the whole text (with possible selection highlight later)."""
        self._rendered_text = self.font.render(self._text, True, self.text_color)
        self._rendered_width = self.rect.w

    def _pixel_to_index(self, pixel_x: int) -> int:
        """Convert horizontal pixel inside the box to character index."""
        if not self._text:
            return 0
        for i in range(len(self._text) + 1):
            sub = self._text[:i]
            w = self.font.size(sub)[0]
            if w > pixel_x:
                return i - 1 if i > 0 else 0
        return len(self._text)

    def _index_to_pixel(self, idx: int) -> int:
        """Pixel offset of a character index."""
        return self.font.size(self._text[:idx])[0]

    def _draw_selection(self, surface: pygame.Surface):
        if self._selection_start is None:
            return
        a = min(self._selection_start, self._cursor_pos)
        b = max(self._selection_start, self._cursor_pos)
        x1 = self.rect.x + 5 + self._index_to_pixel(a)
        x2 = self.rect.x + 5 + self._index_to_pixel(b)
        sel_rect = pygame.Rect(x1, self.rect.y + 2, x2 - x1, self.rect.h - 4)
        pygame.draw.rect(surface, (150, 180, 255), sel_rect)

    def _draw_cursor(self, surface: pygame.Surface):
        cur_x = self.rect.x + 5 + self._index_to_pixel(self._cursor_pos)
        pygame.draw.line(surface, self.text_color,
                         (cur_x, self.rect.y + 4),
                         (cur_x, self.rect.y + self.rect.h - 4), 2)