import unittest
from unittest.mock import Mock, patch
import tkinter as tk

from src.GUI import GUI
from src.Screen import Screen
from src.Keyboard import Keyboard
from src.Memory import Memory
from src.Processor import Processor


class TestGUI(unittest.TestCase):
    def setUp(self):
        self.memory = Mock(spec=Memory)
        self.keyboard = Mock(spec=Keyboard)
        self.screen = Mock(spec=Screen)
        self.processor = Mock(spec=Processor)

        # Mocking the memory attribute of the processor
        self.processor.memory = Mock(spec=Memory)

        # Setting up width and height attributes on the screen mock
        self.screen.width = 16
        self.screen.height = 10

        # Mock the Tk instance and necessary methods
        with patch('tkinter.Tk') as MockTk:
            self.mock_root = MockTk.return_value
            self.mock_root._last_child_ids = {}
            self.mock_root.tk = Mock()

            # Mock Processor initialization
            with patch('src.Processor.Processor', return_value=self.processor):
                # Mock the update_screen method to prevent it from being called during initialization
                with patch.object(GUI, 'update_screen', return_value=None):
                    self.gui = GUI(self.memory, self.keyboard, self.screen)
                    self.gui.root = self.mock_root
                    self.gui.root.after = Mock()

                    # Mock the children of keyboard_frame to return a list
                    self.gui.keyboard_frame.winfo_children = Mock(return_value=[])

        # Ensure the read_video_memory method returns an iterable after GUI initialization
        self.processor.memory.read_video_memory.return_value = [ord('A')] * (self.screen.width * self.screen.height)

    def test_run_program(self):
        # Mock the methods called within run_program
        self.gui.processor.execute_program = Mock()
        self.gui.update_screen = Mock()

        # Call run_program
        self.gui.run_program()

        # Assert the methods are called
        self.gui.processor.execute_program.assert_called_once()
        self.gui.update_screen.assert_called_once()
        self.gui.root.after.assert_called_with(self.gui.interval, self.gui.run_program)

    def test_create_keyboard_buttons(self):
        # Mock the create_button method
        self.gui.create_button = Mock()

        # Call create_keyboard_buttons
        self.gui.create_keyboard_buttons()

        # Assert create_button was called the expected number of times
        self.assertEqual(self.gui.create_button.call_count, 65)  # 64 printable ASCII + Enter key

    def test_key_press(self):
        # Test key press handling
        self.gui.key_press('A')
        self.keyboard.input_character.assert_called_with(ord('A'))


if __name__ == '__main__':
    unittest.main()
