#!/usr/bin/python3

import argparse
import subprocess
import os.path
import sys

arduino_base = "/usr/share/arduino/hardware"
arduino_tools = arduino_base + "/tools"
framework_path = arduino_base + "/arduino/cores/arduino"
compiler = "avr-g++"

compile_flags = [
    "-DF_CPU=16000000",
    "-mmcu=atmega2560",
    "-I" + arduino_base+"/arduino/variants/mega",
    "-I" + framework_path
    ]

framework_files = [
    "HardwareSerial.cpp",
    "wiring_digital.c",
    "wiring_shift.c",
    "wiring.c",
    "Print.cpp",
    "WString.cpp",
    "new.cpp"
    ]


def execute(command):
    print(" ".join(command))
    try:
        subprocess.check_call(command)
        return True
    except subprocess.CalledProcessError:
        # There was an error - command exited with non-zero code
        return False
    except FileNotFoundError:
        print("Command not found: " + command[0])
        return False


def create_output_filenames(sources, extension):
    objects = []
    for source in sources:
        objects.append(os.path.basename(source).replace(".c", extension).replace(".cpp", extension))
    return objects


def get_framework_path_names(sources):
    path_names = []
    for source in sources:
        path_names.append(framework_path+"/"+source)
    return path_names


parser = argparse.ArgumentParser(description="Compile and upload source code to Arduino")
parser.add_argument('sources', metavar='source', nargs='+', help='Source files to compile')
args = parser.parse_args()
sources = args.sources

if not execute([compiler, "-c"] + compile_flags + get_framework_path_names(framework_files)):
    sys.exit(1)

if not execute([compiler, "-Os"] + compile_flags + sources +
               create_output_filenames(framework_files, ".o") + ["-o", "code.elf"]):
    sys.exit(1)


