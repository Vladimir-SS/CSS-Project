import unittest
from src.Screen import Screen


class TestScreen(unittest.TestCase):
    def test_screen_initialization(self):
        screen = Screen(100, 16)
        self.assertEqual(screen.width, 100)
        self.assertEqual(screen.height, 16)


if __name__ == '__main__':
    unittest.main()
