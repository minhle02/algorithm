import random

class InputGenerator:
    def __init__(self):
        pass 

    def gen_input(self) -> str:
        N = random.randint(1, 10)
        M = random.randint(1, 10)
        data = f"{N} {M}\n"
        for _ in range(N):
            data += f"{random.randint(1,20)} "
        data += "\n"
        for _ in range(M):
            data += f"{random.randint(1, 20)} "
        data += "\n"
        return data