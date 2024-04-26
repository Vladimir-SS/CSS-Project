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
- `data_registers` - List to store the values of the 8 data registers.
- `flags` - Dictionary to store the values of conditional flags (CF, PF, ZF, SF, OF).
- Special registers:
  - `stack`: List to simulate stack operations. ( the stack pointer is in the list so we don't need to store it separately)
  - `program_counter`: Points to the current instruction being executed.
- Additional attributes:
  - `instructions`: List to store parsed instructions from the program file.
  - `labels`: Dictionary to store labels and their corresponding instruction indices.
  - `instruction_types`: Dictionary mapping instruction names to their respective methods.
- Types not used at the moment:
  - a reference to the `memory class` (to make operations)
  - might need references to the `peripherals addresses` in memory but not sure
```python
self.keyboard_address = config["keyboard_buffer_address"] self.video_memory_start = config["video_memory_start_address"] self.video_memory_size = config["video_memory_size"]
```
##### Methods:
- `execute_instruction(instruction)`: Executes a single instruction.
- `execute_program(file_name)`: Reads instructions from the text file, parses them, and executes them.
- `parse_instruction(instruction)`: Parses a single instruction from the program file and adds it to the instruction list. (in case of a label, it stores the label and its corresponding instruction index in the labels dictionary).
- `parse_file(file_name)`: Reads the program file and parses each instruction.
- `get_operand_value(operand)`: Returns the value of an operand (register, memory location, or constant value).
- `store_result(destination, result)`: Stores the result of an operation in the destination operand.
- Methods for various instruction types such as `mov`, `add`, `sub`, `mul`, `div`, `cmp`, `jmp`, `je`, `jne`, `jg`, `jl`, `jge`, `jle`, `push`, `pop`, `call`, `ret`.
- Additional methods:
  - `check_keyboard()`

------------------------------------
### Possible classes to use in the processor instead of raw data and checks

#### Instruction class
- one or two operands(binary operation, the first operand stores the result)
##### Attributes:
- `operation` - type of operation (ADD, SUB, JMP)
- `operands` - a list or tuple of operands (registers/memory addresses/immediate values)
- `flag_effects` - optional, indicates how the instruction affects conditional flags
##### Methods
- `execute(self, processor_context)` - executes the instruction using the provided processor context (registers, memory)

#### Operand class
- a 16 bit value
- an operand can be a data register, memory location or constant value

------------------------------------

### Memory
- stores both instruction and data memory
- handles read/write operations
##### Attributes:
- `instruction_memory` - array or list to store the programs instructions
- `data_memory` - array or list to store data, including special areas for peripherals
#### Methods:
- `read(address, is_data=True)` - returns the value stored at the specific address
- `write(address, value, is_data=True)` - writes a value to the specified address

-------------------------------------
### Peripherals classes

#### Keyboard Class
- simulates a keyboard input buffer
##### Attributes:
- `buffer` - a FIFO queue to simulate keypress
##### Methods:
- `read_key()`: Returns the next key from the buffer
- `simulate_keypress(key)`: Adds a keypress to the buffer

#### Screen Class
- simulates a text display screen
##### Attributes:
- `video_memory` - an array or list representing the screen's content
##### Methods:
- `write_to_screen(address, value)` - updates the screen's display based on the video memory address
- `refresh_display()` - optional, to refresh the simulated screen display in the GUI


-------------------------------------
### System class

With an instance of the processor, memory (should be passed to the processor), keyboard and screen

##### Methods:
- `load_configuration(config_file)` - reads the config file(`json`), validates the memory sizes and initializes the memory components
- `load_program(file_path)` - reads the instruction file, parses it and returns the list of instructions (each line from the file)
- `execute_program()` - calls the processor to start execution

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