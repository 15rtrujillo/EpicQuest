from interface.game_console import GameConsole
from interface.game_window import GameWindow


WINDOWED = True


def main():
    if WINDOWED:
        game = GameWindow()
    else:
        game = GameConsole()

    game.initialize()


if __name__ == "__main__":
    main()