from external.npc_def import NpcDef


import model.world.room as room


class Npc:
    """An NPC instance"""

    def __init__(self, npc_def: NpcDef, location: room.Room):
        """
        Create an instance of an NPC based off an NPC definition
        :param NpcDef npc_def: The NPC definition to base this NPC off of
        :param room.Room location: The room the NPC is located within
        """
        self.id = npc_def.id
        self.npc_def = npc_def
        self.hp = self.npc_def.maxHp
        self.location = location
