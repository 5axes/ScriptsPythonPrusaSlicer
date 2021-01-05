#!/usr/bin/python
import sys
import re
import os
import os.path
from os import path

sourceFile=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

destFile = re.sub('\.gcode$','',sourceFile)
tempFile =  destFile+".bak"
# if back file existe remove the old one
if path.exists(tempFile):
    os.remove(tempFile)
os.rename(sourceFile,destFile+".bak")
destFile = re.sub('\.gcode$','',sourceFile)
destFile = destFile + '.gcode'

with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        if oline[:3] == "M73":
            percent = oline.replace("M73 P","").split(" ")[0]
            total_time = int(oline.split("R")[1])
            h, m = divmod(total_time, 60)    # heures, minutes
            total_time_string = " {:d}h{:d}m\n".format( int(h), int(m))
            M117_code = "M117 %" + percent
            tempLine = M117_code + total_time_string
            of.write(tempLine)
        else:
            of.write(oline)
of.close()
f.close()