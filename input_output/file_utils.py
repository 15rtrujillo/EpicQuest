import os


BASE_DIRECTORY = os.getcwd()


def get_file_path(path_to_file: str, file_name: str) -> str:
    """Essentially a wrapper for os.path.join
    path_to_file: The directory the file is contained in
    file_name: The file"""
    return os.path.join(path_to_file, file_name)


def get_files_in_directory(directory: str) -> list[str]:
    """Returns a list of the names of all the files in a directory (including extensions)"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def get_saves_directory() -> str:
    """Returns the directory for save files"""
    return os.path.join(BASE_DIRECTORY, "saves")


def get_regions_directory() -> str:
    """Returns the directory for the map files"""
    return os.path.join(BASE_DIRECTORY, "defs", "regions")


def get_npcs_directory() -> str:
    """Returns the directory for the NPC files"""
    return os.path.join(BASE_DIRECTORY, "defs", "npcs")


def create_saves_directory():
    """Creates the directory for storing save files - Unused"""
    os.mkdir(get_saves_directory())


if __name__ == "__main__":
    print(get_regions_directory())
    print(get_saves_directory())
    print(get_npcs_directory())
