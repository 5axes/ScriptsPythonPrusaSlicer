#!/usr/bin/python
import sys
import re
import os

parmEstimatedHours = ''
parmEstimatedMinutes = ''
parmEstimatedSeconds = ''
parmNotes = ''

sourceFile=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

    coordMinX = 9999.9
    coordMaxX = 0.0
    coordMinY = 9999.9
    coordMaxY = 0.0
    currLine = 1
    parsing = False

for line in lines:
    currLine += 1
    parts = line.split(';', 1)
    if len(parts) > 0:
        # Parse command
        command = parts[0].strip()
        if len(parts) > 1:
            # Parse comments
            comment = parts[1].strip()

        # Track extruder movement ranges
        if not re.search(";", comment):
            # Limit track to print movements, avoid start and end gcode blocks
            if re.search("move to first skirt point", comment):
                #if not parsing:
                #    print("Start extruder movement parsing at line %d with %s" % (currLine, comment))
                parsing = True
            if re.search("PURGING FINISHED", comment):
                #print("Stop extruder movement parsing at line %d with %s" % (currLine, comment))
                parsing = False
        if parsing:
            stringMatch = re.search ('^G[01].*X([0-9.]+)', command)
            if stringMatch:
                val = float(stringMatch.group(1))
                # print("%s: X is %d" % (currLine, val))
                if(val < coordMinX):
                    coordMinX = val
                if(val > coordMaxX):
                    coordMaxX = val
            stringMatch = re.search ('^G[01].*Y([0-9.]+)', command)
            if stringMatch:
                val = float(stringMatch.group(1))
                if(val < coordMinY):
                    coordMinY = val
                if(val > coordMaxY):
                    coordMaxY = val

        # Include files
        includeFile = re.search('#INCLUDE\s+(.*)', comment)
        #if includeFile:
        #    outputFile.write(' -- Would include '+includeFile.group(1)+' stuff here')

        # Parse estimated print time
        stringMatch = re.search ('^notes = (.*)', comment)
        if stringMatch:
            parmNotes = stringMatch.group(1).strip()
        stringMatch = re.search('estimated printing time \(normal mode\) =.* ([0-9]+)h.*', comment)
        if stringMatch:
            parmEstimatedHours = stringMatch.group(1)+'h'
        stringMatch = re.search('estimated printing time \(normal mode\) =.* ([0-9]+)m.*', comment)
        if stringMatch:
            parmEstimatedMinutes = stringMatch.group(1)+'m'
        stringMatch = re.search('estimated printing time \(normal mode\) =.* ([0-9]+)s.*', comment)
        if stringMatch:
            parmEstimatedSeconds = stringMatch.group(1)+'s'
        # Parse print job parameters
        stringMatch = re.search('filament_type = (.*)', comment)
        if stringMatch:
            parmFilamentType = stringMatch.group(1)
        stringMatch = re.search('nozzle_diameter = (.*)', comment)
        if stringMatch:
            parmNozzleDiameter = stringMatch.group(1)
        stringMatch = re.search('layer_height = (.*)', comment)
        if stringMatch:
            parmLayerHeight = stringMatch.group(1)
        # Parse temperatures
        stringMatch = re.search('bed_temperature = (.*)', comment)
        if stringMatch:
            parmBedTemperature = stringMatch.group(1)
        stringMatch = re.search('first_layer_bed_temperature = (.*)', comment)
        if stringMatch:
            parm1stLayerBedTemperature = stringMatch.group(1)
        stringMatch = re.search('temperature = (.*)', comment)
        if stringMatch:
            parmTemperature = stringMatch.group(1)
        stringMatch = re.search('first_layer_temperature = (.*)', comment)
        if stringMatch:
            parm1stLayerTemperature = stringMatch.group(1)

destFile = re.sub('\.gcode$','',sourceFile)
if parmNotes:
    destFile = destFile + ' ('+parmNotes+')'
#destFile = destFile + ' S3r'
if parmFilamentType:
    destFile = destFile + ' '+parmFilamentType
if parmLayerHeight:
    destFile = destFile + ' '+parmLayerHeight
if parmNozzleDiameter:
    destFile = destFile + 'X'+parmNozzleDiameter
if parm1stLayerTemperature:
    destFile = destFile + ' '+parm1stLayerTemperature
if parmTemperature:
    destFile = destFile + '-'+parmTemperature
if parm1stLayerBedTemperature:
    destFile = destFile + ' '+parm1stLayerBedTemperature
if parmBedTemperature:
    destFile = destFile + '-'+parmBedTemperature
if parmEstimatedHours or parmEstimatedMinutes or parmEstimatedSeconds:
    destFile = destFile + ' '
    if parmEstimatedHours:
        destFile = destFile + parmEstimatedHours
    if parmEstimatedMinutes:
        destFile = destFile + parmEstimatedMinutes
    if parmEstimatedSeconds:
        destFile = destFile + parmEstimatedSeconds
destFile = destFile + '.gcode'
#print('Writing to %s' % re.sub('.*/','',destFile))

with open(destFile, "w") as of:
    of.write('; Minimum X = '+ str(coordMinX)+'\n')
    of.write('; Maximum X = '+ str(coordMaxX)+'\n')
    of.write('; Minimum Y = '+ str(coordMinY)+'\n')
    of.write('; Maximum Y = '+ str(coordMaxY)+'\n')
    for lIndex in xrange(len(lines)):
        oline = lines[lIndex]
        #if ("G0" in line or "G1" in line) and ("E" in line) :
        #    line = re.sub("E","B",line)
        of.write(oline)

of.close()
f.close()

os.remove(sourceFile)
