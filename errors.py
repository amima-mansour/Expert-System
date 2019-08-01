#!/usr/bin/Python3.4

from sys import exit
import colors

def usage():
    print("Usage : " + colors.red + "./Expert_system.py" + colors.blue + " [-di]" \
            + colors.green + " file.txt" + colors.normal)
    exit()

def file_fail(file_name, message):
    print(colors.red + "Problem with the file : " + colors.blue + file_name \
            + colors.normal + " " + message)
    exit()

def empty(file_name):
    print(colors.red + "The file " + colors.blue + file_name + colors.red \
            + " is empty !" + colors.normal)
    exit()

def parse(line, message):
    print(colors.red + "Error on line " + str(line) + " : " + colors.purple \
            + message + colors.normal)
    exit()

def conflict(c):
    print(colors.red + "Conflict in node " + str(c) + colors.normal)
    exit()
    
def stoped_input():
    print(colors.red + "You stoped the program, see you later !" + colors.normal)
    exit()
