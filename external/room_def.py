class RoomDef:
    """Definition of a room read from file"""

    def __init__(self):
        """Create a new Room with links to attached rooms"""
        self.id = -1
        self.name = ""
        self.description = ""
        self.north = -1
        self.northeast = -1
        self.east = -1
        self.southeast = -1
        self.south = -1
        self.southwest = -1
        self.west = -1
        self.northwest = -1
        self.up = -1
        self.down = -1
        self.npc_ids: list[int] = list()
        self.item_ids: list[int] = list()
