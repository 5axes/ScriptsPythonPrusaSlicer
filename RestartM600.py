#!/usr/bin/python
import sys
import re
import os
import os.path
from os import path
from os import environ

# first argument passed by PrusaSlicer = Gcode file
sourceFile=sys.argv[1]

# Read the ENTIRE Gcode file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()
f.close()

destFile = re.sub('\.gcode$','',sourceFile)
destFile = destFile + '_restart.gcode'

write_line = False
current_z = 0
valid_code = ['M106', 'M107', 'M201','M203','M204','M205','M104','M140','M190', 'M109', 'M82', 'M83', 'G90', 'G91', 'G21', 'G20']

# Rewrite the ENTIRE Gcode file
with open(destFile, "w") as of:
    # Write first line
    oline = lines[0]
    of.write(oline)
    
    for lIndex in range(len(lines)):
        oline = lines[lIndex]

        if write_line == True:
            of.write(oline)
        else :
            if "Z" in oline and "G1" in oline:
                searchZ = re.search(r"Z(\d*\.?\d*)", oline)
                if searchZ:
                    current_z=float(searchZ.group(1))
            first_code = oline.split(" ")[0]        
            if first_code in valid_code :
                of.write(oline)
        
            if oline[:4] == "M600":
                write_line = True

                line_w = ";RESTART_POSITION Z= {:.3f}\n".format( float(current_z))
                of.write(line_w)
                of.write("G28 X0\n")
                of.write("G28 Y0\n")
                
                # GET PRUSASLICER ENVIRONEMENT VARIABLE
                retract_len = environ.get('SLIC3R_RETRACT_LENGTH')
                deretract_speed = environ.get('SLIC3R_DERETRACT_SPEED')
                f_speed = environ.get('SLIC3R_FIRST_LAYER_SPEED')
                y_maxi = 250 # environ.get('SLIC3R_RECT_SIZE')
                line_w = "G1 Y{:.3f} F{:.1f}\n".format(float(y_maxi),float(f_speed)*60)
                of.write(line_w)
                 
                of.write("G28 Z0\n")
                
                line_w = "G92 E0\n"
                of.write(line_w)
                
                line_w = "G1 E{:.3f} F{:.1f}\n".format(-float(retract_len),float(deretract_speed)*60)
                of.write(line_w)

                line_w = "G1 Z{:.3f} F{:.1f}\n".format( float(current_z),float(f_speed)*60)
                of.write(line_w)

of.close()

