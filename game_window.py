from tkinter import *


class GameWindow:
    """The main game window"""

    def __init__(self):
        """Create the main game window"""
        self.root = None
        self.text_box = None

        self.window_x = 1280
        self.window_y = 720

        self.__configure_window()

    def __configure_window(self):
        """Initialize widgets"""
        self.root = Tk()
        self.root.title("Epic Quest: Text Quest")
        self.root.configure(bg="#000")

        self.text_box = Text(self.root, bg="#000", fg="#FFF", font="Consolas 18")
        self.text_box.pack(fill="both")

        self.root.geometry(f"{self.window_x}x{self.window_y}")

    def show_window(self):
        self.root.mainloop()


if __name__ == "__main__":
    window = GameWindow()
    window.show_window()