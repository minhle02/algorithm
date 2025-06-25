import logging
import os

from typing import Optional

class Logger:
    _logger : Optional[logging.Logger] = None
    _default_file = os.path.join(os.path.dirname(__file__), "log", "output.log")
    _error_file =  os.path.join(os.path.dirname(__file__), "log", "error.log")

    @staticmethod
    def create_folder():
        if not os.path.exists(os.path.dirname(Logger._default_file)):
            os.makedirs(os.path.dirname(Logger._default_file))
        with open(Logger._default_file, "w") as f:
            f.write("")
        with open(Logger._error_file, "w") as f:
            f.write("")

    @staticmethod
    def get_logger() -> logging.Logger:
        if not Logger._logger:
            Logger._logger = logging.getLogger(__name__)
            Logger.create_folder()
            Logger._logger.setLevel(logging.DEBUG)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            Logger._logger.addHandler(stream_handler)

            file_handler = logging.FileHandler(Logger._default_file)
            file_handler.setLevel(logging.DEBUG)
            Logger._logger.addHandler(file_handler)

            error_file_handler = logging.FileHandler(Logger._error_file)
            error_file_handler.setLevel(logging.DEBUG)
            Logger._logger.addFilter(error_file_handler)
        return Logger._logger
