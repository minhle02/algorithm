import os
from pathlib import Path
from .Logger import Logger
from string import Template

class Constant:
    BASE_DIR = Path(__file__).parent.parent
    TEMPLATE_PATH = BASE_DIR / "template"
    DEFAULT_CPP_TEMPLATE = TEMPLATE_PATH / "default.cpp"
    DEFAULT_CLANGD_TEMPLATE = TEMPLATE_PATH / "setting" / "clangd-default.yaml"
    CLANGD_FILE = BASE_DIR / ".clangd"
    WORK_DIR = BASE_DIR / "work"

class SetupProj:
    input_file_name : str =   "input.txt"
    files_to_create : list[str] = ["main.cpp", "brute.cpp"]

    def __init__(self):
        self._logger = Logger.get_logger()
    
    def setup_tool(self):
        with open(Constant.DEFAULT_CLANGD_TEMPLATE, "r") as f:
            clangd_template =  f.read()
        self._logger.info(f"Basedir: {Constant.BASE_DIR}")
        clangd_cfg : str = Template(clangd_template).substitute({"base_dir" : str(Constant.BASE_DIR)})
        with open(Constant.CLANGD_FILE, "w") as f:
            f.write(clangd_cfg)
        self._logger.info(f"Created .clangd file at the base directory")

    def __create_working_cpp_file(self, file_name : str):
        output_file_name = "output_" + file_name.removesuffix(".cpp") + ".txt"
        with open(Constant.DEFAULT_CPP_TEMPLATE, "r") as template_file:
            cpp_template_file = template_file.read()
        subs_data : dict[str, str] = {
            "output" : output_file_name,
            "input" : self.input_file_name,
        }
        cpp_file_data = Template(cpp_template_file).safe_substitute(subs_data)
        
        os.makedirs(Constant.WORK_DIR, exist_ok=True)
        with open(os.path.join(Constant.WORK_DIR, file_name), "w") as main_file:
            main_file.write(cpp_file_data)
        
        with open(os.path.join(Constant.WORK_DIR, output_file_name), "w") as f:
            f.write("")
        self._logger.info(f"Created file {file_name} with output file {output_file_name}")
    
    def __create_input_file(self):
        os.makedirs(Constant.WORK_DIR, exist_ok=True)
        with open(Constant.WORK_DIR / self.input_file_name, "w") as f:
            f.write("")
        self._logger.info(f"Created input file {self.input_file_name}")

    def setup_env(self):
        file_name = "main.cpp"
        brute_file_name = "brute.cpp"

        self._logger.info(f"Create working file at: {Constant.WORK_DIR}")
        self.__create_input_file()
        for f in self.files_to_create:
            self.__create_working_cpp_file(f)
        self._logger.info(f"Created {file_name} and {brute_file_name} from templates.")

if __name__ == "__main__":
    setup = SetupProj()
