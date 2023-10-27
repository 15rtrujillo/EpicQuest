from external.npc_def import Npc
from external.region_def import RegionDef
from external.room_def import RoomDef
from input_output.logger.log_manager import LogManager


import input_output.file_utils as file_utils
import json


def load_region_file(region_file_name: str) -> RegionDef | None:
    """Load a region file and return a new region object containing all the loaded Rooms.
    region_file_name: The name of the region file to load"""
    # Get the absolute path for the region file
    region_directory = file_utils.get_regions_directory()
    region_file_path = file_utils.get_file_path(region_directory, region_file_name)

    # Attempt to open the region file
    region_file = None
    try:
        region_file = open(region_file_path, "r")
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open region file: {region_file_name} at {region_file_path} - The file does not exist.")
        return None
    
    # Attempt to load the JSON from file
    try:
        region_json = json.loads(region_file.read())
    except json.JSONDecodeError:
        LogManager.get_logger().error(f"Error reading region file: {region_file_name} - The file is possibly corrupted.")
        return None
    
    # Get the region's ID and name
    new_region = RegionDef(region_json["id"], region_json["name"])

    # Get the rooms. This should return a list of Room objects
    rooms = region_json["rooms"]
    for room in rooms:
        new_room = RoomDef()
        
        # Loop through the key, value pairs in the room object
        for key, value in room.items():
            # Make sure we're only attempting to add good data
            if key in new_room.__dict__.keys():
                new_room.__dict__[key] = value
        
        # Add the new room to the region
        new_region.add_room(new_room)

    region_file.close()

    LogManager.get_logger().info(f"Loaded {len(new_region.rooms)} Room definitions from {region_file_name}")

    return new_region


def load_npc_file(npc_file_name: str) -> list[Npc] | None:
    """Load a NPC file and return a list of loaded NPCs.
    npc_file_name: The name of the map file to load"""
    # Get the absolute path for the NPC file
    npc_directory = file_utils.get_npcs_directory()
    npc_file_path = file_utils.get_file_path(npc_directory, npc_file_name)

    # Attempt to open the NPC file
    npc_file = None
    try:
        npc_file = open(npc_file_path, "r")
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open NPC file: {npc_file_name} at {npc_file_path} - The file does not exist.")
        return None
    
    # Attempt to load the JSON from file
    try:
        npc_json = json.loads(npc_file.read())
    except json.JSONDecodeError:
        LogManager.get_logger().error(f"Error reading NPC file: {npc_file_name} - The file is possibly corrupted.")
        return None
    
    # The npc_json should be a list of JSON objects. We will loop through these objects and create NPCs
    npcs = []
    for npc in npc_json:
        new_npc = Npc()

        # Loop through the key, value pairs in the Npc JSON object
        for key, value in npc.items():
            # Make sure we're only attempting to add good data
            if key in new_npc.__dict__.keys():
                new_npc.__dict__[key] = value
        
        # Add the new room to the map
        npcs.append(new_npc)

    npc_file.close()

    LogManager.get_logger().info(f"Loaded {len(npcs)} NPC definitions from {npc_file_name}")

    return npcs


if __name__ == "__main__":
    """Try to read the test map file dumped from the Map class test to test map loader"""
    test_map = load_region_file("test_map.eqm")

    for key, value in test_map.__dict__.items():
        print(key, value)

    test_npcs = load_npc_file("test_npcs.eqn")

    for npc in test_npcs:
        print(npc)
