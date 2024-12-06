from typing import Callable


import game
import interface.text_manager as tm
import tkinter as tk


class GameWindow(tk.Tk):
    """The main game window"""

    def __init__(self, tick_function: Callable[[], None]):
        """Create the main game window"""
        super().__init__()
        self.title("Epic Quest: Text Quest")
        self.configure(bg="#000")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Initialization event
        self.bind("<Visibility>", lambda event: self.on_load())

        self.text_frame = tk.Frame(self)
        self.text_frame.grid(column=0, row=0, sticky="NSEW")

        self.text_box = tk.Text(self.text_frame, bg="#000", fg="#FFF", font="Consolas 20", wrap="word")
        self.text_box.bind("<Key>", lambda event: "break")
        self.text_box.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(self)
        self.entry_frame.grid(column=0, row=1, sticky="NSEW")

        self.entry_box = tk.Entry(self.entry_frame, bg="#000", fg="#FFF", font="Consolas 20")
        self.entry_box.bind("<Return>", lambda _: self.get_text())
        self.entry_box.pack(fill="both", expand=True)

        self.window_x = 960
        self.window_y = 540

        self.geometry(f"{self.window_x}x{self.window_y}")

        # Game stuff
        self.text_manager = tm.TextManager(self, self.text_box)
        self.tick_function = tick_function

    def append_to_screen(self, text: str, end: str = "\n"):
        self.text_manager.add(tm.TextToAdd(text, end))

    def typewriter(self, text: str, char_delay: int, end: str):
        self.text_manager.add(tm.TextToTW(text, char_delay, end))

    def clear_text(self):
        self.text_box.delete("1.0", "end")

    def on_load(self):
        """Triggered when the window has loaded"""
        self.unbind("<Visibility>")
        self.after(game.Game.TICK_RATE, self.tick_function)

    def get_text(self):
        """Called when the user presses enter on the text entry box"""
        if self.text_manager.running:
            return
        self.entry_box.delete("0", "end")
        
        return self.entry_box.get()
