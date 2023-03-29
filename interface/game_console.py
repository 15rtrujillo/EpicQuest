from entity.player import Player
from interface.game import Game
from interface.screen import *


class GameConsole(Game):
    
    def __init__(self):
        super().__init__()

    def initialize(self):
        super().initialize()
        # The main game loop to mimic the loop of the game window
        while True:
            self.get_text()

    def display_screen(self, screen: Screen):
        super().display_screen(screen)
        print(self.screen.text, end="")

    def append_to_screen(self, text: str, end: str = "\n"):
        super().append_to_screen(text, end)
        print(text + end, end="")

    def typewriter(self, text: str, char_delay: int = 50, end: str = "\n"):
        """Typewriting usually doesn't work on most consoles.
        We just pass along to append_to_screen"""
        self.append_to_screen(text, end)

    def get_text(self):
        text = input()  
        super().parse_text(text)
