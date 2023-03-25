from entity.npc import Npc
from entity.player import Player
from interface.game import Game
from map import Map
from plugins.default import Default
from plugins.triggers.talk_to_npc_trigger import TalkToNpcTrigger
from plugins.triggers.travel_to_room_trigger import TravelToRoomTrigger
from room import Room
from interface.screen import *

import save_manager


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


def intro(name: str):
    """Play the intro text
    name: The player's name"""
    pass


def load_game() -> Player:
    """Present a list of the saved characters and let the player choose one to load.
    If the player was loaded successfully, returns True"""
    saves = save_manager.get_saves()
    print()
    if len(saves) > 0:
        print("Saved Characters:")
        for save in saves:
            print(save)
        print()
        print("Which save would you like to load?")
        print("Type the name of a character or press ENTER to go back to the main menu")

        # We need to be allowed to take the empty string as input
        saves.append("")
        response = get_text_input("", saves)

        if response == "":
            return False
        
        # Load the player
        player = save_manager.load(response)
        if player is None:
            print()
            print("There was an error loading that character")
            print("Check the log file for more information")
            print()
            return None
        print()
        print(player.name, "loaded successfully!")
        print()
        return player

    else:
        print("There are no saves to load")
        print()
        pause()
        return None


def main():
    print("Epic Quest: Text Quest")
    print()
    print("Loading data...")
    """
    # Load all the definitions into the World
    game_data_loader.load_all()
    print("Data loaded!")

    player = main_menu()

    # Start the main game loop
    while True:
        # Load the location
        current_map = World.world_map[player.map]
        current_room = current_map.rooms[player.room]

        current_npc_ids = current_room.npcs
        current_npcs = list()

        if current_npc_ids is not None:
            for npc_id in current_npc_ids:
                current_npcs.append(World.npcs[npc_id])

        current_item_ids = current_room.items
        current_items = list()

        # Display the room text
        print()
        print(current_room.desc)
        print()
        for npc in current_npcs:
            print("You see", npc.name)
        print()

        
        # Haven't implemented items yet lol
        # for item in current_items:
        #    print(f"You notice a {item.name} on the ground")
        

        print_adjacent_rooms(current_map, current_room)

        # Process the player input
        process_input(player, current_map, current_room, 
                      current_npcs)
    """


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
        user_input = get_text_input(": ").lower()

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
            if subject in direction_words:
                # Handle traveling
                new_room_id = current_room.__dict__[subject]
                new_room = current_map.rooms[new_room_id]
                run_plugins(player, TravelToRoomTrigger, new_room)
                performed_action = True
                
        elif action in talk_words:
            for npc in current_npcs:
                if subject in npc.name:
                    run_plugins(player, TalkToNpcTrigger, npc)
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


def run_plugins(player: Player, trigger_type, data):
    """Run all plugins related to a specific action
    player: The player object
    data: The data being interacted with, like an NPC, room, item, etc.
    trigger_type: The type of trigger that we are calling"""
    block_default = False

    # This is hacky but it should work because each trigger type should only have 1 non-dunder method in it.
    trigger_method_name = [f for f in dir(trigger_type) if not f.startswith("__") and not f.startswith("_")][0]

    # Loop through each inheritor of this trigger type
    for trigger in trigger_type.__subclasses__():
        # Since the trigger methods are non-static, we need to create an instance for them. Maybe this should be changed?
        trigger_instance = trigger()

        # Check if the plugin blocks the default
        # More black magic to call the method lol
        if trigger_instance.__class__.__name__ != "Default" and getattr(trigger_instance, trigger_method_name)(player, data):
            block_default = True
    
    # Move to the new room as the default action
    if not block_default:
        default = Default()
        getattr(default, trigger_method_name)(player, data)


def get_text_input(prompt: str = "Your answer: ", allowed_responses: list[str] = None,
                   case_sensitive: bool = False) -> str:
    """Gets string input from the user.
    prompt: The prompt to be displayed to the user
    allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    case_sensitive: All string comparisons will be case-sensitive if this is set"""
    while True:
        response = input(prompt)
        # If we don't care about validating the response
        if allowed_responses is None:
            return response
        
        # If we want to be case-sensitive
        if case_sensitive:
            if response in allowed_responses:
                return response
        else:
            for allowed_response in allowed_responses:
                if response.lower() == allowed_response.lower():
                    return response
        print()
        print("Please input a valid option")
        print()


def get_int_input(prompt: str = "Your choice: ", number_of_choices: int = -1) -> int:
    """Get integer input from the user. Will loop until the user enters a valid input
    prompt: The prompt to be displayed to the user
    number_of_choices: If this is not -1, then the function will also validate if the user has entered a
    number between 1 and number_of_choices (inclusive)"""
    while True:
        c = input(prompt)
        try:
            if int(c) in range(1, number_of_choices+1):
                return int(c)
            else:
                print()
                print("Please input a valid option")
                print()
        except ValueError:
            print()
            print("Please input a number")
            print()


def pause():
    """Wait for the user to press Enter"""
    input("Press ENTER to continue...")


if __name__ == "__main__":
    main()
