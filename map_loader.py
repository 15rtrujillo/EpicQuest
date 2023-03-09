import json
from log_manager import LogManager
from room import Room


game_map = dict()


def load_map_file(map_file_name: str):
    """Load a map file
    map_file_name: The name of the map file to load"""
    map_file = None
    try:
        map_file = open(map_file_name, "r")
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open the provided map file: {map_file_name} - The file does not exist.")
        return
    
    map_json = json.loads(map_file.read())

    # Read the JSON into a Room class
    print(map_json)

    map_file.close()


if __name__ == "__main__":
    load_map_file("room.eqm")