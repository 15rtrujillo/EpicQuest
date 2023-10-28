from external.npc_def import NpcDef


import model.world.room as room


class Npc:
    def __init__(self, npc_def: NpcDef, location: room.Room):
        self.id: int = npc_def.id
        self.npc_def: NpcDef = npc_def
        self.hp = self.npc_def.maxHp
        self.location: room.Room = location
