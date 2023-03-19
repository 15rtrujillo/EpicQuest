from abc import ABC
from entity.npc import Npc


class TalkToNpcTrigger(ABC):
    """Abstract class with methods to handle talking to NPCs"""

    def talk_to_npc(self, npc: Npc):
        """The code to be ran when an NPC is spoken to
        npc: The NPC being spoken to"""
        pass
