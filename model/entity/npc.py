from external.npc_def import NpcDef


class Npc:
    def __init__(self, npcDef: NpcDef):
        self.id = npcDef.id
        self.npcDef = npcDef
