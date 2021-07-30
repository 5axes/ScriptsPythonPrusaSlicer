#!/usr/bin/python
import sys
import re
import os
import os.path
from os import path

#
# Change the acceleration value for the external perimeter
# Perimeter_acceleration (Perimeter accelerations) must be define in the print profile ( Speed - Acceleration controle)
#

# first argument passed by PrusaSlicer = Gcode file
sourceFile=sys.argv[1]

# Read the ENTIRE Gcode file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

destFile = re.sub('\.gcode$','',sourceFile)
tempFile =  destFile+".bak"
# if back file existe remove the old one
if path.exists(tempFile):
    os.remove(tempFile)
 # Save the GCode file under a .bak file
os.rename(sourceFile,destFile+".bak")
destFile = re.sub('\.gcode$','',sourceFile)
destFile = destFile + '.gcode'


# New Acceleration Value
# P600 : Acceleration value in mm/s²
M204_code = "M204 P600\n"

change_val = False

# Rewrite the ENTIRE Gcode file
with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        
        if oline[:6] == ";TYPE:":
            change_val = False
        if oline[:24] == ";TYPE:External perimeter":
            change_val = True
        if oline[:4] == "M204" and change_val == True:
            of.write(M204_code)
        else:
            of.write(oline)
of.close()
f.close()