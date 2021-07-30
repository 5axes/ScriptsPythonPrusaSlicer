# ScriptsPythonPrusaSlicer
Sample pythton scripts for PrusaSlicer or SuperSlicer

# Installation instructions

### 1. Install python and remember the installation directory 
This version was tested with python 3.8 (32 bits).
You can find a version of the Python distribution and the development environment : https://www.python.org/downloads/

### 2. Copy the scripts in a short path storage location

### 3. Configuration in PrusaSlicer 
Go to: `Print Settings` > `Output options` > `Post-processing scripts`

### With Python 3.x installed:
Add line: `"[python directory]\python.exe"  "[script directory]\ReplaceM73.py";`


ReplaceM73.py
--

Replace the M73 P R instruction into a M117 line for non Prusa MK3 printer. In order to get also the Total number of layer you must add the code :

    ';LAYER_COUNT:[total_layer_count]'

In the Prusa Slicer or SuperSlicer Initial G-Code 


RestartM600.py
--

Re-start the Gcode from the first M600 position founded in the Gcode. Need to define manualy the Change Color or filament position in PrusaSlicer

Listing.py
--

An other sample script
