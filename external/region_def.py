from external.room_def import RoomDef
from input_output.logger.log_manager import LogManager


class RegionDef:
    """Contains information about a map"""

    def __init__(self, id: int, name: str):
        """Create a new map
        id: The map ID
        name: The name of the map"""
        self.id = id
        self.name = name
        self.room_defs: dict[int, RoomDef] = dict()

    def add_room_def(self, room: RoomDef):
        """Add a room to this region def
        room: The room to add"""
        if room.id in self.room_defs.keys():
            LogManager.get_logger().warn(f"Attempted to add Room with ID {room.id} to map with ID "
                                         f"{self.id} but a Room with the same ID already exists. "
                                         f"New Room was not added.")
            return
        self.room_defs[room.id] = room
