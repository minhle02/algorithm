import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from builtins import ValueError
import argparse
import random
from tool import *
from generator import InputGenerator

from typing import override

class Command:
    CHECK = 'check'
    RUN = 'run'
    SETUP = 'setup'

class Constant:
    DEFAULT_MAIN_FILE = 'main.cpp'
    DEFAULT_BRUTE_FILE = 'brute.cpp'

def parse_args():
    parser = argparse.ArgumentParser(description="Command line tool for checking and running code.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    check_parser = subparsers.add_parser(Command.CHECK, help='Run 2 file and check their outputs to match')
    check_parser.add_argument('main',
                              type=str,
                              default=Constant.DEFAULT_MAIN_FILE,
                              nargs='*',
                              help=f'The main file to check (default: {Constant.DEFAULT_MAIN_FILE})')
    check_parser.add_argument('brute',
                                type=str,
                                default=Constant.DEFAULT_BRUTE_FILE,
                                nargs='*',
                                help=f'The brute force file to check (default: {Constant.DEFAULT_BRUTE_FILE})')

    run_parser = subparsers.add_parser(Command.RUN, help='Run a c++ program.')
    run_parser.add_argument("file", nargs="?", default="main.cpp", type=str, help="The main C++ file to run.")
    run_parser.add_argument("--debug", dest="debug", action="store_true", help="Enable debug mode by compiling with __DEBUG__ macro")
    run_parser.add_argument("--no-fileio", dest="no_fileio", action="store_true", help="Disable input/output from file, use stdin/stdout instead")

    setup_parser = subparsers.add_parser(Command.SETUP, help='Setup the environment. Create default files.')
    setup_parser.add_argument("-m", 
                             "--mode", 
                             default="env", 
                             choices=["env", "tool", "all"], 
                             help="Mode to setup: env, tool, all. env for create .cpp file, tool for setup tools (clangd), all for bot")

    return parser.parse_args()

class Checker(CheckerBase):
    def __init__(self):
        super().__init__()
        self._input_gen = InputGenerator()

    @override
    def gen_input(self):
        return self._input_gen.gen_input()

    @property
    def run_count(self) -> int:
        return 1

def main():
    args = parse_args()

    if args.command == Command.CHECK:
        Checker().run(args.main, args.brute)
    elif args.command == Command.RUN:
        runner = Runner(args.file, debug=args.debug, file_io=(not args.no_fileio))
        runner.run()
    elif args.command == Command.SETUP:
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
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
