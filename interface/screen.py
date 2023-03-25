from abc import ABC
from typing import Callable


class Screen(ABC):
    """The abstract base class for screens"""

    def __init__(self, text: str = ""):
        self.text = text


class InfoScreen(Screen):
    """A screen that simply displays text. Usually waits until the user presses ENTER to continue"""

    def __init__(self, text: str = "", next_screen: Screen = None, next_function: Callable[[str], None] = None):
        """Create a screen that displays text
        text: The text to display
        next_screen: The screen that should be displayed after pausing
        next_function: The function that should be called after pausing. This function takes a str parameter, which is the text input of the user"""
        super().__init__(text)
        self.next_screen = next_screen
        self.next_function = next_function

    def has_next_screen(self) -> bool:
        return self.next_screen is not None

    def has_next_function(self) -> bool:
        return self.next_function is not None


class YesOrNoScreen(Screen):
    """A screen that handles a yes or no question"""

    def __init__(self, text: str = "", yes_screen: Screen = None, no_screen: Screen = None):
        """Create a new yes or no screen
        text: The text to display at the top of the screen
        yes_screen: The screen to display if the user enters 'Yes'
        no_screen: The screen to display if the user enters 'No'"""
        super().__init__(text)
        self.yes_screen = yes_screen
        self.no_screen = no_screen

    def has_yes_screen(self) -> bool:
        return self.yes_screen is not None

    def has_no_screen(self) -> bool:
        return self.no_screen is not None


class UnnumberedMenuScreen(Screen):
    """A screen with unnumbered options"""

    def __init__(self, text: str = "", options: dict[str, Screen | Callable[[str], None]] = None,
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
        if self.show_options:
            self.text += (option + "\n")


class NumberedMenuScreen(Screen):
    """A numbered menu where the user can select a specific option"""

    def __init__(self, text: str = "", options: dict[str, Screen | Callable[[str], None]] = None):
        """Create a menu that displays a list of numbered options to the user
        text: The text for the menu, not including the options
        options: A dictionary of the possible options.
        Do not number the options."""
        super().__init__(text)
        self.options = options
        if self.options is not None:
            for option in self.get_numbered_options():
                self.text += (option + "\n")

    def get_numbered_options(self) -> list[str] | None:
        """Get the list of options, numbered"""
        numbered_options = []
        if self.options is None:
            return None

        for i in range(len(self.options)):
            option_text = list(self.options.keys())[i]
            numbered_options.append(f"{i + 1}. {option_text}")

        return numbered_options

    def get_options_count(self) -> int:
        """Get how many options are presented on this menu"""
        if self.options is None:
            return 0
        return len(self.options)

    def get_next_screen(self, choice: int) -> Screen | None:
        """Gets the next screen associated with the provided option. Returns none if there isn't one
        choice: The option selected by the user"""
        try:
            option = list(self.options.keys())[choice-1]
        except IndexError:
            return None
        if isinstance(self.options[option], Screen):
            return self.options[option]
        return None

    def get_next_function(self, choice: int) -> Callable[[str], None] | None:
        """Gets the function associated with the provided option. Returns none if there isn't one
        choice: The option selected by the user"""
        try:
            option = list(self.options.keys())[choice]
        except IndexError:
            return None
        if isinstance(self.options[option], Callable):
            return self.options[option]
        return None

    def add_option(self, option: str, next_action: Screen | Callable[[str], None]):
        """Add a new option to the menu.
        option: The option to add
        next_action: The screen to be shown or the function to be called after this screen"""
        if self.options is None:
            self.options = dict()
        self.options[option] = next_action

        number = self.get_options_count()
        self.text += f"{number}. {option}\n"
