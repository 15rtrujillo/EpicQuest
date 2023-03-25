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

    def get_text(self):
        text = input()  
        super().parse_text(text)


def process_input(player: Player, current_map: map, current_room: Room,
                  current_npcs: list[Npc]):
    """Decide what to do based on what the user inputs
    player: The player object
    current_map: The map the player is currently in
    current_room: The room the player is currently in
    current_npcs: A list of the NPCs in the room"""

    # Create lists of trigger words to check for
    travel_words = ["go", "travel", "head", "walk"]
    talk_words = ["speak", "talk", "approach"]
    attack_words = ["fight", "attack", "battle"]
    examine_words = ["look", "examine", "study"]
    help_words = ["help", "instructions"]

    performed_action = False
    while not performed_action:
        user_input = ""  # get_text_input(": ").lower()

        # Get the tokens
        tokens = user_input.split()

        # Remove the word "to" (for things like "talk to" or "go to")
        try:
            tokens.remove("to")
        except ValueError:
            pass

        # Now we can tell what to do
        action = tokens[0]
        if len(tokens) > 1:
            subject = " ".join(tokens[1:])
        if action in travel_words:
            # if subject in direction_words:
            # Handle traveling
            new_room_id = current_room.__dict__[subject]
            new_room = current_map.rooms[new_room_id]
            # run_plugins(player, TravelToRoomTrigger, new_room)
            performed_action = True
                
        elif action in talk_words:
            for npc in current_npcs:
                if subject in npc.name:
                    # run_plugins(player, TalkToNpcTrigger, npc)
                    performed_action = True

        elif action in attack_words:
            pass
        elif action in examine_words:
            for npc in current_npcs:
                if subject in npc.name:
                    print()
                    print(npc.desc)
                    print()
            # TODO Check items

            # We don't want to say "Nothing interesting happens" if they examine something
            performed_action = True
        elif action in help_words:
            pass
