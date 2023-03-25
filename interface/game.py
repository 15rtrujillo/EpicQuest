from abc import ABC
from entity.npc import Npc
from entity.player import Player
from interface.screen import *
from logger.log_manager import LogManager
from map import Map

import game_data_loader
import file_utils
import save_manager


class Game(ABC):
    """An abstract class that has methods for running the game"""

    def __init__(self):
        self.screen: Screen = None
        self.player: Player = None
        self.world_map = dict()
        self.items = dict()
        self.npcs = dict()

    def initialize(self):
        """Load the game and set up the interface"""
        self.display_screen(InfoScreen("Epic Quest: Text Quest\n\nLoading data...\n",
                                       next_screen=self.create_main_menu_screen()))
        # Map files
        map_files = file_utils.get_files_in_directory(file_utils.get_maps_directory())
        for i, map_file in enumerate(map_files):
            # Make sure it's a map file
            if map_file.find(".eqm") == -1:
                continue

            self.append_to_screen(f"Loading map {i + 1}/{len(map_files)}...")
            new_map = game_data_loader.load_map_file(map_file)
            if new_map is not None:
                self.add_map(new_map)

        # NPC files
        npc_files = file_utils.get_files_in_directory(file_utils.get_npcs_directory())
        for i, npc_file in enumerate(npc_files):
            # Make sure it's a NPC file
            if npc_file.find(".eqn") == -1:
                continue

            self.append_to_screen(f"Loading NPC file {i + 1}/{len(npc_files)}...")
            new_npcs = game_data_loader.load_npc_file(npc_file)

            # Make sure we didn't hit any errors
            if new_npcs is None:
                continue

            for j, new_npc in enumerate(new_npcs):
                self.append_to_screen(f"Loading NPC {j + 1}/{len(new_npcs)}...")
                self.add_npc(new_npc)

        self.pause()

    def display_screen(self, screen: Screen):
        """Displays a screen object and sets it as the active screen.
        The GUI will clear the screen before showing a new one
        screen: The screen to display"""
        self.screen = screen

    def append_to_screen(self, text: str, end: str = "\n"):
        """Adds text to the current screen without clearing it
        text: The text to add
        end: This string will be added to the end of text"""
        self.screen.text += (text + end)

    def pause(self):
        """Waits for the user to press enter to continue to the next screen"""
        self.append_to_screen("\nPress ENTER to continue...\n")

    def parse_text(self, text: str):
        """Decide what to do for the current screen based on the user's input
        text: The input from the user"""
        if isinstance(self.screen, InfoScreen):
            if self.screen.has_next_screen():
                self.display_screen(self.screen.next_screen)
            elif self.screen.has_next_function():
                self.screen.next_function(text)

        elif isinstance(self.screen, NumberedMenuScreen):
            # Make sure we were given an int
            choice = parse_int_input(text, self.screen.get_options_count())
            if choice == -1:
                return_screen = self.screen
                self.display_screen(InfoScreen("Please enter a valid option\n", return_screen))
                self.pause()
            else:
                func = self.screen.get_next_function(choice)
                if func is not None:
                    func(text)
                    return
                screen = self.screen.get_next_screen(choice)
                if screen is not None:
                    self.display_screen(screen)
                    return
                # TODO: Log an error message if we reach this point

        elif isinstance(self.screen, UnnumberedMenuScreen):
            # If they didn't enter something from the list
            option = text
            if not validate_text_input(text, self.screen.get_options()):
                # And if the screen doesn't accept a wildcard
                if not self.screen.has_wildcard_option():
                    # The text is invalid
                    return_screen = self.screen
                    self.display_screen(InfoScreen("Please enter a valid option\n", return_screen))
                    self.pause()
                    return
                else:
                    option = "*"

            func = self.screen.get_next_function(option)
            if func is not None:
                func(text)
                return
            screen = self.screen.get_next_screen(option)
            if screen is not None:
                self.display_screen(screen)
                return

        elif isinstance(self.screen, YesOrNoScreen):
            if validate_text_input(text, ["yes", "y"]) and self.screen.has_yes_screen():
                self.display_screen(self.screen.yes_screen)
            elif validate_text_input(text, ["no", "n"]) and self.screen.has_no_screen():
                self.display_screen(self.screen.no_screen)
            else:
                self.display_screen(InfoScreen("Please enter either \"yes\" or \"no\"\n", self.screen))
                self.pause()

    def create_main_menu_screen(self) -> NumberedMenuScreen:
        """Creates and returns the main menu screen"""
        main_menu_screen = NumberedMenuScreen("Epic Quest: Text Quest\n\nMain Menu\n")

        new_game_screen = UnnumberedMenuScreen("New Game\nPlease input a name for your character"
                                               " or press ENTER to return to the main menu\n",
                                               {"*": self.new_game,
                                                "": main_menu_screen}, False)

        about_game_screen = InfoScreen("""About Epic Quest: Text Quest
The code is open source and pending licensing
The IP of Epic Quest and all things associated with it is Copyright (C) Ryan Trujillo
I love you

Press ENTER to continue...
""", main_menu_screen)

        main_menu_screen.add_option("New Game", new_game_screen)
        main_menu_screen.add_option("Load Game", self.create_load_game_screen())
        main_menu_screen.add_option("About", about_game_screen)
        main_menu_screen.add_option("Quit", YesOrNoScreen("Are you sure you want to quit?\n",
                                                          self.create_quit_game_screen(),
                                                          main_menu_screen))

        return main_menu_screen

    def create_load_game_screen(self) -> UnnumberedMenuScreen:
        """Creates the load game screen and fills it with a list of characters"""
        saves = save_manager.get_saves()
        options_dict = dict()
        for save in saves:
            options_dict[save] = self.load_game
        load_game_screen = UnnumberedMenuScreen("Load Game\nEnter the name of the character you'd like to load\n",
                                                options_dict)
        return load_game_screen

    def create_quit_game_screen(self):
        """Creates the quit game screen"""
        return InfoScreen("Thank you for playing Epic Quest!\n\nPress ENTER to exit...", next_function=self.quit_game)

    def new_game(self, player_name: str):
        """Create a new player save
        player_name: The name entered by the player"""
        saves = save_manager.get_saves()

        # Check if the name is already in use
        if validate_text_input(player_name, saves):
            self.display_screen(InfoScreen(f"A character with the name {player_name} already exists", self.screen))
            self.pause()
            return

        # Name good
        self.player = Player(player_name)
        save_manager.save(self.player)

        # TODO: Start the intro

    def load_game(self, player_name: str):
        pass

    def quit_game(self, _: str):
        """Saves the player and quits the game"""
        if self.player is not None:
            save_manager.save(self.player)
        exit(0)

    def add_map(self, map: Map):
        """Add a map to the world map
        map: The map to add"""
        if map.id in self.world_map.keys():
            LogManager.get_logger().warn(f"Attempted to add Map with ID {map.id} to world map, but a "
                                         f"Map with the same ID already exists. New Map was not added.")
            return
        self.world_map[map.id] = map

    def add_npc(self, npc: Npc):
        """Add an NPC to the NPC definitions dictionary
        npc: The NPC to add"""
        if npc.id in self.npcs.keys():
            LogManager.get_logger().warn(f"Attempted to add NPC with ID {npc.id} to NPC defs list, "
                                         f"but an NPC with the same ID already exists. New NPC was not added.")
            return
        self.npcs[npc.id] = npc


def parse_int_input(text_to_parse: str, number_of_choices: int = 0) -> int:
    """Parses int input. Returns -1 if the input is invalid in some way
    text_to_parse: The text to parse
    number_of_choices: If this is not 0, the parsed int will be range checked form one to this value (inclusive)"""
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


def validate_text_input(text_to_validate: str, allowed_responses: list[str] = None,
                        case_sensitive: bool = False) -> bool:
    """Validates text input
    text_to_validate: The text to validate
    allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    case_sensitive: All string comparisons will be case-sensitive if this is set"""
    # If we don't care about validating the response
    if allowed_responses is None:
        return True

    # If we want to be case-sensitive
    if case_sensitive:
        if text_to_validate in allowed_responses:
            return True
    else:
        if text_to_validate.lower() in [allowed_response.lower() for allowed_response in allowed_responses]:
            return True

    return False
