#This will do the whole process of making a full color gif, start to finish
#It doesn't clean up after itself
#Run as wrapperMandel.py <name> <center (optional, defaults to -.65)> <xRange (optional, defaults to 3)> <NUM_FRAMES (optional, defaults to 100)> <color (optional, True or False, defaults to True)> <resolution (optional, defaults to 1000)> <aspect ratio (optional, defaults to 4/3)> <bound (optional, defaults to 500)>
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("You must at least give a name to save as")
    print("Usage: wrapperMandel.py <name> <center (optional, defaults to -.65)> <xRange (optional, defaults to 3)> <NUM_FRAMES (optional, defaults to 100)> <color (optional, True or False, defaults to True)> <resolution (optional, defaults to 1000)> <aspect ratio (optional, defaults to 4/3)>")
    sys.exit(1)

name = sys.argv[1]
center = '[-.65,0]'
if len(sys.argv)>2:
    center = sys.argv[2]

xRange = '3'
if len(sys.argv)>3:
    xRange = sys.argv[3]

NUM_FRAMES='100'
if len(sys.argv)>4:
    NUM_FRAMES = sys.argv[4]

color = True
if len(sys.argv)>5:
    if sys.argv[5] == "False":
        color = False
    elif sys.argv[4] != "True":
        print("Color should be \"True\" or \"False\"")
        print("Defaulting to \"True\"")

resolution = '1000'
if len(sys.argv)>6:
    resolution = sys.argv[6]

aspectRatio = '4/3'
if len(sys.argv)>7:
    aspectRatio = sys.argv[7]

bound = '500'
if len(sys.argv)>8:
    bound = sys.argv[8]

##We want to store pixel matrices and gifs in specific folders.  If these folders don't exist, let's create them
Path("PixelMatrices").mkdir(exist_ok=True)
Path("Gifs").mkdir(exist_ok=True)

json_dir = "PixelMatrices/"+name+".json"
frame_dir = name
gif_dir = "Gifs/"+name+".gif"

subprocess.run(['python','EscapeTimeMatrixMandel.py',json_dir,center,xRange,resolution,aspectRatio,bound])
if(color):
    subprocess.run(['python','MatrixToFramesColor.py',json_dir,frame_dir,NUM_FRAMES])
else:
    subprocess.run(['python','MatrixToFramesBW.py',json_dir,frame_dir,NUM_FRAMES])

print("Making gif")
subprocess.run(['python','png_to_gif.py',frame_dir,gif_dir])