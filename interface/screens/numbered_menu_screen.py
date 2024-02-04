from interface.screens.screen import Screen
from typing import Callable


class NumberedMenuScreen(Screen):
    """A numbered menu where the user can select a specific option"""

    def __init__(self, text: str, options: dict[str, Screen | Callable[[str], None]] | None = None):
        """
        Create a menu that displays a list of numbered options to the user
        :param str text: The text for the menu, not including the options
        :param dict[str, Screen | Callable[[str], None]] | None options: The possible options the user can select
        and the associated outcome.
        Do not number the options.
        """
        super().__init__(text)
        self.options = options
        if self.options is not None:
            for option in self.get_numbered_options():
                self.text += (option + "\n")

    def get_numbered_options(self) -> list[str] | None:
        """
        Get the list of options, numbered
        :rtype: list[str] | None
        :return: A list of the options with numbers prepended or None if there are no options
        """
        numbered_options = []
        if self.options is None:
            return None

        for i in range(len(self.options)):
            option_text = list(self.options.keys())[i]
            numbered_options.append(f"{i + 1}. {option_text}")

        return numbered_options

    def get_options_count(self) -> int:
        """
        Get how many options are presented on this menu
        :rtype: int
        :return: A count of how many options are present for this menu
        """
        if self.options is None:
            return 0
        return len(self.options)

    def get_next_screen(self, choice: int) -> Screen | None:
        """
        Gets the next screen associated with the selected option.
        :param int choice: The option selected by the user
        :rtype: Screen | None
        :return: The next screen to show based on the user's selection or None if there is no associated Screen
        """
        try:
            option = list(self.options.keys())[choice-1]
        except IndexError:
            return None
        if isinstance(self.options[option], Screen):
            return self.options[option]
        return None

    def get_next_function(self, choice: int) -> Callable[[str], None] | None:
        """
        Gets the function associated with the selected option.
        :param int choice: The option selected by the user
        :rtype: Callable[[str], None] | None
        :return: The function to call based on the user's selection or None if there is no associated function
        """
        try:
            option = list(self.options.keys())[choice]
        except IndexError:
            return None
        if isinstance(self.options[option], Callable):
            return self.options[option]
        return None

    def add_option(self, option: str, next_action: Screen | Callable[[str], None]):
        """
        Add a new option to the menu
        :param str option: The option to add
        :param Screen | Callable[[str], None] next_action: The screen to be shown or the function to be called
        if the user selects this option
        """
        if self.options is None:
            self.options = dict()
        self.options[option] = next_action

        number = self.get_options_count()
        self.text += f"{number}. {option}\n"
