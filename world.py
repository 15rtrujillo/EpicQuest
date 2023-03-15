from logger.log_manager import LogManager
from map import Map
from entity.npc import Npc


class World:
    """Holds all the data about the game world, including map, NPC, and item definitions"""

    world_map = dict()
    items = dict()
    npcs = dict()


    def add_map(map: Map):
        """Add a map to the world map
        map: The map to add"""
        if map.id in World.world_map.keys():
            LogManager.get_logger().warn(f"Attempted to add Map with ID {map.id} to world map, but a Map with the same ID already exists. New Map was not added.")
            return
        World.world_map[map.id] = map


    def add_npc(npc: Npc):
        """Add an NPC to the NPC definitions dictionary
        npc: The NPC to add"""
        if npc.id in World.npcs.keys():
            LogManager.get_logger().warn(f"Attempted to add NPC with ID {npc.id} to NPC defs list, but an NPC with the same ID already exists. New NPC was not added.")
            return
        World.npcs[npc.id] = npc