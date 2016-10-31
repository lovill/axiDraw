import rhinoscriptsyntax as rs

fp = "gcode_out.txt"

inCrv = rs.GetObjects("Select curves to draw", filter=4)
print inCrv

if len(inCrv) > 0:
    inCrv = sorted(inCrv, key=lambda k:rs.CurveStartPoint(k).Y)

#subD = rs.GetReal("Input segment length", number=1.0)

with open(fp, mode='w') as outfile:
    if len(inCrv) >= 1:
        for crv in inCrv:
            pts = rs.PolylineVertices(crv)
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
