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


class NumberedMenuScreen(Screen):
    """A numbered menu where the user can select a specific option"""

    def __init__(self, text: str = "", options: list[str] = None):
        """Create a menu that displays a list of numbered options to the user
        text: The text for the menu, not including the options
        options: An array containing the possible options. Do not number the options"""
        super().__init__(text)
        self.options = options
        for option in self.get_numbered_options():
            self.text += (option + "\n")

    def get_numbered_options(self) -> list[str]:
        """Get the list of options, numbered"""
        numbered_options = []
        for i in range(len(self.options)):
            numbered_options.append(f"{i+1}. {self.options[i]}")

        return numbered_options
    
    def get_options_count(self) -> int:
        """Get how many options are presented on this menu"""
        return len(self.options)
