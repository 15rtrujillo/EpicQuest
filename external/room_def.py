class RoomDef:
    """Holds information about a map location"""

    def __init__(self, id: int = -1, name: str = "", desc: str = "", n: int = -1, ne: int = -1, e: int = -1,
                 se: int = -1, s: int = -1, sw: int = -1, w: int = -1, nw: int = -1, up: int = -1,
                 down: int = -1, npc_ids: list[int] = None, item_ids: list[int] = None):
        """Create a new Room with links to attached rooms
        id: The ID of the room
        name: The name of the room
        desc: The description of the room
        n: The ID of the room to the north
        ne: The ID of the room to the north-east
        e: The ID of the room to the east
        se: The ID of the room to the southeast
        s: The ID of the room to the south
        sw: The ID of the room to the southwest
        w: The ID of the room to the west
        nw: The ID of the room to the northwest
        up: The ID of the room above this one
        down: The ID of the room below this one
        npcs: A list of NPC IDs in the room
        items: A list of item IDs in the room"""
        self.id = id
        self.name = name
        self.desc = desc
        self.north = n
        self.northeast = ne
        self.east = e
        self.southeast = se
        self.south = s
        self.southwest = sw
        self.west = w
        self.northwest = nw
        self.up = up
        self.down = down
        self.npc_ids = npc_ids
        self.item_ids = item_ids
