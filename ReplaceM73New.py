#!/usr/bin/python
import sys
import re
import os
import os.path
#import ctypes
from os import path

# Need to add : ;LAYER_COUNT:[total_layer_count]
# in the Prusa Slicer Initial GCode 

# first argument passed by PrusaSlicer = Gcode file
sourceFile = sys.argv[1]
# Modification pour PrusaSlicer 2.4.0
destFile = os.getenv('SLIC3R_PP_OUTPUT_NAME')
#ctypes.windll.user32.MessageBoxW(0, destFile, "Debug info", 1)

# Read the ENTIRE Gcode file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
f.close()

destFile = sourceFile

# Init Layer_Numb = 0
layer_num = 0
total_layer_count = 0
# Rewrite the ENTIRE Gcode file
with open(destFile, "w") as of:
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        
        if oline[:13] == ";LAYER_COUNT:":
            total_layer_count = int(oline.split(":")[1])
        if oline[:13] == ";LAYER_CHANGE":
            layer_num += 1
        if oline[:3] == "M73":
            # format M117 %12 3h37m
            percent = oline.replace("M73 P","").split(" ")[0]
            total_time = int(oline.split("R")[1])
            h, m = divmod(total_time, 60)    # hours, minutes
            total_time_string = " {:d}h{:d}\n".format( int(h), int(m))
            if total_layer_count > 0 :
                M117_code = "M117 ({:d}/{:d}) %".format( int(layer_num), int(total_layer_count))
            else:
                M117_code = "M117 %"
            M117_code = M117_code + percent
            tempLine = M117_code + total_time_string
            of.write(tempLine)
        else:
            of.write(oline)
of.close()


 
 