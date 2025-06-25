from builtins import ValueError
from tool.SetupProj import SetupProj
import argparse
import random
from tool import *

class Constant:
    DEFAULT_MAIN_FILE = 'main.cpp'
    DEFAULT_BRUTE_FILE = 'brute.cpp'

def parse_args():
    parser = argparse.ArgumentParser(description="Command line tool for checking and running code.")
    parser.add_argument("-m", 
                        "--mode", 
                        default="env", 
                        choices=["env", "tool", "all"], 
                        help="Mode to setup: env, tool, all. env for create .cpp file, tool for setup tools (clangd), all for bot")

    return parser.parse_args()

def main():
    args = parse_args()

    setup_handler = SetupProj()
    if args.mode == "env":
        setup_handler.setup_env()
    elif args.mode == "tool":
        setup_handler.setup_tool()
    elif args.mode == "all":
        setup_handler.setup_env()
        setup_handler.setup_tool()
    else:
        raise ValueError(f"Invalid mode: {args.mode}")

if __name__ == "__main__":
    main()
