from external.npc_def import NpcDef
from external.region_def import RegionDef
from input_output.logger.log_manager import LogManager
from model.entity.npc import Npc
from model.world.region import Region
from model.world.room import Room


import input_output.file_utils as file_utils
import input_output.game_data_loader as game_data_loader


class World:
    """The game world. Contains instances and definitions"""

    def __init__(self):
        """Initialize the game world."""
        self.regions: dict[int, Region] = dict()
        self.region_defs: dict[int, RegionDef] = dict()
        self.npc_defs: dict[int, NpcDef] = dict()

        self.load_region_defs()
        self.load_npc_defs()
        self.populate_world()

    def load_region_defs(self):
        """Load region definitions from file"""
        regions_directory = file_utils.get_regions_directory()
        region_files = file_utils.get_files_in_directory(regions_directory)
        for file_name in region_files:
            new_region_def = game_data_loader.load_region_file(file_name)
            # We check for -1 to disregard test regions
            if new_region_def is None or new_region_def.id == -1:
                continue
            self.region_defs[new_region_def.id] = new_region_def

    def load_npc_defs(self):
        """Load NPC definitions from file"""
        npcs_directory = file_utils.get_npcs_directory()
        npc_files = file_utils.get_files_in_directory(npcs_directory)
        for file_name in npc_files:
            npc_def_list = game_data_loader.load_npc_file(file_name)
            if npc_def_list is None:
                continue
            for new_npc_def in npc_def_list:
                # Discard test npcs
                if new_npc_def.id == -1:
                    continue
                self.npc_defs[new_npc_def.id] = new_npc_def

    def populate_world(self):
        """Instantiate the world based on the definitions"""
        regions_created = 0
        rooms_created = 0
        npcs_created = 0
        for region_def in self.region_defs.values():
            # Create a region
            region = Region(region_def)
            rooms: dict[int, Room] = dict()

            # Create rooms in the region
            for room_def in region_def.room_defs.values():
                room = Room(room_def, region)

                # Create NPCs in the room
                for npc_id in room_def.npc_ids:
                    npc = Npc(self.npc_defs[npc_id], room)
                    npcs_created += 1
                    room.npcs.append(npc)

                # Add the room to a dictionary for now
                rooms_created += 1
                rooms[room.id] = room

            # Go through the room dictionary and add all the connections                
            directions = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest", "up", "down"]
            for room in rooms.values():
                room_dict = room.__dict__
                room_def_dict = room.room_def.__dict__
                for direction in directions:
                    direction_id = room_def_dict[direction]
                    if direction_id != -1:
                        room_dict[direction] = rooms[direction_id]

            region.starting_room = rooms[0]
            regions_created += 1
            self.regions[region.id] = region
        LogManager.get_logger().info(f"Initialized {npcs_created} NPCs in {rooms_created} rooms in {regions_created} regions")
