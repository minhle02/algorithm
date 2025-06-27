from builtins import bool
from dataclasses import dataclass
from builtins import ValueError
from ast import Pass
from sys import stderr
from builtins import staticmethod
from .DataModel import CodeFile, CodeFileType
from .Logger import Logger
from .ExecCommand import ExecCmdHandler, ExecResult
from abc import ABC, abstractmethod
from typing import *
import asyncio
import sys
import os
import subprocess

@dataclass
class RunResult:
    success : bool
    stdout : Optional[str]
    stderr : Optional[str]
    code_file : CodeFile

class RunFileBaseHandler(ABC):
    def __init__(self, code_file : CodeFile, data : Optional[str] = None):
        assert os.path.exists(code_file.file_name), f"File not found: {code_file.file_name}"
        self._code_file = code_file
        self._logger = Logger.get_logger()
        self._data : Optional[str] = data
    
    @property
    def code_file(self) -> CodeFile:
        return self._code_file
    
    @property
    def input_data(self) -> Optional[str]:
        return self._data
    
    @abstractmethod
    async def async_run(self) -> RunResult:
        pass
    
    @abstractmethod
    def sync_run(self) -> RunResult:
        pass

    def log_sync_result(self, result : ExecResult) -> None:
        self._logger.debug(f"(Sync) Run with command: {result.cmd}")
        if result.stderr or result.return_code != 0:
            self._logger.error(f"Run file {self.code_file.file_name} return error, please check")
            self._logger.error(f"stderr:\n{result.stderr}")
            self._logger.error("")
            self._logger.error(f"stdout:\n{result.stdout}")
        else:
            self._logger.debug(f"Run file {self.code_file.file_name} success")
        
    async def log_async_result(self, result : ExecResult, lock : asyncio.Lock) -> None:
        async with lock:
            self._logger.debug(f"(ASYNC) Run with command: {result.cmd}")
            if result.stderr or result.return_code != 0:
                self._logger.error(f"Run file {self.code_file.file_name} return error, please check")
                self._logger.error(f"stderr:\n{result.stderr}")
                self._logger.error("")
                self._logger.error(f"stdout:\n{result.stdout}")
            else:
                self._logger.debug(f"Run file {self.code_file.file_name} success")


class CppRunHandler(RunFileBaseHandler):
    _lock : asyncio.Lock = asyncio.Lock()
    def __init__(self, code_file : CodeFile, data : Optional[str]):
        assert code_file.file_type == CodeFileType.CPP
        super().__init__(code_file, data)
        self._logger = Logger.get_logger()
        self._exec_cmd_handler = ExecCmdHandler()

    @override
    async def async_run(self) -> RunResult:
        cmd = f"./{self.code_file.executable_name}"
        result = await self._exec_cmd_handler.async_exec([cmd], self._data)
        
        await self.log_async_result(result, CppRunHandler._lock)

        return RunResult(result.is_success(), result.stdout, result.stderr, self.code_file)
    
    @override
    def sync_run(self) -> RunResult:
        cmd = f"./{self.code_file.executable_name}"
        result = self._exec_cmd_handler.sync_exec([cmd], self._data)
        self.log_sync_result(result)
        return RunResult(result.is_success(), result.stdout, result.stderr, self.code_file)
    

class PythonRunHandler(RunFileBaseHandler):
    _lock : asyncio.Lock = asyncio.Lock()
    def __init__(self, code_file : CodeFile, data : Optional[str]):
        assert code_file.file_type == CodeFileType.PYTHON
        super().__init__(code_file, data)
        self._logger = Logger.get_logger()
        self._exec_cmd_handler = ExecCmdHandler()
    
    @override
    async def async_run(self) -> RunResult:
        cmds = ["uv", "run", self.code_file.file_name]
        result = await self._exec_cmd_handler.async_exec(cmds, self._data)
        await self.log_async_result(result, PythonRunHandler._lock)
        return RunResult(result.is_success(), result.stdout, result.stderr, self.code_file)
    
    @override
    def sync_run(self) -> RunResult:
        cmds = ["uv", "run", self.code_file.file_name]
        result = self._exec_cmd_handler.sync_exec(cmds, self._data)
        self.log_sync_result(result)
        return RunResult(result.is_success(), result.stdout, result.stderr, self.code_file)


class Run:
    def __init__(self):
        pass

    def __get_handler(self, file_type : CodeFileType) -> type[RunFileBaseHandler]:
        if file_type == CodeFileType.CPP:
            return CppRunHandler
        elif file_type == CodeFileType.PYTHON:
            return PythonRunHandler
        else:
            raise ValueError(f"Unknown file type: {file_type}")

    def sync_run(self, file : CodeFile, input_data : Optional[str] = None) -> RunResult:
        return self.__get_handler(file.file_type)(file, input_data).sync_run()
    
    async def async_run(self, file : CodeFile, input_data : Optional[str] = None)-> RunResult:
        return await self.__get_handler(file.file_type)(file, input_data).async_run()