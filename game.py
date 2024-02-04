from interface.screens.numbered_menu_screen import NumberedMenuScreen
from interface.screens.screen import Screen
from model.entity.player import Player
from model.world.world import World


import interface.game_window as game_window


class Game:
    """The game engine"""
    TICK_RATE: int = 600

    def __init__(self):
        """Create an instance of the game engine"""
        self.world: World = World()
        self.player: Player | None = None
        self.window: game_window.GameWindow | None = None
        self.current_screen: Screen | None = None
        self.next_screen: Screen | None = None
        self.current_tick = 0

    def tick(self):
        self.current_tick += 1
        print("Tick:", self.current_tick)

        self.window.root.after(Game.TICK_RATE, self.tick)
        
    def attach_window(self, window: game_window.GameWindow):
        self.window = window

    def main_menu(self) -> NumberedMenuScreen:
        """
        Create the main menu
        :rtype: NumberedMenuScreen
        :return: The main menu screen
        """
        menu = NumberedMenuScreen("Epic Quest: Text Quest\n\nMain Menu")
        return menu


def parse_int_input(text_to_parse: str, number_of_choices: int = 0) -> int:
    """
    Parses int input
    :param str text_to_parse: The text to parse
    :param int number_of_choices: If this is not 0, the parsed int will be range checked form one to this value
    (inclusive)
    :rtype: int
    :return: The user's input as an int. -1 will be returned if the input is invalid in some way
    """
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


def validate_text_input(text_to_validate: str, allowed_responses: list[str],
                        case_sensitive: bool = False, partial_match: bool = False) -> bool:
    """
    Validates text input
    :param str text_to_validate: The text to validate
    :param list[str] allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    :param bool case_sensitive: All string comparisons will be case-sensitive if this is set
    :param bool partial_match: Checks if the text is a substring of one of the allowed responses
    :rtype: bool
    :return: True if the input is valid according to the conditions specified, False otherwise
    """
    # If we don't care about validating the response
    # But then what is the point of calling this function?
    if allowed_responses is None:
        return True

    for allowed_response in allowed_responses:
        if case_sensitive:
            if partial_match and text_to_validate in allowed_response:
                return True

            elif text_to_validate == allowed_response:
                return True

        else:
            if partial_match and text_to_validate.casefold() in allowed_response.casefold():
                return True

            elif text_to_validate.casefold() == allowed_response.casefold():
                return True

    return False
