#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""                                    

import serial
import time

verbose=False

# Open grbl serial port
s = serial.Serial('COM6',115200)

# Open g-code file
f = open('gcode_out.txt','r');

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input

# Stream g-code to grbl 
for line in f:
    l = line.strip() # Strip all EOL characters for streaming
    if verbose:
        print 'Sending: ' + l,
    s.write(l + '\n') # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    if verbose:
        print ' : ' + grbl_out.strip()

# Wait here until grbl is finished to close serial port and file.
raw_input("  Press <Enter> to exit and disable grbl.")

# Close file and serial port
f.close()
s.close()
