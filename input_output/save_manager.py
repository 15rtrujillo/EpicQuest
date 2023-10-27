from input_output.logger.log_manager import LogManager
from model.entity.player import Player


import input_output.file_utils as file_utils


def get_bytes(value) -> bytes:
    """Convert a specific datatype to bytes for saving"""
    if isinstance(value, str):
        return value.encode()
    elif isinstance(value, int):
        return value.to_bytes(4, "big")
    elif isinstance(value, bool):
        return value.to_bytes(2, "big")
    

def get_data(value: bytes, data_type: type):
    """Convert bytes to a specific datatype for loading"""
    if data_type == str:
        return value.decode()
    elif data_type == int:
        return int.from_bytes(value, "big")
    elif data_type == bool:
        return bool.from_bytes(value, "big")


def get_saves() -> list[str]:
    """Get the names of the players saved in the saves directory"""
    save_files = file_utils.get_files_in_directory(file_utils.get_saves_directory())

    player_names = []
    for file in save_files:
        if file.find(".eq") == -1:
            continue
        player_names.append(file[:file.find(".eq")])
    return player_names


def save(player: Player):
    """Save a player to a binary file at \"[player_name].eq\"
    player: The player to save"""
    save_file_name = file_utils.get_file_path(file_utils.get_saves_directory(), f"{player.name}.eq")
    
    with open(save_file_name, "wb") as save_file:
        save_data = b""
        player_data = player.__dict__
        for key, value in player_data.items():
            save_data += key.encode()
            save_data += b":"
            save_data += get_bytes(value)
            save_data += b"\n"
        save_file.write(save_data)


def load(name: str) -> Player | None:
    """Load a player from a binary file
    name: The name of the player to attempt to load"""
    save_file_name = file_utils.get_file_path(file_utils.get_saves_directory(), f"{name}.eq")

    loaded_data: dict[str, bytes] = dict()

    # Read in everything from the file to populate the dictionary
    try:
        with open(save_file_name, "rb") as save_file:
            for line in save_file.readlines():
                line_data = line.split(b":")
                key = line_data[0].decode()
                value = line_data[1]
                loaded_data[key] = value
    except FileNotFoundError:
        LogManager.get_logger().error(f"Could not open save file: {save_file_name} - The file does not exist.")
        return None

    # Get all the attributes from the player class
    loaded_player = Player(loaded_data["name"].decode())
    player_data = loaded_player.__dict__

    # Match the stuff from the file to the player class
    for key, value in loaded_data.items():
        # Make sure the key from the file exists in the player class
        if key in player_data.keys():
            # Convert the binary data to whatever datatype the class member is
            # We need to trim the end of the value by 1 to get rid of the newline character
            player_data[key] = get_data(value[:-1], type(player_data[key]))
        else:
            LogManager.get_logger().warn(f"Key `{key}` found in save file with value `{value}`. This has most likely "
                                         f"been deprecated and will be removed the next time the player is saved.")

    return loaded_player


if __name__ == "__main__":
    test = Player("test")
    test.gold = 14345
    test.hp = 200
    test.maxhp = 200
    test.level = 4
    print(test.__dict__)
    save(test)
    loaded_test = load("test")

    print(loaded_test.__dict__)

    print(get_saves())
