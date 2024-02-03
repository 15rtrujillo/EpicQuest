from interface.screens.screen import Screen
from typing import Callable


class InfoScreen(Screen):
    """A screen that simply displays text. Usually waits until the user presses ENTER to continue"""

    def __init__(self, text: str, next_screen: Screen | None = None,
                 next_function: Callable[[str], None] | None = None):
        """
        Create a screen that displays text
        :param str text: The text to display
        :param Screen | None next_screen: The screen that should be displayed after pausing
        :param Callable[[str], None] | None next_function: The function that should be called after pausing.
        This function takes a str parameter, which is the text input of the user"""
        super().__init__(text)
        self.next_screen = next_screen
        self.next_function = next_function

    def has_next_screen(self) -> bool:
        return self.next_screen is not None

    def has_next_function(self) -> bool:
        return self.next_function is not None
