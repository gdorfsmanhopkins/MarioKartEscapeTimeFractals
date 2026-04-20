#This will do the whole process of making a full color gif, start to finish
#It doesn't clean up after itself
#Run as wrapper.py <c> <name> <NUM_FRAMES (optional, defaults to 100)> <color (optional, True or False, defaults to True)> <Resolution (optional)>
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python colorGif.py <c> <name> <NUM_FRAMES (optional)> <color (optional, True/False)> <Resolution (optional)>")
    sys.exit(1)

c = sys.argv[1]
name = sys.argv[2]
NUM_FRAMES='100'
if len(sys.argv)>3:
    NUM_FRAMES = sys.argv[3]

color = True
if len(sys.argv)>4:
    if sys.argv[4] == "False":
        color = False
        print("Let's do BW")
    elif sys.argv[4] != "True":
        print("Color should be \"True\" or \"False\"")
        print("Defaulting to \"True\"")

resolution = '1000'
if len(sys.argv)>5:
    resolution = sys.argv[5]


##We want to store pixel matrices and gifs in specific folders.  If these folders don't exist, let's create them
Path("PixelMatrices").mkdir(exist_ok=True)
Path("Gifs").mkdir(exist_ok=True)

json_dir = "PixelMatrices/"+name+".json"
frame_dir = name
gif_dir = "Gifs/"+name+".gif"

subprocess.run(['python','EscapeTimeMatrix.py',c,json_dir,resolution])
if(color):
    subprocess.run(['python','MatrixToFramesColor.py',json_dir,frame_dir,NUM_FRAMES])
else:
    subprocess.run(['python','MatrixToFramesBW.py',json_dir,frame_dir,NUM_FRAMES])

print("Making gif")
subprocess.run(['python','png_to_gif.py',frame_dir,gif_dir])