from abc import ABC


class TalkToNpcTrigger(ABC):
    """Abstract class with methods to handle talking to NPCs"""

    def talk_to_npc(self) -> bool:
        """The code to be run when an NPC is spoken to"""
        pass
