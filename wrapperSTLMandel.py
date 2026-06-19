#This will do the whole process of making a full color gif, start to finish
#It doesn't clean up after itself
#Run as wrapperMandel.py <name> <center (optional, defaults to -.65)> <xRange (optional, defaults to 3)> <resolution (optional, defaults to 1000)> <aspect ratio (optional, defaults to 4/3)> <max_iter (optional, defaults to 100)>
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("You must at least give a name to save as")
    print("Usage: wrapperMandel.py <name> <mountain --or-- hole (optional, defaults to mountain)> <center (optional, defaults to -.65)> <xRange (optional, defaults to 3)> <resolution (optional, defaults to 1000)> <aspect ratio (optional, defaults to 4/3)> <max_iter (optional, defaults to 100)>")
    sys.exit(1)

name = sys.argv[1]

structure = 'mountain'
if len(sys.argv) > 2:
    structure = sys.argv[2]

center = '[-.65,0]'
if len(sys.argv)>3:
    center = sys.argv[3]

xRange = '3'
if len(sys.argv)>4:
    xRange = sys.argv[4]

resolution = '1000'
if len(sys.argv)>5:
    resolution = sys.argv[5]

aspectRatio = '4/3'
if len(sys.argv)>6:
    aspectRatio = sys.argv[6]

max_iter = '100'
if len(sys.argv)>7:
    max_iter = sys.argv[7]

##We want to store pixel matrices and gifs in specific folders.  If these folders don't exist, let's create them
Path("PixelMatrices").mkdir(exist_ok=True)
Path("3DModels").mkdir(exist_ok=True)

json_dir = "PixelMatrices/"+name+".json"
stl_dir = "3DModels/"+name+".stl"

subprocess.run(['python','EscapeTimeMatrixMandel.py',json_dir,center,xRange,resolution,aspectRatio,max_iter])
print("Making STL...")
subprocess.run(['python','MatrixToSTL.py',json_dir,stl_dir,structure])