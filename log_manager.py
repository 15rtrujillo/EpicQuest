from logger import Logger


class LogManager:
    """Manages the singleton Logger"""

    __logger = None

    def get_logger() -> Logger:
        """Get the logger object"""
        if LogManager.__logger == None:
            LogManager.__logger = Logger(f"{test_name}.log")
        return LogManager.__logger