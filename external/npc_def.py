class NpcDef:
    """Definition of an NPC read from file"""

    def __init__(self):
        """Create a new NPC definition"""
        self.id = -1
        self.name = ""
        self.description = ""
        self.maxHp = 100
        self.attackable = False
        self.blocking = False
        self.respawn_ticks = 100
