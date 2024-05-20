import unittest
from unittest.mock import Mock, patch

from src.exceptions.DivisionByZeroException import DivisionByZeroException
from src.Processor import Processor
from src.Memory import Memory


class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.memory = Mock(spec=Memory)
        self.processor = Processor(self.memory)

    def test_initialization(self):
        processor = Processor(self.memory)
        self.assertIsNotNone(processor)
        self.assertEqual(len(processor.data_registers), 8)
        self.assertIsNone(processor.program_counter)
        self.assertEqual(processor.stack_pointer, [])
        self.assertFalse(processor.is_file_parsed)
        self.assertFalse(processor.is_reading_input)

    def test_set_file_name(self):
        self.processor.set_file_name("test.asm")
        self.assertEqual(self.processor.file_name, "test.asm")
        self.assertFalse(self.processor.is_file_parsed)

    def test_execute_instruction_invalid_instruction(self):
        with self.assertRaises(ValueError):
            self.processor.execute_instruction(('INVALID', []))

    def test_execute_instruction_mov(self):
        self.processor.data_registers[0] = 123
        self.processor.execute_instruction(('MOV', ['R1', 'R0']))
        self.assertEqual(self.processor.data_registers[1], 123)

    def test_execute_instruction_add(self):
        self.processor.data_registers[1] = 2
        self.processor.data_registers[2] = 3
        self.processor.execute_instruction(('ADD', ['R2', 'R1']))
        self.assertEqual(self.processor.data_registers[2], 5)

    def test_execute_instruction_sub(self):
        self.processor.data_registers[1] = 5
        self.processor.data_registers[2] = 3
        self.processor.execute_instruction(('SUB', ['R1', 'R2']))
        self.assertEqual(self.processor.data_registers[1], 2)

    def test_execute_instruction_mul(self):
        self.processor.data_registers[1] = 4
        self.processor.data_registers[2] = 3
        self.processor.execute_instruction(('MUL', ['R2', 'R1']))
        self.assertEqual(self.processor.data_registers[2], 12)

    def test_execute_instruction_div(self):
        self.processor.data_registers[0] = 12
        self.processor.data_registers[1] = 3
        self.processor.execute_instruction(('DIV', ['R0', 'R1']))
        self.assertEqual(self.processor.data_registers[0], 4)

    def test_execute_instruction_div_by_zero(self):
        self.processor.data_registers[0] = 12
        self.processor.data_registers[1] = 0
        with self.assertRaises(DivisionByZeroException):
            self.processor.execute_instruction(('DIV', ['R0', 'R1']))

    def test_parse_instruction_mov(self):
        self.processor.parse_instruction('MOV R1, R0')
        self.assertEqual(self.memory.add_instruction.call_count, 1)

    def test_parse_file(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data="MOV R1, R0\nADD R2, R1")):
            self.processor.parse_file("test.asm")
            self.assertTrue(self.processor.is_file_parsed)

    def test_store_result_register(self):
        self.processor.store_result('R0', 10)
        self.assertEqual(self.processor.data_registers[0], 10)

    def test_store_result_memory(self):
        self.processor.parse_memory_operand = Mock(return_value=0)
        self.processor.store_result('M0', 20)
        self.memory.set_data.assert_called_with(0, 20)

    def test_flags_after_cmp(self):
        self.processor.data_registers[0] = 5
        self.processor.data_registers[1] = 5
        self.processor.execute_instruction(('CMP', ['R0', 'R1']))
        self.assertTrue(self.processor.flags['ZF'])

    def test_jump_instructions(self):
        self.memory.goto_label = Mock(return_value=10)
        self.processor.execute_instruction(('JMP', ['label']))
        self.assertEqual(self.processor.program_counter, 10)

    def test_push_instruction(self):
        self.processor.execute_instruction(('PUSH', ['R0']))
        self.assertEqual(self.processor.stack_pointer[-1], 'R0')

    def test_pop_instruction(self):
        self.processor.stack_pointer = ['R0']
        self.processor.execute_instruction(('POP', ['R1']))
        self.assertEqual(self.processor.stack_pointer, [])

    def test_call_instruction(self):
        self.memory.goto_label = Mock(return_value=10)
        self.processor.program_counter = 0
        self.processor.execute_instruction(('CALL', ['label']))
        self.assertEqual(self.processor.program_counter, 10)
        self.assertEqual(self.processor.stack_pointer[-1], 0)

    def test_ret_instruction(self):
        self.processor.stack_pointer = [10]
        self.processor.execute_instruction(('RET', []))
        self.assertEqual(self.processor.program_counter, 10)


if __name__ == '__main__':
    unittest.main()
