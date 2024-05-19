import unittest
from src.Keyboard import Keyboard


class TestKeyboard(unittest.TestCase):
    def setUp(self):
        self.keyboard = Keyboard()

    def test_input_character(self):
        self.keyboard.input_character('A')
        self.assertTrue(self.keyboard.has_characters())

    def test_get_next_character(self):
        self.keyboard.input_character('A')
        char = self.keyboard.get_next_character()
        self.assertEqual(char, 'A')
        self.assertFalse(self.keyboard.has_characters())


if __name__ == '__main__':
    unittest.main()
