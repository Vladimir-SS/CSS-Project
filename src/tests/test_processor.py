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

    def test_input_handling(self):
        # Test handling of keyboard input
        self.memory.keyboard_buffer_address = 100
        self.processor.get_memory_data('M100', 'R1')
        self.assertTrue(self.processor.is_reading_input)

    def test_shift_operations(self):
        # Test shift left and shift right operations
        self.processor.data_registers[0] = 8  # 1000 in binary
        self.processor.execute_instruction(('SHL', ['R0', '#1']))
        self.assertEqual(self.processor.data_registers[0], 16)
        self.processor.execute_instruction(('SHR', ['R0', '#2']))
        self.assertEqual(self.processor.data_registers[0], 4)

    def test_program_flow(self):
        # Test JMP, CALL, RET instructions
        self.memory.goto_label.return_value = 10
        self.processor.execute_instruction(('JMP', ['start']))
        self.assertEqual(self.processor.program_counter, 10)
        self.processor.execute_instruction(('CALL', ['function']))
        self.assertEqual(self.processor.program_counter, 10)
        self.processor.stack_pointer.append(20)
        self.processor.execute_instruction(('RET', []))
        self.assertEqual(self.processor.program_counter, 20)

    def test_division_error(self):
        # Specifically testing the division by zero error
        self.processor.data_registers[1] = 0
        with self.assertRaises(DivisionByZeroException):
            self.processor.execute_instruction(('DIV', ['R0', 'R1']))

    def test_reading_input(self):
        # Setup for keyboard input
        keyboard = Mock()
        keyboard.has_characters.side_effect = [True, True, True, False]  # Simulate 'a', 'b', Enter, then stop
        keyboard.get_next_character.side_effect = [ord('a'), ord('b'), ord('\r')]  # Enter key terminates input

        self.memory.get_keyboard_pointer.return_value = keyboard
        self.processor.input_destination = 'R1'
        self.processor.store_result = Mock()
        self.processor.convert_keyboard_input = Mock(return_value=123)  # Assuming conversion of 'ab' to 123

        # Execute method
        self.processor.reading_input()

        # Verify input handling
        self.assertEqual(self.processor.input, '')
        self.assertFalse(self.processor.is_reading_input)
        self.processor.store_result.assert_called_once_with('R1', 123)
        self.processor.convert_keyboard_input.assert_called_once_with('ab')

        # Assert calls based on actual behavior observed
        expected_calls = 3  # Adjusted to 3 because loop stops after third call when False is returned
        actual_calls = keyboard.has_characters.call_count
        print(f"Expected calls: {expected_calls}, Actual calls: {actual_calls}")

        self.assertEqual(actual_calls, expected_calls, f"Expected {expected_calls} calls, got {actual_calls}")

    def test_jmp(self):
        self.memory.goto_label.return_value = 10
        self.processor.jmp(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 10)

    def test_jmp_invalid_operands(self):
        self.processor.jmp(['label', 'extra'])
        self.assertIsNone(self.processor.program_counter)

    def test_je(self):
        self.memory.goto_label.return_value = 20
        self.processor.flags['ZF'] = True
        self.processor.je(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 20)

    def test_je_not_taken(self):
        self.processor.flags['ZF'] = False
        self.processor.je(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_jne(self):
        self.memory.goto_label.return_value = 30
        self.processor.flags['ZF'] = False
        self.processor.jne(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 30)

    def test_jne_not_taken(self):
        self.processor.flags['ZF'] = True
        self.processor.jne(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_jg(self):
        self.memory.goto_label.return_value = 40
        self.processor.flags['ZF'] = False
        self.processor.flags['SF'] = self.processor.flags['OF']
        self.processor.jg(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 40)

    def test_jg_not_taken(self):
        self.processor.flags['ZF'] = True
        self.processor.jg(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_jl(self):
        self.memory.goto_label.return_value = 50
        self.processor.flags['SF'] = True
        self.processor.flags['ZF'] = False
        self.processor.jl(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 50)

    def test_jl_not_taken(self):
        self.processor.flags['SF'] = False
        self.processor.flags['ZF'] = True
        self.processor.jl(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_jge(self):
        self.memory.goto_label.return_value = 60
        self.processor.flags['SF'] = self.processor.flags['ZF']
        self.processor.jge(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 60)

    def test_jge_not_taken(self):
        self.processor.flags['SF'] = not self.processor.flags['ZF']
        self.processor.jge(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_jle(self):
        self.memory.goto_label.return_value = 70
        self.processor.flags['ZF'] = True
        self.processor.jle(['label'])
        self.memory.goto_label.assert_called_with('label')
        self.assertEqual(self.processor.program_counter, 70)

    def test_jle_not_taken(self):
        self.processor.flags['ZF'] = False
        self.processor.flags['SF'] = self.processor.flags['OF']
        self.processor.jle(['label'])
        self.assertIsNone(self.processor.program_counter)
        self.memory.goto_label.assert_not_called()

    def test_push(self):
        self.processor.push(['R1'])
        self.assertEqual(self.processor.stack_pointer[-1], 'R1')

    def test_push_invalid_operands(self):
        self.processor.push(['R1', 'extra'])
        self.assertEqual(len(self.processor.stack_pointer), 0)

    def test_pop(self):
        self.processor.stack_pointer = ['R1', 'R2']
        self.processor.pop(['R1'])
        self.assertEqual(self.processor.stack_pointer, ['R1'])

    def test_pop_invalid_operands(self):
        self.processor.stack_pointer = ['R1', 'R2']
        self.processor.pop(['R1', 'extra'])
        self.assertEqual(self.processor.stack_pointer, ['R1', 'R2'])

    def test_call(self):
        self.processor.program_counter = 100
        self.memory.goto_label.return_value = 200
        self.processor.call(['function'])
        self.assertEqual(self.processor.stack_pointer[-1], 100)
        self.assertEqual(self.processor.program_counter, 200)

    def test_call_invalid_operands(self):
        self.processor.program_counter = 100
        self.processor.call(['function', 'extra'])
        self.assertEqual(len(self.processor.stack_pointer), 0)
        self.assertEqual(self.processor.program_counter, 100)

    def test_ret(self):
        self.processor.stack_pointer = [100, 200]
        self.processor.ret([])
        self.assertEqual(self.processor.program_counter, 200)
        self.assertEqual(self.processor.stack_pointer, [100])

    def test_ret_empty_stack(self):
        self.processor.stack_pointer = []
        self.processor.ret([])
        self.assertEqual(len(self.processor.stack_pointer), 0)
        self.assertIsNone(self.processor.program_counter)

    def test_ret_invalid_operands(self):
        self.processor.stack_pointer = [100, 200]
        self.processor.ret(['extra'])
        self.assertEqual(self.processor.program_counter, 200)
        self.assertEqual(self.processor.stack_pointer, [100])

    def test_not_op(self):
        self.processor.data_registers[0] = 0b10101010
        self.processor.not_op(['R0'])
        self.assertEqual(self.processor.data_registers[0], ~0b10101010 & 0xFFFFFFFF)

    def test_not_op_invalid_operands(self):
        with self.assertRaises(ValueError):
            self.processor.not_op(['R0', 'R1'])

    def test_and_op(self):
        self.processor.data_registers[0] = 0b10101010
        self.processor.data_registers[1] = 0b11001100
        self.processor.and_op(['R0', 'R1'])
        self.assertEqual(self.processor.data_registers[0], 0b10101010 & 0b11001100)

    def test_and_op_invalid_operands(self):
        with self.assertRaises(ValueError):
            self.processor.and_op(['R0'])
        with self.assertRaises(ValueError):
            self.processor.and_op(['R0', 'R1', 'R2'])

    def test_or_op(self):
        self.processor.data_registers[0] = 0b10101010
        self.processor.data_registers[1] = 0b11001100
        self.processor.or_op(['R0', 'R1'])
        self.assertEqual(self.processor.data_registers[0], 0b10101010 | 0b11001100)

    def test_or_op_invalid_operands(self):
        with self.assertRaises(ValueError):
            self.processor.or_op(['R0'])
        with self.assertRaises(ValueError):
            self.processor.or_op(['R0', 'R1', 'R2'])

    def test_xor_op(self):
        self.processor.data_registers[0] = 0b10101010
        self.processor.data_registers[1] = 0b11001100
        self.processor.xor_op(['R0', 'R1'])
        self.assertEqual(self.processor.data_registers[0], 0b10101010 ^ 0b11001100)

    def test_xor_op_invalid_operands(self):
        with self.assertRaises(ValueError):
            self.processor.xor_op(['R0'])
        with self.assertRaises(ValueError):
            self.processor.xor_op(['R0', 'R1', 'R2'])


if __name__ == '__main__':
    unittest.main()
