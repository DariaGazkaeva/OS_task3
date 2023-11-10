#!/bin/python3

import random
import time

operations = ["+", "-", "*", "/"]


def main():
    n = random.randint(120, 180)
    for i in range(n):
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        o = operations[random.randint(0, len(operations) - 1)]
        print(x, o, y, flush=True)
        time.sleep(1)


main()
