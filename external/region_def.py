from logger.log_manager import LogManager
from room_def import RoomDef


class RegionDef:
    """Contains information about a map"""

    def __init__(self, id: int, name: str):
        """Create a new map
        id: The map ID
        name: The name of the map"""
        self.id = id
        self.name = name
        self.rooms: dict[int, RoomDef] = dict()

    def add_room(self, room: RoomDef):
        """Add a room to this map
        room: The room to add"""
        if room.id in self.rooms.keys():
            LogManager.get_logger().warn(f"Attempted to add Room with ID {room.id} to map with ID "
                                         f"{self.id} but a Room with the same ID already exists. "
                                         f"New Room was not added.")
            return
        self.rooms[room.id] = room
