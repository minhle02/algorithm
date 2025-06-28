from builtins import str
from dataclasses import dataclass, field
from enum import Enum
import os

class CodeFileType(Enum):
    UNKNOWN = 0
    PYTHON = 1
    CPP = 2

@dataclass
class CodeFile:
    file_name : str
    file_type : CodeFileType = field(init=False)
    executable_name : str = field(init=False)

    def __post_init__(self):
        if self.file_name.endswith(".cpp"):
            self.file_type = CodeFileType.CPP
            self.executable_name = os.path.basename(self.file_name).removesuffix(".cpp") + ".exe"
        elif self.file_name.endswith(".py"):
            self.file_type = CodeFileType.PYTHON
            self.executable_name = self.file_name
        else:
            self.file_type = CodeFileType.UNKNOWN
            self.executable_name = ""
    
    def remove(self):
        """
        Remove executable file (only .exe)
        """
        if self.file_type == CodeFileType.CPP:
            if self.executable_name and os.path.exists(self.executable_name):
                os.remove(self.executable_name)