#!/usr/bin/Python3.4
import os
import colors

def print_title(title):
    'Print beautiful row of \'#\''

    rows, columns = os.popen('stty size', 'r').read().split()
    r = ""
    columns = int(columns)
    c = columns
    c -= len(title) + 4
    c /= 2
    while (c > 0):
        r += "#"
        c -= 1
    print(colors.green + r + " " + title + " " + r + colors.normal)

