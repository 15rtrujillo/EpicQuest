from datetime import datetime


class Logger:
    """Handles logging to a file"""

    DEBUG = True

    def __init__(self, file_path: str):
        """
        Create a Logger
        :param str file_path: The path to the log file
        """
        self.file_path = file_path

    def info(self, message: str):
        """
        Log an information message
        :param str message: The info message to be logged
        """
        self.__log("INFO", message)

    def warn(self, message: str):
        """
        Log a warning message
        :param str message: The warning message to be logged
        """
        self.__log("WARN", message)

    def error(self, message: str):
        """
        Log an error message
        :param str message: The error message to be logged
        """
        self.__log("ERROR", message)
        
    def __log(self, message_type: str, message: str):
        """
        Log a message to file
        :param str message_type: The type of message to log. Will be prefixed to the message
        :param str message: The message to be logged
        """
        log_message = f"[{self.__get_timestamp()}] [{message_type}] {message}\n"

        # If debug mode is on, we will print log messages to the console as well as to file
        if Logger.DEBUG:
            print(log_message, end="")

        with open(self.file_path, "a") as log_file:
            log_file.write(log_message)

    @staticmethod
    def __get_timestamp() -> str:
        """
        Get the current timestamp
        :rtype: str
        :return: A timestamp in YYYY-mm-dd HH:MM:SS format
        """
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    logger = Logger("test.log")
    logger.info("This is an info test")
    logger.warn("This is a warn test")
    logger.error("This is an error test")
