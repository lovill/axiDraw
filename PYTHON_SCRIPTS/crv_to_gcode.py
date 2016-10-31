import rhinoscriptsyntax as rs

fp = "gcode_out.txt"

inCrv = rs.GetObject("Select curve to draw")

subD = rs.GetReal("Input segment length", number=1.0)

pts = rs.DivideCurveLength(inCrv, subD)

with open(fp, mode='w') as outfile:
    for i, pt in enumerate(pts):
        if i == 0:
            #raise pen
            outfile.write("M03 S0 \n")
            #go to first position
            outfile.write("G00 X%.3f Y%.3f \n" %(pt.X,pt.Y) )
            #drop pen
            outfile.write("M03 S1024 \n")
            continue
        #go to next position (with pen down)
        outfile.write("G00 X%.3f Y%.3f \n" %(pt.X,pt.Y) )
    #lift pen
    outfile.write("M03 S0 \n")
    outfile.write("G00 X0 Y0 \n")

outfile.close()
