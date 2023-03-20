from logger.log_manager import LogManager
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
        if room.id in self.rooms.keys():
            LogManager.get_logger().warn(f"Attempted to add Room with ID {room.id} to map with ID "
                                         f"{self.id} but a Room with the same ID already exists. "
                                         f"New Room was not added.")
            return
        self.rooms[room.id] = room


if __name__ == "__main__":
    """Dumps the Map class to a map file for testing"""
    import json
    temp = Map()
    temp_room = Room()
    temp.add_room(temp_room)
    file = open("test_map.eqm", "wb")
    file.write(json.dumps(temp, default=lambda o: o.__dict__, indent=4).encode())
