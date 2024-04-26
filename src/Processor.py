class Processor:
    def __init__(self, memory):
        self.data_registers = [0 for _ in range(8)]
        self.flags = {
            'CF': False,  # Carry Flag: is set when an arithmetic operation generates a carry or borrows from the most significant bit; used in testing for overflow in signed integer arithmetic
            'PF': False,  # Parity Flag: is set only when the least significant byte of the result has an even number of 1 bits
            'ZF': False,  # Zero Flag: is set when the result of an operation is 0
            'SF': False,  # Sign Flag: holds the value of the most significant bit of the result; indicates the sign of a signed integer (0 = positive, 1 = negative)
            'OF': False   # Overflow Flag: is set when an overflow occurs in signed integer arithmetic
        }
        # Special-purpose registers
        self.program_counter = None
        self.stack_pointer = []
        self.memory = memory # Memory "pointer" - used to access memory without overcomplicating the memory class by making it static

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

    def execute_instruction(self, instruction):
        if instruction is None: # Skip labels
            return
        instruction_type, operands = instruction
        self.instruction_types[instruction_type](operands)

    def execute_program(self, file_name):
        self.parse_file(file_name)

        if self.program_counter is None:
            self.program_counter = 0

        while self.memory.check_instruction_memory_address(self.program_counter):
            self.execute_instruction(self.memory.get_instruction(self.program_counter))
            self.program_counter += 1

    def parse_instruction(self, instruction):
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
        with open(file_name, 'r') as file:
            for line in file:
                self.parse_instruction(line.strip())

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
                # Address specified by a data register
                register_index = int(operand[2:])
                return self.data_registers[register_index]
            else:
                # Address specified by a constant value
                return int(operand[1:])
        else:
            raise ValueError("Invalid memory operand format")

    def get_operand_value(self, operand):
        if operand.startswith('R'):
            register_index = int(operand[1:])
            return self.data_registers[register_index]
        elif operand.startswith('#'):
            return int(operand[1:])
        elif operand.startswith('M'):
            address = self.parse_memory_operand(operand)
            return self.memory.get_data(address)
        else:
            print("Error: Unsupported operand type")
            return 0  # Return a default value if unsupported

    def store_result(self, destination, result):
        if destination.startswith('R'):
            register_index = int(destination[1:])
            self.data_registers[register_index] = result
        else:
            print("Error: Unsupported destination operand")

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
            source = self.data_registers[int(source[1:])]
        elif source.startswith('M'):
            source = self.memory.get_data(self.parse_memory_operand(source))
        else:
            print("Error: Unsupported source operand")
            return

        # Handle different destination operand types: data registers, memory locations
        if destination.startswith('R'):
            dest_register = int(destination[1:])
            self.data_registers[dest_register] = source
        elif destination.startswith('M'):
            self.memory.set_data(self.parse_memory_operand(destination), source)
        else:
            print("Error: Unsupported destination operand")

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
            print("Error: Division by zero")
            return

        self.store_result(operands[0], result)
        print('DIV', operands)

    def cmp(self, operands):
        if len(operands) != 2:
            print("Error: CMP instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])

        self.flags['ZF'] = operand1 == operand2
        self.flags['SF'] = (operand1 - operand2) < 0
        self.flags['CF'] = operand1 < operand2
        self.flags['OF'] = ((operand1 - operand2) > 2147483647) or ((operand1 - operand2) < -2147483648)

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
            self.stack_pointer.append(operands[0])

        print('CALL', operands)

    def ret(self, operands):
        if operands:
            self.program_counter = self.stack_pointer.pop()

        print('RET', operands)

    def not_op(self, operands):
        if len(operands) != 1:
            print("Error: NOT instruction requires one operand")
            return

        operand = self.get_operand_value(operands[0])
        result = ~operand & 0xFFFFFFFF
        self.store_result(operands[0], result)
        print('NOT', operands)

    def and_op(self, operands):
        if len(operands) != 2:
            print("Error: AND instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])
        result = operand1 & operand2
        self.store_result(operands[0], result)
        print('AND', operands)

    def or_op(self, operands):
        if len(operands) != 2:
            print("Error: OR instruction requires two operands")
            return

        operand1 = self.get_operand_value(operands[0])
        operand2 = self.get_operand_value(operands[1])
        result = operand1 | operand2
        self.store_result(operands[0], result)
        print('OR', operands)

    def xor_op(self, operands):
        if len(operands) != 2:
            print("Error: XOR instruction requires two operands")
            return

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