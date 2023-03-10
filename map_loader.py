import json
from log_manager import LogManager
from room import Room


game_map = dict()


def load_map_file(map_file_name: str):
    """Load a map file
    map_file_name: The name of the map file to load"""

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

    # Loop through every object in the JSON array to create a new room
    for json_obj in map_json:
        new_room = Room()

        # Now loop through every attribute of the JSON object and assign it to a class member
        for key, value in json_obj.items():
            if key in new_room.__dict__.keys():
                new_room.__dict__[key] = value

        # Add the room to the map
        game_map[new_room.id] = new_room

    map_file.close()


if __name__ == "__main__":
    """Try to read the room file dumped from the Room class test to test map loader"""
    load_map_file("room.eqm")