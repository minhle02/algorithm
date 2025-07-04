import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))     # For tool package

from builtins import ValueError
import argparse
import random
from tool import *
from generator import Generator

from typing import override

class Command:
    CHECK = 'check'
    RUN = 'run'
    SETUP = 'setup'

class Constant:
    DEFAULT_MAIN_FILE = 'main.cpp'
    DEFAULT_BRUTE_FILE = 'brute.cpp'
    DEFAUL_NUMBER_OF_TESTS = 20

def parse_args():
    parser = argparse.ArgumentParser(description="Command line tool for checking and running code.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    check_parser = subparsers.add_parser(Command.CHECK, help='Run 2 file and check their outputs to match')
    check_parser.add_argument('files',
                              type=str,
                              default=[Constant.DEFAULT_MAIN_FILE, Constant.DEFAULT_BRUTE_FILE],
                              nargs='*',
                              help=f'Running all files with the same input and compare the output." \
                                "Default: [{Constant.DEFAULT_MAIN_FILE}, {Constant.DEFAULT_BRUTE_FILE}]')
    check_parser.add_argument("-n",
                            "--num-tests",
                            dest="num_tests",
                            default=Constant.DEFAUL_NUMBER_OF_TESTS,
                            help=f"Number of tests to generate and test. Default : {Constant.DEFAUL_NUMBER_OF_TESTS}")

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
    def __init__(self, run_count : int):
        super().__init__(Generator())
        self._run_count = run_count

    @property
    def run_count(self) -> int:
        return self._run_count

def main():
    args = parse_args()

    if args.command == Command.CHECK:
        assert len(args.files) >= 2, "Use at least 2 files"
        Checker(args.num_tests).run(*args.files)
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
