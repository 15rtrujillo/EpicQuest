from entity.npc import Npc
from entity.player import Player
from logger.log_manager import LogManager
from map import Map
from plugins.default import Default
from plugins.triggers.travel_to_room_trigger import TravelToRoomTrigger
from room import Room
from world import World

import game_data_loader
import save_manager


direction_words = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest", "up", "down"]


def intro(name: str):
    """Play the intro text
    name: The player's name"""
    pass


def new_game() -> Player:
    """Create a new player.
    Returns True if a player was created successfully"""
    # Get the currently existing saves so the player can't duplicate an existing character
    saves = save_manager.get_saves()

    print()
    print("New Game")
    print()
    name_good = False
    player_name = ""
    while not name_good:
        player_name = get_text_input("Please enter a name for your character "
                                     "or press ENTER to return to the main menu\n")
        
        if player_name == "":
            return None
        
        # Check if the player name already exists
        name_good = True
        for save in saves:
            if player_name.lower() == save.lower():
                print()
                print("A character with that name already exists!")
                print()
                name_good = False
                break
    
    # Create the new player
    player = Player(player_name)
    save_manager.save(player)

    # TODO: Call the story intro here
    return player


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


def about():
    """Displays the about section"""
    print()
    print("Epic Quest: Text Quest")
    print("The code is open source and pending licensing")
    print("The IP of Epic Quest and all things associated with it is Copyright (C) Ryan Trujillo")
    print("I love you")
    print()
    pause()


def exit_game(player: Player):
    """Quit the game and save the player
    player: The player to save"""
    if player is not None:
        save_manager.save(player)
    print()
    print("Thank you for playing Epic Quest.")
    print("Goodbye!")
    exit(0)


def main_menu() -> Player:
    """Display the main menu for the game and create/load a player"""
    while True:
        print()
        print("Epic Quest: Text Quest")
        print()
        print("Main Menu")
        print("1. New Game")
        print("2. Load Game")
        print("3. About")
        print("4. Exit")
        print()
        choice = get_int_input(number_of_choices=4)
        if choice == 1:
            player = new_game()
            if player is not None:
                break
        elif choice == 2:
            player = load_game()
            if player is not None:
                break
        elif choice == 3:
            about()
        elif choice == 4:
            exit_game(None)
    return player


def main():
    print("Epic Quest: Text Quest")
    print()
    print("Loading data...")

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

        if current_item_ids is not None:
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

        """
        Haven't implemented items yet lol
        for item in current_items:
            print(f"You notice a {item.name} on the ground")
        """

        print_adjacent_rooms(current_map, current_room)

        # Process the player input
        process_input(player, current_map, current_room, 
                      current_npcs)


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

    while True:
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

                # Run all plugins associated with traveling to a new room
                block_default = False
                for trigger in TravelToRoomTrigger.__subclasses__():
                    trigger_instance = trigger()
                    # Check if the plugin blocks the default
                    if trigger_instance.__class__.__name__ != "Default" and trigger_instance.travel_to_room(player, new_room):
                        block_default = True
                
                # Move to the new room as the default action
                if not block_default:
                    default = Default()
                    default.travel_to_room(player, new_room)
                break
                
        elif action in talk_words:
            pass
        elif action in attack_words:
            pass
        elif action in examine_words:
            pass
        elif action in help_words:
            pass
        print()
        print("Nothing interesting happens")
        print()


def print_adjacent_rooms(current_map: Map, current_room: Room):
    """Prints out the names of all the rooms linked to this one
    current_map: The map the player is currently located in
    current_room: The room the plyaer is currently located in"""
    for direction in direction_words[:-2]:
        new_room_id = current_room.__dict__[direction]
        if new_room_id != -1:
            new_room = current_map.rooms[new_room_id]
            print("To the", direction, "you see", new_room.name)


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
