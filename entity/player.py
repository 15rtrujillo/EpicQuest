class Player:
    """Holds all the data for players. Can also be used to create
        enemy players."""

    def __init__(self, name: str):
        """Create a new player with default values
        name: The name of the player"""
        self.name = name
        self.gold = 100
        self.hp = 100
        self.level = 1
        self.xp = 0
        self.location = 0