from collections import deque
class Keyboard:
    """
    Represents a simulated keyboard peripheral device.

    Attributes:
    - key_queue (deque): A queue to store characters pressed on the keyboard.

    Methods:
    - input_character(character): Simulates inputting a character into the keyboard buffer.
    - get_next_character(): Retrieves the next character from the keyboard buffer.
    - has_characters(): Checks if there are characters in the keyboard buffer.
    """
    def __init__(self):
        """
        Initializes the Keyboard object with an empty queue to store characters.
        """
        self.key_queue = deque()

    def input_character(self, character):
        """
        Simulates inputting a character into the keyboard buffer.

        Parameters:
        - character (str): The character to be input into the keyboard buffer.
        """
        self.key_queue.append(character)

    def get_next_character(self):
        """
        Retrieves the next character from the keyboard buffer.

        Returns:
        - str: The next character from the keyboard buffer, or None if the buffer is empty.
        """
        if self.key_queue:
            return self.key_queue.popleft()
        return None

    def has_characters(self):
        """
        Checks if there are characters in the keyboard buffer.

        Returns:
        - bool: True if there are characters in the buffer, False otherwise.
        """
        return len(self.key_queue) > 0