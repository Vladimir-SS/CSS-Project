import tkinter as tk
from tkinter import filedialog
from Screen import Screen
from Keyboard import Keyboard
from Processor import Processor
from Memory import Memory


class GUI:
    def __init__(self, memory: Memory, keyboard: Keyboard, screen: Screen, buttons_per_row=16):
        self.processor = Processor(memory)
        self.keyboard = keyboard
        self.screen = screen
        self.buttons_per_row = buttons_per_row
        self.interval = 500  # ms

        self.root = tk.Tk()
        self.root.title("Peripheral Devices Simulation")

        self.screen_frame = tk.Frame(self.root)
        self.screen_frame.pack()

        self.screen_text = tk.Text(self.screen_frame, width=screen.width, height=screen.height)
        self.screen_text.pack()

        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.pack()

        self.create_keyboard_buttons()
        self.processor.memory.set_keyboard_pointer(keyboard)

        select_file_button = tk.Button(self.keyboard_frame, text="Select Assembly File", height=2,
                                       command=self.select_asm_file)
        select_file_button.grid(row=2, column=self.buttons_per_row)

        self.run_program()

        self.root.mainloop()

    def select_asm_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Assembly files", "*.asm")])
        if file_path:
            self.processor.set_file_name(file_path)

    def run_program(self):
        self.processor.execute_program()
        self.update_screen()
        self.root.after(self.interval, self.run_program)

    def create_keyboard_buttons(self):
        for row in range(4):
            for col in range(self.buttons_per_row):
                char_code = row * self.buttons_per_row + col + 32
                char_str = chr(char_code)
                if char_code < 127:
                    self.create_button(char_str, int(ord(char_str) / self.buttons_per_row),
                                       ord(char_str) % self.buttons_per_row)

        self.create_button('\r', 3, self.buttons_per_row, "Enter", width=12)

    def create_button(self, char_str, row, col, name=None, width=5, height=2):
        button_text = name if name else char_str
        button = tk.Button(self.keyboard_frame, text=button_text, width=width, height=height,
                           command=lambda c=char_str: self.key_press(c))
        button.grid(row=row, column=col)

    def key_press(self, char):
        self.keyboard.input_character(ord(char))

    def update_screen(self):
        self.screen_text.delete(1.0, tk.END)
        video_memory = self.processor.memory.read_video_memory()
        for i, char_code in enumerate(video_memory):
            if char_code is not None:
                self.screen_text.insert(tk.END, chr(char_code))
            if (i + 1) % self.screen.width == 0:
                self.screen_text.insert(tk.END, '\n')