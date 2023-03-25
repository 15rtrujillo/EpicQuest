from interface.screen import *
from interface.game import *


import tkinter as tk


class GameWindow(Game):
    """The main game window"""

    def __init__(self):
        """Create the main game window"""
        # GUI Stuff
        self.root = tk.Tk()
        self.root.title("Epic Quest: Text Quest")
        self.root.configure(bg="#000")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.bind("<Visibility>", lambda event: self.load_data())

        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(column=0, row=0, sticky="NSEW")

        self.text_box = tk.Text(self.text_frame, bg="#000", fg="#FFF", font="Consolas 20")
        self.text_box.bind("<Key>", lambda event: "break")
        self.text_box.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(column=0, row=1, sticky="NSEW")

        self.entry_box = tk.Entry(self.entry_frame, bg="#000", fg="#FFF", font="Consolas 20")
        self.entry_box.bind("<Return>", lambda event: self.get_text())
        self.entry_box.pack(fill="both", expand=True)

        self.window_x = 960
        self.window_y = 540

        self.root.geometry(f"{self.window_x}x{self.window_y}")

        # Game stuff
        super().__init__()

    def initialize(self):
        """Display the window and start event listeners"""
        # This automatically calls load_data()
        self.root.mainloop()

    def display_screen(self, screen: Screen):
        super().display_screen(screen)
        self.clear_text()
        self.text_box.insert("end", self.screen.text)

    def append_to_screen(self, text: str, end: str = "\n"):
        super().append_to_screen(text, end)
        self.text_box.insert('end', text + end)

    """GUI-specific functions"""

    def load_data(self):
        """This method is specific to the GUI and is used to call the initialize method
        on the superclass, because we want to wait until after the mainloop starts to do so"""
        self.root.unbind("<Visibility>")
        super().initialize()

    def clear_text(self):
        """Clears the text box"""
        self.text_box.delete("1.0", "end")

    def typewriter(self, text: str, delay: int = 50, index = 0):
        """Add text to the textbox with a typewriter effect
        text: The text to add
        delay: The delay between each character in ms
        index: Used in recursion, do not set"""
        self.append_to_screen(text[index], end="")
        index += 1
        if index < len(text):
            self.root.after(delay, lambda: self.typewriter(text, delay, index))

    def get_text(self):
        """Called when the user presses enter on the text entry box"""
        text = self.entry_box.get()
        self.entry_box.delete("0", "end")
        super().parse_text(text)
