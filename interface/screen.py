from abc import ABC


class Screen(ABC):
    """The abstract base class for screens."""
    def __init__(self, text: str = ""):
        self.text = text


class InfoScreen(Screen):
    """A screen that simply displays text. Usually waits until the user presses ENTER to continue"""
    def __init__(self, text: str = ""):
        """Create a screen that displays text
        text: The text to display"""
        super().__init__(text)


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


class UnnumberedMenuScreen(Screen):
    """A screen with unnumbered options"""

    def __init__(self, text: str = "", options: list[str] = None, show_options: bool = True):
        """Create a menu that displays a question"""
        super().__init__(text)
        self.options = options
        if show_options and self.options is not None:
            for option in options:
                self.text += (option + "\n")

    def get_options(self) -> list[str]:
        """Get a string array of the options associated with this menu"""
        options_text = []
        if self.options is None:
            return options_text

        for option in self.options:
            options_text.append(option)
        return options_text


class NumberedMenuScreen(Screen):
    """A numbered menu where the user can select a specific option"""

    def __init__(self, text: str = "", options: list[str, Screen] = None):
        """Create a menu that displays a list of numbered options to the user
        text: The text for the menu, not including the options
        options: An array of the possible options.
        Do not number the options."""
        super().__init__(text)
        self.options = options
        for option in self.get_numbered_options():
            self.text += (option + "\n")

    def get_numbered_options(self) -> list[str]:
        """Get the list of options, numbered"""
        numbered_options = []
        if self.options is None:
            return numbered_options

        for i in range(len(self.options)):
            numbered_options.append(f"{i+1}. {self.options[i]}")

        return numbered_options
    
    def get_options_count(self) -> int:
        """Get how many options are presented on this menu"""
        if self.options is None:
            return 0
        return len(self.options)
