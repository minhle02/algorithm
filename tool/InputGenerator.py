from abc import abstractmethod
import random

class InputGenerator:
    def __init__(self):
        pass 
    
    @abstractmethod
    def gen_input(self) -> str:
        pass