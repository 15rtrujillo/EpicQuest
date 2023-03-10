class Room:
    """Holds information about a map location"""

    def __init__(self, id: int = -1, name: str = "", desc: str = "", n: int = -1, ne: int = -1, e: int = -1, se: int = -1, s: int = -1, sw: int = -1, w: int = -1, nw: int = -1, up: int = -1, down: int = -1):
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
        down: The ID of the room below this one"""
        self.id = id
        self.name = name
        self.desc = desc
        self.n = n
        self.ne = ne
        self.e = e
        self.se = se
        self.s = s
        self.sw = sw
        self.w = w
        self.nw = nw
        self.up = up
        self.down = down


if __name__ == "__main__":
    """Dumps the Room class to a map file for testing"""
    import json
    temp = Room(-1, "", "")
    file = open("room.eqm", "wb")
    file.write(json.dumps([temp], default=lambda o: o.__dict__, indent=4).encode())