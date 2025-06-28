from builtins import isinstance
from builtins import ValueError
from builtins import isinstance
from builtins import int
import asyncio
import subprocess
from typing import Optional
from dataclasses import dataclass

from .Logger import Logger
from abc import ABC, abstractmethod

@dataclass
class ExecResult:
    return_code : Optional[int]
    stdout : Optional[str]
    stderr : Optional[str]
    stdin : Optional[str]
    cmd : list[str]

    def is_success(self):
        if self.stderr or self.return_code != 0:
            return False
        return True

class ExecCmdHandler:
    """
    Run a shell command in sync/async mode
    """
    def __init__(self):
        pass

    def __get_bytes(self, data : str):
        return data.encode("utf-8")
    
    async def async_exec(self, cmds : list[str], input_data : Optional[str] = None) -> ExecResult:
        proc = await asyncio.create_subprocess_exec(
            *cmds,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        if input_data:
            stdout_bytes, stderr_bytes = await proc.communicate(self.__get_bytes(input_data))
        else:
            stdout_bytes, stderr_bytes = await proc.communicate()

        stdout = stdout_bytes.decode("utf-8")
        stderr = stderr_bytes.decode(f"utf-8")
        return ExecResult(
            return_code=proc.returncode,
            stdout=stdout,
            stderr=stderr,
            stdin=input_data,
            cmd=cmds
        )
    
    def sync_exec(self, cmds: list[str], input_data : str | None = None) -> ExecResult:
        proc = subprocess.Popen(
            cmds,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if not input_data:
            stdout, stderr = proc.communicate()
        else:
            stdout, stderr = proc.communicate(input=input_data)

        return ExecResult(
            return_code = proc.returncode,
            stdout = stdout,
            stderr = stderr,
            stdin = input_data,
            cmd = cmds
        )
