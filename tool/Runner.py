import os
import sys
import subprocess
from typing import Optional

from .Logger import Logger

class Runner:
    def __init__(self, main_file: str, debug: bool = True, file_io: bool = True):
        self.main_file = main_file
        self._output_file = "output.exe"
        self._logger = Logger.get_logger()
        self.debug = debug
        self.file_io = file_io
    
    def __get_additional_include_path(self)  -> str:
        path = os.path.join(os.path.dirname(__file__), os.pardir, "include")
        return os.path.abspath(path)

    def compile(self):
        if sys.platform == "darwin":
            self._logger.debug("On MACOS machine, add include path to compile command")
            compile_command = f"g++ {self.main_file} -I{self.__get_additional_include_path()} -o {self._output_file} -std=gnu++17"
        else:
            compile_command = f"g++ {self.main_file} -o {self._output_file} -std=gnu++17"

        if self.debug:
            compile_command += " -D__DEBUG__"
        if self.file_io:
            compile_command += " -DLOCALONLY"
        self._logger.debug(f"Compiling {self.main_file} with command: {compile_command}")
        result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {result.stderr}")
        self._logger.info(f"Compiled {self.main_file} successfully.")
        return self._output_file

    def run(self, input_data: Optional[str] = None):
        output_file = self.compile()

        run_command = f"./{output_file}"
        if input_data is None:
            process = subprocess.run(run_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            stdout = process.stdout.decode('utf-8')
            stderr = process.stderr.decode('utf-8')
        else:
            process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=input_data)

        os.remove(output_file)
        if process.returncode != 0 or stderr:
            self._logger.error(f"Error during execution: {stderr}")
            return ""

        self._logger.info("Execution completed successfully.")
        if not self.file_io:
            self._logger.info(f"Output:\n{stdout.strip()}")
