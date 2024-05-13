# Specifications

#   The main components of the system are:

    # the processor
    # the memory
    # the peripheral devices

#   Processor specifications

    # The processor has 8 data registers, each of them 16-bit wide, and a set of conditional flags (see below). It also possible to define special-purpose registers (e.g., stack pointer or program counter).
    # The processor's instructions perform the following operations:
        # assignment
        # addition, subtraction, multiplication, division
        # Boole operations: NOT, AND, OR, XOR, shift
        # comparison: sets the internals flags depending on the relation between the two operands (==, !=, <, >, <=, >=)
        # jumps: unconditional, conditional (based on the flags set by previous comparison)
        # push/pop (using part of the system memory as a stack)
        # function call/return (also using the stack)
        # For each unary operation, the operand also stores the result (where needed).
        # Each binary operation is implemented by an instruction with 2 operands, and the first operand is also the destination where the result is stored.
        # The operands (always 16-bit wide) may be:
            # data registers
            # memory locations
            # constant values
    # The instructions executed by the processor are read from a text file, where they are written in an assembly-like language.

#   Memory specifications

    # There are two separate memory spaces for the instruction codes and for the program data, respectively.
    # The sizes of the two memory components are set up through the program's configuration file and must comply with the following restrictions:
        # each size must be a multiple of 1 KB ( = 1024 bytes)
        # each size may not exceed 65536 ( = 216) bytes
    # Whenever an instruction uses a memory location as an operand, the address is specified either by a constant value or by a data register.
    # Because all operands are 16-bit wide, any read/write operation to the data memory is accessing two consecutive addresses at once.
    # For the instruction memory, each instruction is considered to occupy 1 byte. The address of each instruction is equal to the line number in the input text file.

#   Peripheral devices specifications

    # There are two peripheral devices: the keyboard and the screen.
    # The keyboard is simulated by a FIFO buffer, which can be read by the processor.
    # The screen is simulated by a video memory, which can be written by the processor. The screen is a text display, of rectangular shape.
    # The peripheral devices are accessible through a graphical interface, which allows the user to input data to the keyboard buffer and see the screen.
    # Both devices are mapped into the data memory:
        # The keyboard buffer is allocated a single address, which is repeatedly read by the processor in order to get the characters input by the user.
        # The screen is allocated a range of consecutive addresses, equal in size to the number of characters of the screen. Each byte in that range corresponds to a character on the screen, starting with the upper-left corner and moving right, then down. Any write to a location in the video memory will have immediate effect on the corresponding character on the screen.
        # The addresses allocated to the devices in the data memory are set up through the program's configuration file.
    # Unlike the memory cells, the peripheral devices are accessed on 8 bits:
        # Whenever a byte is read from the address associated with the keyboard buffer, only the lower byte of the destination operand is overwritten.
        # Also, when video memory is accessed, only the lower byte of the source operand is written to the destination address.

from Processor import Processor
from Memory import Memory
from GUI import GUI
from Screen import Screen
from Keyboard import Keyboard

def read_config_file(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        config = {}
        for line in lines:
            key, value = line.split(":")
            config[key.strip()] = int(value.strip())
        return config

config = read_config_file('config.cfg')

memory = Memory(config['instruction_memory_size'], config['data_memory_size'], config['keyboard_buffer'], config['video_memory_start'], config['video_memory_end'])
program = Processor(memory, 'asm-example-file.txt')

gui = GUI(program, Keyboard(), Screen(100, 16))

print("\n\nDATA MEMORY: size:=", len(memory.data_memory))
count = 0
for mem in memory.data_memory:
    count += 1
    if mem is not None:
        print(count, ":", mem)

print("INSTRUCTION MEMORY: ", memory.instruction_memory)
print("REGISTERS VALUES: ", program.data_registers)
print("STACK:", program.stack_pointer)
print("LABELS:", memory.labels)
