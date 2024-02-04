from external.npc_def import NpcDef
from external.region_def import RegionDef
from external.room_def import RoomDef
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

    def load_region_defs(self):
        """Load region definitions from file"""
        regions_directory = file_utils.get_regions_directory()
        region_files = file_utils.get_files_in_directory(regions_directory)
        for file_name in region_files:
            new_region_def = game_data_loader.load_region_file(file_name)
            # We check for -1 to disregard test regions
            if new_region_def is None or new_region_def.id == -1:
                continue

            # Make sure a region with this ID doesn't already exist
            if new_region_def.id in self.region_defs.keys():
                LogManager.get_logger().warn(f"The region {new_region_def.name} has the same ID as "
                                             f"{self.region_defs[new_region_def.id].name} (ID: "
                                             f"{new_region_def.id})\n{new_region_def.name} was not loaded.")
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

                if new_npc_def.id in self.npc_defs.keys():
                    LogManager.get_logger().warn(f"The NPC {new_npc_def.name} has the same ID as "
                                                 f"{self.npc_defs[new_npc_def.id].name} (ID: "
                                                 f"{new_npc_def.id})\n{new_npc_def.name} was not loaded.")
                    continue

                self.npc_defs[new_npc_def.id] = new_npc_def

    def instantiate_region(self, region_id) -> Region:
        """
        Instantiate a region based on a region definition
        :param int region_id: The ID of the region to instantiate
        :rtype: Region
        :return: The new region instance
        """
        # Create a region
        region_def = self.region_defs[region_id]
        region = Region(region_def)
        rooms: dict[int, Room] = dict()

        # Create rooms in the region
        for room_id in region_def.room_defs.keys():
            room = self.instantiate_room(room_id, region)
            # Add the room to a dictionary for now
            rooms[room_id] = room

        # Go through the room dictionary and add all the connections
        directions = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest", "up",
                      "down"]
        for room in rooms.values():
            room_dict = room.__dict__
            room_def_dict = room.room_def.__dict__
            for direction in directions:
                direction_id = room_def_dict[direction]
                if direction_id != -1:
                    room_dict[direction] = rooms[direction_id]

        region.starting_room = rooms[0]
        return region

    def instantiate_room(self, room_id: int, located_in: Region) -> Room:
        """
        Instantiate a room based on a room definition
        :param int room_id: The ID of the room to instantiate
        :param Region located_in: The region this room is located in
        :rtype: Room
        :return: The new room instance
        """
        room_def = self.region_defs[located_in.id].room_defs[room_id]
        room = Room(room_def, located_in)
        # Create NPCs in the room
        for npc_id in room_def.npc_ids:
            npc = Npc(self.npc_defs[npc_id], room)
            room.npcs.append(npc)
        return room

    def instantiate_npc(self, npc_id: int, location: Room) -> Npc:
        """
        Instantiate an NPC based on an NPC definition
        :param int npc_id: The ID of the NPC to instantiate
        :param Room location: The room the NPC is located in
        :rtype: NPC
        :return: The new NPC instance
        """
        raise NotImplementedError()

    def populate_world(self):
        """Instantiate the world based on the definitions"""
        for region_id in self.region_defs.keys():
            region = self.instantiate_region(region_id)
            self.regions[region_id] = region
