from interface.screens.screen import Screen


class YesNoScreen(Screen):
    """A screen that handles a yes or no question"""

    def __init__(self, text: str, yes_screen: Screen | None = None, no_screen: Screen | None = None):
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