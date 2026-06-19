#This will do the whole process of a 3D printable STL, start to finish
#It doesn't clean up after itself
#Run as wrapperSTL.py <c> <name> <mountain --or-- hole (optional, defaults to mountain)> <Resolution (optional)> <bound (optional, defaults to 500)>

import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: wrapperSTL.py <c> <name> <mountain --or-- hole (optional, defaults to mountain)> <Resolution (optional)> <max_iter (optional, defaults to 100)>")
    sys.exit(1)

c = sys.argv[1]
name = sys.argv[2]
structure = 'mountain'
if len(sys.argv) > 3:
    structure = sys.argv[3]

resolution = '1000'
if len(sys.argv)>4:
    resolution = sys.argv[4]

max_iter = '100'
if len(sys.argv)>5:
    max_iter = sys.argv[5]


##We want to store pixel matrices and gifs in specific folders.  If these folders don't exist, let's create them
Path("PixelMatrices").mkdir(exist_ok=True)
Path("3DModels").mkdir(exist_ok=True)

json_dir = "PixelMatrices/"+name+".json"
stl_dir = "3DModels/"+name+".stl"

subprocess.run(['python','EscapeTimeMatrix.py',c,json_dir,resolution,max_iter])

print("Making STL...")
subprocess.run(['python','MatrixToSTL.py',json_dir,stl_dir,structure])