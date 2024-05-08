from Exceptions import MemoryOverflowError
from Exceptions import InvalidMemoryAddrError
class Memory:
    """
    Represents the memory component of the system.

    This class manages the instruction memory, data memory, and peripheral devices
    such as the keyboard buffer and video memory. It provides methods for accessing
    and manipulating data within these memory components.

    Attributes:
        MAX_MEMORY_SIZE (int): Maximum memory size in bytes.
        MIN_MEMORY_SIZE (int): Minimum memory size in bytes.
        instruction_memory (list): List to store program instructions.
        data_memory (list): List to store data, including special areas for peripherals.
        keyboard_buffer_address (int): Address of the keyboard buffer in data memory.
        video_memory_start (int): Start address of video memory in data memory.
        labels (dict): Dictionary to store labels and their corresponding addresses.

    Methods:
        __init__: Initializes the Memory object.
        set_keyboard_value: Sets the value in the keyboard buffer.
        get_keyboard_pointer: Gets the value from the keyboard buffer.
        write_to_video_memory: Writes a value to the video memory.
        read_video_memory: Reads the content of video memory.
        get_instruction: Retrieves instruction from the given address.
        add_instruction: Adds an instruction to the instruction memory.
        set_data: Sets data at the specified address in data memory.
        goto_label: Jumps to the address associated with the specified label.
        check_instruction_memory_overflow: Checks for overflow in instruction memory.
        check_instruction_memory_address: Checks if the address is within bounds of instruction memory.
        check_data_memory_overflow: Checks for overflow in data memory.
        check_memory_address: Checks if the address is within bounds of data memory and not the keyboard buffer.
        validate_memory_size: Validates the memory size.
    """
    MAX_MEMORY_SIZE = 65536  # Maximum memory size in bytes
    MIN_MEMORY_SIZE = 1024   # Minimum memory size in bytes

    def __init__(self, instruction_memory_size, data_memory_size, keyboard_buffer_address, video_memory_start):
        """
        Initializes the Memory object.

        Parameters:
            instruction_memory_size (int): Size of instruction memory.
            data_memory_size (int): Size of data memory.
            keyboard_buffer_address (int): Address of the keyboard buffer.
            video_memory_start (int): Start address of video memory.

        Raises:
            InvalidMemoryAddrError: If keyboard buffer or video memory address is out of bounds.
        """
        self.validate_memory_size(instruction_memory_size)
        self.validate_memory_size(data_memory_size)

        self.instruction_memory_size = instruction_memory_size
        self.data_memory_size = data_memory_size

        self.instruction_memory = []
        self.data_memory = [None] * data_memory_size

        # Peripheral devices
        self.keyboard_buffer_address = keyboard_buffer_address
        if keyboard_buffer_address >= data_memory_size:
            raise InvalidMemoryAddrError("Keyboard buffer address out of bounds")

        self.video_memory_start = video_memory_start
        if video_memory_start >= data_memory_size:
            raise InvalidMemoryAddrError("Video memory address out of bounds")

        # Additional helper variables
        self.labels = {}

    def set_keyboard_pointer(self, ptr):
        """
        Sets the pointer to the Keyboard instance in the keyboard buffer.

        Parameters:
            ptr: Keyboard instance to be set in the keyboard buffer.
        """
        self.data_memory[self.keyboard_buffer_address] = ptr

    def get_keyboard_pointer(self):
        """
        Gets the Keyboard instance from the keyboard buffer.

        Returns:
            The Keyboard instance from the keyboard buffer, or None if no instance is set.
        """
        if self.data_memory[self.keyboard_buffer_address] is None:
            return None

        return self.data_memory[self.keyboard_buffer_address]

    def write_to_video_memory(self, value):
        """
        Writes a value to the video memory.

        Parameters:
            value: Value to be written to the video memory.
        """
        for i in range(self.video_memory_start, len(self.data_memory)):
            if self.data_memory[i] is None:
                self.data_memory[i] = value
                return

    def read_video_memory(self):
        """
        Reads the content of video memory.

        Returns:
            The content of video memory.
        """
        return self.data_memory[self.video_memory_start:self.keyboard_buffer_address]

    def get_instruction(self, address):
        """
        Retrieves instruction from the given address.

        Parameters:
            address (int): Address of the instruction.

        Returns:
            Instruction at the specified address.

        Raises:
            InvalidMemoryAddrError: If the address is out of bounds.
        """
        if self.check_instruction_memory_address(address):
            return self.instruction_memory[address]
        else:
            raise InvalidMemoryAddrError("Invalid instruction memory address")

    def add_instruction(self, instruction, label = None):
        """
        Adds an instruction to the instruction memory.

        Parameters:
            instruction: Instruction to be added.
            label (str): Optional label associated with the instruction.
        """
        self.check_instruction_memory_overflow(len(self.instruction_memory))
        self.instruction_memory.append(instruction)
        if label is not None:
            self.labels[label] = len(self.instruction_memory) - 1

    def set_data(self, address, value):
        """
        Sets data at the specified address in data memory.

        Parameters:
            address (int): Address in data memory.
            value: Value to be set.

        Raises:
            InvalidMemoryAddrError: If the address is out of bounds.
        """
        self.check_memory_address(address)
        self.data_memory[address] = value

    def goto_label(self, label):
        """
        Jumps to the address associated with the specified label.

        Parameters:
            label (str): Label to jump to.

        Returns:
            Address associated with the label.

        Raises:
            ValueError: If the label is not found.
        """
        if label not in self.labels:
            raise ValueError("Label not found: ", label)
        return self.labels[label]

    # Helper methods for validations

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
        if address == self.keyboard_buffer_address:
            raise InvalidMemoryAddrError("Cannot overwrite keyboard buffer")

    def validate_memory_size(self, size):
        """
        Validates the memory size.

        Parameters:
            size (int): Size of memory.

        Raises:
            ValueError: If the size is not a multiple of 1 KB or exceeds the maximum size.
        """
        if size % Memory.MIN_MEMORY_SIZE != 0 or size > Memory.MAX_MEMORY_SIZE:
            raise ValueError("Memory size must be a multiple of 1 KB (1024 bytes) and not exceed 65536 bytes")