import json
from PIL import Image
import math
from pathlib import Path
import helpers

if __name__=="__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python MatrixToFramesBW.py <input_dir> <output_dir> <NUM_FRAMES> <LpNorm (optional, for redistribution)>")
        sys.exit()
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    NUM_FRAMES = int(sys.argv[3])
    NUM_DIGS = int(math.log10(NUM_FRAMES)) #For naming the files correctly
    STEP_SIZE = 1/NUM_FRAMES

    LpNorm = 2
    if len(sys.argv)==5:
        LpNorm = float(sys.argv[4])

    print("Loading Matrix...")
    save_location = open(input_dir)
    ETMatrix = json.load(save_location)


    #We will normalize the matrix to having values between 0 and 1, first linearly, and then redistributing using the function above
    ETMatrix = helpers.normalizeMatrix(ETMatrix,LpNorm)

    print("Making the Frames!")
    Path(output_dir).mkdir(exist_ok=True)

    height = len(ETMatrix[0])
    width = len(ETMatrix)

    img = Image.new('RGB', (width, height), color = 'white')
    pixels = img.load()

    t=0
    for v in range(NUM_FRAMES):
        for i in range(width):
            for j in range(height):
                if ETMatrix[i][j]<t:
                    ETMatrix[i][j]=1
                    pixels[i,j] = (0,0,0)
        img.save(output_dir + '/frame'+str(int(v+10**(NUM_DIGS+1)))+'.png')
        print("Made Frame #",v+1,"out of",NUM_FRAMES)
        t += STEP_SIZE