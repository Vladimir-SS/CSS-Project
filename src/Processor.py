from exceptions.DivisionByZeroException import DivisionByZeroException


class Processor:
    """
    Emulates a processor with specified components and operations.

    Attributes:
    - data_registers (list): List of 8 data registers, each 16-bit wide.
    - flags (dict): Dictionary to hold conditional flags such as carry, parity, zero, sign, and overflow flags.
    - program_counter (int or None): Holds the current instruction's address.
    - stack_pointer (list): Stack pointer for function calls and returns.
    - memory (Memory): Memory object to access system memory.
    - instruction_types (dict): Dictionary mapping instruction names to their corresponding methods.
    - is_file_parsed (bool): Indicates whether the file has been parsed.
    - file_name (str): Name of the file containing instructions.
    - Keyboard input handling:
        - is_reading_input (bool): Indicates whether the processor is waiting for keyboard input.
        - input (str): Keyboard input string.
        - input_destination (str): Destination operand for keyboard input.

    Methods:
    - __init__: Initializes the Processor object.
    - set_file_name: Set the name of the file containing instructions to be executed.
    - execute_instruction: Executes a single instruction.
    - execute_program: Execute instructions from a file sequentially.
    - parse_instruction: Parses a single instruction and adds it to memory.
    - parse_file: Parses instructions from a file and adds them to memory.
    - parse_memory_operand: Parses a memory operand to determine its address.
    - check_register_index: Checks if the given index is a valid register index.
    - get_operand_value: Gets the value of an operand.
    - store_result: Stores the result of an operation.
    - assert_16_bit: Truncates a value to fit within 16 bits.
    - reading_input: Handles keyboard input.
    - get_memory_data: Gets the value of a memory operand. ( starts reading input if keyboard buffer is accessed)
    - convert_keyboard_input: Converts keyboard input to a numerical value or ASCII value.
    """

    def __init__(self, memory, file_name=None):
        """
        Initializes the Processor object.

        Parameters:
        - memory (Memory): An instance of the Memory class.

        Attributes:
        - data_registers (list): List of 8 data registers, each 16-bit wide.
        - flags (dict): Dictionary to hold conditional flags.
        - program_counter (int or None): Holds the current instruction's address.
        - stack_pointer (list): Stack for function calls and returns.
        - memory (Memory): Memory object to access system memory.
        - instruction_types (dict): Dictionary mapping instruction names to their corresponding methods. ( to avoid using if-elif-else statements)
        """
        self.data_registers = [0 for _ in range(8)]
        self.flags = {
            'CF': False,
            # Carry Flag: is set when an arithmetic operation generates a carry or borrows from the most significant bit; used in testing for overflow in signed integer arithmetic
            'PF': False,
            # Parity Flag: is set only when the least significant byte of the result has an even number of 1 bits
            'ZF': False,  # Zero Flag: is set when the result of an operation is 0
            'SF': False,
            # Sign Flag: holds the value of the most significant bit of the result; indicates the sign of a signed integer (0 = positive, 1 = negative)
            'OF': False  # Overflow Flag: is set when an overflow occurs in signed integer arithmetic
        }
        # Special-purpose registers
        self.program_counter = None
        self.stack_pointer = []
        self.memory = memory  # Memory "pointer" - used to access memory without overcomplicating the memory class by making it static

        # Helper variables
        self.is_file_parsed = False
        self.file_name = file_name
        # Keyboard input handling
        self.is_reading_input = False
        self.input = ''
        self.input_destination = None

        self.instruction_types = {
            # Assignment
            'MOV': self.mov,
            # Arithmetic operations
            'ADD': self.add,
            'SUB': self.sub,
            'MUL': self.mul,
            'DIV': self.div,
            # Comparison
            'CMP': self.cmp,
            # Jumps
            'JMP': self.jmp,
            'JE': self.je,
            'JNE': self.jne,
            'JG': self.jg,
            'JL': self.jl,
            'JGE': self.jge,
            'JLE': self.jle,
            # Stack operations
            'PUSH': self.push,
            'POP': self.pop,
            # Function call/return
            'CALL': self.call,
            'RET': self.ret,
            # Boolean operations
            'NOT': self.not_op,
            'AND': self.and_op,
            'OR': self.or_op,
            'XOR': self.xor_op,
            'SHL': self.shl,
            'SHR': self.shr
        }

    def set_file_name(self, file_name):
        """
        Set the name of the file containing instructions to be executed.

        Parameters:
        - file_name (str): The name of the file containing instructions.
        """
        assert isinstance(file_name, str), "File name must be a string"

        self.file_name = file_name
        self.is_file_parsed = False

    def execute_instruction(self, instruction):
        """
        Execute a single instruction. ( skips label instructions)

        Parameters:
        - instruction (tuple): A tuple containing the instruction type and operands.
        """
        if instruction is None:  # Skip labels
            return
        instruction_type, operands = instruction

        assert instruction_type in self.instruction_types, "Unknown instruction type"

        self.instruction_types[instruction_type](operands)

    def execute_program(self):
        """
        Execute instructions from a file sequentially.

        Parameters:
        - file_name (str): The name of the file containing instructions to be executed.
        """
        if self.file_name is None:
            return

        if not self.is_file_parsed:
            self.parse_file(self.file_name)

            if self.program_counter is None:
                self.program_counter = 0

        if self.is_reading_input:
            self.reading_input()
            return

        if self.memory.check_instruction_memory_address(self.program_counter):
            self.execute_instruction(self.memory.get_instruction(self.program_counter))
            self.program_counter += 1

    def parse_instruction(self, instruction):
        """
        Parse a single instruction and add it to memory.

        Parameters:
        - instruction (str): A single instruction in assembly-like language.
        """
        if instruction.startswith(';') or instruction == '':
            return

        # Remove comments (text after ';')
        instruction = instruction.split(';')[0]

        instruction_parts = instruction.split()
        opcode = instruction_parts[0]

        if opcode in self.instruction_types:
            operands = [operand.replace(',', '') for operand in instruction_parts[1:]]
            self.memory.add_instruction((opcode, operands))
        elif opcode.endswith(':'):
            self.memory.add_instruction(None, opcode[:-1])

    def parse_file(self, file_name):
        """
        Parse instructions from a file and add them to memory.

        Parameters:
        - file_name (str): Name of the file containing instructions.
        """
        with open(file_name, 'r') as file:
            for line in file:
                self.parse_instruction(line.strip())

        self.is_file_parsed = True

    def parse_memory_operand(self, operand):
        """
        Parse a memory operand to determine if the address is specified by a constant value or by a data register.

        Parameters:
        - operand (str): The memory operand string.

        Returns:
        - int: The memory address.
        """
        if operand.startswith('M'):
            if operand[1:].startswith('R'):
                register_index = int(operand[2:])
                self.check_register_index(register_index)
                return self.data_registers[register_index]
            else:
                return int(operand[1:])
        else:
            raise ValueError("Invalid memory operand format")

    def check_register_index(self, index):
        """
        Check if the given index is a valid register index.

        Parameters:
        - index (int): The register index.

        Raises:
        - ValueError: If the index is invalid.
        """
        if index < 0 or index >= len(self.data_registers):
            raise ValueError("Invalid register index")

    def get_operand_value(self, operand):
        """
        Get the value of an operand based on its type. ( ensures 16-bit width of operands)

        Parameters:
        - operand (str): Operand string.

        Returns:
        - int: Value of the operand.
        """
        if operand.startswith('R'):
            register_index = int(operand[1:])
            self.check_register_index(register_index)
            return self.data_registers[register_index]
        elif operand.startswith('#'):
            return self.assert_16_bit(int(operand[1:]))
        elif operand.startswith('M'):
            address = self.parse_memory_operand(operand)
            return self.memory.get_data(address)
        else:
            print("Error: Unsupported operand type")
            return 0  # Return a default value if unsupported

    def store_result(self, destination, result):
        """
        Store the result of an operation.

        Parameters:
        - destination (str): Destination operand.
        - result (int): Result of the operation.
        """
        self.assert_16_bit(result)

        if destination.startswith('R'):
            register_index = int(destination[1:])
            self.check_register_index(register_index)
            self.data_registers[register_index] = result
        elif destination.startswith('M'):
            address = self.parse_memory_operand(destination)
            self.memory.set_data(address, result)
        else:
            print("Error: Unsupported destination operand")

    def assert_16_bit(self, value):
        """
        Truncate a value to fit within 16 bits.

        Parameters:
        - value (int): The value to be truncated.

        Returns:
        - int: The truncated 16-bit value.
        """
        max_value_16bit = (1 << 15) - 1  # Maximum value of a 16-bit signed integer (32767)
        min_value_16bit = -(1 << 15)  # Minimum value of a 16-bit signed integer (-32768)

        if value > max_value_16bit:
            print("Warning: Value exceeds the maximum 16-bit signed integer. Truncated to fit within 16 bits.")
            return max_value_16bit
        elif value < min_value_16bit:
            print("Warning: Value is less than the minimum 16-bit signed integer. Truncated to fit within 16 bits.")
            return min_value_16bit
        else:
            return value

    def reading_input(self):
        """
        Handle keyboard input.
        """
        if self.memory.get_keyboard_pointer() is not None:
            keyboard = self.memory.get_keyboard_pointer()
            while keyboard.has_characters():
                char = keyboard.get_next_character()
                if char == 13:  # Enter key
                    self.is_reading_input = False
                    print('Input:', self.input)
                    self.store_result(self.input_destination, self.convert_keyboard_input(self.input))
                    self.input = ''
                    break
                self.input += chr(char)

    def get_memory_data(self, operand, destination):
        """
        Gets the value of a memory operand.

        Parameters:
        - operand (str): Operand string.
        - destination (str): Destination operand. ( used only when reading input from keyboard buffer)

        Returns:
        - int: Value of the memory operand.
        """
        if operand.startswith('M'):
            address = self.parse_memory_operand(operand)
            if address == self.memory.keyboard_buffer_address:
                self.is_reading_input = True
                self.input_destination = destination
                return None
            else:
                return self.memory.get_data(address)
        else:
            raise ValueError("Invalid memory operand format")

    def convert_keyboard_input(self, keyboard_input):
        """
        Convert keyboard input to a numerical value or ASCII value.

        Returns:
        - int: The numerical value if input is a digit; ASCII value if input is a single char and non-numeric; -1 otherwise.
        """
        if keyboard_input.isdigit():
            return int(keyboard_input)
        elif len(keyboard_input) == 1:
            return ord(keyboard_input)  # Return ASCII value for single characters
        else:
            return -1

    def mov(self, operands):
        if len(operands) != 2:
            print("Error: MOV instruction requires two operands")
            return

        destination = operands[0]
        source = operands[1]

        # Extract source operand value
        if source.startswith('#'):
            source = int(source[1:])
        elif source.startswith('R'):
            register_index = int(source[1:])
            self.check_register_index(register_index)
            source = self.data_registers[register_index]
        elif source.startswith('M'):
            source = self.get_memory_data(source, destination)
            if source is None:
                return
        else:
            print("Error: Unsupported source operand")
            return

        # Handle different destination operand types: data registers, memory locations
        self.store_result(destination, source)

        print('MOV', operands)

    def add(self, operands):
        if len(operands) != 2:
            print("Error: ADD instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        result = operand1 + operand2

        self.store_result(operands[0], result)

        print('ADD', operands)

    def sub(self, operands):
        if len(operands) != 2:
            print("Error: SUB instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        result = operand1 - operand2

        self.store_result(operands[0], result)
        print('SUB', operands)

    def mul(self, operands):
        if len(operands) != 2:
            print("Error: MUL instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        result = operand1 * operand2

        self.store_result(operands[0], result)
        print('MUL', operands)

    def div(self, operands):
        if len(operands) != 2:
            print("Error: DIV instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        if operand2 != 0:
            result = operand1 // operand2
        else:
            raise DivisionByZeroException("Video memory address out of bounds")
            return

        self.store_result(operands[0], result)
        print('DIV', operands)

    def cmp(self, operands):
        """
        Perform comparison operation.

        Compares two operands and sets conditional flags accordingly.

        Parameters:
        - operands (list): List of two operands.

        Flags Updated:
        - ZF (Zero Flag): Set if the two operands are equal.
        - SF (Sign Flag): Set if the result of subtraction is negative.
        - CF (Carry Flag): Set if the first operand is less than the second operand.
        - OF (Overflow Flag): Set if the result of subtraction exceeds the signed integer range.
        """
        if len(operands) != 2:
            print("Error: CMP instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        self.flags['ZF'] = operand1 == operand2
        self.flags['SF'] = (operand1 - operand2) < 0
        self.flags['CF'] = operand1 < operand2
        self.flags['OF'] = ((operand1 - operand2) > 32767) or ((operand1 - operand2) < -32768)

        print('CMP', operands[0], operand1, operands[1], operand2)

    def jmp(self, operands):
        if len(operands) != 1:
            print("Error: JMP instruction requires one operand")
            return

        if operands:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JMP', operands)

    def je(self, operands):
        if len(operands) != 1:
            print("Error: JE instruction requires one operand")
            return

        if self.flags['ZF']:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JE', operands)

    def jne(self, operands):
        if len(operands) != 1:
            print("Error: JNE instruction requires one operand")
            return

        if not self.flags['ZF']:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JNE', operands)

    def jg(self, operands):
        if len(operands) != 1:
            print("Error: JG instruction requires one operand")
            return

        if not self.flags['ZF'] and self.flags['SF'] == self.flags['OF']:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JG', operands)

    def jl(self, operands):
        if len(operands) != 1:
            print("Error: JLT instruction requires one operand")
            return

        if self.flags['SF'] and not self.flags['ZF']:
            self.program_counter = self.memory.goto_label(operands[0])
        print('JL', operands)

    def jge(self, operands):
        if len(operands) != 1:
            print("Error: JGE instruction requires one operand")
            return

        if self.flags['SF'] == self.flags['ZF']:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JGE', operands)

    def jle(self, operands):
        if len(operands) != 1:
            print("Error: JLE instruction requires one operand")
            return

        if self.flags['ZF'] or self.flags['SF'] != self.flags['OF']:
            self.program_counter = self.memory.goto_label(operands[0])

        print('JLE', operands)

    def push(self, operands):
        if len(operands) != 1:
            print("Error: PUSH instruction requires one operand")
            return

        if operands:
            self.stack_pointer.append(operands[0])

        print('PUSH', operands)

    def pop(self, operands):
        if len(operands) != 1:
            print("Error: POP instruction requires one operand")
            return

        if operands:
            self.stack_pointer.pop()

        print('POP', operands)

    def call(self, operands):
        if len(operands) != 1:
            print("Error: CALL instruction requires one operand")
            return

        if operands:
            self.stack_pointer.append(self.program_counter)
            self.program_counter = self.memory.goto_label(operands[0])

        print('CALL', operands)

    def ret(self, operands):
        if not self.stack_pointer:
            print("Error: Stack is empty")
            return

        label = self.stack_pointer.pop()
        if label:
            if isinstance(label, int):
                self.program_counter = label
            else:
                self.program_counter = self.memory.goto_label(label)

        print('RET', operands)

    def not_op(self, operands):
        if len(operands) != 1:
            raise ValueError("NOT instruction requires one operand")
        operand = self.get_operand_value(operands[0])
        result = ~operand & 0xFFFFFFFF
        self.store_result(operands[0], result)
        print('NOT', operands)

    def and_op(self, operands):
        if len(operands) != 2:
            raise ValueError("AND instruction requires two operands")
        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])
        result = operand1 & operand2
        self.store_result(operands[0], result)
        print('AND', operands)

    def or_op(self, operands):
        if len(operands) != 2:
            raise ValueError("OR instruction requires two operands")
        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])
        result = operand1 | operand2
        self.store_result(operands[0], result)
        print('OR', operands)

    def xor_op(self, operands):
        if len(operands) != 2:
            raise ValueError("XOR instruction requires two operands")
        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])
        result = operand1 ^ operand2
        self.store_result(operands[0], result)
        print('XOR', operands)

    def shl(self, operands):
        if len(operands) != 2:
            print("Error: SHL instruction requires two operands")
            return

        operand = self.get_operand_value(operands[0])
        shift_amount = self.get_operand_value(operands[1])
        result = operand << shift_amount
        self.store_result(operands[0], result)
        print('SHL', operands)

    def shr(self, operands):
        if len(operands) != 2:
            print("Error: SHR instruction requires two operands")
            return

        operand = self.get_operand_value(operands[0])
        shift_amount = self.get_operand_value(operands[1])
        result = operand >> shift_amount  # Performing bitwise right shift operation
        self.store_result(operands[0], result)
        print('SHR', operands)
