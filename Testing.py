#!/usr/bin/Python3.4

from sys import argv as av
from sys import exit
from pathlib import Path
import os
import subprocess
import colors

def usage():
    print("Usage : " + colors.red + "./Testing" + colors.blue + " [-d]" + colors.green + " directory" + colors.normal)

args = ["./Expert_system.py"]
if len(av) == 3 and av[1] == "-d":
    args.append("-d")
elif len(av) != 2:
    usage()
    exit()
try:
    list_files = os.listdir(av[-1])
except:
    print(colors.red + "File " + av[-1] + " not found" + colors.normal)
    exit()
for filename in list_files:
    arg_file = list(args)
    full_name = av[-1] + '/' + filename
    my_file = Path(full_name)
    if not my_file.is_file() or my_file.is_dir():
        continue
    print(colors.yellow + "Running Expert system with " + colors.blue + filename + colors.normal)
    arg_file.append(full_name)
    subprocess.call(arg_file)
