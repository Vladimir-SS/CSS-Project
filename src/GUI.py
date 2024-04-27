import tkinter as tk
import threading
from Screen import Screen
from Keyboard import Keyboard
from Processor import Processor

class GUI:
    def __init__(self, processor: Processor, keyboard: Keyboard, screen: Screen):
        self.processor = processor
        self.keyboard = keyboard
        self.screen = screen

        self.root = tk.Tk()
        self.root.title("Peripheral Devices Simulation")

        self.screen_frame = tk.Frame(self.root)
        self.screen_frame.pack()

        self.screen_text = tk.Text(self.screen_frame, width=screen.width, height=screen.height)
        self.screen_text.pack()

        self.root.bind('<KeyPress>', self.key_press)

        # self.observe_memory_thread = threading.Thread(target=self.observe_memory)
        # self.observe_memory_thread.daemon = True
        # self.observe_memory_thread.start()

        self.root.mainloop()

    def key_press(self, event): # mby remove this and use keyboard.input_character directly
        self.keyboard.input_character(self.processor.memory, ord(event.char))
        self.processor.observe_memory()
        self.update_screen()

    def update_screen(self):
        self.screen_text.delete(1.0, tk.END)
        video_memory = self.processor.memory.read_video_memory()
        for i, char_code in enumerate(video_memory):
            if char_code is not None:
                self.screen_text.insert(tk.END, chr(char_code))
            if (i + 1) % self.screen.width == 0:
                self.screen_text.insert(tk.END, '\n')

    def observe_memory(self):
        while True:
            self.processor.observe_memory()  # Call processor's observe_memory method
            self.root.update() # Update GUI
            self.update_screen()  # Update screen text