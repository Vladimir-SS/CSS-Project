class Keyboard:
    """
    Represents a simulated keyboard peripheral device.

    Methods:
    - input_character(memory, character): Simulates inputting a character into the keyboard buffer.
    """
    def input_character(self, memory, character):
        """
        Simulates inputting a character into the keyboard buffer.

        Parameters:
        - memory (Memory): An instance of the Memory class representing the system's memory.
        - character (str): The character to be input into the keyboard buffer.
        """
        memory.set_keyboard_value(character)