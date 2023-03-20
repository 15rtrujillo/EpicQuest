from abc import ABC
from entity.npc import Npc
from entity.player import Player


class TalkToNpcTrigger(ABC):
    """Abstract class with methods to handle talking to NPCs"""

    def talk_to_npc(self, player: Player, npc: Npc) -> bool:
        """The code to be ran when an NPC is spoken to
        player: The player
        npc: The NPC being spoken to"""
        pass
