from logger.log_manager import LogManager
from map import Map
from room import Room

import json
import file_utils


game_map = dict()


def load_map_file(map_file_name: str):
    """Load a map file
    map_file_name: The name of the map file to load"""

    # Get the absolute path for the map file
    # FIXME: This needs to be updated to use the maps path
    map_file_name = file_utils.get_file_path(f"defs/{map_file_name}")

    # Attempt to open the map file
    map_file = None
    try:
        map_file = open(map_file_name, "r")
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

    # Loop through every object in the JSON array to create a new room
    for json_obj in map_json:
        new_room = Room()

        # Now loop through every attribute of the JSON object and assign it to a class member
        for key, value in json_obj.items():
            if key in new_room.__dict__.keys():
                new_room.__dict__[key] = value

        # Add the room to the map
        if not new_room.id in game_map.keys():
            game_map[new_room.id] = new_room
        else:
            LogManager.get_logger().warn(f"Room ID {new_room.id} in map file {map_file_name} already exists")

    map_file.close()

    LogManager.get_logger().info(f"Loaded {len(game_map)} Room definitions from {map_file_name}")


def load_all():
    """Load all game definitions"""
    load_map_file("game_map.eqm")


if __name__ == "__main__":
    """Try to read the room file dumped from the Room class test to test map loader"""
    load_map_file("room.eqm")