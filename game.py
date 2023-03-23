from abc import ABC


WINDOWED = True


class Game(ABC):
    """An interface that has methods for running the game"""

    def initialize(self):
        """Load the game and set up the interface"""
        pass

    def display_main_menu(self):
        """Display the main menu that allows the player to save, load or exit the game"""
        pass

    def handle_main_menu(self, choice: int):
        """Handle the player's choice
        choice: The choice the user selected"""
        pass
