from interface.screens.screen import Screen


class YesNoScreen(Screen):
    """A screen that handles a yes or no question"""

    def __init__(self, text: str, yes_screen: Screen | None = None, no_screen: Screen | None = None):
        """
        Create a new yes or no screen
        :param str text: The text to display at the top of the screen
        :param Screen | None yes_screen: The screen to display if the user enters 'Yes'
        :param Screen | None no_screen: The screen to display if the user enters 'No'
        """
        super().__init__(text)
        self.yes_screen = yes_screen
        self.no_screen = no_screen

    def has_yes_screen(self) -> bool:
        """
        Check if there is a Screen associated with the user saying 'Yes'
        :rtype: bool
        :return: True if there is an associated screen, False otherwise
        """
        return self.yes_screen is not None

    def has_no_screen(self) -> bool:
        """
        Check if there is a Screen associated with the user saying 'No'
        :rtype: bool
        :return: True if there is an associated screen, False otherwise
        """
        return self.no_screen is not None
