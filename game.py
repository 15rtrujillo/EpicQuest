from logger.log_manager import LogManager
from entity.player import Player
from world import World

import game_data_loader
import save_manager


player = None


def new_game() -> bool:
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
        player_name = get_text_input("Please enter a name for your character or press ENTER to return to the main "
                                     "menu\n")
        
        if player_name == "":
            return False
        
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
    global player
    player = Player(player_name)
    save_manager.save(player)

    # TODO: Call the story intro here
    return True


def load_game() -> bool:
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
        global player
        player = save_manager.load(response)
        if player is None:
            print()
            print("There was an error loading that character")
            print("Check the log file for more information")
            print()
            return False
        print()
        print(player.name, "loaded successfully!")
        print()
        return True

    else:
        print("There are no saves to load")
        print()
        pause()
        return False


def about():
    """Displays the about section"""
    print()
    print("Epic Quest: Text Quest")
    print("The code is open source and pending licensing")
    print("The IP of Epic Quest and all things associated with it is Copyright (C) Ryan Trujillo")
    print("I love you")
    print()
    pause()


def exit_game():
    """Quit the game and save the player"""
    if player is not None:
        save_manager.save(player)
    print()
    print("Thank you for playing Epic Quest.")
    print("Goodbye!")
    exit(0)


def main_menu():
    while True:
        """Display the main menu for the game"""
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
            if new_game():
                break
        elif choice == 2:
            if load_game():
                break
        elif choice == 3:
            about()
        elif choice == 4:
            exit_game()


def main():
    print("Epic Quest: Text Quest")
    print()
    print("Loading data...")

    # Load all the definitions into the World
    game_data_loader.load_all()
    print("Data loaded!")

    main_menu()


def get_text_input(prompt: str = "Your answer: ", allowed_responses: list[str] = None,
                   case_sensitive: bool = False) -> str:
    """Gets string input from the user.
    prompt: The prompt to be displayed to the user
    allowed_responses: If this is not None, the user's input will be checked against a list of allowed responses. If the
    user enters an invalid response, they will be prompted to try again
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
    number_of_choices: If this is not -1, then the function will also validate if the user has entered a number between
    1 and number_of_choices (inclusive)"""
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
