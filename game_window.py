from tkinter import *


class GameWindow:
    """The main game window"""

    def __init__(self):
        """Create the main game window"""
        self.root = None
        self.text_frame = None
        self.text_box = None
        self.entry_frame = None
        self.entry_box = None

        self.window_x = 600
        self.window_y = 450

        self.__configure_window()

    def __configure_window(self):
        """Initialize widgets"""
        self.root = Tk()
        self.root.title("Epic Quest: Text Quest")
        self.root.configure(bg="#000")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.text_frame = Frame(self.root)
        self.text_frame.grid(column=0, row=0, sticky="NSEW")

        self.text_box = Text(self.text_frame, bg="#000", fg="#FFF", font="Consolas 18")
        self.text_box.pack(fill="both", expand=True)

        self.entry_frame = Frame(self.root)
        self.entry_frame.grid(column=0, row=1, sticky="NSEW")

        self.entry_box = Entry(self.entry_frame, bg="#000", fg="#FFF", font="Consolas 18")
        self.entry_box.pack(fill="both", expand=True)

        self.root.geometry(f"{self.window_x}x{self.window_y}")

    def show_window(self):
        self.root.mainloop()


if __name__ == "__main__":
    window = GameWindow()
    window.show_window()