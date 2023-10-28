from external.room_def import RoomDef


import model.entity.npc as npc
import model.world.region as region


class Room:
    def __init__(self, room_def: RoomDef, located_in: region.Region):
        self.id: int = room_def.id
        self.room_def: RoomDef = room_def
        self.located_in: region.Region = located_in
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
        self.npcs: list[npc.Npc] | None = None
