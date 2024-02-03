from external.room_def import RoomDef


import model.entity.npc as npc
import model.world.region as region


class Room:
    """A room is a container for everything the player can interact with in a specific scene"""

    def __init__(self, room_def: RoomDef, located_in: region.Region):
        """
        Create a new room based on a room definition
        :param RoomDef room_def: The room definition to base this room on
        :param Region located_in: The region this room is located in
        """
        self.id: int = room_def.id
        self.room_def = room_def
        self.located_in = located_in
        self.north: Room | None = None
        self.northeast: Room | None = None
        self.east: Room | None = None
        self.southeast: Room | None = None
        self.south: Room | None = None
        self.southwest: Room | None = None
        self.west: Room | None = None
        self.northwest: Room | None = None
        self.up: Room | None = None
        self.down: Room | None = None
        self.npcs: list[npc.Npc] = list()
