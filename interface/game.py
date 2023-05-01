from abc import ABC
from entity.npc import Npc
from entity.player import Player
from interface.screen import Screen, InfoScreen, NumberedMenuScreen, UnnumberedMenuScreen, YesOrNoScreen, RoomScreen
from logger.log_manager import LogManager
from map import Map
from plugins.default import Default
from plugins.plugin_manager import PluginManager
from plugins.triggers.talk_to_npc_trigger import TalkToNpcTrigger
from plugins.triggers.travel_to_room_trigger import TravelToRoomTrigger
from room import Room

import constants.word_lists as word_lists
import game_data_loader
import file_utils
import plugins.tutorial.MysteriousFigure
import save_manager


class Game(ABC):
    """An abstract class that has methods for running the game"""

    def __init__(self):
        self.screen: Screen | None = None
        self.player: Player | None = None
        self.world_map: dict[int, Map] = dict()
        # self.item_defs: dict[int, Item] = dict()
        self.npc_defs: dict[int, Npc] = dict()
        self.current_map: Map | None = None
        self.current_room: Room | None = None
        self.current_npcs: list[Npc] | None = None
        # self.current_items: list[Item] = None

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

    def typewriter(self, text: str, char_delay: int, end: str):
        """Add text to the textbox with a typewriter effect
        text: The text to add
        char_delay: The delay between each character in ms
        end: The character to append to the very end of the typewritten text"""
        pass

    def clear_text(self):
        """Clears all the text on the GUI screen
        Does nothing with the console"""
        pass

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

            # TODO: Probably should log an error if we get here

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

                # There is no next screen or function. Log an error
                LogManager.get_logger().error(f"A numbered menu screen has no associated screen or "
                                              f"function for option {choice}")

        elif isinstance(self.screen, UnnumberedMenuScreen):
            option = text
            # If they didn't enter something from the list
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

            # TODO: Probably should log an error here

        elif isinstance(self.screen, YesOrNoScreen):
            if validate_text_input(text, word_lists.YES, partial_match=True)\
                    and self.screen.has_yes_screen():
                self.display_screen(self.screen.yes_screen)

            elif validate_text_input(text, word_lists.NO, partial_match=True)\
                    and self.screen.has_no_screen():
                self.display_screen(self.screen.no_screen)

            else:
                self.display_screen(InfoScreen("Please enter either \"yes\" or \"no\"\n", self.screen))
                self.pause()

        elif isinstance(self.screen, RoomScreen):
            if text == "":
                return
            # Get the tokens
            tokens = text.split()

            # Remove the word "to" (for things like "talk to" or "go to")
            try:
                tokens.remove("to")
            except ValueError:
                pass

            # The first token should be an action word
            action = tokens[0]

            # The rest of the tokens should be the subject we're acting on
            subject = None
            if len(tokens) > 1:
                subject = " ".join(tokens[1:])

            # Handle travelling
            if validate_text_input(action, word_lists.TRAVEL):
                if subject is not None and validate_text_input(subject, word_lists.DIRECTIONS):
                    # Handle traveling
                    new_room_id = self.current_room.__dict__[subject]
                    # Make sure that we can actually go the way they want to
                    if new_room_id != -1:
                        new_room = self.current_map.rooms[new_room_id]
                        self.run_plugins(TravelToRoomTrigger, new_room)
                        return

            elif validate_text_input(action, word_lists.TALK):
                if subject is not None:
                    # Check which NPC in the room we're talking to
                    for npc in self.current_npcs:
                        if validate_text_input(subject, [npc.name], partial_match=True):
                            # Handle talking
                            self.display_screen(InfoScreen(next_screen=self.screen))
                            self.run_plugins(TalkToNpcTrigger, npc)
                            return

            self.display_screen(InfoScreen("Nothing interesting happens...\n", self.screen))
            self.pause()

    def create_main_menu_screen(self) -> NumberedMenuScreen:
        """Creates and returns the main menu screen"""
        main_menu_screen = NumberedMenuScreen("Epic Quest: Text Quest\n\nMain Menu\n")

        new_game_screen = UnnumberedMenuScreen("New Game\nPlease input a name for your character"
                                               " or press ENTER to return to the main menu\n",
                                               {"*": self.new_game,
                                                "": main_menu_screen}, False)

        load_game_screen = self.create_load_game_screen()
        if isinstance(load_game_screen, UnnumberedMenuScreen):
            load_game_screen.add_option("", main_menu_screen)
        elif isinstance(load_game_screen, InfoScreen):
            load_game_screen.next_screen = main_menu_screen

        about_game_screen = InfoScreen("""About Epic Quest: Text Quest
The code is open source and pending licensing
The IP of Epic Quest and all things associated with it is Copyright (C) Ryan Trujillo
I love you

Press ENTER to continue...
""", main_menu_screen)

        main_menu_screen.add_option("New Game", new_game_screen)
        main_menu_screen.add_option("Load Game", load_game_screen)
        main_menu_screen.add_option("About", about_game_screen)
        main_menu_screen.add_option("Quit", YesOrNoScreen("Are you sure you want to quit?\n",
                                                          self.create_quit_game_screen(),
                                                          main_menu_screen))

        return main_menu_screen

    def create_load_game_screen(self) -> UnnumberedMenuScreen:
        """Creates the load game screen and fills it with a list of characters"""
        saves = save_manager.get_saves()
        if len(saves) > 0:
            options_dict = dict()
            for save in saves:
                options_dict[save] = self.load_game
            load_game_screen = UnnumberedMenuScreen("Load Game\nEnter the name of the character you'd like to load "
                                                    "or press ENTER to return to the main menu\n",
                                                    options_dict)
        else:
            load_game_screen = InfoScreen("Load Game\nThere are no characters to load\n"
                                          "\nPress ENTER to return to the main menu...\n")
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
        self.display_screen(self.create_room_screen())

    def load_game(self, player_name: str):
        # Attempt to load the player
        player = save_manager.load(player_name)
        if player is None:
            self.display_screen(InfoScreen(f"There was an error loading the character named {player_name}. "
                                           f"Check the log file for more details.",
                                           self.create_main_menu_screen()))
            self.pause()

        self.player = player
        self.display_screen(self.create_room_screen())

    def quit_game(self, _: str):
        """Saves the player and quits the game"""
        if self.player is not None:
            save_manager.save(self.player)
        exit(0)

    def create_room_screen(self) -> RoomScreen:
        """Creates the screen for the current room"""
        current_map_id = self.player.map
        current_room_id = self.player.room
        self.current_map = self.world_map[current_map_id]
        self.current_room = self.current_map.rooms[current_room_id]

        # Get NPCs
        current_npc_ids = self.current_room.npcs
        current_npcs = list()

        if current_npc_ids is not None:
            for npc_id in current_npc_ids:
                current_npcs.append(self.npc_defs[npc_id])

        self.current_npcs = current_npcs

        return RoomScreen(self.current_map, self.current_room, self.current_npcs)

    def run_plugins(self, trigger_type, data):
        """Run all plugins related to a specific action
        trigger_type: The type of trigger that we are calling
        data: The data being interacted with, like an NPC, room, item, etc."""
        block_default = False

        # This is hacky, but it should work because each trigger type should only have 1 non-dunder method in it.
        trigger_method_name = [f for f in dir(trigger_type) if not f.startswith("__") and not f.startswith("_")][0]

        # Set up the script context
        script_context = PluginManager.get_script_context()
        script_context.game = self
        script_context.interacting_player = self.player
        if trigger_type == TalkToNpcTrigger:
            script_context.interacting_npc = data
        elif trigger_type == TravelToRoomTrigger:
            script_context.interacting_room = data

        # Loop through each inheritor of this trigger type
        for trigger in trigger_type.__subclasses__():
            # Since the trigger methods are non-static, we need to create an instance for them.
            # Maybe this should be changed?
            trigger_instance = trigger()

            # Check if the plugin blocks the default
            # More black magic to call the method lol
            if trigger_instance.__class__.__name__ != "Default" and getattr(trigger_instance, trigger_method_name)():
                block_default = True

        # Move to the new room as the default action
        if not block_default:
            default = Default()
            getattr(default, trigger_method_name)()

        script_context.clear_context()

    def add_map(self, new_map: Map):
        """Add a map to the world map
        new_map: The map to add"""
        if new_map.id in self.world_map.keys():
            LogManager.get_logger().warn(f"Attempted to add Map with ID {new_map.id} to world map, but a "
                                         f"Map with the same ID already exists. New Map was not added.")
            return
        self.world_map[new_map.id] = new_map

    def add_npc(self, new_npc: Npc):
        """Add an NPC to the NPC definitions dictionary
        new_npc: The NPC to add"""
        if new_npc.id in self.npc_defs.keys():
            LogManager.get_logger().warn(f"Attempted to add NPC with ID {new_npc.id} to NPC defs list, "
                                         f"but an NPC with the same ID already exists. New NPC was not added.")
            return
        self.npc_defs[new_npc.id] = new_npc


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


def validate_text_input(text_to_validate: str, allowed_responses: list[str],
                        case_sensitive: bool = False, partial_match: bool = False) -> bool:
    """Validates text input
    text_to_validate: The text to validate
    allowed_responses: If this is not None, the user's input will be checked against a list of
    allowed responses. If the user enters an invalid response, they will be prompted to try again
    case_sensitive: All string comparisons will be case-sensitive if this is set
    partial_match: Checks if the text is a substring of one of the allowed responses"""
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
            if partial_match and text_to_validate.lower() in allowed_response.lower():
                return True

            elif text_to_validate.lower() == allowed_response.lower():
                return True

    return False
