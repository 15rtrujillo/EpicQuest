from screens.screen import *

import game_console
import tkinter as tk


# Reusable screens will be defined here
main_menu_screen = NumberedMenuScreen("Epic Quest: Text Quest\n\nMain Menu",
                                      ["New Game",
                                       "Load Game",
                                       "About",
                                       "Exit"])


class GameWindow:
    """The main game window"""

    def __init__(self):
        """Create the main game window"""
        # GUI Stuff
        self.root = tk.Tk()
        self.root.title("Epic Quest: Text Quest")
        self.root.configure(bg="#000")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.bind("<Visibility>", lambda event: self.show_main_menu())

        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(column=0, row=0, sticky="NSEW")

        self.text_box = tk.Text(self.text_frame, bg="#000", fg="#FFF", font="Consolas 20")
        self.text_box.bind("<Key>", lambda event: "break")
        self.text_box.pack(fill="both", expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(column=0, row=1, sticky="NSEW")

        self.entry_box = tk.Entry(self.entry_frame, bg="#000", fg="#FFF", font="Consolas 20")
        self.entry_box.bind("<Return>", lambda event: self.parse_text())
        self.entry_box.pack(fill="both", expand=True)

        self.window_x = 960
        self.window_y = 540

        self.root.geometry(f"{self.window_x}x{self.window_y}")

        # Game stuff
        self.screen = None

    def show_main_menu(self):
        """Creates and displays the main menu"""
        self.root.unbind("<Visibility>")
        self.display_screen(main_menu_screen)

    def display_screen(self, screen: Screen):
        """Adds a screen to the text box and sets it as the active screen
        screen: The screen to display"""
        self.screen = screen
        self.clear_text()
        self.update_text(screen.text + "\n")
        if isinstance(screen, NumberedMenuScreen):
            for option in screen.get_numbered_options():
                self.update_text(option + "\n")

    def parse_text(self):
        """This function will handle parsing the text of the game
        event: Unused"""
        text = self.entry_box.get()
        if self.screen is None:
            return
        elif isinstance(self.screen, NumberedMenuScreen):
            if self.screen is main_menu_screen:
                pass

    def show_window(self):
        """Display the window and start event listeners"""
        self.root.mainloop()

    def typewriter(self, text: str, delay: int = 50, index = 0):
        """Add text to the textbox with a typewriter effect
        text: The text to add
        delay: The delay between each character in ms
        index: Used in recursion, do not set"""
        self.update_text(text[index])
        index += 1
        if index < len(text):
            self.root.after(delay, lambda: self.typewriter(text, delay, index))

    def update_text(self, text: str):
        """Add text to the text box
        text: The text to add"""
        self.text_box.insert('end', text)

    def clear_text(self):
        """Clears the text box"""
        self.text_box.delete("1.0", "end")


def handle_main_menu(choice: int):
    """Handle inputs for the main menu screen
    choice: Which option the user selected"""
    if choice == 1:
        # New Game
        pass
    elif choice == 2:
        # Load Game
        pass
    elif choice == 3:
        # About
        pass
    elif choice == 4:
        # Quit
        pass


def parse_int_input(text_to_parse: str, number_of_choices: int = 0) -> int:
    """Parses int input. Returns -1 if the input is invalid in some way
    text_to_parse: The text to parse
    number_of_choices: If this is not 0, the parsed int will be range checked form one to this value (inclusive)"""
    try:
        int_input = int(text_to_parse)
        if number_of_choices == -1:
            return int_input
        if int_input in range(1, number_of_choices + 1):
            return int_input
        else:
            return -1
    except ValueError:
        return -1


if __name__ == "__main__":
    window = GameWindow()
    window.show_window()
