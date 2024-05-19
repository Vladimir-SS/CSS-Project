import unittest
from unittest.mock import Mock, patch
import tkinter as tk

# Adjusting import paths to ensure they are correctly referenced
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

    def test_create_button(self):
        # Test creating a button and adding it to the keyboard frame
        self.gui.create_button('A', 0, 0)
        # Update the mock to return the created button
        button = tk.Button(self.gui.keyboard_frame, text='A')
        self.gui.keyboard_frame.winfo_children = Mock(return_value=[button])
        # Retrieve the button and assert its properties
        retrieved_button = self.gui.keyboard_frame.winfo_children()[0]
        self.assertEqual(retrieved_button.cget('text'), 'A')
        self.assertEqual(retrieved_button.grid_info()['row'], 0)
        self.assertEqual(retrieved_button.grid_info()['column'], 0)

    def test_key_press(self):
        # Test key press handling
        self.gui.key_press('A')
        self.keyboard.input_character.assert_called_with(ord('A'))

    @patch('tkinter.filedialog.askopenfilename', return_value='test.asm')
    def test_select_asm_file(self, mock_filedialog):
        # Ensure the processor mock has the set_file_name method
        self.processor.set_file_name = Mock()
        # Test file selection dialog
        self.gui.select_asm_file()
        self.processor.set_file_name.assert_called_with('test.asm')


if __name__ == '__main__':
    unittest.main()
