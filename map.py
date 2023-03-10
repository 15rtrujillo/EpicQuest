from room import Room


class Map:
    """Contains infromation about a map"""

    def __init__(self, id: int = -1, name: str = ""):
        """Create a new map
        id: The map ID
        name: The name of the map"""
        self.id = id
        self.name = name
        self.rooms = dict()


    def add_room(self, room: Room):
        """Add a room to this map
        room: The room to add"""
        self.rooms[room.id] = room