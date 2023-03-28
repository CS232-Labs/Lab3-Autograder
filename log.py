import os
import sys
from grade_structure import Grade

verbosity = 0
grade = Grade()

# Utility characters for test case printing
pass_char = u" \u2714 "
fail_char = u" \u2717 "

def set_verbosity(verbose):
    global verbosity
    verbosity = verbose

# Helpers for marking messages
def error(str):
    if verbosity > 0:
        print("\033[0;31m"+str+"\033[0m")

def critical_error(str):
    sys.exit("\033[0;31m"+str+"\033[0m")

def info(str):
    if verbosity > 1:
        print("\033[0;35m"+str+"\033[0m")
    
def test_pass(str):
    print("\033[0;32m"+str+"\033[0m")

def test_fail(str):
    print("\033[0;31m"+str+"\033[0m")

# Assert for verification script to be run on linux
if not sys.platform.startswith('linux'):
    critical_error(f"[ERROR] Autograder requires linux")

# Extracting directory of file instead of run directory
basedir = os.path.dirname(os.path.realpath(__file__))

# Unifying binaries for usage
nasm_path = os.path.join(basedir, "nasm")
spim_path = os.path.join(basedir, "spim")
modified_spim_path = os.path.join(basedir, "spim_for_recursion")
instructions_spim_path = os.path.join(basedir, "spim_for_instructions")
exceptions_path = os.path.join(basedir, "exceptions.s")
