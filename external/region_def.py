from external.room_def import RoomDef
from input_output.logger.log_manager import LogManager


class RegionDef:
    """Definition of a region read from file"""

    def __init__(self, id: int, name: str):
        """
        Create a new region definition
        :param int id: The ID of the region
        :param str name: The name of the region
        """
        self.id = id
        self.name = name
        self.room_defs: dict[int, RoomDef] = dict()

    def add_room_def(self, room: RoomDef):
        """
        Add a room to this region definition
        :param RoomDef room: The room to add
        """
        if room.id in self.room_defs.keys():
            LogManager.get_logger().warn(f"Attempted to add Room with ID {room.id} to region with ID "
                                         f"{self.id} but a Room with the same ID already exists. "
                                         f"New Room was not added.")
            return
        self.room_defs[room.id] = room
