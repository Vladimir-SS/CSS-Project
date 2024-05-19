import unittest
from src.Memory import Memory
from src.Exceptions.MemoryOverflowError import MemoryOverflowError
from src.Exceptions.InvalidMemoryAddrError import InvalidMemoryAddrError


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(8192, 4096, 4095, 0, 1023)

    def test_initialization(self):
        # Test valid initialization
        mem = Memory(8192, 4096, 4095, 0, 1023)
        self.assertIsNotNone(mem)

        # Test invalid keyboard buffer address
        with self.assertRaises(InvalidMemoryAddrError):
            Memory(8192, 4096, 4096, 0, 1023)

        # Test invalid video memory start address
        with self.assertRaises(InvalidMemoryAddrError):
            Memory(8192, 4096, 4095, 4096, 1023)

        # Test invalid video memory end address
        with self.assertRaises(InvalidMemoryAddrError):
            Memory(8192, 4096, 4095, 0, 4096)

    def test_add_instruction(self):
        self.memory.add_instruction('MOV R0, 1')
        instruction = self.memory.get_instruction(0)
        self.assertEqual(instruction, 'MOV R0, 1')

    def test_add_instruction_with_label(self):
        self.memory.add_instruction('MOV R0, 1', label='start')
        instruction = self.memory.get_instruction(0)
        self.assertEqual(instruction, 'MOV R0, 1')
        self.assertEqual(self.memory.goto_label('start'), 0)

    def test_instruction_memory_overflow(self):
        with self.assertRaises(MemoryOverflowError):
            for _ in range(8192 + 1):
                self.memory.add_instruction('MOV R0, 1')

    def test_data_memory_operations(self):
        self.memory.set_data(2010, 1234)
        data = self.memory.get_data(2010)
        self.assertEqual(data, 1234)

    def test_set_data_out_of_bounds(self):
        with self.assertRaises(InvalidMemoryAddrError):
            self.memory.set_data(4096, 1234)

    def test_get_data_out_of_bounds(self):
        with self.assertRaises(InvalidMemoryAddrError):
            self.memory.get_data(4096)

    def test_set_data_to_keyboard_buffer(self):
        with self.assertRaises(InvalidMemoryAddrError):
            self.memory.set_data(4095, 1234)

    def test_set_data_to_video_memory(self):
        self.memory.set_data(0, 1234)
        self.assertEqual(self.memory.get_data(0), 210)  # 1234 & 0xFF = 210

    def test_keyboard_pointer_operations(self):
        self.memory.set_keyboard_pointer('keyboard_instance')
        self.assertEqual(self.memory.get_keyboard_pointer(), 'keyboard_instance')

    def test_read_video_memory(self):
        self.memory.set_data(0, ord('A'))
        self.memory.set_data(1023, ord('Z'))
        video_memory = self.memory.read_video_memory()
        self.assertEqual(video_memory[0], ord('A') & 0xFF)
        self.assertEqual(video_memory[-1], ord('Z') & 0xFF)

    def test_goto_label(self):
        self.memory.add_instruction('MOV R0, 1', label='start')
        self.assertEqual(self.memory.goto_label('start'), 0)

    def test_goto_invalid_label(self):
        with self.assertRaises(ValueError):
            self.memory.goto_label('invalid_label')

    def test_invalid_instruction_address(self):
        with self.assertRaises(InvalidMemoryAddrError):
            self.memory.get_instruction(8192)

    def test_validate_memory_size(self):
        with self.assertRaises(ValueError):
            Memory(70000, 4096, 4095, 0, 1023)  # Size exceeding maximum

        with self.assertRaises(ValueError):
            Memory(8192, 70000, 4095, 0, 1023)  # Size exceeding maximum

        with self.assertRaises(ValueError):
            Memory(8191, 4096, 4095, 0, 1023)  # Size not multiple of 1 KB

    def test_memory_overflow_error(self):
        with self.assertRaises(MemoryOverflowError):
            raise MemoryOverflowError("Test Exception")


if __name__ == '__main__':
    unittest.main()
