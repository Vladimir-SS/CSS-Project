from Exceptions import MemoryOverflowError
from Exceptions import InvalidMemoryAddrError
class Memory:
    MAX_MEMORY_SIZE = 65536  # Maximum memory size in bytes
    MIN_MEMORY_SIZE = 1024   # Minimum memory size in bytes

    def __init__(self, instruction_memory_size, data_memory_size, keyboard_buffer, video_memory_start):
        self.validate_memory_size(instruction_memory_size)
        self.validate_memory_size(data_memory_size)

        self.instruction_memory_size = instruction_memory_size
        self.data_memory_size = data_memory_size

        self.instruction_memory = []
        self.data_memory = [None] * data_memory_size

        # Peripheral devices
        self.keyboard_buffer = keyboard_buffer
        if keyboard_buffer >= data_memory_size:
            raise InvalidMemoryAddrError("Keyboard buffer address out of bounds")

        self.video_memory_start = video_memory_start
        if video_memory_start >= data_memory_size:
            raise InvalidMemoryAddrError("Video memory address out of bounds")

        # Additional helper variables
        self.labels = {}

    def set_keyboard_value(self, value):
        self.data_memory[self.keyboard_buffer] = value

    def get_keyboard_value(self):
        if self.data_memory[self.keyboard_buffer] is None:
            return None

        return self.data_memory[self.keyboard_buffer]

    def write_to_video_memory(self, value):
        # print("Writing to video memory: ", self.data_memory)
        for i in range(self.video_memory_start, len(self.data_memory)):
            if self.data_memory[i] is None:
                self.data_memory[i] = value
                return

    def read_video_memory(self):
        return self.data_memory[self.video_memory_start:]

    def get_instruction(self, address):
        self.check_instruction_memory_address(address)
        return self.instruction_memory[address]

    def add_instruction(self, instruction, label = None):
        self.check_instruction_memory_overflow(len(self.instruction_memory))
        self.instruction_memory.append(instruction)
        if label is not None:
            self.labels[label] = len(self.instruction_memory) - 1

    def set_data(self, address, value):
        self.check_memory_address(address)
        self.data_memory[address] = value

    def goto_label(self, label):
        if label not in self.labels:
            raise ValueError("Label not found: ", label)
        return self.labels[label]

    def check_instruction_memory_overflow(self, address):
        if address >= self.instruction_memory_size:
            raise MemoryOverflowError("Instruction memory overflow")

    def check_instruction_memory_address(self, address):
        if address >= self.instruction_memory_size or address < 0 or address is None or address >= len(self.instruction_memory):
            return False
        return True

    def check_data_memory_overflow(self, address):
        if address + 1 >= self.data_memory_size:
            raise MemoryOverflowError("Data memory overflow")

    def check_memory_address(self, address):
        if address >= self.data_memory_size or address < 0 or address is None:
            raise InvalidMemoryAddrError("Data memory overflow")

    def validate_memory_size(self, size):
        if size % Memory.MIN_MEMORY_SIZE != 0 or size > Memory.MAX_MEMORY_SIZE:
            raise ValueError("Memory size must be a multiple of 1 KB (1024 bytes) and not exceed 65536 bytes")