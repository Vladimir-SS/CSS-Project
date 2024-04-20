class Memory:
    def __init__(self, instruction_memory_size, data_memory_size):
        self.instruction_memory_size = instruction_memory_size
        self.data_memory_size = data_memory_size
        self.instruction_memory = [None] * instruction_memory_size
        self.data_memory = [None] * data_memory_size
        self.keyboard_buffer = None
        self.screen = None