import os


script_path = os.path.dirname(os.path.abspath(__file__))


def get_file_path(file_name: str) -> str:
    """Returns an absolute path to the given file name
    file_name: The name of the file to append"""
    return os.path.join(script_path, os.path.relpath(file_name))


def get_saves_directory() -> str:
    """Returns the directory for save files"""
    return os.path.join(script_path, "saves")


def get_maps_directory() -> str:
    """Returns the directory for the map files"""
    return os.path.join(script_path, os.path.relpath("defs/maps"))


def create_saves_directory():
    """Creates the directory for storing save files"""
    os.mkdir(get_saves_directory())


if __name__ == "__main__":
    print(get_maps_directory())
    print(get_saves_directory())