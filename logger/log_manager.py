from logger.logger import Logger

import file_utils


class LogManager:
    """Manages the singleton Logger"""

    __logger = None

    def get_logger() -> Logger:
        """Get the logger object"""
        if LogManager.__logger == None:
            LogManager.__logger = Logger(file_utils.get_file_path("epicquest.log"))
        return LogManager.__logger