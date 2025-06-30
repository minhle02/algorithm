import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))     # For tool package
import random
from tool import InputGenerator
from typing import override

class Generator(InputGenerator):
    def __init__(self):
        pass 
    
    @override
    def gen_input(self) -> str:
        V1 = random.randint(1, 5)
        V2 = random.randint(V1 + 1, 10)
        C1 = random.randint(1, 10)
        C2 = random.randint(1, 10)
        x = random.randint(1, C2)
        N = random.randint(1, 5)

        total = V1 * C1 + V2 * C2

        A : list[int] = []
        count1 = []
        count2 = []

        c1_sum = C1
        c2_sum = C2
        for i in range(N):
            if i != N - 1:
                c1 = random.randint(0, c1_sum)
                c2 = random.randint(0, c2_sum)
            else:
                c1 = c1_sum
                c2 = c2_sum
            c1_sum -= c1
            c2_sum -= c2
            count1.append(c1)
            count2.append(c2)
            A.append(c1 * V1 + c2 * V2)
        try:
            # assert(sum(A) == total)
            assert(sum(count1) == C1)
            assert(sum(count2) == C2)

        except AssertionError as e:
            print("error!!!!")
            print(A)
            print(count1)
            print(count2)
            print(f"{V1} {C1} {V2} {C2}")
            return ""



        # Add 1 testcase only
        data = "1\n" \
        f"{V1} {C1} {V2} {C2}\n" \
        f"{N} {x}\n" \
        f"{' '.join([str(el) for el in A])}"

        return data

if __name__ == "__main__":
    print(InputGenerator().gen_input())
