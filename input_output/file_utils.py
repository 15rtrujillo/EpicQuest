import os


BASE_DIRECTORY: str = os.getcwd()


def get_file_path(path_to_file: str, file_name: str) -> str:
    """
    Essentially a wrapper for os.path.join
    :param str path_to_file: The directory the file is contained in
    :param str file_name: The name of the file
    :rtype: str
    :return: A path that appends the file name to the end of the path to the file
    """
    return os.path.join(path_to_file, file_name)


def get_files_in_directory(directory: str) -> list[str]:
    """
    Get a list of the names of all the files in a directory (including extensions)
    :rtype: list[str]
    :return: A list of the files (with extensions) in a directory
    """
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files


def get_saves_directory() -> str:
    """
    Obtain the path to the save file directory
    :rtype: str
    :return: A path to the save file directory
    """
    return os.path.join(BASE_DIRECTORY, "saves")


def get_regions_directory() -> str:
    """
    Obtain the path to the region files directory
    :rtype: str
    :return: A path to the region files directory
    """
    return os.path.join(BASE_DIRECTORY, "defs", "regions")


def get_npcs_directory() -> str:
    """
    Obtain the path to the NPC files directory
    :rtype: str
    :return: A path to the NPC files directory
    """
    return os.path.join(BASE_DIRECTORY, "defs", "npcs")


def create_saves_directory():
    """Creates the directory for storing save files"""
    os.mkdir(get_saves_directory())


if __name__ == "__main__":
    print(get_regions_directory())
    print(get_saves_directory())
    print(get_npcs_directory())
