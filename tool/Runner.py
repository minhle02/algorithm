import os
import sys
import subprocess
from typing import Optional

from .Logger import Logger
from .Compile import Compile
from .DataModel import CodeFile
from .Run import Run

class Runner:
    def __init__(self, main_file: str, debug: bool = True, file_io: bool = True):
        self._compile_handler = Compile()
        self._run_handler = Run()
        self._file = CodeFile(main_file)
        self._logger = Logger.get_logger()
        if debug:
            self._compile_handler.set_debug()
        
        if file_io:
            self._compile_handler.set_fileio()
    
    def __get_additional_include_path(self)  -> str:
        path = os.path.join(os.path.dirname(__file__), os.pardir, "include")
        return os.path.abspath(path)

    def run(self, input_data: Optional[str] = None):
        if self._compile_handler.sync_compile(self._file):
            data = self._run_handler.sync_run(self._file)
            if self._file.executable_name:
                os.remove(self._file.executable_name)
            if data:
                self._logger.info(f"Output of running file {self._file.file_name}:")
                self._logger.info(data.stdout)
        else:
            self._logger.error(f"Compilation Failed. Please check")
