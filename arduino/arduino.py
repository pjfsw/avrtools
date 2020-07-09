#!/usr/bin/python3

import argparse
import subprocess
import os.path
import sys

arduino_base = "/usr/share/arduino/hardware"
arduino_tools = arduino_base + "/tools"
avrdude_conf = arduino_tools+"/avrdude.conf"
framework_path = arduino_base + "/arduino/cores/arduino"
compiler = "avr-g++"

port="/dev/ttyACM0"

# Board configuration
compile_mcu="atmega2560"
dude_mcu="m2560"
variant="mega"


compile_flags = [
    "-DF_CPU=16000000",
    "-mmcu="+compile_mcu,
    "-I" + arduino_base+"/arduino/variants/"+variant,
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
        objects.append(os.path.basename(source).replace(".cpp", extension).replace(".c", extension))
    return objects


def get_framework_path_names(sources):
    path_names = []
    for source in sources:
        path_names.append(framework_path+"/"+source)
    return path_names


parser = argparse.ArgumentParser(description="Compile and upload source code to Arduino")
parser.add_argument('sources', metavar='source', nargs='*', help='Source files to compile')
parser.add_argument("--clean", action="store_true", help="Clean output files")
parser.add_argument("--upload", action="store_true", help="Upload code.elf")

args = parser.parse_args()
sources = args.sources
output_framework_files = create_output_filenames(framework_files, ".o") 
elf = "code.elf"
ihex = "code.ihex"

if args.clean:
    to_clean = output_framework_files+[elf,ihex]

    execute(["rm"]+to_clean)
    sys.exit(0)

if len(sources) > 0:
    if not execute([compiler, "-c"] + compile_flags + get_framework_path_names(framework_files)):
        sys.exit(1)

    if not execute([compiler, "-Os"] + compile_flags + sources + output_framework_files+["-o", elf]):
        sys.exit(1)

    if not execute(["avr-objcopy", "-O", "ihex", "-R", ".eeprom", elf, ihex]):
        sys.exit(1)

if args.upload:
    execute([
    "avrdude",
    "-v",
    "-C", avrdude_conf,
    "-b", "115200",
    "-c", "avrisp2",
    "-p", dude_mcu,
    "-P", port,
    "-U", "flash:w:"+ihex+":i"
    ])



