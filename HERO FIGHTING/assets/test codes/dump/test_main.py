import unittest
from unittest.mock import MagicMock, patch
import pygame
from main import Player

class TestPlayerAnimation(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Player(
            idle_ani="idle",
            atk1_ani="atk1",
            atk2_ani="atk2",
            atk3_ani="atk3",
            sp_ani="sp"
        )
        self.player.attacking = False
        self.player.last_atk_time = 0
        self.player.player_idle = [MagicMock() for _ in range(8)]
        self.player.player_atk = [MagicMock() for _ in range(18)]
        self.player.image = None

    @patch('pygame.time.get_ticks', return_value=200)
    def test_idle_animation(self, mock_get_ticks):
        self.player.animation()
        self.assertEqual(self.player.player_idle_index, 1)
        self.assertEqual(self.player.image, self.player.player_idle[1])

    @patch('pygame.time.get_ticks', return_value=200)
    def test_attack_animation(self, mock_get_ticks):
        self.player.attacking = True
        self.player.animation()
        self.assertEqual(self.player.player_atk_index, 1)
        self.assertEqual(self.player.image, self.player.player_atk[0])

    @patch('pygame.time.get_ticks', return_value=500)
    def test_attack_animation_resets(self, mock_get_ticks):
        self.player.attacking = True
        self.player.player_atk_index = len(self.player.player_atk) - 1
        self.player.animation()
        self.assertFalse(self.player.attacking)
        self.assertEqual(self.player.player_atk_index, 0)

    @patch('pygame.time.get_ticks', return_value=500)
    def test_idle_animation_wraps_around(self, mock_get_ticks):
        self.player.player_idle_index = len(self.player.player_idle) - 1
        self.player.animation()
        self.assertEqual(self.player.player_idle_index, 0)

if __name__ == '__main__':
    unittest.main()