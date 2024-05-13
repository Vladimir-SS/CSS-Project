## Terms definitions

- `Registor` = Small, fast storage locations directly within the CPU, used to hold temporary data that the processor needs during the execution of programs, such as operands for arithmetic operations, address pointers for accessing memory, or intermediate results and special states of the machine. These registers are much faster to access than main memory, which is why processors use them for immediate operations.
- `Conditional Flags` = Used for decision-making (e.g., comparison results), reflecting how real CPUs manage operations and control flow. They are set or cleared after the outcome of each operation. [More about conditional flags](http://unixwiz.net/techtips/x86-jumps.html)
```python
self.flags = {
	'CF': False,  # Carry Flag: is set when an arithmetic operation generates a carry or borrows from the most significant bit; used in testing for overflow in signed integer arithmetic
	'PF': False,  # Parity Flag: is set only when the least significant byte of the result has an even number of 1 bits
	'ZF': False,  # Zero Flag: is set when the result of an operation is 0
	'SF': False,  # Sign Flag: holds the value of the most significant bit of the result; indicates the sign of a signed integer (0 = positive, 1 = negative)
	'OF': False   # Overflow Flag: is set when an overflow occurs in signed integer arithmetic
}
```

- `Program Counter (PC)`: Points to the next instruction to execute.
- `Stack Pointer (SP)`: Points to the current top of the stack in memory, used for push/pop operations. More about [stack in assembly](https://www.cs.ubbcluj.ro/~vancea/asc/stack_in_assembly.php)

## Main classes

### Processor
- holds data registers and flags
- executes instructions (assignment, addition, substraction, multiplication, division, boolean op, comparison, jumps, push/pop and function call/return using a part of memory as stack)

The processor reads and parses the entire instruction set from the file and stores it in the instruction memory at the start. During execution, the processor fetches each instruction based on the program counter (PC), processes it, and then moves to the next one.

The keyboard buffer is allocated a single address - this address is part of the data memory and is **checked by the processor** to see if there's any new input (the processor will periodically check this address to see if it contains any new data (non-zero value), process the data if present, and then reset the buffer).
#### Attributes:
- `data_registers`: List to store the values of the 8 data registers.
- `flags`: Dictionary to store the values of conditional flags (CF, PF, ZF, SF, OF).
- Special registers:
  - `stack_pointer`: List to simulate stack operations. ( the stack pointer is in the list so we don't need to store it separately)
  - `program_counter`: Points to the current instruction being executed.
- Additional attributes:
  - `memory`: Reference to the memory class to access memory locations.
  - `instruction_types`: Dictionary mapping instruction names to their respective methods.
  - `is_file_parsed (bool)`: Indicates whether the file has been parsed.
  - `file_name (str)`: Name of the file containing instructions.
  - Keyboard input handling:
    - `is_reading_input (bool)`: Indicates whether the processor is waiting for keyboard input.
    - `input (str)`: Keyboard input string.
    - `input_destination (str)`: Destination operand for keyboard input.
##### Methods:
- `set_file_name`: Set the name of the file containing instructions to be executed.
- `execute_instruction(instruction)`: Executes a single instruction.
- `execute_program(file_name)`: Execute instructions from a file sequentially.
- `parse_instruction(instruction)`: Parses a single instruction from the program file and adds it to the instruction list. (in case of a label, it stores the label and its corresponding instruction index in the labels dictionary).
- `parse_file(file_name)`: Reads the program file and parses each instruction.
- `parse_memory_operand`: Parses a memory operand to determine its address.
- `check_register_index(index)`: Checks if the given index is a valid register index.
- `get_operand_value(operand)`: Returns the value of an operand (register, memory location, or constant value).
- `store_result(destination, result)`: Stores the result of an operation in the destination operand.
- `assert_16_bit(value)`: Truncates a value to fit within 16 bits.
- `reading_input`: Handles keyboard input.
- `get_memory_data(operand, destination)`: Gets the value of a memory operand. (starts reading input if keyboard buffer is accessed)
- `convert_keyboard_input(keyboard_input)`: Converts keyboard input to a numerical value or ASCII value.
- Methods for various instruction types such as `mov`, `add`, `sub`, `mul`, `div`, `cmp`, `jmp`, `je`, `jne`, `jg`, `jl`, `jge`, `jle`, `push`, `pop`, `call`, `ret`.
------------------------------------
### Memory
- stores both instruction and data memory
- handles read/write operations
##### Attributes:
- `MAX_MEMORY_SIZE`: Maximum memory size in bytes.
- `MIN_MEMORY_SIZE`: Minimum memory size in bytes.
- `instruction_memory`: List to store program instructions.
- `data_memory`: List to store data, including special areas for peripherals.
- `video_memory_start`: Start address of video memory.
- `video_memory_end`: End address of video memory.
- `keyboard_buffer`: Address of the keyboard buffer.
- `labels`: Dictionary to store labels and their corresponding addresses.
#### Methods:
- `set_keyboard_pointer(ptr)`: Sets the pointer to the Keyboard instance in the keyboard buffer.
- `get_keyboard_pointer`: Gets the Keyboard instance from the keyboard buffer.
- `read_video_memory()`: Reads the content of video memory.
- `get_instruction(address)`: Retrieves instruction from the given address.
- `add_instruction(instruction, label=None)`: Adds an instruction to the instruction memory.
- `set_data(address, value)`: Sets data at the specified address in data memory.
- `get_data(address)`: Gets data from the specified address in data memory.
- `goto_label(label)`: Jumps to the address associated with the specified label.
- `check_instruction_memory_overflow(address)`: Checks for overflow in instruction memory.
- `check_instruction_memory_address(address)`: Checks if the address is within bounds of instruction memory.
- `check_data_memory_overflow(address)`: Checks for overflow in data memory.
- `check_memory_address(address)`: Checks if the address is within bounds of data memory.
- `validate_memory_size(size)`: Validates the memory size.

-------------------------------------
## Assembly-Like Language Syntax

- **Assigment:** `MOV destination, source`
- **Arithmetic operations:**
  - `ADD destination, source`
  - `SUB destination, source`
  - `MUL destination, source`
  - `DIV destination, source`
- **Comparison:** `CMP operand1, operand2`
- **Jumps:**
  - `JMP label`
  - `JE label`
  - `JNE label`
  - `JG label`
  - `JL label`
  - `JGE label`
  - `JLE label`
- **Stack operations:**
  - `PUSH source`
  - `POP destination`
  - Function call/return:
      - `CALL label`
      - `RET`
- **Boolean operations:**
  - `NOT destination`
  - `AND destination, source`
  - `OR destination, source`
  - `XOR destination, source`
  - `SHL destination, source`
  - `SHR destination, source`
- **Data types:**
  - Data registers: `R0`, `R1`, `R2`, `R3`, `R4`, `R5`, `R6`, `R7`
  - Memory locations: `M<value>/<register>`
  - Constant values: `#<value>`