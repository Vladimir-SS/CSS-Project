class Screen:
    """
    Represents a screen simulated by video memory. ( used only to store the screen dimensions)

    Attributes:
    - width (int): The width of the screen.
    - height (int): The height of the screen.
    """
    def __init__(self, width, height):
        """
        Initializes the Screen object with the specified width and height.
        """
        self.width = width
        self.height = height