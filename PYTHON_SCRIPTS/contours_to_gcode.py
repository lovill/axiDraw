from System import *
import Rhino
from Rhino.DocObjects import *
from Rhino.Geometry import *
from Rhino.Input import *
from Rhino.Input.Custom import *
from Rhino.Commands import *
from scriptcontext import doc
import rhinoscriptsyntax as rs

fp = "gcode_out.txt"

#in_mesh = rs.GetObject("Select mesh object to contour")
rc, obj_refs = Rhino.Input.RhinoGet.GetMultipleObjects("Select mesh(s) to contour", False, ObjectType.Mesh)

layer_height = rs.GetReal("Input contour height length", number=1.0)

curves = None

for obj_ref in obj_refs:
    geometry = obj_ref.Geometry()

    if type(geometry) == Brep:
      curves = Brep.CreateContourCurves(geometry, base_point, end_point, layer_height)
    else:
      curves = Mesh.CreateContourCurves(geometry, Rhino.Geometry.Point3d(0,0,0), Rhino.Geometry.Point3d(0,0,42), layer_height)

#crvs = Mesh.CreateContourCurves(geo, Rhino.Geometry.Point3d(0,0,0), Rhino.Geometry.Point3d(0,0,1), layer_height)
run = True

with open(fp, mode='w') as outfile:
    if run and len(curves) >= 1:
        for crv in curves:
            for p in range( crv.PointCount ):
                pt = crv.Point(p)
                if p == 0:
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
