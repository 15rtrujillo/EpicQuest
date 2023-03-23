from logger.log_manager import LogManager
from map import Map
from entity.npc import Npc
from room import Room


import json
import file_utils


def load_map_file(map_file_name: str) -> Map:
    """Load a map file and return a new Map object containing all the loaded Rooms.
    map_file_name: The name of the map file to load"""

    # Get the absolute path for the map file
    map_files_path = file_utils.get_maps_directory()
    map_file_path = file_utils.get_file_path(map_files_path + "/" + map_file_name)

    # Attempt to open the map file
    map_file = None
    try:
        map_file = open(map_file_path, "r")
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open map file: {map_file_name} - The file does not exist.")
        return None
    
    # Attempt to load the JSON from file
    try:
        map_json = json.loads(map_file.read())
    except json.JSONDecodeError:
        LogManager.get_logger().error(f"Error reading map file: {map_file_name} - The file is possibly corrupted.")
        return None
    
    # Get the map's ID and name
    new_map = Map(map_json["id"], map_json["name"])

    # Get the rooms. This should return a list of Room objects
    rooms = map_json["rooms"]
    for room in rooms:
        new_room = Room()
        
        # Loop through the key, value pairs in the room object
        for key, value in room.items():
            # Make sure we're only attempting to add good data
            if key in new_room.__dict__.keys():
                new_room.__dict__[key] = value
        
        # Add the new room to the map
        new_map.add_room(new_room)

    map_file.close()

    LogManager.get_logger().info(f"Loaded {len(new_map.rooms)} Room definitions from {map_file_name}")

    return new_map


def load_npc_file(npc_file_name: str) -> list[Npc]:
    """Load a NPC file and return a list of loaded NPCs.
    npc_file_name: The name of the map file to load"""
    # Get the absolute path for the map file
    npc_files_path = file_utils.get_npcs_directory()
    npc_file_path = file_utils.get_file_path(npc_files_path + "/" + npc_file_name)

    # Attempt to open the map file
    npc_file = None
    try:
        npc_file = open(npc_file_path, "r")
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open NPC file: {npc_file_name} - The file does not exist.")
        return None
    
    # Attempt to load the JSON from file
    try:
        npc_json = json.loads(npc_file.read())
    except json.JSONDecodeError:
        LogManager.get_logger().error(f"Error reading map file: {npc_file_name} - The file is possibly corrupted.")
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
    test_map = load_map_file("test_map.eqm")

    for key, value in test_map.__dict__.items():
        print(key, value)

    test_npcs = load_npc_file("test_npcs.eqn")

    for npc in test_npcs:
        print(npc)
