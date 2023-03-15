from logger.log_manager import LogManager
from map import Map
from room import Room


import json
import file_utils


def load_map_file(map_file_name: str) -> Map:
    """Load a map file and return a map dictionary of Room IDs to Room objects
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
        return
    
    # Attempt to load the JSON from file
    try:
        map_json = json.loads(map_file.read())
    except json.JSONDecodeError:
        LogManager.get_logger().error(f"Error reading map file: {map_file_name} - The file is possibly corrupted.")
        return
    
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


def load_all():
    """Load all game definitions"""
    map_files = file_utils.get_files_in_directory(file_utils.get_maps_directory())
    for map_file in map_files:
        # TODO: Figure out what to actually do with the loaded map. Like, where to store the master map?
        load_map_file(map_file)


if __name__ == "__main__":
    """Try to read the test map file dumped from the Map class test to test map loader"""
    test_map = load_map_file("test_map.eqm")

    for key, value in test_map.__dict__.items():
        print(key, value)