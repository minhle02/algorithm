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

class CompileBaseHandler(ABC):
    def __init__(self, code_file : CodeFile):
        assert os.path.exists(code_file.file_name), f"File not found: {code_file.file_name}"
        self._code_file = code_file
        self._logger = Logger.get_logger()
    
    @property
    def code_file(self) -> CodeFile:
        return self._code_file
    
    @abstractmethod
    async def async_compile(self) -> bool:
        pass
    
    @abstractmethod
    def sync_compile(self) -> bool:
        pass

    def log_sync_result(self, result : ExecResult) -> None:
        self._logger.debug(f"(Sync) Compile with command: {result.cmd}")
        if result.stderr or result.return_code != 0:
            self._logger.error(f"Compile file {self.code_file.file_name} return error, please check")
            self._logger.error(f"stderr:\n{result.stderr}")
            self._logger.error("")
            self._logger.error(f"stdout:\n{result.stdout}")
        else:
            self._logger.info(f"Compile file {self.code_file.file_name} success")
        
    async def log_async_result(self, result : ExecResult, lock : asyncio.Lock) -> None:
        async with lock:
            self._logger.debug(f"(ASYNC) Compile with command: {result.cmd}")
            if result.stderr or result.return_code != 0:
                self._logger.error(f"Compile file {self.code_file.file_name} return error, please check")
                self._logger.error(f"stderr:\n{result.stderr}")
                self._logger.error("")
                self._logger.error(f"stdout:\n{result.stdout}")
            else:
                self._logger.info(f"Compile file {self.code_file.file_name} success")

class CppCompileFlagsConfig():
    _initialized = False
    _instance : Optional['CppCompileFlagsConfig'] = None

    def __init__(self):
        if self._initialized:
            raise Exception(f"Class is a singleton, use instance() to get instead")
        self._initialized = True
        self._compile_flags : list[str] = []
    
    @staticmethod
    def instance() -> 'CppCompileFlagsConfig':
        if not CppCompileFlagsConfig._instance:
            CppCompileFlagsConfig._instance = CppCompileFlagsConfig()
        return CppCompileFlagsConfig._instance

    def __set_flag(self, flag : str):
        if flag not in self._compile_flags:
            self._compile_flags.append(flag)
    
    def set_debug_flag(self):
        debug_command = "-D__DEBUG__"
        self.__set_flag(debug_command)
    
    def set_fileio_flag(self):
        fileio_command = "-DLOCALONLY"
        self.__set_flag(fileio_command)
    
    def get_flag(self) -> list[str]:
        return self._compile_flags

class CppCompileHandler(CompileBaseHandler):
    _lock : asyncio.Lock = asyncio.Lock()
    def __init__(self, code_file : CodeFile):
        assert code_file.file_type == CodeFileType.CPP
        super().__init__(code_file)
        self._logger = Logger.get_logger()
        self._exec_handler = ExecCmdHandler()

    
    def get_compiler(self) -> str:
        return "g++"
    
    def __get_macos_include_dir(self) -> str:
        include_dir = os.path.join(os.path.dirname(__file__), os.pardir, "include")
        include_dir = os.path.abspath(include_dir)
        return f"-I{include_dir}"

    def __get_compile_command(self) -> list[str]:
        compiler = self.get_compiler()
        cmds : list[str] = [compiler]
        if sys.platform == "darwin":
            include_dir = self.__get_macos_include_dir()
            self._logger.debug(f"Compile on MACOS host, adding additinal include dir argumenr: {include_dir}")
            cmds.append(include_dir)
        
        cmds.append(f"-o")
        cmds.append(f"{self.code_file.executable_name}")
        cmds.append("-std=gnu++17")
        
        cmds.extend(CppCompileFlagsConfig.instance().get_flag())
        cmds.append(self.code_file.file_name)
        return cmds

    @override
    def sync_compile(self) -> bool:
        cmds = self.__get_compile_command()
        result = self._exec_handler.sync_exec(cmds)
        self.log_sync_result(result)
        return result.is_success()

    @override
    async def async_compile(self) -> bool:
        cmds = self.__get_compile_command()
        result = await self._exec_handler.async_exec(cmds)
        await self.log_async_result(result, CppCompileHandler._lock)
        return result.is_success()

class PythonCompileHandler(CompileBaseHandler):
    def __init__(self, code_file : CodeFile):
        assert code_file.file_type == CodeFileType.PYTHON
        super().__init__(code_file)
        self._logger = Logger.get_logger()
    
    @override
    def sync_compile(self) -> bool:
        self._logger.debug(f"File {self.code_file.file_name} do not need compilation")
        return True
    
    @override
    async def async_compile(self) -> bool:
        self._logger.debug(f"File {self.code_file.file_name} do not need compilation")
        return True

class Compile:
    def __init__(self):
        pass

    def __get_handler(self, file_type : CodeFileType) -> type[CompileBaseHandler]:
        if file_type == CodeFileType.CPP:
            return CppCompileHandler
        elif file_type == CodeFileType.PYTHON:
            return PythonCompileHandler
        else:
            raise ValueError(f"Unknown file type: {file_type}")
    
    def set_debug(self) :
        CppCompileFlagsConfig.instance().set_debug_flag()
    
    def set_fileio(self):
        CppCompileFlagsConfig.instance().set_fileio_flag()
    
    def sync_compile(self, file : CodeFile) -> bool:
        return self.__get_handler(file.file_type)(file).sync_compile()
    
    async def async_compile(self, file : CodeFile) -> bool:
        return await self.__get_handler(file.file_type)(file).async_compile()