from logger.log_manager import LogManager
from entity.player import Player
from world import World

import game_data_loader
import save_manager


def main_menu():
    """Display the main menu for the game"""
    print("Epic Quest: Quest for Epicness")
    print()
    print("Main Menu")
    print("1. New Game")
    print("2. Load Game")
    print("3. About")
    print("4. Exit")
    choice = get_int_input(number_of_choices=4)


def main():
    print("Epic Quest: Quest for Epicness")
    print()
    print("Loading data...")

    # Load all the definitions into the World
    game_data_loader.load_all()
    print("Data loaded!")


def get_int_input(prompt: str = "Your choice: ", number_of_choices: int = -1) -> int:
    """Get integer input from the user. Will loop until the user enters a valid input
    prompt: The prompt to be displayed to the user
    number_of_choices: If this is not -1, then the function will also validate if the user has entered a number between 1 and number_of_choices (inclusive)"""
    while True:
        c = input(prompt)
        try:
            if int(c) in range(1, number_of_choices+1):
                return int(c)
            else:
                print("Please input a valid option")
        except:
            print("Please input a number")


def pause():
    """Wait for the user to press Enter"""
    input("Press ENTER to continue...")


if __name__ == "__main__":
    main()