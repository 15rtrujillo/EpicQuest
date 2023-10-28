class NpcDef:
    """Holds information about NPCs"""

    def __init__(self):
        """Create a new NPC definition"""
        self.id = -1
        self.name = ""
        self.desc = ""
        self.maxHp = 100
        self.attackable = False
        self.blocking = False
        self.respawn_ticks = 100
