from builtins import isinstance
from ast import Return
import random
import asyncio
import os
import sys

from .Logger import Logger
from .Compile import Compile
from .Run import Run, RunResult
from .DataModel import CodeFile
from .ExecCommand import ExecResult
from .InputGenerator import InputGenerator
from tabulate import tabulate

class CheckerBase:
    def __init__(self, generator : InputGenerator):
        self._logger = Logger.get_logger()
        self._compile_handler = Compile()
        self._run_handler = Run()
        self._input_gen = generator

    def gen_input(self) -> str:
        raise NotImplementedError("This function must be implemented")

    @property
    def run_count(self) -> int:
        return 20

    async def compile_file(self, *files : CodeFile) -> bool:
        tasks : list[asyncio.Task] = []
        async with asyncio.TaskGroup() as tg:
            for file in files:
                task = tg.create_task(self._compile_handler.async_compile(file))
                tasks.append(task)
        for task in tasks:
            if not task.result():
                return False
        return True
    
    async def run_files(self, data : str, *files : CodeFile) -> list[RunResult]:
        tasks : list[asyncio.Task] = []

        async with asyncio.TaskGroup() as tg:
            for file in files:
                task = tg.create_task(self._run_handler.async_run(file, data))
                tasks.append(task)
        return [task.result() for task in tasks]

    def check_output(self, output : list[str]):
        return all(el == output[0] for el in output) if len(output) > 0 else True
    
    def __print_error_output(self, output : list[str], data : str, *files : CodeFile):
        self._logger.error(f"ERROR!!! Check fail output")
        self._logger.error(f"Data:\n{data}")
        self._logger.error("")
        outputs = [o.splitlines() for o in output]
        headers = [file.file_name for file in files] 
        outputs = [list(row) for row in zip(*outputs)]
        self._logger.debug(f"Result: \n {tabulate(tabular_data=outputs, headers=headers)}")
        self._logger.debug("")
    
    def __print_success_output(self, output : list[str], data : str, *files : CodeFile):
        self._logger.debug(f"Check success")
        self._logger.debug(f"Data:\n{data}")

    async def check(self, *files : CodeFile):
        self._logger.info(f"Checking...")
        self._logger.info("")
        success = True
        for i in range(self.run_count):
            self._logger.debug("")
            self._logger.debug("="*20)
            self._logger.debug(f"Attempt {i + 1}:")
            data = self._input_gen.gen_input()
            results = await self.run_files(data, *files)
            output : list[str]= []
            for result in results:
                code_file = result.code_file
                if not result.success:
                    success = False
                    self._logger.error(f"Fail to run file {code_file.file_name}")
                    self._logger.error(f"Data:\n{data}")
                    break
                output.append(result.get_clean_stdout())
            else:
                if not self.check_output(output):
                    success = False
                    self.__print_error_output(output, data, *files)
                else:
                    self.__print_success_output(output, data, *files)
        if success:
            self._logger.info("Success")

    def run(self, *files : str) -> None:
        code_files = [CodeFile(file) for file in files]
        if not asyncio.run(self.compile_file(*code_files)):
            self._logger.error(f"Fail to compile file. please check")
            return 
    
        asyncio.run(self.check(*code_files))
        for code_file in code_files:
            if code_file.executable_name:
                code_file.remove()
