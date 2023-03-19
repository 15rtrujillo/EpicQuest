import os


script_path = os.path.dirname(os.path.abspath(__file__))


def get_file_path(file_name: str) -> str:
    """Returns an absolute path to the given file name
    file_name: The name of the file to append"""
    return os.path.join(script_path, os.path.relpath(file_name))


def get_files_in_directory(directory: str) -> list[str]:
    """Returns a list of the names of all the files in a directory (including extensions)"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def get_saves_directory() -> str:
    """Returns the directory for save files"""
    return os.path.join(script_path, "saves")


def get_maps_directory() -> str:
    """Returns the directory for the map files"""
    return os.path.join(script_path, os.path.relpath("defs/maps"))


def get_npcs_directory() -> str:
    """Returns the directory for the NPC files"""
    return os.path.join(script_path, os.path.relpath("defs/npcs"))


def create_saves_directory():
    """Creates the directory for storing save files - Unused"""
    os.mkdir(get_saves_directory())


if __name__ == "__main__":
    print(get_maps_directory())
    print(get_saves_directory())
