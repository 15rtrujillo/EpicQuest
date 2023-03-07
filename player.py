import pickle


class Player:
    """Holds all the data for players. Can also be used to create
        enemy players."""

    def __init__(self, name: str):
        """Create a new player with default values
        name: The name of the player"""
        self.name = name
        self.gold = 100
        self.hp = 100
        self.maxhp = 100
        self.level = 1
        self.xp = 0
        self.location = 0


def save(player: Player):
    """Save a player to file at \"[player_name].eq\"
    player: The player to save"""
    save_file_name = player.name + ".eq"
    save_file = open(save_file_name, "wb")
    save_file.write("yo".encode())
    """
    pickle.dump(player, save_file)
    """


def load(name: str) -> Player:
    """Load a player from file
    name: The name of the player to attempt to load"""
    save_file_name = name + ".eq"
    try:
        save_file = open(save_file_name, "rb")
        return pickle.load(save_file)
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    test = Player("test")
    save(test)

    loaded_test = load("failure")