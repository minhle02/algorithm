# Collections of tool for competitive programming

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

## Table of contents

- [Collections of tool for competitive programming](#collections-of-tool-for-competitive-programming)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
    - [Python](#python)
    - [C++ compiler](#c-compiler)
  - [Usage](#usage)
    - [Setup work directory](#setup-work-directory)
    - [Run code file](#run-code-file)
      - [Options for `.cpp` files](#options-for-cpp-files)
    - [Checking output of code file](#checking-output-of-code-file)
      - [Testcase generation](#testcase-generation)
      - [Running check](#running-check)

<!-- TOC end -->

## Installation

### Python
The project use `uv` as a python package manager. 

Install `uv` with (assuming there is `python` on your machine):

```
pip install uv
```

For more information about `uv`, visit: https://docs.astral.sh/uv/

Setup virtual environment:

```
uv venv   # for the 1st time only
uv sync   # Sync the packages
```

### C++ compiler

Most online judge environment use `gcc` compilers, therefore, by default this project will use `g++` as compiler for `.cpp` files.

## Usage

By default, the working directory is `work`. You should write your code here.

The `work` folder is equipped with two script files: 

- `script.py`: Run code file, check code file, setup environment
- `generator.py`: Implement of testcase input generation. 

### Setup work directory

The working directory is `work`. 

To quickly setup work directory, run:

```
uv run setup.py setup
```

It will automatically create two files `main.cpp` and `brute.cpp` in folder `work`

You should write your code (the optimized version) to `main.cpp`. 

If you want to check your optimized version against a brute force version, write the brute force solution to `brute.cpp`

### Run code file

In the `work` folder, run command:

```
uv run script.py run
```

The script will run file `main.cpp` (default)

To run any file, simply run:

```
uv run script.py run <file>
```

The `script.py` can run the following file:
- C++ code: `.cpp`
- Python `.py`

#### Options for `.cpp` files

1. File I/O
    By default, the script automatically add flag `-D__FILEIO__` during compilation to enable input/output from file. 
    Check this snippet in default `main.cpp` file

    ```cpp
    #ifdef __FILEIO__
        freopen("input.txt", "r", stdin);
        freopen("output_brute.txt", "w", stdout);
    #endif
    ```

    You can disable this by adding `--no-fileio` flag to the run script

2. Debug
    The script does not automatically use debug mode. 
    When compiling with debug mode, the script will add flag `-D__DEBUG__` during compilation. You can add debug code such as:

    ```cpp
    #ifdef __DEBUG__
    #define PRINT_VECTOR(v) do {cout << "Container " << #v << "\n"; for (auto&e : v) {cout << e << " ";} cout << "\n";} while (false)
    #define DEBUG(...) do {printf(__VA_ARGS__);} while (false)
    #define DEBUG_COUT std::cout
    #else
    #define PRINT_VECTOR(v) (void)0
    #define DEBUG(...) (void)0
    #define DEBUG_COUT if (false) std::cout
    #endif
    ```

    To enable debug mode, add flag `--debug` when running script


### Checking output of code file

Sometimes, your optimized code is running OK with sample testcase, but repeatedly failed to run on server. 
You can generate random testcase and test your brute force solution against you optimized version.

#### Testcase generation

In file `generator.py`, the script already setup a basic InputGenerator class:

```py
class InputGenerator:
    def __init__(self):
        pass 

    def gen_input(self) -> str:
        pass
```

Fill in the `gen_input` function as you wished. Remember to return a `str` object. 
Every time the script attempt to check for output, 
it gets the data from `gen_input` first, then sends to executable files

#### Running check

Write your brute force solution to `brute.cpp` file, and write your optimized version to `main.cpp` file

**Note**: Brute force solution must be very SIMPLE, such that it always return correct output 

Then run:
```
uv run script.py check
```

By default, the `check` command compiles and runs files: `main.cpp` and `brute.cpp`, compares the output, then logs any error. 
If no error was found, it logs `SUCCESS`

Also, when running `check` mode, the script does **NOT ADD** any compile flags (such as `-D__FILEIO__` and `-D__DEBUG__`)

If you don't want to use `brute.cpp` and `main.cpp` for output comparision, you can run the command with:
```
uv run script.py check <file1> <file2> ....
```

For example, if you write your brute force solution in `brute.py` (PYTHON), and main code in `main.cpp`:
```
uv run script.py check brute.py main.cpp
```

You can add as many files to the check command as you wish. But noted that you **MUST supplied at least 2 files**, and all files must be `.py` or `.cpp`
