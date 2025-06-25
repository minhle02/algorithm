import random
import asyncio
import os
import sys

from .Logger import Logger

class CheckerBase:
    def __init__(self):
        self._logger = Logger.get_logger()

    def gen_input(self) -> str:
        raise NotImplementedError("This function must be implemented")

    @property
    def run_count(self) -> int:
        return 20

    def __get_executable_name(self, file : str) -> str:
        file = os.path.basename(file)
        return file.removesuffix(".cpp") + ".exe"

    def __get_compile_command(self, file : str) -> tuple[str, list[str]]:
        cmd = ["g++", file]
        if sys.platform == "darwin":
            cmd.append(f"-I{os.path.join(os.path.dirname(__file__), os.pardir, "include")}")
        output = self.__get_executable_name(file)
        cmd.append("-o")
        cmd.append(output)
        cmd.append("-std=gnu++17")
        return output, cmd


    async def compile_file(self, file_path : str):
        output_file, cmd  = self.__get_compile_command(file_path)
        self._logger.debug(f"Compiling with command: {cmd}")
        proc = await asyncio.subprocess.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.wait()
        return output_file

    async def run_file(self, data : str, file_path : str):
        self._logger.debug(f"Running file {file_path}")
        cmd = f"./{file_path}"
        proc = await asyncio.create_subprocess_exec(
            cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate(data.encode("ascii"))
        return stdout.decode("ascii")

    def check_output(self, output1 : str, output2 : str) -> bool:
        lines1 = output1.strip().splitlines()
        lines2 = output2.strip().splitlines()
        if len(lines1) != len(lines2):
            self._logger.debug(f"Output length mismatch: {len(lines1)} != {len(lines2)}")
            return False
        for line1, line2 in zip(lines1, lines2):
            if line1.split() != line2.split():
                self._logger.debug(f"Output mismatch:\n{line1}\nvs\n{line2}")
                return False
        return True

    async def check(self, file1 : str, file2 : str):
        assert os.path.exists(file1), f"File {file1} does not exist"
        assert os.path.exists(file2), f"File {file2} does not exist"
        is_error = False
        self._logger.info("Compiling...")
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(
                self.compile_file(file1))
            task2 = tg.create_task(
                self.compile_file(file2))
        file1 = task1.result()
        file2 = task2.result()
        self._logger.info("Running...")
        for i in range(self.run_count):
            self._logger.debug(f"")
            self._logger.debug("="*40)
            self._logger.debug(f"Attempt {i}")
            data : str = self.gen_input()
            self._logger.debug(f"Data:\n{data}")
            async with asyncio.TaskGroup() as tg:
                task1 : asyncio.Task = tg.create_task(
                self.run_file(data, file1))

                task2 : asyncio.Task = tg.create_task(
                self.run_file(data, file2))

            out1 = task1.result()
            out2 = task2.result()
            if not self.check_output(out1, out2):
                self._logger.error("Error!!!")
                self._logger.error(f"Data:\n {data}")
                is_error = True
            else:
                self._logger.debug("Running ok")

        self._logger.debug("="*40)
        if not is_error:
            self._logger.info("SUCCESS")
        os.remove(file1)
        os.remove(file2)

    def run(self, file1 : str, file2 : str):
        asyncio.run(self.check(file1, file2))
