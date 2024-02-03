class Player:
    """Player data"""

    def __init__(self, name: str):
        """
        Create a new player with default values
        :param str name: The name of the player
        """
        self.name = name
        self.gold = 100
        self.hp = 100
        self.level = 1
        self.xp = 0
        self.region = 0
        self.room = 0
