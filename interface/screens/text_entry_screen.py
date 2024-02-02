from interface.screens.screen import Screen
from typing import Callable


class TextEntryScreen(Screen):
    """A screen for getting text input from the user"""

    def __init__(self, text: str, options: dict[str, Screen | Callable[[str], None]] | None = None,
                 show_options: bool = True):
        """Create a menu that displays a question
        options: The possible options the user can select and the associated outcome.
        If the option is *, the user can enter anything
        If the option is \"\", the user must press ENTER
        show_options: If this is true, the options will be displayed on the screen"""
        super().__init__(text)
        self.options = options
        self.show_options = show_options
        if self.show_options and self.options is not None:
            for option in options.keys():
                self.text += (option + "\n")

    def get_options(self) -> list[str] | None:
        """Get a string array of the options associated with this menu"""
        options_text = []
        if self.options is None:
            return None

        for option in self.options.keys():
            options_text.append(option)
        return options_text

    def get_next_screen(self, option: str) -> Screen | None:
        """Gets the next screen associated with the provided option. Returns none if there isn't one
        option: The option selected by the user"""
        if option in self.options.keys() and isinstance(self.options[option], Screen):
            return self.options[option]
        return None

    def get_next_function(self, option: str) -> Callable[[str], None] | None:
        """Gets the function associated with the provided option. Returns none if there isn't one
        option: The option selected by the user"""
        if option in self.options.keys() and isinstance(self.options[option], Callable):
            return self.options[option]
        return None

    def has_wildcard_option(self) -> bool:
        """Check if there is a wildcard option for this menu"""
        for option in self.options.keys():
            if option == "*":
                return True
        return False

    def has_enter_option(self) -> bool:
        """Check if there is a ENTER option for this menu"""
        for option in self.options.keys():
            if option == "":
                return True
        return False

    def add_option(self, option: str, next_action: Screen | Callable[[str], None]):
        """Add a new option to the menu.
        option: The option to add
        next_action: The screen to be shown or the function to be called after this screen"""
        if self.options is None:
            self.options = dict()
        self.options[option] = next_action
        if self.show_options and option != "":
            self.text += (option + "\n")
