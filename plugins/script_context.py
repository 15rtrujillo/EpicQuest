from external.npc_def import Npc
from entity.player import Player
from map_def import MapDef
from room_def import RoomDef

import interface.game as game_interface


class ScriptContext:
    """Holds the context for the current plugin"""

    def __init__(self):
        """Create a context for the script"""
        self.game: game_interface.Game | None = None
        self.interacting_player: Player | None = None
        self.interacting_npc: Npc | None = None
        self.interacting_map: MapDef | None = None
        self.interacting_room: RoomDef | None = None
        # self.interacting_item: Item | None = None

    def clear_context(self):
        self.game = None
        self.interacting_player = None
        self.interacting_npc = None
        self.interacting_map = None
        self.interacting_room = None
