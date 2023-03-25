from entity.npc import Npc
from entity.player import Player
from map import Map
from room import Room

import interface.game as game_interface


class ScriptContext:
    """Holds the context for the current plugin"""

    def __init__(self):
        """Create a context for the script"""
        self.game: game_interface.Game | None = None
        self.interacting_player: Player | None = None
        self.interacting_npc: Npc | None = None
        self.interacting_map: Map | None = None
        self.interacting_room: Room | None = None
        # self.interacting_item: Item | None = None

    def clear_context(self):
        self.game = None
        self.interacting_player = None
        self.interacting_npc = None
        self.interacting_map = None
        self.interacting_room = None
